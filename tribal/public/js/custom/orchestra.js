$(document).ready(function($) {
	initInlinesForm([
    	["#fabric-group>div", 'fabric_set', 'Add Fabric']
    ])
    changeItem()
})
var showError=function(msg){
    //if(msg instanceof Array) msg=msg.join('<br/>');
    //$.modaldialog.error(msg);
    $.prompt(msg,{
        opacity: 0.6,
        prefix:'cleanred',
        top:'40%',
        left:'35%'
    });
}
var toCreate=function(){
	$('#id').val('');
	toConfirm();
}
var toConfirm=function(){
	var msg = []
	var fabric_length = $('.a_add_composition').length-1;
	if(fabric_length>0){
		var totalPercents = 0;
		$("input[name^='fabric_set'][name$='composition_percents']").each(function(){
			if($(this).val())
				totalPercents+=parseInt($(this).val());
		})
		if(totalPercents != fabric_length*100){
			msg.push('The sum number of percents on each fabric must 100%.')
		}
	}else
		msg.push('Please at least add one fabric & compositions.')

	if($('input[name=product_family_langs]:checked').length==-1)
		msg.push('Please at least select one product family language.')
	
	var flag = false;
	$('.required').each(function(){
		var fieldType = $(this).attr('type')
		if(!$(this).attr('disabled') && $(this).attr('name').indexOf('__prefix__')==-1 && !flag){
			if(fieldType=='checkbox' || fieldType=='radio'){
				if($('input[name='+$(this).attr('name')+']:checked').length==0){
					flag = true
				}
			}else if($(this).val()==''){
				flag = true
			}
		}
	})
	if(flag) msg.push('Please input value for the <span class=red>*</span> fields.')
	if(msg.length==0){
		$('#care_img_ids').val($('input[name=_care_img_wash]:checked').val()+','+$('input[name=_care_img_bleach]:checked').val()+','+$('input[name=_care_img_dry]:checked').val()+','+$('input[name=_care_img_iron]:checked').val()+','+$('input[name=_care_img_clean]:checked').val())
		$('#_form').submit()
	}else showError(msg.join('</br>'))
}
var addComposition=function(obj){
	$(obj).before('<div>'+$(obj).parent().children().html()+'<a class="deletelink" href="javascript:void(0)" onclick="delComposition(this)"></a></div>')
}
var delComposition=function(obj){
	$(obj).parent().remove();
}
var delFabric=function(obj){
	$(obj).parent().remove();
}
var addCare=function(obj){
	$('#a_add_care').before('<div>'+$(obj).parent().children().html()+' <a class="deletelink" href="javascript:void(0)" onclick="delCare(this)"></a></div>')
}
var delCare=function(obj){
	$(obj).parent().remove();
}
var changeCustomer=function(obj){
	if($(obj).val()){
		var json = customers_json[$(obj).val()];
		if($(obj).attr('name').indexOf('billto')==0){
			$('#billto_name').val(json.name);
			$('#billto_contact').val(json.contact);
			$('#billto_email').val(json.email);
		}else if($(obj).attr('name').indexOf('shipto')==0){
			$('#shipto_name').val(json.name);
			$('#shipto_contact').val(json.contact);
			$('#shipto_email').val(json.email);
		}
	}else{
		if($(obj).attr('name').indexOf('billto')==0){
			$('#billto_name').val('');
			$('#billto_contact').val('');
			$('#billto_email').val('');
		}else if($(obj).attr('name').indexOf('shipto')==0){
			$('#shipto_name').val('');
			$('#shipto_contact').val('');
			$('#shipto_email').val('');
		}
	}
}
var changeItem=function(){
	var obj = $('#item_id')
	var value = $('option:selected', obj).text()
	if(value.indexOf('& ')>=0)
		obj.next().attr('disabled', false)
	else{
		obj.next().val('')
		obj.next().attr('disabled', true)
	}
}