var diagType = %DIAG_TYPE%;
var dataset = %DATASET%;
var datasetLabels = %DATASET_LABELS%;
var datasetMeta = %DATASET_META%;
var diagramTitle = %DIAGRAM_TITLE%;
var xTitle = %X_TITLE%;
var yTitle = %Y_TITLE%;
var enableLogs = %ENABLE_LOGS%;
var $canvas = $NODE.find("canvas");
var targetDatasets = [];

function isRelType(t) {
    return (t == "polarArea"
            || t == "doughnut"
            || t == "pie");
}

for (var i = 0; i < dataset.length; ++i) {
    var d = dataset[i];
    var m = datasetMeta[i];
    pairs = [];

    if (isRelType(diagType)) {
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

    if (isRelType(diagType)) {
        result.fill = undefined;
        result.lineTension = undefined;
    }

    targetDatasets.push(result);
}

if (isRelType(diagType)) {
    var scales = {
	    ticks: {
		    beginAtZero: true
	    },
	    reverse: false
    };
} else {
    var scales = {
	    xAxes: [{
		    display: true,
		    scaleLabel: {
			    display: true,
			    labelString: xTitle
		    }
	    }],
	    yAxes: [{
		    display: true,
		    scaleLabel: {
			    display: true,
			    labelString: yTitle
		    }
	    }]
    };
}

var config = {
	type: diagType,
	data: {
        labels: datasetLabels,
		datasets: targetDatasets
	},
	options: {
		responsive: true,
        legend: {
			position: "right",
		},
		title: {
			display: true,
			text: diagramTitle
		},
		tooltips: {
			mode: 'index',
			intersect: false,
		},
		hover: {
			mode: 'nearest',
			intersect: true
		},
		scales: scales
	}
};

if (enableLogs) {
    console.log(config);
}

try {
    var diagram = new Chart($canvas[0].getContext('2d'), config);
}
catch(e) {
    var $errorNode = $("<span>" +
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

    $NODE.css({
        backgroundColor: "black",
        position: "relative",
        height: 300
    });
    $NODE.empty();
    $NODE.append($errorNode);
}
