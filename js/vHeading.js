/* %EXPORT% %{ */
VizTools.Heading = {
    create(node, linkRef) {
        var obj = {
            node: node,
            linkRef: linkRef
        };
        obj.__proto__ = VizTools.Heading;

        if (obj.linkRef.length) {
            var $link = $("<a></a>")
            $link.attr("href", obj.linkRef)
            $link.attr("target", "_blank")
            $link.append(obj.node.contents())
            obj.node.empty()
            obj.node.append($link)
        }

        return obj;
    }
};
/* %} %ENDEXPORT% */

heading = VizTools.Heading.create($NODE,
                                  %HEADING_HREF%);
$NODE = heading.node;
