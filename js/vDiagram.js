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

        var targetDatasets = obj.createDataset();
        var scales = obj.createScales();
        var config = obj.createConfig(targetDatasets,
                                      scales);
        obj.generate(config);

        return obj;
    },

    isSingleDiag() {
        return (this.diagType == "polarArea"
                || this.diagType == "doughnut"
                || this.diagType == "pie");
    },

    createDataset() {
        var targetDatasets = [];

        for (var i = 0; i < this.dataset.length; ++i) {
            var d = this.dataset[i];
            var m = this.datasetMeta[i];
            pairs = [];

            if (this.isSingleDiag()) {
                pairs = d.y;
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

            if (!m.interpolation) {
                result.lineTension = 0;
            }

            if (this.isSingleDiag()) {
                result.fill = undefined;
                result.lineTension = undefined;
            }

            targetDatasets.push(result);
        }

        return targetDatasets;
    },

    createScales() {
        if (this.isSingleDiag()) {
            return {
	            ticks: {
		            beginAtZero: true
	            },
	            reverse: false
            };
        } else {
            return {
	            xAxes: [{
		            display: true,
		            scaleLabel: {
			            display: true,
			            labelString: this.xTitle
		            }
	            }],
	            yAxes: [{
		            display: true,
		            scaleLabel: {
			            display: true,
			            labelString: this.yTitle
		            },
                    ticks: {
		                beginAtZero: true
	                }
	            }]
            };
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
