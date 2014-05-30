$(document).ready(function(){
    var dateFormat = 'yy-mm-dd';

    $(".datePicker").datepicker({firstDay: 1 , dateFormat: dateFormat});


     $("thead :checkbox").bind("click",function(){
		if($(this).attr("checked") == true){

			$("tbody :checkbox").each(function(){
				$("tbody input").attr("checked","checked");
			});

		}
		else{
			$("tbody :checkbox").each(function(){
			$("tbody input").removeAttr("checked");
			});
		}
		});

      $(".ajaxSearchField").each(function(){
        var jqObj = $(this);
        var latest = $('#search_form input[name=latest]').val() || 0;
            jqObj.autocomplete("/tag/getAjaxField", {
                    extraParams: {
                       fieldName: jqObj.attr("name"),
                       latest: latest
                    },
                    formatItem: function(item){
                           return item[0]
                    },
                    matchCase : false
            });

    });
});

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

function toExport(){
    var item_ids = "";
    
    $("tbody :checked").each(function(){
        item_ids += $(this).val() + "_" ;
    });
    if( item_ids == "" ){
        showError("Please select at least one record to generate the excel!");
    }else{
        $("#item_ids").val(item_ids);
        $("#record_form").submit();
    }

}



function span2input(span_id){
	if($("#recordsArea tbody input[id='"+span_id+"']").length ==0){
		var span2 = $("#" + span_id);
		var value = span2.text();
		if (jQuery.trim(value) == "") {
			span2.replaceWith("<input size=36 type='text' name='" + span_id + "' id='" + span_id + "' value='' ref='" + span2.text() + "'/>");
		}
		else {
			span2.replaceWith("<input size=36 type='text' name='" + span_id + "' id='" + span_id + "' value='" + span2.text() + "' ref='" + span2.text() + "'/>");
		}
	}
}

function input2span(input_id,flag){
	var input = $("#recordsArea tbody input[id='"+input_id+"']");
	if(input.length !=0){
		if(flag){
			input.replaceWith("<span id='"+input.attr("id")+"'>"+input.val()+"</span>");
		}else{
			input.replaceWith("<span id='"+input.attr("id")+"'>"+input.attr("ref")+"</span>");
		}
	}
}




var editStatus = false;
function addSO(){
	var checked = $("#recordsArea tbody :checked");
	if (checked.length==0){
		showError("Please select at least one record to add SO NO.");
		return
	}
	$("#recordsArea input[type='checkbox']").attr("disabled","disabled");
	checked.each(function(){
		span2input( "so_"+$(this).val());
                span2input( "soRemark_"+$(this).val());
	});
	editStatus = true;
}

function toCancel(){
	if(!editStatus){
		return ;
	}else{
		editStatus = false;
	}
	$("#recordsArea tbody input[type='text']").each(function(){
		input2span( $(this).attr("id"),false );
	});
	$("#recordsArea input[type='checkbox']").removeAttr("disabled");
	return;
}
$.ajaxSetup({ cache: false });
function toSave(){
	$(":checked").each(function(){
		var id = $(this).val();
		var so = jQuery.trim($("#so_" + id).val());
		var so_remark = jQuery.trim($("#soRemark_" + id).val());
	});
	////////////////////////////////////////////////////////////////////////////////////////
	if (!editStatus) {
		return;
	}
	else {
		editStatus = false;
	}
	var params = {};
	var flag = false;
	$("#recordsArea tbody input[type='text']").each(function(){
		var tmp = $(this);
		if(tmp.val() != tmp.attr("ref")){
			params[tmp.attr("name")] = jQuery.trim(tmp.val());
			flag = true;
		}
	});
	//If nothing change, don't submit to back-end,just return .
	if(!flag){
		showError("No record change!");
		$("#recordsArea tbody input[type='text']").each(function(){
			input2span( $(this).attr("id"),false );
		});
		$("#recordsArea input[type='checkbox']").removeAttr("disabled");
		return;
	}
	$.post(
	"/tag/saveSO",
	params,
	function(data){
		if (data["flag"] == "OK") {
			$("#recordsArea tbody input[type='text']").each(function(){
				input2span($(this).attr("id"), true);
			});
		}
		else {
			showError("The server is unavailable now,please try later!")
			$("#recordsArea tbody input[type='text']").each(function(){
				input2span($(this).attr("id"), false);
			});
		}
	$("#recordsArea input[type='checkbox']").removeAttr("disabled");
	}, 'json');

}


