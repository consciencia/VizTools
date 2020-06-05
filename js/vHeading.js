var linkRef = %HEADING_HREF%;

if (linkRef.length) {
    var $link = $("<a></a>")
    $link.attr("href", linkRef)
    $link.attr("target", "_blank")
    $link.append($NODE.contents())
    $NODE.empty()
    $NODE.append($link)
}
