/* %EXPORT% %{ */
VizTools.Menu = {
    create(children, renderName, menuLabels, defaultLabel) {
        var obj = {
            $root: $("<div class='viztools_vmenu'></div>"),
            children: children,
            renderName: renderName,
            menuLabels: menuLabels,
            defaultLabel: defaultLabel
        };
        obj.__proto__ = VizTools.Menu;

        obj.$root.attr("id", obj.renderName);
        var $menuBar = $("<div class='viztools_vmenu_bar'></div>");
        obj.$root.append($menuBar);
        var $contentBox = $("<div class='viztools_vmenu_box'></div>");
        obj.$root.append($contentBox);

        if (obj.children.length != obj.menuLabels.length)
        {
            throw Error("menuLabels.length != children.length'");
        }

        var defaultIndex = -1;
        var menuEntries = [];
        var $ul = $("<ul></ul>");
        $menuBar.append($ul);

        for (var i = 0; i < obj.menuLabels.length; ++i)
        {
            var $li = $("<li>" + obj.menuLabels[i]  + "</li>");

            $li.data("index", i);
            $li.on("click", function() {
                var index = Number($(this).data("index"));

                for (var y = 0; y < menuEntries.length; ++y)
                {
                    menuEntries[y].removeClass("clicked");
                }

                $(this).addClass("clicked");

                while ($contentBox[0].firstChild) {
                    $contentBox[0].removeChild($contentBox[0].firstChild);
                }

                $contentBox.append(obj.children[index].force().node);
            });

            $ul.append($li);
            menuEntries.push($li);

            if (obj.menuLabels[i] == obj.defaultLabel
                && defaultIndex < 0)  {
                defaultIndex = i;
                $li.addClass("clicked");
            }
        }

        if (defaultIndex >= 0) {
            $contentBox.append(obj.children[defaultIndex].force().node);
        }

        return obj;
    }
};
/* %} %ENDEXPORT% */

menu = VizTools.Menu.create($CHILDREN,
                            $RENDERNAME,
                            %MENU_LABELS%,
                            %DEFAULT_LABEL%);
$NODE = menu.$root;
