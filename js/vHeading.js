var linkRef = %HEADING_HREF%;

if (linkRef.length) {
    var $link = $("<a></a>")
    $link.attr("href", linkRef)
    $link.append($NODE.contents())
    $NODE.empty()
    $NODE.append($link)
}
