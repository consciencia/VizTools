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
VizTools.HBox = {
    create(children, renderName) {
        var obj = {
            $root: $("<div class='viztools_vhbox'></div>"),
            children: children,
            renderName: renderName
        };
        obj.__proto__ = VizTools.HBox;

        obj.$root.attr("id", obj.renderName);

        var percentagePerItem = 100 / obj.children.length;
        percentagePerItem = percentagePerItem.toString() + "%";

        for (var i = 0; i < obj.children.length; ++i) {
            var child = obj.children[i].force();
            var $helperNode =
                $("<div class='viztools_vhbox_helper' style='width: "
                  + percentagePerItem
                  + ";'></div>");

            $helperNode.append(child.node);
            obj.$root.append($helperNode);
        }

        return obj;
    }
};
/* %} %ENDEXPORT% */

hbox = VizTools.HBox.create($CHILDREN, $RENDERNAME);
$NODE = hbox.$root;
