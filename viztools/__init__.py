import os
import copy
import json


def thisdir():
    segs = os.path.realpath(__file__).split(os.path.sep)[:-1]
    return os.path.sep.join(segs)


class VBase:
    NEXTID = 0

    def __init__(self, name, resourceRoot=None):
        self._name = name
        self._resourceRoot = resourceRoot
        self._html = self._loadResource("html", name)
        self._css = self._loadResource("css", name)
        self._js = self._loadResource("js", name)
        self._children = []
        self._params = {}
        self._instId = self._genId()
        self._renderName = self._genRenderName(self._instId)
        self._usedMark = False
        if self._html is None and self._js is None:
            raise Exception("One of following must be provided [js, html]!")
        self._html = self._html or ""
        self._css = self._css or ""
        self._js = self._js or ""
        if self._resourceRoot:
            if os.path.isfile(self._resourceRoot):
                self._resourceRoot = os.path.realpath(self._resourceRoot)
                self._resourceRoot = self._resourceRoot.split(os.path.sep)[:-1]
                self._resourceRoot = os.path.sep.join(self._resourceRoot)
            elif not os.path.isdir(self._resourceRoot):
                raise Exception("Resource root '%s' is not file or dir!" %
                                self._resourceRoot)

    def _loadResource(self, root, name=None):
        if name:
            p = os.path.join(thisdir() + os.path.sep + "..",
                             root,
                             name + "." + root)
        else:
            p = root
        if os.path.exists(p):
            with open(p, "rb") as h:
                return h.read()
        if self._resourceRoot:
            p = os.path.join(self._resourceRoot, self._name + "." + root)
            if os.path.exists(p):
                with open(p, "rb") as h:
                    return h.read()
        return None

    def _inject(self, to, data):
        for key in data:
            val = data[key]
            to = to.replace("%" + key + "%", str(val))
        return to

    def _genId(self):
        VBase.NEXTID += 1
        return VBase.NEXTID

    def _genRenderName(self, id):
        return "Viztools$" + self._name + "$" + str(id)

    def clone(self):
        temp = copy.deepcopy(self)
        temp._instId = temp._genId()
        temp._renderName = temp._genRenderName(temp._instId)
        temp._usedMark = False
        temp._children = [n.clone() for n in temp._children]
        return temp

    def addChild(self, child):
        if child._usedMark:
            raise Exception("Node '%s' is already used!" %
                            self._renderName)
        child._usedMark = True
        self._children.append(child)

    def params(self, key, val=None):
        if val:
            self._params[key] = val
            return None
        else:
            return self._params[key]

    def render(self):
        instId = self._instId
        renderName = self._renderName
        self._params["ID"] = instId
        childCss = ""
        childJs = ""
        childExprs = "["
        for ch in self._children:
            r = ch.render()
            childCss += r["css"]
            childJs += r["js"]
            childExprs += r["expr"] + ","
        if childExprs[-1] == ",":
            childExprs = childExprs[:-1]
        childExprs += "]"
        finalHtml = self._html.replace("\n", "")
        finalHtml = finalHtml.replace("\"", "\\\"")
        jsInjectObj = {
            "PREV": childJs,
            "RENDERNAME": renderName,
            "HTML": self._inject(finalHtml,
                                 self._params),
            "JS": self._inject(self._js,
                               self._params)
        }
        exprInjectObj = {
            "RENDERNAME": renderName,
            "CHILDREN": childExprs
        }
        return {
            "css": childCss + self._inject(self._css, self._params) + "\n\n",
            "js": self._inject("%PREV% function %RENDERNAME%($CHILDREN) {\n" +
                               "    var $temp = \"%HTML%\";\n" +
                               "    if ($temp) {\n" +
                               "        var $NODE = $($temp);\n" +
                               "    } else {\n" +
                               "        var $NODE = null;\n" +
                               "    }\n" +
                               "    %JS%\n" +
                               "    return { \"node\": $NODE };\n" +
                               "}\n\n", jsInjectObj),
            "expr": self._inject("%RENDERNAME%(%CHILDREN%)", exprInjectObj)
        }


class VMain(VBase):
    def __init__(self, title, author):
        VBase.__init__(self, "vMain")
        jsLibRoot = os.path.join(thisdir(),
                                 "..",
                                 "libs",
                                 "js")
        jsLibs = os.listdir(jsLibRoot)
        jsLibs = [os.path.join(jsLibRoot, jsLib) for jsLib in jsLibs]
        self._jslibraries = ""
        for jsLib in jsLibs:
            self._jslibraries += self._loadResource(jsLib)
        cssLibRoot = os.path.join(thisdir(),
                                  "..",
                                  "libs",
                                  "css")
        cssLibs = os.listdir(cssLibRoot)
        cssLibs = [os.path.join(cssLibRoot, cssLib) for cssLib in cssLibs]
        self._csslibraries = ""
        for cssLib in cssLibs:
            self._csslibraries += self._loadResource(cssLib)
        self._title = title
        self._author = author

    def addCss(self, css):
        self._css += css

    def addJs(self, js):
        self._js += js

    def render(self):
        children = [child.render() for child in self._children]
        childJs = ""
        childCss = ""
        childExprs = ""
        for child in children:
            childJs += child["js"]
            childCss += child["css"]
            childExprs += "var node = " + child["expr"] + ";\n"
            childExprs += "$(document.body).append(node[\"node\"]);\n"
        return self._inject(self._html, {
            "JS_LIBS": self._jslibraries,
            "CSS_LIBS": self._csslibraries,
            "CUSTOM_JS": self._js,
            "CUSTOM_CSS": self._css,
            "CHILD_JS": childJs,
            "CHILD_CSS": childCss,
            "CHILD_EXPRS": childExprs,
            "TITLE": self._title,
            "AUTHOR": self._author
        })


class VStyle(VBase):
    def __init__(self, node, style, selector=None, noLiveUpdates=False):
        VBase.__init__(self, "vStyle")
        VBase.addChild(self, node)
        self.params("STYLE", json.dumps(style))
        self.params("SELECTOR", json.dumps(selector))
        self.params("NOUPDATES", json.dumps(noLiveUpdates))

    def addChild(self, child):
        raise Exception("You cant add more children nodes to " +
                        "style pseudo-node!")


class VHBox(VBase):
    def __init__(self):
        VBase.__init__(self, "vHBox")


class VVBox(VBase):
    def __init__(self):
        VBase.__init__(self, "vVBox")


class VLabel(VBase):
    def __init__(self, content):
        VBase.__init__(self, "vLabel")
        self.params("LABEL_STR", content)

    def addChild(self, child):
        raise Exception("You cant add more children nodes to " +
                        "label node!")


class VParagraph(VBase):
    def __init__(self, content):
        VBase.__init__(self, "vParagraph")
        self.params("PARAGRAPH_STR", content)

    def addChild(self, child):
        raise Exception("You cant add more children nodes to " +
                        "paragraph node!")


class VHeading(VBase):
    def __init__(self, level, content):
        VBase.__init__(self, "vHeading")
        if type(level) is not int:
            raise Exception("Level must be integer!")
        self.params("HEADING_LEVEL", level)
        self.params("HEADING_STR", content)

    def addChild(self, child):
        raise Exception("You cant add more children nodes to " +
                        "heading node!")


class VMenu(VBase):
    def __init__(self):
        VBase.__init__(self, "vMenu")
        self._labels = []
        self._default = None

    def addEntry(self, label, node, default=False):
        self.addChild(node)
        self._labels.append(label)
        if default:
            if self._default:
                raise Exception("Default '%s' was already chosen!" %
                                self._default)
            self._default = label

    def render(self):
        self._default = self._default or ""
        self.params("DEFAULT_LABEL",
                    json.dumps(self._default))
        self.params("MENU_LABELS",
                    json.dumps(self._labels))
        return VBase.render(self)


class VTableBrowser(VBase):
    def __init__(self):
        VBase.__init__(self, "vTableBrowser")
        self._rows = []
        self._keys = []

    def addChild(self, child):
        raise Exception("You cant add children to this node!")

    def registerKeys(self, keys):
        if type(keys) is not list:
            raise Exception("Invalid input!")
        if len(self._keys) != 0:
            raise Exception("Keys already registered!")
        self._keys = keys

    def addRow(self, row):
        if type(row) is not dict:
            raise Exception("Invalid input '%s'!" % type(row))
        if len(self._keys) == 0:
            raise Exception("Keys are not registered!")
        r = copy.deepcopy(row)
        for key in r:
            if key not in self._keys:
                raise Exception("Key '%s' not registered!" %
                                key)
            r[key] = str(r[key])
        self._rows.append(r)

    def render(self):
        self.params("TABLE_ROWS",
                    json.dumps(self._rows))
        self.params("TABLE_KEYS",
                    json.dumps(self._keys))
        return VBase.render(self)


class VDiagram(VBase):
    def __init__(self, title, xtitle, ytitle):
        VBase.__init__(self, "vDiagram")
        self._title = title
        self._xtitle = xtitle
        self._ytitle = ytitle
        self._type = "line"
        self._dataset = []
        self._labels = []
        self._datasetMeta = []
        self._enableLogs = False

    def addChild(self, child):
        raise Exception("You cant add children to this node!")

    def enableLogs(self):
        self._enableLogs = True

    def setType(self, diagType):
        suppTypes = ["line", "bar", "doughnut", "pie", "polarArea"]
        if diagType not in suppTypes:
            raise Exception("Invalid diagram type '%s'!" %
                            diagType)
        self._type = diagType

    def setLabels(self, labels):
        if type(labels) is not list:
            raise Exception("Input parameter must be list!")
        self._labels = labels

    def addDataset(self, x, y, label,
                   bgColor, borderColor,
                   fill=False, interpolation=False):
        if self._type == "line" or self._type == "bar":
            if type(x) is not list or type(y) is not list:
                raise Exception("Invalid input!")
            if len(x) != len(y):
                raise Exception("Sizes dont match!")
            for v in x:
                if v not in self._labels:
                    raise Exception("Label '%s' not found in labels!" % v)
        else:
            if len(y) != len(self._labels):
                raise Exception("Sizes dont match!")
        self._dataset.append({
            "x": x,
            "y": y
        })
        self._datasetMeta.append({
            "label": label,
            "backgroundColor": bgColor,
            "borderColor": borderColor,
            "fill": fill,
            "interpolation": interpolation
        })

    def render(self):
        self.params("DIAG_TYPE",
                    json.dumps(self._type))
        self.params("DATASET",
                    json.dumps(self._dataset))
        self.params("DATASET_LABELS",
                    json.dumps(self._labels))
        self.params("DATASET_META",
                    json.dumps(self._datasetMeta))
        self.params("DIAGRAM_TITLE",
                    json.dumps(self._title))
        self.params("X_TITLE",
                    json.dumps(self._xtitle))
        self.params("Y_TITLE",
                    json.dumps(self._ytitle))
        self.params("ENABLE_LOGS",
                    json.dumps(self._enableLogs))
        return VBase.render(self)


class VDiagramXy(VDiagram):
    def __init__(self, title, xtitle, ytitle):
        VDiagram.__init__(self, title, xtitle, ytitle)

    def setType(self, diagType):
        suppTypes = ["line", "bar"]
        if diagType not in suppTypes:
            raise Exception("Invalid diagram type '%s'!" %
                            diagType)
        VDiagram.setType(self, diagType)

    def addDataset(self, x, y, label,
                   bgColor, borderColor,
                   fill=False, interpolation=False):
        if type(x) is not list or type(y) is not list:
            raise Exception("Invalid input (x or y)!")
        if len(x) != len(y):
            raise Exception("Sizes dont match (xy)!")
        VDiagram.addDataset(self, x, y, label,
                            bgColor, borderColor,
                            fill, interpolation)


class VDiagramRel(VDiagram):
    def __init__(self, title):
        VDiagram.__init__(self, title, "", "")
        self._labelCount = 0

    def setType(self, diagType):
        suppTypes = ["doughnut", "pie", "polarArea"]
        if diagType not in suppTypes:
            raise Exception("Invalid diagram type '%s'!" %
                            diagType)
        VDiagram.setType(self, diagType)

    def setLabels(self, labels):
        VDiagram.setLabels(self, labels)
        self._labelCount = len(labels)

    def setData(self, vals, bgColors, borderColors):
        if len(vals) != len(bgColors) or\
           len(vals) != len(borderColors) or\
           len(vals) != self._labelCount:
            raise Exception("Invalid input!")
        VDiagram.addDataset(self,
                            None,
                            vals,
                            "",
                            bgColors,
                            borderColors)

    def addDataset(self, x, y, label,
                   bgColor, borderColor,
                   fill=False, interpolation=False):
        raise Exception("Cant add additional datasets!")