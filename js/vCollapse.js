// MIT License
//
// Copyright (c) 2020 Consciencia <consciencia@protonmail.com>
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
/* %ENDLICENSE% */

/* %EXPORT% %{ */
VizTools.Collapse = {
    create(root , child) {
        var obj = {
            $root: root,
            child: child,
            $header: root.find(".header"),
            $body: root.find(".body"),
            collapsed: true
        };
        obj.__proto__ = VizTools.Collapse;

        obj.$header.on("click", obj.toggle.bind(obj));

        return obj;
    },

    toggle() {
        if (this.collapsed) {
            this.collapsed = false;
            this.$body.append(this.child.force().node);
            this.$header.css({
                "border-bottom": "1px solid black"
            });
            this.$body.css({
                padding: "5px"
            });
            this.$body.animate({
                height: ($(this.child.force().node).height()
                         + 10
                         + "px")
            });
        } else {
            this.collapsed = true;
            this.$body.animate({
                height: "0px"
            }, () => {
                this.$header.css({
                    "border-bottom": "0px solid black"
                });
                this.$body.css({
                    padding: "0px"
                });
                this.$body.empty();
            });
        }
    }
};
/* %} %ENDEXPORT% */

var collapse = VizTools.Collapse.create($NODE, $CHILDREN[0]);
