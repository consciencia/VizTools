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
