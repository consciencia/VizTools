/* %EXPORT% %{ */
VizTools.HBox = {
    create(children, renderName) {
        var obj = {
            $root: $("<div class='viztools_vhbox'></div>"),
            children: children,
            renderName: renderName
        };
        obj.__proto__ = VizTools.HBox;

        obj.$root.attr("id", obj.renderName);

        var percentagePerItem = 100 / obj.children.length;
        percentagePerItem = percentagePerItem.toString() + "%";

        for (var i = 0; i < obj.children.length; ++i) {
            var child = obj.children[i];
            var $helperNode =
                $("<div class='viztools_vhbox_helper' style='width: "
                  + percentagePerItem
                  + ";'></div>");

            $helperNode.append(child.node);
            obj.$root.append($helperNode);
        }

        return obj;
    }
};
/* %} %ENDEXPORT% */

hbox = VizTools.HBox.create($CHILDREN, $RENDERNAME);
$NODE = hbox.$root;
