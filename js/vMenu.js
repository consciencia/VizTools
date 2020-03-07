$NODE = $("<div class='viztools_vmenu'></div>");
$NODE.attr("id", $RENDERNAME);
var $menuBar = $("<div class='viztools_vmenu_bar'></div>");
$NODE.append($menuBar);
var $contentBox = $("<div class='viztools_vmenu_box'></div>");
$NODE.append($contentBox);
var menuLabels = %MENU_LABELS%;

if ($CHILDREN.length != menuLabels.length)
{
    throw Error("menuLabels != $CHILDREN'");
}

var defaultLabel = %DEFAULT_LABEL%;
var defaultIndex = -1;
var menuEntries = [];
var $ul = $("<ul></ul>");
$menuBar.append($ul);

for (var i = 0; i < menuLabels.length; ++i)
{
    var $li = $("<li>" + menuLabels[i]  + "</li>");
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

        $contentBox.append($CHILDREN[index].node);
    });

    $ul.append($li);
    menuEntries.push($li);

    if (menuLabels[i] == defaultLabel && defaultIndex < 0)  {
        defaultIndex = i;
        $li.addClass("clicked");
    }
}

if (defaultIndex >= 0) {
    $contentBox.append($CHILDREN[defaultIndex].node);
}
