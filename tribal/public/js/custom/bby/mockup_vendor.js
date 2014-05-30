function toEdit(obj){
    var t = $(obj);
    var view_div = $(t.parents(".option-view")[0]);
    var edit_div = $(view_div.siblings(".option-edit")[0]);
    view_div.slideUp();
    edit_div.slideDown();
}

function toCancel(obj){
    var t = $(obj);
    var edit_div = $(t.parents(".option-edit")[0]);
    var view_div = $(edit_div.siblings(".option-view")[0]);
    edit_div.slideUp();
    view_div.slideDown();
}

function toSend(){
    return confirm("Are you sure to send the record to next step?");
}

function toSubmit(){
    return confirm("Are you sure to confirm the record?");
}
function toSave(obj) {
    var t = $(obj);
    var form = t.parents("form")[0];
    $(".template",form).remove();
    $(form).submit();
}

var count = max_id;  //come from the python code in the template ,which mean the last id + 100, to avoid the duplicate id


function addline(obj,template_clz,append_clz){
    var div = $($(obj).parents(".option-edit")[0]);
    var t = $(".template."+template_clz,div);
	
    var n = t.clone();
    $('.datePicker',n).attr("id","");
    n.removeClass("template");
	
    //	var index = count++;
    //	$("input,select,textarea",n).each(function(){
    //		var tmp = $(this);
    //		var new_name = tmp.attr("name").replace("_x","_"+index);
    //		tmp.removeClass("hasDatepicker");
    //		tmp.attr("name",new_name);
    //	});
	
    $("fieldset",n).each(function(){
//        var index = count++;
        $("input,select,textarea",this).each(function(){
            var tmp = $(this);
	/*
            var new_name = tmp.attr("name").replace("_x","_"+index);
            tmp.attr("name",new_name);
	*/
            tmp.removeClass("hasDatepicker");
        });
    });
    $('.datePicker',n).datepicker({
        changeMonth : true,
        changeYear : true,
        dateFormat : dateFormat
    });
	
    var table = $(t.parents("table")[0]);
    table.append(n);
    reindex(table);
//	table = $("."+append_clz);	
//	table.append(n);    	
//	var child_index = 1;
//	table.children("tbody").children("tr").each(function(){
//		var tmp = $(this);
//		if(!tmp.hasClass('template')){
//			tmp.children("td:first-child").children("span").text(child_index);
//			child_index++;
//		}
//	});
	
}

function reindex(table){
    var child_index = 1;
    table.children("tbody").children("tr").each(function(){
        var tmp = $(this);
        if(!tmp.hasClass('template')){
            tmp.children("td:first-child").children("span").text(child_index);
            $("input[type='hidden'][name^='round_']",tmp).val(child_index);
            child_index++;
        }
    });
}



function addsline(obj,template_clz){
    var td = $($(obj).parents("td")[0]);
    var t = $(".template."+template_clz,td);
    var n = t.clone();
    $('.datePicker',n).attr("id","");
    n.removeClass("template");
    var index = count++;
    $("input,select,textarea",n).each(function(){
        var tmp = $(this);
        var new_name = tmp.attr("name").replace("_x","_"+index);
        tmp.removeClass("hasDatepicker");
        tmp.attr("name",new_name);
    });
	
    $('.datePicker',n).datepicker({
        changeMonth : true,
        changeYear : true,
        dateFormat : dateFormat
    });
    var table = $(t.parents("table")[0]);
    table.append(n);
}


function deletesline(obj){
    var t = $(obj);
    var table = $(t.parents("table")[0]);
    $(t.parents("tr")[0]).remove();
}


function deletebline(obj){
    var t = $(obj);
    var table = $(t.parents("table")[0]);
    $(t.parents("tr")[0]).remove();

    reindex(table);
}


function addFile(obj){
    var td = $(obj).parents("td")[0];
    var table = $(".popup-table",td);

    var tmp = $(".template",table).clone();
    tmp.removeClass("template");
    var index = count++;
    $("input",tmp).each(function(){
        var t = $(this);
        t.attr("name",t.attr("name")+"_"+index);
    });
    table.append(tmp);
}

function delFile(obj){
    var tr = $(obj).parents("tr")[0];
    $(tr).remove();
}


function getFileName(obj){
    var tmp = $(obj);
    var path = tmp.val();
    if( path && path.length > 0){
        var location = path.lastIndexOf("\\") > -1 ?path.lastIndexOf("\\") + 1 : 0;
        var fn = path.substr( location,path.length-location );
		
        var tr = tmp.parents("tr")[0];
        $("input[type='text']",tr).val(fn);
		
    //tmp.prev("input[type='text']").val(fn);
    }
}

function ajaxDelFile(type,id,fid,obj) {
    if(!confirm("Are you sure to delete the file?")){
        return
    }
    $.getJSON("/bbymockup/ajaxDeleteFile",
    {
        "type" : type,
        "id" : id,
        "fid" : fid,
        "datetime" : (new Date()).getTime()
    },
    function(r){
        if(r.result == "0"){
            alert("Delete the file successfully!");
            $($(obj).parents("li")[0]).remove();
        }else{
            alert("Error when deleting the file!");
        }
    });
}
function ajaxDelPdfFile(type,id,fid,obj) {
    if(!confirm("Are you sure to delete the file?")){
        return
    }
    $.getJSON("/bbymockup/ajaxDeleteFile",{
        "type" : type,
        "id" : id,
        "fid" : fid,
        "datetime" : (new Date()).getTime(),
        "attachment_pdf": true
    },function(r){
        if(r.result == "0"){
            alert("Delete the file successfully!");
            $(obj).parent().parent().remove();
        }else{
            alert("Error when deleting the file!");
        }
    });
}