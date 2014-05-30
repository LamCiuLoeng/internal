$(document).ready(function(){
    $(".numeric").numeric();
    $(".wi-select").change(function(){
        var t = $(this);
        var type = t.attr("name");
        if(!t.val()){
            $("#"+type+"_img").attr("src","/images/blank.png");
            $("#"+type+"_content").text("");
        }else{
            $.getJSON("/orsay/item2/ajaxGetWashing",{
                "id":t.val()
                },
            function(res){
                if(res.flag =="1"){
                    $.prompt("Error occur on the server side!",{
                        opacity: 0.6,
                        prefix:'cleanred'
                    });
                }else{
                    $("#"+type+"_img").attr("src",res.img);
                    $("#"+type+"_content").text(res.content);
                }
            });
        }
    });
});