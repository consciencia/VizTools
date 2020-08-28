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
