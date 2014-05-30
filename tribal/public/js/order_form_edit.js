$(document).ready(function(){
	jQuery.validator.addMethod("isLabelCode", function(value, element) {
		return this.optional(element) || /^[1-8][A-S][1-5][1-2][A-M][1-4]$/.test(value);
	}, "input format: 1A21B4");
	
	$("#orderForm").validate({
		rules:{
			labelCode:{isLabelCode: true}
		},
		showErrors: function(errorMap, errorList){
			this.defaultShowErrors();
		}
	});
	
	
	$("select[name^='fc_'],select[name^='wi_']").change(function(){
		var t = $(this);
		var p = t.parent("td");
		var values = new Array();
		
		$("select",p).each(function(){
			var tmp = $(this);
			var s = $(":selected",tmp);
			if(s.val()){ 
				values.push(s.text());
			}
		});
		
		var n = t.attr("name");
		
		$("a",p).attr("href","/order/ajaxInstruction?cls="+n.split("_")[0]+"&val="+values.join(""));
		
	});
	
});
