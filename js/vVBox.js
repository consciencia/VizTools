/* %EXPORT% %{ */
VizTools.VBox = {
    create($children, renderName) {
        var obj = {
            $root: $("<div class='viztools_vvbox'></div>"),
            $children: $children
        };
        obj.__proto__ = VizTools.VBox;

        obj.$root.attr("id", renderName);

        for (var i = 0; i < obj.$children.length; ++i) {
            var child = obj.$children[i];
            var childDomNode = child["node"];
            var $helperNode =
                $("<div class=\"viztools_vvbox_helper\"></div>");

            $helperNode.append(childDomNode);
            obj.$root.append($helperNode);
        }

        return obj;
    }
};
/* %} %ENDEXPORT% */

vbox = VizTools.VBox.create($CHILDREN, $RENDERNAME);
$NODE = vbox.$root;
