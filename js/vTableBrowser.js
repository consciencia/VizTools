var tableKeys = %TABLE_KEYS%;
var tableRows = %TABLE_ROWS%;
var $table = $NODE.find("table");
var $heading = $("<tr></tr>");

for (var i = 0; i < tableKeys.length; ++i) {
    var $column = $("<th>" + tableKeys[i]  + "</th>");
    $heading.append($column);
}

$table.append($heading);

for (var i = 0; i < tableRows.length; ++i) {
    var $row = $("<tr></tr>");
    $table.append($row);

    for (var y = 0; y < tableKeys.length; ++y) {
        var key = tableKeys[y];
        var val = tableRows[i][key];
        var $column = $("<td>" + val + "</td>");
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
