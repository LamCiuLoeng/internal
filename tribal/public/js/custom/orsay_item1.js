var globalCount = 0;
var changeSize = function(){
    var value = $('#size_input').val();
    if(value==0){
        $('#size1').fadeOut();
        $('#size_id').val(0);
    }else{
        var names=value.split(',');
        $('#size1').fadeIn();
        $('#size_id').val(names[0]);
        $('#size11').html('SIZE '+names[1]);
        $('#size12').html('EUR '+names[2]);
        $('#size13').html('SLO '+names[3]);
    }
}
var changeArticle = function(){
    var value = $('#article_desc_input').val();
    if(value==0){
        $('#article1').fadeOut();
        $('#article_desc_id').val(0);
    }else{
        var names=value.split(',');
        $('#article1').fadeIn();
        $('#article_desc_id').val(names[0]);
        $('#article1').html(names[1]);
    }
}
var changeReferenceNo = function(){
    $('#number1').fadeIn();
    $('#number11').html($('#reference_no').val()+'/'+$('#reference_color_no').val());
}
var changeOrderNo = function(){
    $('#number1').fadeIn();
    $('#number12').html($('#order_no').val());
}
var changeOrignCollection = function(){
    var value = $('#orign_collection_input').val();
    if(value==0){
        $('#collection1').fadeOut();
        $('#orign_collection_id').val(0);
    }
    else{
        var names=value.split(',');
        $('#orign_collection_id').val(names[0]);
        $('#collection1').fadeIn();
        $('#collection1').html(names[1]);
    }
}
var changeOrignLocation = function(){
    var value = $('#orign_location').val()
    $('#location1').fadeIn();
    $('#location1').html('Made in '+value);
}
var changeTrademark = function(){
    var value = $('#trademark').val()
    $('#trademark1').fadeIn();
    $('#trademark1').html(value);
}
var addPartRow = function(){$('#partLink').before('<div id="'+(++globalCount)+'" class="part1">'+$('#partDiv').html()+'</div>');}
var addPartRow1 = function(){addPartRow();addMaterialRow($('#'+globalCount+' > div > a'));}
var addMaterialRow = function(obj){$(obj).before('<div id="'+(++globalCount)+'">'+$('#materialDiv').html()+'</div>');$(".numeric").numeric();}
var delPartRow = function(obj){$(obj).parent().remove();writePart();}
var delMaterialRow = function(obj){
    obj = $(obj);
    var text = obj.prev().prev();
    text.val('');
    changeMaterialPercent(text);
    obj.parent().remove();
    writePart();
}
var changePart = function(obj){
    obj = $(obj);
    var count = 0;
    $('.partClass1').each(function(i, jq){
        var val = $(jq).val();
        if(val!=0&&obj.val()==val) count++;
    })
    if(count>1){
        obj.attr('selectedIndex', 0);
        alert("can't select same part option");
    }
    writePart();
}
var changeMaterial = function(obj){
    obj = $(obj);
    var val2 = $(obj).val();
    changeMaterialAll(obj, val2);
}
var changeMaterialPercent = function(obj){
    obj = $(obj);
    var val2 = $(obj).next().val();
    changeMaterialAll(obj, val2);
}
var changeMaterialAll = function(obj, val2){
    var parentId = obj.parent().parent().parent().attr('id');
    var total = 0;
    var error = false;
    var count = 0;
    $('#'+parentId+' > div > div').each(function(i, jq){
        jq = $(jq);
        var input = jq.find('input');
        var select = jq.find('select');
        var value1 = input.val();
        var value2 = select.val();
        if(value1!=''){
            if(parseFloat(value1)>0) total += parseFloat(value1);
            else error = true;
        }
        if(value2!=0&&value2==val2) count++;
    })
    if(error){
        alert('please input correct format');
        obj.val('');
    }else if(total>100){
        total -= parseFloat(obj.val());
        alert("the total of all you input can't more than 100");
        obj.val('');
    }else if(count>1){
        obj.attr('selectedIndex', 0);
        alert("can't select same material option");
    }
    writePart();
    $('#'+parentId+' > div > span').html('input: '+total+'% ; remainder: '+(100-total)+'%')
}
var writePart = function(){
    $('#part1').html('')
    $('.part1 > select').each(function(i, obj){
        obj = $(obj);
        var parentId = obj.parent().attr('id');
        var value = obj.val();
        var hasPart = value.length>1 ? true : false;
        var id=0,text='';
        if(hasPart){
            id = value.substring(0, value.indexOf(','));
            text = value.substring(value.indexOf(',')+1);
        }
        $('#part1').append('<div id="part1_'+parentId+'"><div class="part11">'+text+'</div><div class="part12 none">'+id+'</div></div>')
        var total = 0;
        $('#'+parentId+' > div > div').each(function(i, jq){
            jq = $(jq);
            var input = jq.find('input');
            var select = jq.find('select');
            var value1 = input.val();
            var value2 = select.val();
            if(value1!=''&&value2.length>1){
                total += parseFloat(value1);
                var id = value2.substring(0, value2.indexOf(','));
                var text = value2.substring(value2.indexOf(',')+1);
                $('#part1_'+parentId).append('<div class="material11">'+value1+'% </div><div class="material12">'+text+'</div><br/><div class="material13 none">'+id+'</div><div class="material14 none">'+value1+'</div>')
            }
        })
        if(total != 100) $('#part1_'+parentId).remove();
    })
}
var changeAppendix = function(obj){
    obj = $(obj);
    var count1 = 0;
    var value = obj.val();
    $('.appendixClass1').each(function(i, jq){
        var val = $(jq).val()
        if(value==val) count1++;
    })
    if(count1>1){
        obj.attr('selectedIndex',0);
        alert("can't select same option");
    }
    writeAppendix();
}
var writeAppendix = function(){
    $('#appendix1').html('')
    $('.appendix1 > select').each(function(i, obj){
        obj = $(obj);
        var parentId = obj.parent().attr('id');
        var value = obj.val();
        if(value.length>1){
            var id = value.substring(0, value.indexOf(','));
            var _text = value.substring(value.indexOf(',')+1);
            var text = _text.substring(_text.indexOf(',')+1);
            $('#appendix1').append('<div id="appendix1_'+parentId+'"><div class="appendix11">'+text+'</div><div class="appendix12 none">'+id+'</div></div>')
        }
    })
}
var delAppendix = function(parentId){$('#appendix1_'+parentId).remove();}
var addAppendixRow = function(){$('#appendixLink').before('<div id="'+(++globalCount)+'" class="appendix1">'+$('#appendixDiv').html()+'</div>');}
var delAppendixRow = function(obj){
    obj = $(obj);
    delAppendix(obj.parent().attr('id'));
    obj.parent().remove();
}