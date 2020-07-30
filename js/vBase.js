var $temp = "%HTML%";

if ($temp) {
    var $NODE = $($temp);
} else {
    var $NODE = null;
}

var $ID = %ID%;
var $RENDERNAME = "%RENDERNAME%";


%JS%


return {
    node: $NODE
};
