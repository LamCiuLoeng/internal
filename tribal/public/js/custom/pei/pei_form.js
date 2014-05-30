function changeBillTo(obj){
	var t = $(obj);
	
	if (t.val() != '0') {
		$(".other_billto").hide();
		
		var vs = billToInfo[t.val()];
		
		$("#billAddress").attr("disabled", "disalbe");
		$("#billAttn").attr("disabled", "disalbe");
		$("#billTel").attr("disabled", "disalbe");
		$("#billFax").attr("disabled", "disalbe");
		$("#billEmail").attr("disabled", "disalbe");
		
		$("#billAddress").val(vs.address);
		$("#billAttn").val(vs.attn);
		$("#billTel").val(vs.tel);
		$("#billFax").val(vs.fax);
		$("#billEmail").val(vs.email);	
	} else {
		$("#billAddress").removeAttr("disabled");
		$("#billAttn").removeAttr("disabled");
		$("#billTel").removeAttr("disabled");
		$("#billFax").removeAttr("disabled");
		$("#billEmail").removeAttr("disabled");
		$(".other_billto").show();
	}
}

function changeShipTo(obj){
	var t = $(obj);
	
	if (t.val() != '0') {
		$(".other_shipto").hide();
		
		var vs = shipToInfo[t.val()];
		
		$("#shipAddress").attr("disabled", "disalbe");
		$("#shipAttn").attr("disabled", "disalbe");
		$("#shipTel").attr("disabled", "disalbe");
		$("#shipFax").attr("disabled", "disalbe");
		$("#shipEmail").attr("disabled", "disalbe");
		
		$("#shipAddress").val(vs.address);
		$("#shipAttn").val(vs.attn);
		$("#shipTel").val(vs.tel);
		$("#shipFax").val(vs.fax);
		$("#shipEmail").val(vs.email);
	} else {
		$("#shipAddress").removeAttr("disabled");
		$("#shipAttn").removeAttr("disabled");
		$("#shipTel").removeAttr("disabled");
		$("#shipFax").removeAttr("disabled");
		$("#shipEmail").removeAttr("disabled");
		$(".other_shipto").show();
	}
}


function toConfirm(){
	var valid = true;
	var msg = Array();
	
	if( !$("#buyerPO").val() ){ msg.push("* Please input the 'Buyer PO#'!"); };
	if( !$("#vendorPO").val() ){ msg.push("* Please select the 'Customer PO#'!"); };
	
	/*var isDesc = true;
	$("input[name^='itemDesc_']").each(function(){
		var t = $(this);
		var cls = t.attr("class").indexOf("required");
		if( cls != -1 && ( !t.val() || t.val() == "0" )){ isDesc = false; }
	});
	
	if(!isDesc){ msg.push("* Please input item description!"); }*/
	
	var isQtyInput = true;
	$("input[name^='price_']").each(function(){
		var qtyId = $(this).attr("name").split("_")[1];
		
		if($(this).val() && $(this).val() != "0") {
			if (!$("input[name^='quantity_" + qtyId + "']").val() || $("input[name^='quantity_" + qtyId + "']").val() == "0") {
				isQtyInput = false;
			}			
		}
	});
	
	if(!isQtyInput){ msg.push("* Please input Quantity!"); }
	
	var isPriceInput = true;
	$("input[name^='quantity_']").each(function(){
		var priceId = $(this).attr("name").split("_")[1];

		if($(this).val() && $(this).val() != "0") {
			if (!$("input[name^='price_" + priceId + "']").val() || $("input[name^='price_" + priceId + "']").val() == "0") {
				isPriceInput = false;
			}			
		}
	});
	
	if(!isPriceInput){ msg.push("* Please input Price!"); }
	
	/*var valid = true;
	$(".required").each(function(){
		var t = $(this);
		if(!t.val()){
			valid = false;
		}
	});*/

	if( msg.length > 0 ){
		$.prompt(msg.join("<br />"),{opacity: 0.6,prefix:'cleanred'});
		return false;
	}else{
		$.prompt("We are going to confirm your order information in our Production System upon your final confirmation.<br /> \
				 Are you sure to confirm the order now?",
	    		{opacity: 0.6,
	    		 prefix:'cleanblue',
	    		 buttons:{'Yes':true,'No,Go Back':false},
	    		 focus : 1,
	    		 callback : function(v,m,f){
	    		 	if(v){
	    		 		$("form").submit();
	    		 	}
	    		 }
	    		}
	    	);
	}
}

function toCancel(){
	if(confirm("The form hasn't been saved,are you sure to leave the page?")){
		return true;
	}else{
		return false;
	}
}

function removeThickBoxEvents() {
        $('.thickbox').each(function(i) {
            $(this).unbind('click');
        });
    }

function bindThickBoxEvents() {
        removeThickBoxEvents();
        tb_init('a.thickbox, area.thickbox, input.thickbox');
    }

var INDEX = 1;

function toAdd(){
	INDEX++;
	var c = $(".template");
	var tr = c.clone()
	$("td",tr).each(function(){
		var t = $(this);
		var n = t.attr("id").replace("_x","_"+INDEX);

		t.attr("id",n);
	});
	$("input",tr).each(function(){
		var t = $(this);
		var n = t.attr("name").replace("_x","_"+INDEX);
		var cls = t.attr("class");

		t.attr("name",n);
		if (t.attr("type") != "checkbox") {
			t.attr("class", cls + " required");
		}
	});
	/*$("a",tr).each(function(){
		var t = $(this);
		if (t.attr("class") == 'FC_item') {
			var func = function(){
				showFCDiv(this, INDEX);
			}
		} else {
			var func = function() {
				showWIDiv(this, INDEX);
			}
		}
		
		t.unbind('click').removeAttr('onclick');
		t.bind('click', func);
	});*/
	$("select",tr).each(function(){
		var t = $(this);
		var n = t.attr("name").replace("_x","_"+INDEX);
		var i = t.attr("id").replace("_x","_"+INDEX);

		t.attr("name",n);
		t.attr("id",i);
	});
	tr.insertBefore(c[0]);
	tr.removeClass("template");
	tr.show();
	bindThickBoxEvents();
	$(".numeric").numeric();
	$("input[name^='stock']",tr).focus();
}

function clearInput(obj,exclude){
	var t = $(obj).parents("table")[0];
	
	var excludeStr = "";
	if(exclude.length > 0){ 
		exclude.unshift("");
		exclude.push("");
		excludeStr = exclude.join("|");
	}
	
	$("input,select,textarea",t).each(function(){
		var temp = $(this);
		if( excludeStr.indexOf("|"+temp.attr("id")+"|") < 0 ){ temp.val(""); }
	});
}

function changeImg(obj) {
	var itemId = $(obj).val();
	var fieldId = $(obj).attr("id").split("_");
	var imgCol = $("#img_" + fieldId[1] + "_ext");
	imgCol.html("<a href='/images/pei/" +itemId + ".jpg' title='Sample Image' class='thickbox'>View Item</a>")
	bindThickBoxEvents();
}

$(document).ready(function(){

	$(".numeric").numeric();
	$('#photo').fancyZoom({directory:'/images/fancyZoom'});
	
	var dateFormat = 'yy-mm-dd';

    $('.datePicker').datepicker({firstDay: 1 , dateFormat: dateFormat});
});

function showShade() {
	$(".shade").css("display", "inline");
	$(".shade").css("width", $(document).width());
	$(".shade").css("height", $(document).height());
	
	$(".T_iframe").css("display", "inline");
	$(".T_iframe").css("width", $(document).width());
	$(".T_iframe").css("height", $(document).height());
	$(".T_iframe").css({'opacity':'0.0'});
	$(".shade").slideDown();
}

function editVariable(form, item) {
	var jq = $(".item_variable");
	
	if (form == '1') {
		$.get("/pei/ajax_tf_woven_label",{form: form, item: item}, function(html){
			jq.append(html);
			$(".numeric").numeric();
			put_tf_woven_label_json(item);
		});
	} else if (form == '2') {
		INDEX = 1;
		
		$.get("/pei/ajax_ca_hangtag",{form: form, item: item}, function(html){
			jq.append(html);
			$(".numeric").numeric();
			put_ca_hangtag_json(item);
		});
	}
	
	showShade();
	$(".item_variable").slideDown();
}

function viewVariable(header, form, item) {
	var jq = $(".item_variable");
	
	if (form == '1') {
		$.get("/pei/ajax_view_tf_woven_label",{header: header, item: item}, function(html){
			jq.append(html);
		});
	} else if (form == '2') {
		$.get("/pei/ajax_view_ca_hangtag",{header: header, item: item}, function(html){
			jq.append(html);
		});
	}
	
	showShade();
	$(".item_variable").slideDown();
}

function put_tf_woven_label_json(item) {
	var json_data = $("input[name='variable_" + item + "']").val();

	if(json_data != '') {
		var data = eval("(" + json_data + ")");
		
		for(var idx in data) {
			var detail = data[idx];
			
			if (parseInt(idx) > 0) {
				toAdd();
			}

			$("input[name='cor_" + (parseInt(idx) + 1) + "_ext']").val(detail.Country_of_Origin);
			$("#size_" + (parseInt(idx) + 1) + "_ext").val(detail.Size);
			$("input[name='qty_" + (parseInt(idx) + 1) +"_ext']").val(detail.Siz_Qty);
		}
	}
}

function put_ca_hangtag_json(item) {
	var json_data = $("input[name='variable_" + item + "']").val();

	if(json_data != '') {
		var data = eval("(" + json_data + ")");

		for(var idx in data) {
			var detail = data[idx];
			
			if (parseInt(idx) > 0) {
				toAdd();
			}

			$("#styleOne_" + (parseInt(idx) + 1) + "_ext").val(detail.Style.mainPart);
			$("#styleTwo_" + (parseInt(idx) + 1) + "_ext").val(detail.Style.extraPart);
			$("#colorName_" + (parseInt(idx) + 1) + "_ext").val(detail.Color.name);
			$("#colorCode_" + (parseInt(idx) + 1) + "_ext").val(detail.Color.code);
			$("#upc_" + (parseInt(idx) + 1) + "_ext").val(detail.UPC);
			$("#size_" + (parseInt(idx) + 1) + "_ext").val(detail.Size);
			$("input[name='qty_" + (parseInt(idx) + 1) +"_ext']").val(detail.Size_Qty);
		}
	}
}

function saveTFWovenLabelDiv(item) {
	var tf_woven_label_json = "[";
	var total = 0;

	$("input[name^='qty_']").each(function(){
		if($(this).val() && $(this).val() != "0") {
			var idx = $(this).attr("name").split("_")[1];
			var country = $("input[name='cor_" + idx + "_ext']").val();
			var size = $("#size_" + idx + "_ext").val();
			var qty = $(this).val();
			
			tf_woven_label_json += "{'Country_of_Origin': '" + country + "', 'Size': '"
			tf_woven_label_json += size + "', 'Size_Qty': '" + qty + "', 'Item_Group': '"
			tf_woven_label_json += idx + "'}, "
			
			total += parseInt($(this).val());
		}
	});
	
	tf_woven_label_json = tf_woven_label_json.substr(0, tf_woven_label_json.length - 2) + "]";
	
	$("input[name='variable_" + item + "']").val(tf_woven_label_json);
	$("input[name='quantity_" + item + "']").val(total);
	closeDiv();
}

function saveCAHangTagDiv(item) {
	var ca_hangtag_json = "[";
	var total = 0;

	$("input[name^='qty_']").each(function(){
		if($(this).val() && $(this).val() != "0") {
			var idx = $(this).attr("name").split("_")[1];
			var mainStyle = $("#styleOne_" + idx + "_ext").val();
			var extraStryle = $("#styleTwo_" + idx +"_ext").val();
			var color = $("#colorName_" + idx + "_ext").val();
			var colorCode = $("#colorCode_" + idx + "_ext").val();
			var upc = $("#upc_" + idx + "_ext").val();
			var size = $("#size_" + idx + "_ext").val();
			var qty = $(this).val();
			
			ca_hangtag_json += "{'Style': {'mainPart': '" + mainStyle + "', 'extraPart': '" + extraStryle
			ca_hangtag_json += "'}, 'Color': {'name': '" + color + "', 'code': '" + colorCode
			ca_hangtag_json += "'}, 'UPC': '" + upc + "', 'Size': '" + size + "', 'Size_Qty': '"
			ca_hangtag_json += qty + "', 'Item_Group': '" + idx + "'}, "
			
			total += parseInt($(this).val());
		}
	});
	
	ca_hangtag_json = ca_hangtag_json.substr(0, ca_hangtag_json.length - 2) + "]";
	
	$("input[name='variable_" + item + "']").val(ca_hangtag_json);
	$("input[name='quantity_" + item + "']").val(total);
	closeDiv();
}

function closeDiv() {
	$("#item_variables").remove();
	$(".shade").slideUp();
	$(".item_variable").slideUp();
}
