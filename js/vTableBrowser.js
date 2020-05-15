/* %EXPORT% %{ */
function getNumberOfLines(node) {
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
}

function tableResizer() {
    if (this.is(':visible')) {
        this.find("td, th").each(function() {
            var $cell = $(this);
            var lines = getNumberOfLines(this);

            if (lines > 1) {
                $cell.css({
                    "font-size": "11px"
                });
            }
        });
    } else {
        setTimeout(tableResizer.bind(this), 100);
    }
}

function tableCreateHeadings(tableKeys, $heading) {
    for (var i = 0; i < tableKeys.length; ++i) {
        var $column = $("<th>" + tableKeys[i]  + "</th>");
        $column.data("index", i);
        $heading.append($column);
    }
}

function tableCreateRows(tableKeys, tableRows, $table) {
    for (var i = 0; i < tableRows.length; ++i) {
        var $row = $("<tr></tr>");
        $table.append($row);

        for (var y = 0; y < tableKeys.length; ++y) {
            var key = tableKeys[y];
            var val = tableRows[i][key];
            var $column = $("<td>" + val + "</td>");
            $column.data("index", y);
            $column.data("value", val);
            $column.data("valueIsNumeric", !isNaN(Number(val)));
            $row.append($column);
        }

        $row.on("click", function() {
            var $this = $(this);

            if ($this.hasClass("mark")) {
                $this.removeClass("mark");
            } else {
                $this.addClass("mark");
            }
        });
    }
}
/* %} %ENDEXPORT% */

var tableKeys = %TABLE_KEYS%;
var tableRows = %TABLE_ROWS%;
var $table = $NODE.find("table");
var $heading = $("<tr></tr>");

$table.append($heading);
tableCreateHeadings(tableKeys, $heading);
tableCreateRows(tableKeys, tableRows, $table);

setTimeout(tableResizer.bind($table), 100);
