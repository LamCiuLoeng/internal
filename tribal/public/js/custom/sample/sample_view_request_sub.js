var count = 11;
function ajaxMark(params){
	if(params.action == 'C' && $(".job_spands").length < 1){
		alert("Please add the job report before you mark the job as complete!");
		return ;
	}
	
	if(params.action == 'X'){
		if(!confirm('Are you sure to delete this item?')){
			return;
		}
	}
    $("body").mask("Loading...");
    params['timestr'] = Date.parse(new Date());
    $.getJSON("/sample/ajaxMark", params, function (req){
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

    var params = {
        "form_clz" : $("input[name='form_clz']",d).val(),
        "form_id"  : $("input[name='form_id']",d).val(),
        "time_spand"    : $("input[name='time_spand']",d).val(),
        "remark"   : $("textarea[name='remark']",d).val(),
        "complete_time" : $("input[name='complete_time']",d).val(),
        "designers" : $("#designers",d).val()
    };


    $(".spend",d).each(function(){
        var t= $(this);
        params[t.attr("name")] = t.val();
    });


    $(".one-row",d).each(function(){
        var t = $(this);
        params[$("select",t).attr("name")] = $("select",t).val();
        params[$("input",t).attr("name")] = $("input",t).val();
    });

    $.getJSON("/sample/ajaxAddJob",
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
    var html = '<tr class="job_tr"><td style="padding-top: 15px;"><hr><div class="job_spands">';

    for(var i=0;i<data.other_spend.length;i++){
        var t = data.other_spend[i];
        html += '<div class="job_spand"><label class="label">'+ t[0] +' :</label><div class="field">'+t[1]+'</div></div>';
    }

    html += '<div class="clear"><br /></div></div><table width="100%" cellspacing="5" cellpadding="0" border="0"><tbody>';

    for(var i = 0 ;i < data.material.length ; i++){
        html += '<tr><td width="15%" align="right" class="title-JL">Material :</td>'+
        '<td width="30%" class="sample-content">'+data.material[i].stock+'</td>'+
        '<td width="15%" align="right" class="title-JL">Qty :</td>'+
        '<td width="30%" class="sample-content">'+data.material[i].qty+'</td>'+
        '<td width="10%">&nbsp;</td></tr>';
    }

    html += '<tr><td align="right" class="title-JL">Mins : </td>' +
    '<td class="sample-content">'+data.time_spand+'</td>' +
    '<td align="right" class="title-JL">&nbsp;</td>' +
    '<td>&nbsp;</td><td>&nbsp;</td></tr>' +
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
		$.getJSON("/sample/ajaxDeleteJob",
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
    var params = {
        "t": clz
    }
    $.getJSON("/sample/ajaxJobForm", params, function(r){
        if(!r.success){
            alert(r.msg);
        }else{
            var k = $("#job-div").clone(true).addClass("clone-div");
            k.append('<input type="hidden" name="form_clz" value="'+clz+'"/>');
            k.append('<input type="hidden" name="form_id"  value="'+id+'"/>');

            var html = '';
            for(var i=0;i<r.formConfig.length;i++){
                var c = r.formConfig[i];
                html += '<div class="one_spand"><label class="label">' + c.label + ' :</label><input type="text" class="spend  numeric" name="'+c.name+'"/></div>';
            }
            html += '<div class="clear"><br /></div>';
            html = $(html);
            $(".numeric",html).numeric();
            $(".other_spand",k).append(html);

            if(!r.need_stock){
                $(".one-row",k).remove();
            }

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
    });
}





function addRow(obj){
    var t = $(obj);
    var c = $(".row-template",".clone-div").clone().addClass("one-row").removeClass("row-template");
    $("input,select",c).each(function(){
        var n = $(this).attr("name");
        $(this).attr("name",n.replace("_X","_"+count));
    });
    $(".numeric",c).numeric();
    c.insertAfter(t.parents(".one-row")[0]);
    count++;
    c.slideDown();
}

function removeRow(obj){
    var t = $(obj);
    var p = $(t.parents(".one-row")[0]);
    p.remove();
}



function updateJob(id){
	$.getJSON("/sample/ajaxJobInfo", {'job_id' : id}, function(r){
		if(!r.success){
			alert(r.msg);
		}else{
			var k = $("#job-div").clone(true).addClass("clone-div");
			k.append('<input type="hidden" name="job_id" value="'+id+'"/>');
			var html = '';
			for(var i=0;i<r.other_spend.length;i++){
				var c = r.other_spend[i];
				html += '<div class="one_spand"><label class="label">' + c[2].label + ' :</label><input type="text" class="spend  numeric" name="'+c[0]+'" value="'+c[1]+'" /></div>';
			}
			html += '<div class="clear"><br /></div>';
			html = $(html);
			$(".numeric",html).numeric();
			$(".other_spand",k).append(html);
			$(".one-row",k).remove();
			
			for(var i=0;i<r.materials.length;i++){
				var t = r.materials[i];
				var c = $(".row-template",k).clone().addClass("one-row").removeClass("row-template").css('display','block');
				$("select[name^='stock']",c).attr("name","oldstock_"+t[0]).val(t[1]);
				$("input[name^='qty']",c).attr("name","oldqty_"+t[0]).val(t[2]);
				$(".row-template",k).before(c);
			}
			
			
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

    var params = {
        "job_id"  : $("input[name='job_id']",d).val(),
        "time_spand"    : $("input[name='time_spand']",d).val(),
        "remark"   : $("textarea[name='remark']",d).val()
    };


    $(".spend",d).each(function(){
        var t= $(this);
        params[t.attr("name")] = t.val();
    });


    $(".one-row",d).each(function(){
        var t = $(this);
        params[$("select",t).attr("name")] = $("select",t).val();
        params[$("input",t).attr("name")] = $("input",t).val();
    });

    $.getJSON("/sample/ajaxReviseJob",
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