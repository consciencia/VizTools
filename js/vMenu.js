$NODE = $("<div class='viztools_vmenu'></div>");
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
var $ul = $("<ul></ul>");
$menuBar.append($ul);

for (var i = 0; i < menuLabels.length; ++i)
{
    var $li = $("<li>" + menuLabels[i]  + "</li>");
    $li.data("index", i);
    $li.on("click", function() {
        var index = Number($(this).data("index"));

        while ($contentBox[0].firstChild) {
            $contentBox[0].removeChild($contentBox[0].firstChild);
        }

        $contentBox.append($CHILDREN[index].node);
    });
    $ul.append($li);

    if (menuLabels[i] == defaultLabel && defaultIndex < 0)  {
        defaultIndex = i;
    }
}

if (defaultIndex >= 0) {
    $contentBox.append($CHILDREN[defaultIndex].node);
}
