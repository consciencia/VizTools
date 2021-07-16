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
        obj.createRows(0);

        setTimeout(obj.resize.bind(obj), 100);

        return obj;
    },

    resize() {
        if (this.$table.is(":visible")) {
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

    createRows(offset) {
        var blksize = 200;

        for (var i = offset;
             i < offset + blksize && i < this.tableRows.length;
             ++i) {
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

        var cb = this.createRows.bind(this);

        // This ugly workaround is for browser inability to render
        // large table at once. They just freeze and thats it.
        // When we incrementally add small blocks of rows, browsers
        // will surprisingly not freeze and render even very large
        // tables.
        setTimeout(() => cb(offset + blksize), 100);
    }
};
/* %} %ENDEXPORT% */

VizTools.TableBrowser.create($NODE.find("table"),
                             %TABLE_KEYS%,
                             %TABLE_ROWS%);
