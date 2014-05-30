function changeBillTo(obj){
	var t = $(obj);
	var vs = billToInfo[t.val()];
	$("#billAddress").val(vs.address);
	$("#billAttn").val(vs.attn);
	$("#billTel").val(vs.tel);
	$("#billFax").val(vs.fax);
	$("#billEmail").val(vs.email);
}

function changeShipTo(obj){
	var t = $(obj);
	var vs = shipToInfo[t.val()];
	$("#shipAddress").val(vs.address);
	$("#shipAttn").val(vs.attn);
	$("#shipTel").val(vs.tel);
	$("#shipFax").val(vs.fax);
	$("#shipEmail").val(vs.email);
}


function toConfirm(){
	var valid = true;
	var msg = Array();
	
	if( !$("#buyerPO").val() ){ msg.push("* Please input the 'Vendor PO#'!"); };
	if( !$("#vendorPO").val() ){ msg.push("* Please select the 'Packaging Country'!"); };
	
	var isDesc = true;
	$("input[name^='itemDesc_']").each(function(){
		var t = $(this);
		var cls = t.attr("class").indexOf("required");
		if( cls != -1 && ( !t.val() || t.val() == "0" )){ isDesc = false; }
	});
	
	if(!isDesc){ msg.push("* Please input item description!"); }
	
	var isPriceInput = true;
	$("input[name^='price_']").each(function(){
		var t = $(this);
		var cls = t.attr("class").indexOf("required");
		if( cls != -1 && ( !t.val() || t.val() == "0" )){ isPriceInput = false; }
	});
	
	if(!isPriceInput){ msg.push("* Please input Prices!"); }
	
	var isQtyInput = true;
	$("input[name^='quantity_']").each(function(){
		var t = $(this);
		var cls = t.attr("class").indexOf("required");
		if( cls != -1 && ( !t.val() || t.val() == "0" )){ isQtyInput = false; }
	});
	
	if(!isQtyInput){ msg.push("* Please input quantity!"); }
	
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
