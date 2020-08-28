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
