$NODE = $("<div class='viztools_vhbox'></div>");

for (var i = 0; i < $CHILDREN.length; ++i) {
    var child = $CHILDREN[i];
    var childDomNode = child["node"];
    var helperNode = $("<div class='viztools_vhbox_helper'></div>");
    helperNode.append(childDomNode);
    $NODE.append(helperNode);
}
