var style = %STYLE%;
var selector = %SELECTOR%;
var noLiveUpdates = %NOUPDATES%;
$NODE = $CHILDREN[0].node;

function setStyle() {
    if (selector) {
        $($NODE).find(selector).css(style);
    } else {
        $($NODE).css(style);
    }
}

setStyle();

if (!noLiveUpdates) {
    var MutationObserver = (window.MutationObserver
                            || window.WebKitMutationObserver
                            || window.MozMutationObserver);
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === "characterData") {
                setStyle();
            } else if (mutation.type === "childList") {
                if ( mutation.addedNodes.length) {
                    setStyle();
                }
            }
        });
    });
    observer.observe($NODE[0], {
        childList: true,
        characterData: true,
        subtree: true
    });
}
