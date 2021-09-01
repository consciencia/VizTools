# MIT License
#
# Copyright (c) 2020 Consciencia <consciencia@protonmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import re
import six
import time
import copy
import json
import chardet
import datetime
import threading
import http.server


__author__ = "Consciencia"


def thisdir():
    return os.path.dirname(os.path.realpath(__file__))


def stringToColor(chars):
    hash = 0
    for char in chars:
        hash = ord(char) + ((hash << 5) - hash)
    color = "#"
    for i in range(3):
        value = (hash >> (i * 8)) & 0xFF
        color += hex(value)[2:].zfill(2)
    return color


def sanitizeHtml(code):
    code = code.replace("\"", "\\\"")
    code = code.replace("\r\n", "<br>")
    code = code.replace("\n", "<br>")
    # TODO: Remove <script> and <style> tags.
    return code


class Series:
    def __init__(self,
                 x=None,
                 y=None,
                 xlabel="X",
                 ylabel="Y",
                 borderColor=None,
                 fillColor=None):
        if x is None:
            x = []
        if y is None:
            y = []
        if len(x) != len(y):
            raise Exception("Invalid input!")
        self._x = copy.deepcopy(x)
        self._y = copy.deepcopy(y)
        self._xlabel = xlabel
        self._ylabel = ylabel
        self._borderColor = borderColor
        self._fillColor = fillColor
        self._pad = 15
        self._radiuses = []
        if self._borderColor is None:
            self._borderColor = stringToColor(self._ylabel)
        if self._fillColor is None:
            self._fillColor = stringToColor(self._ylabel)

    def xlabel(self, val=None):
        if val is not None:
            if not isinstance(val, (type(""), type(u""))):
                raise Exception("Invalid input!")
            self._xlabel = val
        else:
            return self._xlabel

    def ylabel(self, val=None):
        if val is not None:
            if not isinstance(val, (type(""), type(u""))):
                raise Exception("Invalid input!")
            self._ylabel = val
        else:
            return self._ylabel

    def borderColor(self, val=None):
        if val is not None:
            if not isinstance(val, (list, type(""), type(u""))):
                raise Exception("Invalid input!")
            self._borderColor = val
        else:
            return self._borderColor

    def fillColor(self, val=None):
        if val is not None:
            if not isinstance(val, (list, type(""), type(u""))):
                raise Exception("Invalid input!")
            self._fillColor = val
        else:
            return self._fillColor

    def x(self, vals=None, idx=None):
        if vals is not None:
            if idx is None:
                if not isinstance(vals, list):
                    raise Exception("Invalid vals!")
                vals = [v.strftime("%d.%m.%Y")
                        for v in vals
                        if isinstance(v, datetime.datetime)]
                for v in vals:
                    if not isinstance(v, (int, float, type(""), type(u""))):
                        raise Exception("Invalid vals!")
                if len(vals) == len(self._y) or len(self._y) == 0:
                    self._x = copy.deepcopy(vals)
                else:
                    raise Exception("Invalid vals!")
            else:
                if isinstance(vals, datetime.datetime):
                    vals = vals.strftime("%d.%m.%Y"),
                if not isinstance(vals, (int, float, type(""), type(u""))):
                    raise Exception("Invalid vals!")
                self._x[idx] = vals
        elif idx is None:
            return copy.deepcopy(self._x)
        else:
            return self._x[idx]

    def y(self, vals=None, idx=None):
        if vals is not None:
            if idx is None:
                if not isinstance(vals, list):
                    raise Exception("Invalid vals!")
                for v in vals:
                    if not isinstance(v, (int, float)):
                        raise Exception("Invalid vals!")
                if len(vals) == len(self._x):
                    self._y = copy.deepcopy(vals)
                else:
                    raise Exception("Invalid vals!")
            else:
                if not isinstance(vals, (int, float)):
                    raise Exception("Invalid vals!")
                self._y[idx] = vals
        elif idx is None:
            return copy.deepcopy(self._y)
        else:
            return self._y[idx]

    def radiuses(self, vals=None, idx=None):
        if vals is not None:
            if idx is None:
                if not isinstance(vals, list):
                    raise Exception("Invalid vals!")
                for v in vals:
                    if not isinstance(v, int):
                        raise Exception("Invalid vals!")
                if len(vals) == len(self._x):
                    self._radiuses = copy.deepcopy(vals)
                else:
                    raise Exception("Invalid vals!")
            else:
                if not isinstance(vals, int):
                    raise Exception("Invalid vals!")
                self._radiuses[idx] = vals
        elif idx is None:
            return copy.deepcopy(self._radiuses)
        else:
            return self._radiuses[idx]

    def arraysInPair(self):
        return (self.x(), self.y())

    def pairsInArray(self):
        result = []
        for i in range(len(self._x)):
            result.append((self._x[i], self._y[i]))
        return result

    def push(self, x, y):
        self._x.append(x)
        self._y.append(y)

    def pop(self):
        if len(self._x) == 0:
            return None
        return (self._x.pop(-1), self._y.pop(-1))

    def clone(self):
        return copy.deepcopy(self)

    def clear(self):
        self._x = []
        self._y = []

    def __len__(self):
        return len(self._x)

    def __iter__(self):
        for i in range(len(self)):
            yield (self.x(None, i), self.y(None, i))

    def __getitem__(self, idx):
        return (self.x(None, idx), self.y(None, idx))

    def __setitem__(self, idx, pair):
        self.x(pair[0], idx)
        self.y(pair[1], idx)

    def __str__(self):
        acc = ""
        acc += self._xlabel.ljust(self._pad) + "| " + self._ylabel + "\n"
        for i in range(len(self._x)):
            acc += str(self._x[i]).ljust(self._pad)
            acc += "| " + str(self._y[i]) + "\n"
        return acc


class MultiSeries:
    def __init__(self, serieses=None, noCheck=False):
        if serieses is None:
            serieses = []
        if type(serieses) is list:
            for series in serieses:
                if not isinstance(series, Series):
                    raise Exception("Invalid input")
        elif isinstance(serieses, Series):
            serieses = [serieses]
        else:
            raise Exception("Invalid input")
        if not isinstance(noCheck, bool):
            raise Exception("Invalid input")
        self._serieses = serieses
        self._pad = 15
        self._noCheck = noCheck
        self.check()

    def content(self):
        return self._serieses

    def check(self):
        if not self._noCheck and len(self._serieses) > 1:
            x = (self._serieses[0].xlabel(), self._serieses[0].x())
            for series in self._serieses[1:]:
                if x != (series.xlabel(), series.x()):
                    raise Exception("Non matching series found (%s != %s)!"
                                    % (x, (series.xlabel(), series.x())))

    def add(self, series):
        if not isinstance(series, Series):
            raise Exception("Invalid input")
        self._serieses.append(series)
        self.check()

    def xlabel(self, val=None):
        if val is not None:
            for series in self._serieses:
                series.xlabel(val)
        elif len(self._serieses):
            return self._serieses[0].xlabel()
        else:
            return "<no data>"

    def ylabels(self, vals=None, idx=None):
        if vals is not None:
            if idx is None:
                if not isinstance(vals, list):
                    raise Exception("Invalid input!")
                for i, series in enumerate(self._serieses):
                    series.ylabel(vals[i])
            else:
                self._serieses[idx].ylabel(vals)
        elif idx is not None:
            return self._serieses[idx].ylabel()
        else:
            return [series.ylabel() for series in self._serieses]

    def borderColors(self, vals=None, idx=None):
        if vals is not None:
            if idx is None:
                if not isinstance(vals, list):
                    raise Exception("Invalid input!")
                for i, series in enumerate(self._serieses):
                    series.borderColor(vals[i])
            else:
                self._serieses[idx].borderColor(vals)
        elif idx is not None:
            return self._serieses[idx].borderColor()
        else:
            return [series.borderColor() for series in self._serieses]

    def fillColors(self, vals=None, idx=None):
        if vals is not None:
            if idx is None:
                if not isinstance(vals, list):
                    raise Exception("Invalid input!")
                for i, series in enumerate(self._serieses):
                    series.fillColor(vals[i])
            else:
                self._serieses[idx].fillColor(vals)
        elif idx is not None:
            return self._serieses[idx].fillColor()
        else:
            return [series.fillColor() for series in self._serieses]

    def x(self, vals=None, idx=None):
        if vals is not None:
            for series in self._serieses:
                series.x(vals, idx)
        else:
            return self._serieses[0].x(None, idx)

    def y(self, vals=None, idx=None):
        if vals is not None:
            for i, series in enumerate(self._serieses):
                series.y(vals[i], idx)
        else:
            return [series.y(None, idx)
                    for series in self._serieses]

    def arraysInPair(self):
        return (self.x(), self.y())

    def pairsInArray(self):
        result = []
        for i, x in enumerate(self.x()):
            result.append((x, self.y(None, i)))
        return result

    def push(self, x, y):
        for i, series in enumerate(self._serieses):
            series.push(x, y[i])

    def pop(self):
        result = []
        for series in self._serieses:
            result.append(series.pop())
        if len(result) == 0 or result[0] is None:
            return None
        vals = []
        for _, y in result:
            vals.append(y)
        return (result[0][0], vals)

    def clone(self):
        return copy.deepcopy(self)

    def clear(self):
        for series in self._serieses:
            series.clear()

    def __len__(self):
        if len(self._serieses) > 0:
            return len(self._serieses[0])
        return 0

    def __iter__(self):
        for i in range(len(self)):
            yield (self.x(None, i), self.y(None, i))

    def __getitem__(self, idx):
        return (self.x(None, idx), self.y(None, idx))

    def __setitem__(self, idx, pair):
        self.x(pair[0], idx)
        self.y(pair[1], idx)

    def __str__(self):
        acc = ""
        memo = {}
        if len(self._serieses):
            acc += self._serieses[0].xlabel().ljust(self._pad)
            for series in self._serieses:
                label = series.ylabel()
                if label in memo:
                    memo[label] += 1
                    label = label + ("[%s]" % memo[label])
                else:
                    memo[label] = 0
                acc += ("| " + label).ljust(self._pad)
            acc += "\n"
            for i, x in enumerate(self._serieses[0].x()):
                acc += str(x).ljust(self._pad)
                for series in self._serieses:
                    acc += ("| %s" % series.y(None, i)).ljust(self._pad)
                acc += "\n"
        return acc


class HttpHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # self.headers
        if self.path not in HttpServer.ROUTES:
            self.send_error(404,
                            "Unknown route",
                            "Not found handler for '%s'!" % self.path)
        else:
            route = HttpServer.ROUTES[self.path]
            if hasattr(route, "clone"):
                route = route.clone()
            response = route.render()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))


class HttpServer(threading.Thread):
    ROUTES = {}
    INST = None

    def __init__(self, addr=("127.0.0.1", 10000), blocking=False):
        if HttpServer.INST is not None:
            raise Exception("HttpServer already exists!")
        self._addr = addr
        self._blocking = blocking
        self._server = http.server.ThreadingHTTPServer(addr, HttpHandler)
        threading.Thread.__init__(self)
        self.setDaemon(True)
        HttpServer.INST = self

    def start(self):
        threading.Thread.start(self)
        if self._blocking:
            while True:
                time.sleep(1)

    def run(self):
        self._server.serve_forever()

    @staticmethod
    def uriPrefix():
        return "http://%s:%s/" % HttpServer.INST._addr

    @staticmethod
    def addRoute(path, handler):
        if not isinstance(path, (type(""), type(u""))):
            raise Exception("Path must be string!")
        if not hasattr(handler, "render"):
            raise Exception("Handler has no method \"render\"!")
        if not callable(handler.render) :
            raise Exception("Attribute \"render\" is not callable!")
        HttpServer.ROUTES[path] = handler

    @staticmethod
    def removeRoute(path):
        if not isinstance(path, (type(""), type(u""))):
            raise Exception("Path must be string!")
        del HttpServer.ROUTES[path]


class VBase:
    NEXTID = 0
    METASTORE = {
        "cssFragments": {},
        "resourceCache": {},
        "stats": {}
    }

    def __init__(self, name, resourceRoot=None, detached=None):
        self._name = name
        self._resourceRoot = resourceRoot
        self._html = self._loadResource("html", name)
        self._css = self._loadResource("css", name)
        self._js = self._loadResource("js", name)
        self._baseJs = self._loadResource("js", "vBase")
        self._children = []
        self._params = {}
        self._instId = self._genId()
        self._renderName = self._genRenderName(self._instId)
        self._usedMark = False
        if not detached and self._html is None and self._js is None:
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
        except Exception:
            encoding = chardet.detect(payload)["encoding"]
            if encoding:
                payload = payload.decode(encoding)
            else:
                raise Exception("Failed to infer encoding!")
        return payload

    def _loadResource(self, root, name=None):
        key = "%s%s" % (root, name)
        if key in VBase.METASTORE["resourceCache"]:
            return VBase.METASTORE["resourceCache"][key]
        if name:
            p = os.path.join(thisdir() + os.path.sep + "..",
                             root,
                             name + "." + root)
        else:
            p = root
        if os.path.exists(p):
            with open(p, "rb") as h:
                content = self._inferEncoding(h.read())
                VBase.METASTORE["resourceCache"][key] = content
                return content
        if self._resourceRoot:
            p = os.path.join(self._resourceRoot, self._name + "." + root)
            if os.path.exists(p):
                with open(p, "rb") as h:
                    content = self._inferEncoding(h.read())
                    VBase.METASTORE["resourceCache"][key] = content
                    return content
        VBase.METASTORE["resourceCache"][key] = None
        return None

    def _inject(self, to, data):
        if six.PY2:
            if not isinstance(to, u"".__class__):
                to = to.decode("utf-8")
            for key in data:
                val = data[key]
                if isinstance(val, u"".__class__):
                    pass
                elif isinstance(val, "".__class__):
                    val = val.decode("utf-8")
                else:
                    val = str(val).decode("utf-8")
                if not isinstance(key, u"".__class__):
                    key = key.decode("utf-8")
                to = to.replace("%" + key + "%", val)
        else:
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

    def _removeLicense(self, data):
        regexp = "\\/\\*\\s+%ENDLICENSE%\\s*\\*\\/"
        frags = re.split(regexp, data)
        if len(frags) > 2:
            raise Exception("Too many %ENDLICENSE% statements!")
        elif len(frags) < 2:
            return data
        return frags[1]

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
        localHtml = self._html.replace("\r\n", "")
        localHtml = localHtml.replace("\n", "")
        localHtml = localHtml.replace("\"", "\\\"")
        self._js = self._removeLicense(self._js)
        self._baseJs = self._removeLicense(self._baseJs)
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
            "js": self._inject("%PREV% "
                               + "function %RENDERNAME%($CHILDREN) {\n"
                               + self._baseJs
                               + "}\n\n", jsInjectObj),
            "jsFragments": childJsFragments,
            "expr": self._inject("%RENDERNAME%(%CHILDREN%)", exprInjectObj)
        }


class VMain(VBase):
    lock = threading.Lock()

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
        with VMain.lock:
            VBase.NEXTID = 0
            VBase.METASTORE["cssFragments"] = {}
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
                childExprs += "$(document.body).append(node.force().node);\n"
            childJsFragmentsStr = ""
            for fragment in childJsFragments:
                childJsFragmentsStr += fragment + "\n\n"
            return self._inject(self._html, {
                "JS_LIBS": self._jslibraries,
                "CSS_LIBS": self._csslibraries,
                "CUSTOM_JS": self._removeLicense(self._js),
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
        VBase.params(self, "STYLE", json.dumps(style))
        VBase.params(self, "SELECTOR", json.dumps(selector))
        VBase.params(self, "NOUPDATES", json.dumps(noLiveUpdates))
        self._node = node

    def __getattr__(self, name):
        # Slow but very short way how to make proxy.
        # https://stackoverflow.com/questions/26091833/proxy-object-in-python
        return getattr(self._node, name)

    def params(self, key, val=None):
        return self._node.params(key, val)

    def addChild(self, child):
        self._node.addChild(child)


class VHBox(VBase):
    def __init__(self):
        VBase.__init__(self, "vHBox")


class VVBox(VBase):
    def __init__(self):
        VBase.__init__(self, "vVBox")


class VVoid(VBase):
    def __init__(self):
        VBase.__init__(self, "vVoid")


class VGrid(VBase):
    def __init__(self, x, y=None):
        VBase.__init__(self, "vGrid", None, True)
        self._grid = []
        if type(x) is int and type(y) is int:
            for i in range(x):
                self._grid.append([None] * y)
        elif type(x) is list and y is None:
            for cnt in x:
                self._grid.append([None] * cnt)
        else:
            raise Exception("Invalid arguments!")

    def addChild():
        raise Exception("You cant add children this way!")

    def at(self, x, y, child=None):
        if child is not None:
            self._grid[x][y] = child
        return self._grid[x][y]

    def render(self):
        vbox = VVBox()
        for row in self._grid:
            hbox = VHBox()
            for column in row:
                if column is None:
                    hbox.addChild(VVoid())
                else:
                    hbox.addChild(column)
            vbox.addChild(hbox)
        return vbox.render()


class VLabel(VBase):
    def __init__(self, content):
        VBase.__init__(self, "vLabel")
        self.params("LABEL_STR", sanitizeHtml(content))

    def addChild(self, child):
        raise Exception("You cant add more children nodes to " +
                        "label node!")


class VParagraph(VBase):
    def __init__(self, content):
        VBase.__init__(self, "vParagraph")
        self.params("PARAGRAPH_STR", sanitizeHtml(content))

    def addChild(self, child):
        raise Exception("You cant add more children nodes to " +
                        "paragraph node!")


class VHeading(VBase):
    def __init__(self, level, content):
        VBase.__init__(self, "vHeading")
        if type(level) is not int:
            raise Exception("Level must be integer!")
        self.params("HEADING_LEVEL", level)
        self.params("HEADING_STR", sanitizeHtml(content))
        self.params("HEADING_HREF", json.dumps(""))

    def setHref(self, link):
        if not isinstance(link, ("".__class__, u"".__class__)):
            raise Exception("Link must be str!")
        self.params("HEADING_HREF", json.dumps(link))

    def addChild(self, child):
        raise Exception("You cant add more children nodes to " +
                        "heading node!")


class VCollapse(VBase):
    def __init__(self, title):
        VBase.__init__(self, "vCollapse")
        self._title = title
        self._components = []

    def addChild(self, child):
        self._components.append(child)

    def beforeRender(self):
        self.params("COLLAPSE_TITLE", self._title)
        vbox = VVBox()
        for component in self._components:
            vbox.addChild(component)
        VBase.addChild(self, vbox)


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
            r[key] = sanitizeHtml(str(r[key]))
        self._rows.append(r)

    def setDataset(self, series):
        if isinstance(series, Series):
            series = MultiSeries(series)
        if not isinstance(series, MultiSeries):
            raise Exception("Invalid input!")
        keys = [series.xlabel()] + series.ylabels()
        self.registerKeys(keys)
        for x, ys in series:
            row = {}
            row[keys[0]] = x
            for i, y in enumerate(ys):
                row[keys[i + 1]] = y
            self.addRow(row)

    def beforeRender(self):
        self.params("TABLE_ROWS",
                    json.dumps(self._rows))
        self.params("TABLE_KEYS",
                    json.dumps(self._keys))


class VDiagram(VBase):
    def __init__(self, title, xtitle="X", ytitle="Y"):
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
        raise Exception("You can't add children to this node!")

    def enableLogs(self):
        self._enableLogs = True

    def setType(self, diagType):
        suppTypes = ["line", "bar", "doughnut",
                     "pie", "polarArea", "radar",
                     "bubble"]
        if diagType not in suppTypes:
            raise Exception("Invalid diagram type '%s'!" %
                            diagType)
        self._type = diagType

    def setDataset(self, series):
        if isinstance(series, Series):
            series = MultiSeries(series)
        if not isinstance(series, MultiSeries):
            raise Exception("Parameter \"series\" must be either "
                            "Series or MultiSeries!")
        self._labels = series.x()
        for s in series.content():
            self._dataset.append({
                "x": s.x(),
                "y": s.y()
            })
            self._datasetMeta.append({
                "label": s.ylabel(),
                "backgroundColor": s.fillColor(),
                "borderColor": s.borderColor(),
                "fill": False,
                "interpolation": False
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


class VDiagramDoughnut(VDiagram):
    def __init__(self, title):
        VDiagram.__init__(self, title)
        self.setType("doughnut")


class VDiagramPie(VDiagram):
    def __init__(self, title):
        VDiagram.__init__(self, title)
        self.setType("pie")


class VDiagramPolarArea(VDiagram):
    def __init__(self, title):
        VDiagram.__init__(self, title)
        self.setType("polarArea")


class VDiagramRadar(VDiagram):
    def __init__(self, title):
        VDiagram.__init__(self, title)
        self.setType("radar")


class VDiagramLine(VDiagram):
    def __init__(self, title, xtitle, ytitle):
        VDiagram.__init__(self, title, xtitle, ytitle)
        self.setType("line")


class VDiagramBar(VDiagram):
    def __init__(self, title, xtitle, ytitle):
        VDiagram.__init__(self, title, xtitle, ytitle)
        self.setType("bar")


class VDiagramBubble(VDiagram):
    def __init__(self, title, xtitle="X", ytitle="Y"):
        VDiagram.__init__(self, title, xtitle, ytitle)
        self.setType("bubble")

    def setDataset(self, series):
        if isinstance(series, Series):
            series = MultiSeries(series)
        if not isinstance(series, MultiSeries):
            raise Exception("Parameter \"series\" must be either "
                            "Series or MultiSeries!")
        self._labels = []
        for s in series.content():
            radiuses = s.radiuses()
            if len(radiuses) == 0:
                radiuses = [3] * len(s.x())
            self._dataset.append({
                "x": s.x(),
                "y": s.y(),
                "r": radiuses
            })
            self._datasetMeta.append({
                "label": s.ylabel(),
                "backgroundColor": s.fillColor(),
                "borderColor": s.borderColor()
            })


class VDiagramCandleStick(VBase):
    def __init__(self, title):
        VBase.__init__(self, "vDiagramCandleStick")
        self._title = title
        self._dataset = []
        self._enableLogs = False

    def addChild(self, child):
        raise Exception("You cant add children to this node!")

    def enableLogs(self):
        self._enableLogs = True

    def setDataset(self, multiseries):
        if not isinstance(multiseries, MultiSeries):
            raise Exception("Parameter \"series\" must be either "
                            "Series or MultiSeries!")
        serieses = multiseries.content()
        if len(serieses) != 4:
            raise Exception("MultiSeries with four parts must be passed "
                            "(open, high, low, close)!")
        for x, ys in multiseries:
            self._dataset.append({
                "x": x,
                "y": ys
            })

    def beforeRender(self):
        self.params("DIAGRAM_TITLE",
                    json.dumps(self._title))
        self.params("DATASET",
                    json.dumps(self._dataset))
        self.params("ENABLE_LOGS",
                    json.dumps(self._enableLogs))
