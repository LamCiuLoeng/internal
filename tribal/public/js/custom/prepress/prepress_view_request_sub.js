var count = 11;

function showStatusActionDialog(params) {
    var action_dict = {
        // action: [Dialog title, Div id of Cloned]
        'P': ['Pending','#pending-div'],
        'C': ['Complete','#complete-div'],
        'add_job_report': ['Job Report','#complete-div']
    }
    var args = action_dict[params.action]
    var clone_div = $(args[1]).clone(true);
    // If the action is add_job_report, you need update the hidden input value of clone_div.
    if(params.action == 'add_job_report') $("input[name='action']", clone_div).val("add_job_report")
    clone_div.dialog({
        title   : args[0],
        width   : 550,
        closeText : "Close",
        modal   : true,
        autoOpen: true,
        position: 'top',
        buttons: {
            'Submit': function() {
                if(params.action == 'P') {
                    var pending_reason = clone_div.find("#pending_reason").val();
                    if(pending_reason == "") {
                        clone_div.find(".validateTips").text("Reason is required").addClass("ui-state-error");
                        return false;
                    }
                    params['pending_reason'] = pending_reason
                    ajaxMark(params);
                } else {
                    var msg = [];
                    if(!$("input[name='time_spand']",clone_div).val()){
                        msg.push('Please fill in the "Mins".');
                    }
                    if(!$("input[name='item']",clone_div).val()){
                        msg.push('Please fill in the "Items".');
                    }
                    
                    if(msg.length > 0){
                        alert(msg.join("\n"));
                        return false;
                    }
                    clone_div.wrap('<form enctype="multipart/form-data" method="POST" action="/prepress/completeSubForm"></form>');
                    clone_div.parent("form").submit();
                }
            }
        },
        close: function(event, ui) {
            clone_div.remove()
        }
    });
}

function ajaxMark(params){
    // 如果点击的是Complete按钮，且没有添加 Job Report，则弹出Complete对话框，添加JobReport；否则直接改变状态。
	if(params.action == 'C' && $(".job_spands").length < 1){
        showStatusActionDialog(params);
		return ;
	}
	
	if(params.action == 'X'){
		if(!confirm('Are you sure to delete this item?')){
			return;
		}
	}
    $("body").mask("Loading...");
    params['timestr'] = Date.parse(new Date());
    $.getJSON("/prepress/ajaxMark", params, function (req){
        if( req.flag == "0" ){
            alert("The record has been updated successfully!");
            window.location.reload(true);
        }else if(req.flag == "2"){
            alert("No such action!");
        }else{
            alert("Error on the serve !");
        }
        $("body").unmask();
    })
}

function saveJob(){
    var d = $(".clone-div");

    if(!$("input[name='time_spand']",d).val()){
        alert("Please fill in the 'Mins' field!");
        return ;
    }
    
    if(!$("input[name='item']",d).val()){
        alert("Please fill in the 'Items' field!");
        return ;
    }

    var params = {
        "form_clz" : $("input[name='form_clz']",d).val(),
        "form_id"  : $("input[name='form_id']",d).val(),
        "time_spand"    : $("input[name='time_spand']",d).val(),
        "item"   : $("input[name='item']",d).val(),
        "remark"   : $("textarea[name='remark']",d).val(),
        "complete_time" : $("input[name='complete_time']",d).val(),
    };

    $.getJSON("/prepress/ajaxAddJob",
        params,
        function(req){
            if(req.flag!=0){
                alert("Error on the server side!");
            }else{
                alert("Save successfully!");
                var html = generateHTML(req.data);
                $("#jobs-table").append(html);
            }
            $(".clone-div").dialog("close");
        }
    );
}


function  generateHTML(data){
    var html = '<tr class="job_tr"><td style="padding-top: 15px;"><hr>';

    html += '<table width="100%" cellspacing="5" cellpadding="0" border="0"><tbody>';

    html += '<tr><td align="right" class="title-JL">Mins : </td>' +
    '<td class="sample-content">'+data.time_spand+'</td>' +
    '<td align="right" class="title-JL">&nbsp;</td>' +
    '<td>&nbsp;</td><td>&nbsp;</td></tr>' +
    '<tr><td align="right" class="title-JL">Items : </td>' + 
	'<td class="sample-content">'+data.remark+'</td>' + 
	'<td align="right" class="title-JL">&nbsp;</td>' + 
	'<td>&nbsp;</td>' + 
	'<td>&nbsp;</td></tr>' +    
    '<tr><td align="right" class="title-JL">Remark : </td><td class="sample-content" colspan="3">'+data.remark + '</td></tr>' +
    '<tr><td align="right" class="title-JL">Created By :</td>'+
    '<td class="sample-content">'+data.create_by+'</td>'+
    '<td align="right" class="title-JL">Creat Time :</td>'+
    '<td class="sample-content">'+data.create_time+'</td>'+
    '<td>&nbsp;</td></tr></tbody></table><p style="text-align:right">';
    
    html += '<input type="button" class="btn" value="Revise" onclick="updateJob('+data.id+')"/> ';
    html += '<input type="button" class="btn" value="Delete" onclick="deleteJobFromPage(this,'+data.id+')"/>';
    html +='</p></td></tr>' ;
    return html;
}


function deleteJobFromPage(obj,id) {
	if(confirm("Are you sure to delete this job report?")){
		$.getJSON("/prepress/ajaxDeleteJob",
	        {"id" : id},
	        function(req){
	            if(req.flag!=0){
	                alert("Error on the server side!");
	            }else{
	                alert("Delete the job successfully!");
	                var tr = $($(obj).parents(".job_tr")[0]);
					tr.remove();
	            }
	        }
	     );
	}
}

function reviseJob(){

}

function addHidden(clz,id){
	var k = $("#job-div").clone(true).addClass("clone-div");
	k.append('<input type="hidden" name="form_clz" value="'+clz+'"/>');
	k.append('<input type="hidden" name="form_id"  value="'+id+'"/>');
	$(".numeric",k).numeric();
	
    k.dialog({
        title   : "Job Report",
        width   : 550,
        closeText : "Close",
        buttons : {
            "Save":saveJob
        },
        modal   : true,
        autoOpen: false,
        close: function(event, ui) {
            k.remove();
        }
    });

    k.dialog("open");
}



function updateJob(id){
	$.getJSON("/prepress/ajaxJobInfo", {'job_id' : id}, function(r){
		if(!r.success){
			alert(r.msg);
		}else{
			var k = $("#job-div").clone(true).addClass("clone-div");
			k.append('<input type="hidden" name="job_id" value="'+id+'"/>');
			var html = '';
			html = $(html);
			$(".numeric",html).numeric();
			$(".one-row",k).remove();
			$("input[name='time_spand']",k).val(r.time_spand);
			$("textarea[name='remark'",k).val(r.remark);
			k.dialog({
                title   : "Job Report",
                width   : 550,
                closeText : "Close",
                buttons : {
                    "Save":saveReviseJob
                },
                modal   : true,
                autoOpen: false,
                close: function(event, ui) {
                    k.remove();
                }
            });

            k.dialog("open");
		}
	})
}

function saveReviseJob(){
	var d = $(".clone-div");

    if(!$("input[name='time_spand']",d).val()){
        alert("Please fill in the 'Mins' field!");
        return ;
    }
    
    if(!$("input[name='item']",d).val()){
        alert("Please fill in the 'Items' field!");
        return ;
    }

    var params = {
        "job_id"  : $("input[name='job_id']",d).val(),
        "time_spand"    : $("input[name='time_spand']",d).val(),
        "item" : $("input[name='item']",d).val(),
        "remark"   : $("textarea[name='remark']",d).val()
    };

	/*
    $(".spend",d).each(function(){
        var t= $(this);
        params[t.attr("name")] = t.val();
    });

    $(".one-row",d).each(function(){
        var t = $(this);
        params[$("select",t).attr("name")] = $("select",t).val();
        params[$("input",t).attr("name")] = $("input",t).val();
    });
	*/

    $.getJSON("/prepress/ajaxReviseJob",
        params,
        function(req){
            if(req.flag!=0){
                alert("Error on the server side!");
            }else{
                alert("Save successfully!");
                var html = generateHTML(req.data);
                $("#job_tr_"+params.job_id).replaceWith(html);
            }
            $(".clone-div").dialog("close");
        }
        );
}