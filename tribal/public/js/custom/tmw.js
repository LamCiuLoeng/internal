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
        // var latest = $('#search_form input[name=latest]').val() || 0;
            jqObj.autocomplete("/tmw/getAjaxField", {
                    extraParams: {
                       fieldName: jqObj.attr("name")
                       // latest: latest
                    },
                    formatItem: function(item){
                           return item[0];
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
    var item_ids = [];
    
    $("tbody :checked").each(function(){
        item_ids.push($(this).val());
    });
    if(item_ids.length < 1){
        showError("Please select at least one record to generate the report!");
    }else{
        $("#item_ids").val(item_ids.join("|"));
        $("#record_form").submit();
    }

}