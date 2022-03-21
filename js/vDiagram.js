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
VizTools.Diagram = {
    create($root,
           diagType,
           dataset,
           datasetLabels,
           datasetMeta,
           diagramTitle,
           xTitle,
           yTitle,
           enableLogs) {
        var obj = {
            $root: $root,
            diagType: diagType,
            dataset: dataset,
            datasetLabels: datasetLabels,
            datasetMeta: datasetMeta,
            diagramTitle: diagramTitle,
            xTitle: xTitle,
            yTitle: yTitle,
            enableLogs: enableLogs
        };
        obj.__proto__ = VizTools.Diagram;

        if (obj.enableLogs) {
            console.log(obj);
        }

        var targetDatasets = obj.createDataset();
        var scales = obj.createScales();
        var config = obj.createConfig(targetDatasets,
                                      scales);
        obj.generate(config);

        return obj;
    },

    isMultiaxis() {
        var result = false;
        var lastVal = null;

        for (var entry of this.datasetMeta) {
            if (lastVal === null) {
                lastVal = entry.primaryYAxis;
            } else if (lastVal != entry.primaryYAxis) {
                result = true;

                break;
            }
        }

        return result;
    },

    isPieLikeDiag() {
        return (this.diagType == "polarArea"
                || this.diagType == "doughnut"
                || this.diagType == "pie"
                || this.diagType == "radar");
    },

    isScatterLikeDiag() {
        return (this.diagType == "bubble"
                || this.diagType == "scatter");
    },

    createDataset() {
        var targetDatasets = [];

        for (var i = 0; i < this.dataset.length; ++i) {
            var d = this.dataset[i];
            var m = this.datasetMeta[i];
            pairs = [];

            if (this.isPieLikeDiag()) {
                pairs = d.y;
            } else if (this.isScatterLikeDiag()) {
                for (var y = 0; y < d.x.length; ++y) {
                    pairs.push({
                        x: d.x[y],
                        y: d.y[y],
                        r: d.r[y]
                    });
                }
            } else {
                for (var y = 0; y < d.x.length; ++y) {
                    pairs.push({
                        x: d.x[y],
                        y: d.y[y]
                    });
                }
            }

            var result = {
                label: m.label,
                backgroundColor: m.backgroundColor,
                borderColor: m.borderColor,
                data: pairs,
                fill: m.fill,
            };

            if (this.isMultiaxis()) {
                if (m.primaryYAxis) {
                    result.yAxisID = "y";
                } else {
                    result.yAxisID = "y2";
                }
            }

            if (!this.isScatterLikeDiag() && !m.interpolation) {
                result.lineTension = 0;
            }

            if (this.isPieLikeDiag()) {
                result.fill = undefined;
                result.lineTension = undefined;
            }

            targetDatasets.push(result);
        }

        return targetDatasets;
    },

    createScales() {
        if (this.isPieLikeDiag() || this.isScatterLikeDiag()) {
            return {};
        } else {
            var result = {
	              x: {
		                display: true,
		                scaleLabel: {
			                  display: true,
			                  labelString: this.xTitle
		                }
	              },
	              y: {
		                display: true,
		                scaleLabel: {
			                  display: true,
			                  labelString: this.yTitle
		                },
                    beginAtZero: true
	              }
            };

            if (this.isMultiaxis())
            {
                result.y.position = "left";
                result.y2 = {
                    display: true,
                    position: "right",
                    beginAtZero: true
                };
            }

            return result;
        }
    },

    createConfig(targetDatasets, scales) {
        return {
	          type: this.diagType,
	          data: {
                labels: this.datasetLabels,
		            datasets: targetDatasets
	          },
	          options: {
		            responsive: true,
                legend: {
			              position: "right",
		            },
		            title: {
			              display: true,
			              text: this.diagramTitle
		            },
		            tooltips: {
			              mode: "index",
			              intersect: false,
		            },
		            hover: {
                    mode: "point",
			              intersect: true
		            },
		            scales: scales
	          }
        };
    },

    generate(config) {
        var $canvas = this.$root.find("canvas");

        $canvas.css({
            width: "100%",
        });
        $canvas.height($canvas.width() / 2);

        if (this.enableLogs) {
            console.log(config);
        }

        try {
            var diagram = new Chart($canvas[0].getContext('2d'), config);
        }
        catch(e) {
            var $errorNode =
                $("<span>" +
                  String(e) +
                  (e.stack ? "<br><br>" + e.stack : "") +
                  "</span>");

            $errorNode.css({
                backgroundColor: "lightgray",
                color: "red",
                transform: "translate(-50%, -50%)",
                top: "50%",
                left: "50%",
                position: "absolute"
            });

            this.$root.css({
                backgroundColor: "black",
                position: "relative",
                height: 300
            });
            this.$root.empty();
            this.$root.append($errorNode);
        }
    }
};
/* %} %ENDEXPORT% */

VizTools.Diagram.create($NODE,
                        %DIAG_TYPE%,
                        %DATASET%,
                        %DATASET_LABELS%,
                        %DATASET_META%,
                        %DIAGRAM_TITLE%,
                        %X_TITLE%,
                        %Y_TITLE%,
                        %ENABLE_LOGS%);
