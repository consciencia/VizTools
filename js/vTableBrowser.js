/* %EXPORT% %{ */
VizTools.TableBrowser = {
    create($table, tableKeys, tableRows) {
        var obj = {
            $table: $table,
            $heading: $("<tr></tr>"),
            tableKeys: tableKeys,
            tableRows: tableRows
        };
        obj.__proto__ = VizTools.TableBrowser;

        obj.$table.append(obj.$heading);

        obj.createHeadings();
        obj.createRows();

        setTimeout(obj.resize.bind(obj), 100);

        return obj;
    },

    resize() {
        if (this.$table.is(':visible')) {
            this.$table.find("td, th").each(function() {
                var $cell = $(this);

                if (VizTools.Utils.nodeHeightInLines(this) > 1) {
                    $cell.css({
                        "font-size": "11px"
                    });
                }
            });
        } else {
            setTimeout(this.resize.bind(this), 100);
        }
    },

    createHeadings() {
        for (var i = 0; i < this.tableKeys.length; ++i) {
            var $column = $("<th>" + this.tableKeys[i]  + "</th>");
            $column.data("index", i);
            this.$heading.append($column);
        }
    },

    createRows() {
        for (var i = 0; i < this.tableRows.length; ++i) {
            var $row = $("<tr></tr>");
            this.$table.append($row);

            for (var y = 0; y < this.tableKeys.length; ++y) {
                var key = this.tableKeys[y];
                var val = this.tableRows[i][key];
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
