/* %EXPORT% %{ */
VizTools.DiagramCandleStick = {
    create($root, title, dataset, enableLogs) {
        var obj = {
            $root: $root,
            dataset: dataset,
            title: title,
            enableLogs: enableLogs,
            options: null,
            chart: null
        };
        obj.__proto__ = VizTools.DiagramCandleStick;

        obj.createConfig();

        return obj;
    },

    start() {
        // Container must be placed into DOM in time of diagram initialization.
        // In order to satisfy this requirement, we simply defer diagram
        // creation.
        setTimeout(this.mount.bind(this), 1000);
    },

    createConfig() {
        this.options = {
            series: [{
                data: this.dataset
            }],
            chart: {
                type: "candlestick"
            },
            title: {
                text: this.title,
                align: "center"
            },
            xaxis: {
                type: "category"
            },
            yaxis: {
                tooltip: {
                    enabled: true
                }
            }
        };

        if (this.enableLogs) {
            console.log(this.options);
        }
    },

    mount() {
        this.options.chart.height = this.$root.width() / 2;

        this.chart = new ApexCharts(this.$root[0],
                                    this.options);
        this.chart.render();
    }
};
/* %} %ENDEXPORT% */

var diagram = VizTools.DiagramCandleStick.create($NODE,
                                                 %DIAGRAM_TITLE%,
                                                 %DATASET%,
                                                 %ENABLE_LOGS%);
diagram.start();
