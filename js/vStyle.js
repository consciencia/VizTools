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
VizTools.Style = {
    create(node, style, selector, noLiveUpdates) {
        var obj = {
            node: node,
            style: style,
            selector: selector,
            noLiveUpdates: noLiveUpdates
        };
        obj.__proto__ = VizTools.Style;

        obj.setStyle()
        obj.spawnUpdateMonitor()

        return obj;
    },

    setStyle() {
        if (this.selector) {
            $(this.node).find(this.selector).css(this.style);
        } else {
            $(this.node).css(this.style);
        }
    },

    spawnUpdateMonitor() {
        if (this.noLiveUpdates) {
            return;
        }

        var self = this;
        var MutationObserver = (window.MutationObserver
                                || window.WebKitMutationObserver
                                || window.MozMutationObserver);
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === "characterData") {
                    self.setStyle();
                } else if (mutation.type === "childList") {
                    if (mutation.addedNodes.length) {
                        self.setStyle();
                    }
                }
            });
        });

        observer.observe(this.node, {
            childList: true,
            characterData: true,
            subtree: true
        });
    }
};
/* %} %ENDEXPORT% */

styleObj = VizTools.Style.create($CHILDREN[0].force().node,
                                 %STYLE%,
                                 %SELECTOR%,
                                 %NOUPDATES%);
$NODE = styleObj.node;
