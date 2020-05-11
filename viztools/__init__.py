import os
import copy
import json
import re
import chardet


def thisdir():
    segs = os.path.realpath(__file__).split(os.path.sep)[:-1]
    return os.path.sep.join(segs)


class VBase:
    NEXTID = 0
    METASTORE = {
        "cssFragments": {},
        "stats": {}
    }

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

    def _inferEncoding(self, payload):
        try:
            payload = payload.decode("utf-8")
        except:
            encoding = chardet.detect(payload)["encoding"]
            if encoding:
                payload = payload.decode(encoding)
            else:
                raise Exception("Failed to infer encoding!")
        return payload

    def _loadResource(self, root, name=None):
        if name:
            p = os.path.join(thisdir() + os.path.sep + "..",
                             root,
                             name + "." + root)
        else:
            p = root
        if os.path.exists(p):
            with open(p, "rb") as h:
                content = self._inferEncoding(h.read())
                return content
        if self._resourceRoot:
            p = os.path.join(self._resourceRoot, self._name + "." + root)
            if os.path.exists(p):
                with open(p, "rb") as h:
                    content = self._inferEncoding(h.read())
                    return content
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

    def _extractJsFragments(self):
        fragmentRegex = ("\\/\\*\\s*%EXPORT%\\s+%\\{\\s*\\*\\/"
                         + "((?:\n|.)*)"
                         + "\\/\\*\\s*%\\}\\s+%ENDEXPORT%\\s*\\*\\/")
        rawFragments = re.findall(fragmentRegex, self._js)
        fragments = {}
        for rawFragment in rawFragments:
            fragments[rawFragment.strip()] = True
        return re.sub(fragmentRegex, "", self._js), fragments

    def _mergeJsFragments(self, destFrags, sourceFrags):
        for fragment in sourceFrags:
            destFrags[fragment] = True

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

    def beforeRender(self):
        pass

    def render(self):
        if self._name in VBase.METASTORE["stats"]:
            VBase.METASTORE["stats"][self._name] += 1
        else:
            VBase.METASTORE["stats"][self._name] = 1
        self.beforeRender()
        instId = self._instId
        renderName = self._renderName
        self._params["ID"] = instId
        self._params["RENDERNAME"] = renderName
        childCss = ""
        childJs = ""
        childJsFragments = {}
        childExprs = "["
        for ch in self._children:
            r = ch.render()
            childCss += r["css"]
            childJs += r["js"]
            self._mergeJsFragments(childJsFragments, r["jsFragments"])
            childExprs += r["expr"] + ","
        if childExprs[-1] == ",":
            childExprs = childExprs[:-1]
        childExprs += "]"
        localHtml = self._html.replace("\n", "")
        localHtml = localHtml.replace("\"", "\\\"")
        localJs, localJsFragments = self._extractJsFragments()
        self._mergeJsFragments(childJsFragments, localJsFragments)
        jsInjectObj = {
            "PREV": childJs,
            "ID": instId,
            "RENDERNAME": renderName,
            "HTML": self._inject(localHtml,
                                 self._params),
            "JS": self._inject(localJs,
                               self._params)
        }
        exprInjectObj = {
            "RENDERNAME": renderName,
            "CHILDREN": childExprs
        }
        localCss = self._inject(self._css, self._params) + "\n\n"
        if localCss in VBase.METASTORE["cssFragments"]:
            localCss = ""
        else:
            VBase.METASTORE["cssFragments"][localCss] = True
        return {
            "css": childCss + localCss,
            "js": self._inject("%PREV% function %RENDERNAME%($CHILDREN) {\n" +
                               "    var $temp = \"%HTML%\";\n" +
                               "    if ($temp) {\n" +
                               "        var $NODE = $($temp);\n" +
                               "    } else {\n" +
                               "        var $NODE = null;\n" +
                               "    }\n" +
                               "    \n" +
                               "    var $ID = %ID%;\n" +
                               "    var $RENDERNAME = \"%RENDERNAME%\";\n" +
                               "    \n" +
                               "    %JS%\n\n" +
                               "    return { \"node\": $NODE };\n" +
                               "}\n\n", jsInjectObj),
            "jsFragments": childJsFragments,
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
        VBase.METASTORE["stats"] = {}
        VBase.METASTORE["stats"][self._name] = 1
        children = [child.render() for child in self._children]
        childJs = ""
        childJsFragments = {}
        childCss = ""
        childExprs = ""
        for child in children:
            childJs += child["js"]
            self._mergeJsFragments(childJsFragments, child["jsFragments"])
            childCss += child["css"]
            childExprs += "var node = " + child["expr"] + ";\n"
            childExprs += "$(document.body).append(node[\"node\"]);\n"
        childJsFragmentsStr = ""
        for fragment in childJsFragments:
            childJsFragmentsStr += fragment + "\n\n"
        return self._inject(self._html, {
            "JS_LIBS": self._jslibraries,
            "CSS_LIBS": self._csslibraries,
            "CUSTOM_JS": self._js,
            "CUSTOM_CSS": self._css,
            "CHILD_JS": childJsFragmentsStr + childJs,
            "CHILD_CSS": childCss,
            "CHILD_EXPRS": childExprs,
            "TITLE": self._title,
            "AUTHOR": self._author
        })

    def renderToFile(self, destination):
        page = self.render().encode("utf-8")
        with open(destination, "wb") as hndl:
            hndl.write(page)

    def printStats(self):
        stats = []
        for component in VBase.METASTORE["stats"]:
            stats.append((component, VBase.METASTORE["stats"][component]))
        stats.sort(key=lambda x: x[1])
        stats.reverse()
        print("------ BEGIN VIZTOOLS STATS ---")
        for stat in stats:
            print("    %s - %s" % stat)
        print("    ======")
        print("    = %s components" % sum([x[1] for x in stats]))
        print("------ END VIZTOOLS STATS ---")


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

    def beforeRender(self):
        self._default = self._default or ""
        self.params("DEFAULT_LABEL",
                    json.dumps(self._default))
        self.params("MENU_LABELS",
                    json.dumps(self._labels))


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

    def beforeRender(self):
        self.params("TABLE_ROWS",
                    json.dumps(self._rows))
        self.params("TABLE_KEYS",
                    json.dumps(self._keys))


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

    def addSingleDataset(self, x, y, label,
                         bgColor, borderColor,
                         fill=False, interpolation=False):
        if self._labels != []:
            raise Exception("Labels already set!")
        self.setLabels(x)
        self.addDataset(x, y, label,
                        bgColor, borderColor,
                        fill, interpolation)

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

    def beforeRender(self):
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
