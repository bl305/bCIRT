var origheight=0;
var stretchheight="250px";
var idlast="";

function incrow(item,prefx,asize){
    var evitem=prefx+item;
    if (asize === undefined) {
        asize = stretchheight;
    }
    if (idlast == ""){
        origheight=document.getElementById(evitem).offsetHeight;
        document.getElementById(evitem).style.height = asize;
        idlast=evitem;
    }
    else{
        var changethis=idlast;
        var newheight=origheight+"px";
        document.getElementById(changethis).style.height = newheight;
        document.getElementById(evitem).style.height = asize;
        idlast=evitem;
    }
}


