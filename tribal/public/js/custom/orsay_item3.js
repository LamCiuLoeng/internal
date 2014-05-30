var globalCount = 0;
var size_val=[],article_val=[],collection_val=[],part_ids_val=[],material_ids_val=[],material_percents_val=[],appendix_ids_val=[];
var setFormVal = function(){
    $('#size_id').val(size_val[0]);
    $('#article_desc_id').val(article_val[0]);
    $('#orign_collection_id').val(collection_val[0]);
    $('#part_ids').val(part_ids_val.join(','));
    $('#material_ids').val(material_ids_val.join(','));
    $('#material_percents').val(material_percents_val.join(','));
    $('#appendix_ids').val(appendix_ids_val.join(','));
}
var initFormVal = function(id){
    $.getJSON("/orsay/item3/ajaxOrderInfo",{"id":id}, function(res){
        var detail = res.detail;
        var order = res.order;
        var percents = res.percents;
        var materials = res.materials;
        $('#order_id').val(order.id);
        $('#detail_id').val(detail.id);
        $('#company_code').val(order.company_code)
        $('#cust_name').val(order.cust_name)
        $('#cust_code').val(order.cust_code)
        $('#billto_address').val(order.billto_address)
        $('#billto_contact_sales').val(order.billto_contact_sales)
        $('#billto_tel_no').val(order.billto_tel_no)
        $('#shipto_address').val(order.shipto_address)
        $('#shipto_contact_person').val(order.shipto_contact_person)
        $('#shipto_tel_no').val(order.shipto_tel_no)
        $('#customer_po').val(order.customer_po);
        $('#qty').val(order.qty);
        changeSelect($('#size_input'), detail.size_id)
        changeSelect($('#article_input'), detail.article_desc_id)
        $('#reference_no').val(detail.reference_no)
        $('#reference_color_no').val(detail.reference_color_no)
        $('#order_no').val(detail.order_no)
        changeSelect($('#orign_collection_input'), detail.orign_collection_id)
        $('#orign_location').val(detail.orign_location)
        changeSelect($('#trademark'), detail.trademark)
        var part_ids = detail.part_ids.split(',');
        for(var i=0;i<part_ids.length;i++){
            addPartRow();
            var part = $('#partLink').prev();
            changeSelect($(' > select', part), part_ids[i]);
            var materialLink = $(' > div > a', part);
            for(var j=0;j<materials[i].length;j++){
                if(j>0)addMaterialRow(materialLink);
                var material = materialLink.prev();
                changeSelect($(' > select', material), materials[i][j].id);
                $(' > input', material).val(percents[i][j]);
            }
        }
        var appendix_ids = detail.appendix_ids.split(',');
        var openLink, pageObj;
        var j=0;
        for(var i=0;i<appendix_ids.length;i++){
            var id = appendix_ids[i];
            if(id==0){
                j=0;
                addAppendixPage();
                pageObj = $('#appendixPageLink').prev();
                openLink = $(' > a:last-child', pageObj);
            }else{
                if(j>0) addAppendixRow(openLink);
                var appendix = $(openLink).prev();
                changeSelect($(' > select', appendix), appendix_ids[i]);
                j++;
            }
        }
        writePage();
    });
}
var writePage = function(){
    writeSize()
    writeArticle()
    writeReferenceNo()
    writeReferenceColorNo()
    writeOrderNo()
    writeOrignCollection()
    writeOrignLocation()
    writeTrademark();
    writePart();
    writeAppendix();
}
var writeSize = function(){
    size_val = $('#size_input').val().split(',');
    if(size_val.length==1){
        $('#size11').html('');
        $('#size12').html('');
        $('#size13').html('');
    }else{
        $('#size11').html('SIZE '+size_val[1]);
        $('#size12').html('EUR '+size_val[2]);
        $('#size13').html('SLO '+size_val[3]);
    }
}
var writeArticle = function(){
    article_val = $('#article_input').val().split(',');
    if(article_val.length==1) $('#article1').html('&nbsp;');
    else $('#article1').html(article_val[1]);
}
var writeReferenceNo = function(){$('#number11').html($('#reference_no').val());}
var writeReferenceColorNo = function(){$('#number12').html($('#reference_color_no').val());}
var writeOrderNo = function(){$('#number13').html($('#order_no').val());}
var writeOrignCollection = function(){
    collection_val = $('#orign_collection_input').val().split(',');
    if(collection_val.length==1) $('#collection1').html('');
    else $('#collection1').html(collection_val[1]);
}
var writeOrignLocation = function(){$('#location1').html('Made in '+$('#orign_location').val());}
var writeTrademark = function(){$('#trademark1').html($('#trademark').val());}
var writePart = function(){
    $('#part1').html('')
    part_ids_val=[],material_ids_val=[],material_percents_val=[]
    var tmp_part_id = '';
    $('.part1 > select').each(function(i, obj){
        obj = $(obj);
        var parentId = obj.parent().attr('id');
        var value = obj.val();
        if(value.length>1){
            tmp_part_id=value.substring(0, value.indexOf(','));
            $('#part1').append('<div id="part1_'+parentId+'"><div class="part11">'+value.substring(value.indexOf(',')+1)+'</div></div>')
        }else $('#part1').append('<div id="part1_'+parentId+'"></div>')
        var total = 0;
        var tmp_material_ids_val=[],tmp_material_percents_val=[]
        $('#'+parentId+' > div > div').each(function(i, jq){
            jq = $(jq);
            var value1 = jq.find('input').val();
            var value2 = jq.find('select').val();
            if(value1!=''&&value2.length>1){
                total += parseFloat(value1);
                tmp_material_ids_val.push(value2.substring(0, value2.indexOf(',')))
                tmp_material_percents_val.push(value1)
                $('#part1_'+parentId).append('<div class="material11">'+value1+'% </div><div class="material12">'+value2.substring(value2.indexOf(',')+1).split('/').join('<br/>')+'</div><br/>')
            }
        })
        if(total != 100) $('#part1_'+parentId).remove();
        else{
            part_ids_val.push(tmp_part_id);
            material_ids_val=material_ids_val.concat(tmp_material_ids_val);
            material_percents_val=material_percents_val.concat(tmp_material_percents_val);
        }
    })
}
var writeAppendix = function(){
    $('.page11').each(function(i,obj){$(obj).find('div').html('')})
    appendix_ids_val=[]
    $('.page1').each(function(i,obj){
        appendix_ids_val.push(0)
        obj = $(obj)
        $(' > div > select', obj).each(function(i, select){
            select = $(select)
            var value = select.val();
            if(value.length>1){
                appendix_ids_val.push(value.substring(0, value.indexOf(',')));
                var _text = value.substring(value.indexOf(',')+1);
                var text = _text.substring(_text.indexOf(',')+1).split('/').join('<br/><br/>');
                $('#page_'+obj.attr('id')).find('div').append(text)
            }
        })
    })
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
    var parent = obj.parent().parent();
    var total = 0;
    var error = false;
    var count = 0;
    $(' > div', parent).each(function(i, jq){
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
    $(' > span', parent).html('input: '+total+'% ; remainder: '+(100-total)+'%')
    writePart();
}
var changeAppendix = function(obj){
    obj = $(obj);
    var count1 = 0;
    var value = obj.val();
    $('.appendixClass1').each(function(i, jq){
        var val = $(jq).val()
        if(value==val&&value!=0) count1++;
    })
    if(count1>1){
        obj.attr('selectedIndex',0);
        alert("can't select same option");
    }
    writeAppendix();
}
var addPartRow = function(){$('#partLink').before('<div id="'+(++globalCount)+'" class="part1">'+$('#partDiv').html()+'</div>');addMaterialRow($('#'+globalCount+' > div > a'));}
var delPartRow = function(obj){$(obj).parent().remove();writePart();}
var addMaterialRow = function(obj){$(obj).before('<div id="'+(++globalCount)+'">'+$('#materialDiv').html()+'</div>');$(".numeric").numeric();}
var delMaterialRow = function(obj){
    obj = $(obj);
    var text = obj.prev().prev();
    text.val('');
    changeMaterialPercent(text);
    obj.parent().remove();
    writePart();
}
var addAppendixPage = function(){
    $('#careLabelImage').append('<div id="page_'+(++globalCount)+'" class="box4 page11">'+$('#appendixPage').html()+'</div>')
    $('#appendixPageLink').before('<div id="'+(globalCount)+'" class="page1">'+$('#appendixPageDiv').html()+'</div>')
    addAppendixRow($('#'+globalCount+' > a').next());
}
var delAppendixPage = function(obj){
    obj = $(obj);
    var parent = obj.parent()
    var parent_id = parent.attr('id');
    parent.remove();
    $('#page_'+parent_id).remove();
    writeAppendix();
}
var addAppendixRow = function(obj){
    obj = $(obj);
    obj.before('<div id="'+(++globalCount)+'" class="appendix1">'+$('#appendixDiv').html()+'</div>');
}
var delAppendixRow = function(obj){
    obj = $(obj);
    var parent = obj.parent()
    $('#appendix1_'+parent.attr('id')).remove();
    parent.remove();
    writeAppendix();
}