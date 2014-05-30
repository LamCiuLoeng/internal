String.prototype.getQuery = function(name) {
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = this.substr(this.indexOf("\?")+1).match(reg);
    if (r!=null) return unescape(r[2]); return null;
}
function getTransaction(obj){
    var langs = ["deutsch", "franzosisch", "polnisch", "ungarisch", "tcheschisch", "englisch", "slowakisch", "rumanisch", "slowenisch"]
    var str = [];
    for(var i=0;i<langs.length;i++){
        str.push(obj[langs[i]])
    }
    return str.join(' / ')
}
function getID(str){
    if(str.indexOf(',')==-1) return str
    else return str.substring(0, str.indexOf(','));
}
function changeSelect(select, value){
    $(' option', select).each(function(i, obj){
        obj = $(obj)
        if(value==getID(obj.val())) obj.attr('selected','selected ')
    })
}
function getCustomerInfo(obj){
    var c = $(obj);
    if(c.val()==''){
    	//$("#billto_company_name").val('');
        $("#billto_address").val('');
        $("#billto_contact_sales").val('');
        $("#billto_tel_no").val('');
        $("#company_code").val('');
        $("#cust_name").val('');
        //$("#shipto_company_name").val('');
        $("#shipto_address").val('');
        $("#shipto_contact_person").val('');
        $("#shipto_tel_no").val('');
    }else{
        $("body").mask("Loading...");
        $.getJSON("/orsay/ajaxCustomerInfo", {
            "cn":c.val()
        }, function(res){
            if(res.flag == "1"){
                $.prompt("Error!",{
                    opacity: 0.6,
                    prefix:'cleanred'
                });
            }else{
                var b = res.data.billto[0];
                var s = res.data.shipto[0];
                $("#billto_address").val(b[0]);
                $("#billto_contact_sales").val(b[1]);
                $("#billto_tel_no").val(b[2]);
                $("#company_code").val(b[3]);
                $("#cust_name").val(b[4]);
                if(s!=undefined && s.length>0){
                    $("#shipto_address").val(s[0]);
                    $("#shipto_contact_person").val(s[1]);
                    $("#shipto_tel_no").val(s[2]);
                }else{
                    $("#shipto_address").val('N/A');
                    $("#shipto_contact_person").val('N/A');
                    $("#shipto_tel_no").val('N/A');
                }
            }
            $('body').unmask();
        });
    }
}
function toCancel(){
    if(confirm("The form hasn't been saved,are you sure to leave the page?")) return true;
    else return false;
}
function toConfirm(flag){
    var msg
    if(flag==1){
        var part_ids_val=[],material_ids_val=[],material_percents_val=[],appendix_ids_val=[];
        $('.part12').each(function(i,obj){part_ids_val.push($(obj).html());})
        $('.material14').each(function(i,obj){material_percents_val.push($(obj).html());})
        $('.material13').each(function(i,obj){material_ids_val.push($(obj).html());})
        $('.appendix12').each(function(i,obj){appendix_ids_val.push($(obj).html());})
        $('#part_ids').val(part_ids_val);
        $('#material_ids').val(material_ids_val);
        $('#material_percents').val(material_percents_val);
        $('#appendix_ids').val(appendix_ids_val);
        msg = validation1();
    }else if(flag==2){
        msg = validation2();
    }else if(flag==3){
        setFormVal();
        msg = validation1();
    }
    if(msg.length > 0){
        var message = "<p>Sorry that can't submit the form ,please check and modify your input as the below:</p><ul>";
        for(i in msg){
            message += "<li>"+msg[i]+"</li>";
        }
        message += "</ul>";
        $.prompt(message,{
            opacity: 0.6,
            prefix:'cleanred'
        });
        return false;
    }
    $.prompt("We are going to confirm your order information in our Production System upon your final confirmation.<br /> \
                 Are you sure to confirm the order now?",{
        opacity: 0.6,
        prefix:'cleanblue',
        buttons:{
            'Yes':true,
            'No,Go Back':false
        },
        focus : 1,
        callback : function(v,m,f){
            if(v) $('#_form').submit();
        }
    });
}
function validation1(){
    var msg = Array();
    if(!$("#cust_code").val())
        msg.push("Please select the 'Customer.'!");
    if(!$("#customer_po").val())
        msg.push("Please input the 'Customer Order No.'!");
    if(!$("#qty").val())
        msg.push("Please input the 'Total this order Quantity (pieces)'!");
    if($('#size_id').val()==0)
        msg.push("Please select the 'Size'!");
    if($('#article_desc_id').val()==0)
        msg.push("please select 'article description'!");
    if(!$('#reference_no').val())
        msg.push("Please input the 'Reference code'!");
    else if($('#reference_no').val().length != 6)
        msg.push("Please check the Reference code must 6-digital number!");
    if(!$("#reference_color_no").val())
        msg.push("Please input the 'Reference color code'!");
    else if($('#reference_color_no').val().length != 2)
        msg.push("Please check the Reference color code must 2-digital number!");
    if(!$("#order_no").val())
        msg.push("Please input the 'Order no'!");
    else if($('#order_no').val().length != 6)
        msg.push("Please check the Order no must 6-digital number!");
    if($('#orign_collection_id').val()==0)
        msg.push("Please select the 'orign collection'!");
    if($('#orign_location').val()==0)
        msg.push("Please select the 'orign location'!");
    //if($('#part_ids').val().length==0)
    //    msg.push("Please select the 'part'!");
    /*if($('#material_ids').val().length==0)
        msg.push("Please select the 'material'!");
    if(appendix_ids.length==0)
        msg.push("Please select the 'appendix'!");*/
    return msg;
}
function validation2(){
    var msg = Array();
    if(!$("#cust_code").val())
        msg.push("Please select the 'Customer.'!");
    if( !$("#customer_po").val() )
        msg.push("Please input the 'Customer Order No.'!");
    if( !$("#qty").val() )
        msg.push("Please input the 'Total this order Quantity (pieces)'!");
    if( !$("#washing").val() )
        msg.push("Please input the 'Washing'!");
    if( !$("#bleeding").val() )
        msg.push("Please input the 'Bleeding'!");
    if( !$("#various").val() )
        msg.push("Please input the 'Various'!");
    if( !$("#ironing").val() )
        msg.push("Please input the 'Ironing'!");
    if( !$("#accessories").val() )
        msg.push("Please input the 'Accessories'!");
    return msg;
}
function toSearch(){
	$('#_form').submit();
}