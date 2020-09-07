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

var VizTools = window.VizTools || {
    Utils: {
        nodeHeightInLines(node) {
            var $element = $(node);
            var originalHtml = $element.html();
            var words = originalHtml.split(/[\s/]/);
            var linePositions = [];

            for (var i in words) {
                words[i] = "<span>" + words[i] + "</span>";
            }

            $element.html(words.join(" "));
            $element.children("span").each(function () {
                var lp = $(this).position().top;

                if (linePositions.indexOf(lp) == -1) {
                    linePositions.push(lp);
                }
            });

            $element.html(originalHtml);

            return linePositions.length;
        },
        Thunk: {
            create(cb) {
                var obj = {
                    cb,
                    val: undefined
                };
                obj.__proto__ = VizTools.Utils.Thunk;

                return obj;
            },

            force() {
                if (this.val != undefined) {
                    return this.val;
                } else {
                    this.val = this.cb();

                    return this.val;
                }
            }
        }
    }
};
