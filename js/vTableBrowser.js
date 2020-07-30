/* %EXPORT% %{ */
VizTools.TableBrowser = {
    create($table, tableKeys, tableRows) {
        var $heading = $("<tr></tr>");

        $table.append($heading);
        VizTools.TableBrowser.createHeadings(tableKeys, $heading);
        VizTools.TableBrowser.createRows(tableKeys, tableRows, $table);

        setTimeout(VizTools.TableBrowser.resize.bind($table),
                   100);
    },

    resize() {
        if (this.is(':visible')) {
            this.find("td, th").each(function() {
                var $cell = $(this);

                if (VizTools.Utils.nodeHeighInLines(this) > 1) {
                    $cell.css({
                        "font-size": "11px"
                    });
                }
            });
        } else {
            setTimeout(VizTools.TableBrowser.resize.bind(this),
                       100);
        }
    },

    createHeadings(tableKeys, $heading) {
        for (var i = 0; i < tableKeys.length; ++i) {
            var $column = $("<th>" + tableKeys[i]  + "</th>");
            $column.data("index", i);
            $heading.append($column);
        }
    },

    createRows(tableKeys, tableRows, $table) {
        for (var i = 0; i < tableRows.length; ++i) {
            var $row = $("<tr></tr>");
            $table.append($row);

            for (var y = 0; y < tableKeys.length; ++y) {
                var key = tableKeys[y];
                var val = tableRows[i][key];
                var $column = $("<td>" + val + "</td>");
                $column.data("index", y);
                $column.data("value", val);
                $column.data("valueIsNumeric",
                             !isNaN(Number(val)));
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
};
/* %} %ENDEXPORT% */

VizTools.TableBrowser.create($NODE.find("table"),
                             %TABLE_KEYS%,
                             %TABLE_ROWS%);
