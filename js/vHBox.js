$NODE = $("<div class='viztools_vhbox'></div>");
$NODE.attr("id", $RENDERNAME);

var percentagePerItem = 99 / $CHILDREN.length;
percentagePerItem = percentagePerItem.toString() + "%";

for (var i = 0; i < $CHILDREN.length; ++i) {
    var child = $CHILDREN[i];
    var childDomNode = child["node"];
    var helperNode = $("<div class='viztools_vhbox_helper' style='width: "
                       + percentagePerItem
                       + ";'></div>");
    helperNode.append(childDomNode);
    $NODE.append(helperNode);
}
