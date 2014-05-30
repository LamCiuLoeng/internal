$(function(){
    $(".numeric").numeric();
    initDate();
});
var disableBtn = function(obj, bool){
    if(!(obj instanceof Array)) obj = [obj]
    for(var i=0;i<obj.length;i++){
        var jq = $(obj[i]);
        if(bool){
            jq.attr('disabled', true);
            jq.addClass("btndisable");
        }
        else{
            jq.attr('disabled', false);
            jq.removeClass("btndisable");
        }
    }
}

var toggleIcon = function(obj){
    if($(obj).parent().attr('class')=='toggle1'){
        $(obj).parent().next().slideUp();
        $(obj).parent().attr('class', 'toggle2')
    }else{
        $(obj).parent().next().slideDown();
        $(obj).parent().attr('class', 'toggle1')
    }
}

var getCboxArr = function(){
    var str = []
    $(".cboxClass").each(function(i, obj){
        var jq=$(obj)
        if(jq.attr('checked'))
            str.push(jq.val())
    })
    return str
}
var getCboxStr = function(){
    return getCboxArr().join(',')
}
var toSearch = function(){
    $('#search_form').submit();
}

var showError = function(msg){
    //if(msg instanceof Array) msg=msg.join('<br/>');
    //$.modaldialog.error(msg);
    $.prompt(msg,{
        opacity: 0.6,
        prefix:'cleanred'
    });
}
var showMsg = function(msg){
    //if(msg instanceof Array) msg=msg.join('<br/>');
    //$.growlUI('Success','  ');
    //$.modaldialog.success(msg);
    //$.prompt(msg,{opacity: 0.6,prefix:'cleanblue'});
    $.prompt(msg,{
        opacity: 0.6,
        prefix:'cleanblue'
    });
}