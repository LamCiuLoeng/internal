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

function ajaxDelFile(type,id,fid,obj){
	if(!confirm("Are you sure to delete the file?")){
		return 
	}
	$.getJSON("/bbymockup/ajaxDeleteFile",
          {
          	type : type,
          	id : id,
          	fid : fid
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


var count = 100;

/*
function addline(obj,clz){
	var div = $($(obj).parents(".option-edit")[0]);
	var t = $(".template."+clz,div);
	
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
	var child_index = 1;
	table.children("tbody").children("tr").each(function(){
		var tmp = $(this);
		if(!tmp.hasClass('template')){
			tmp.children("td:first-child").children("span").text(child_index);
			child_index++;
		}
	});
}
*/

function deletebline(obj){
	var t = $(obj);
	var table = $(t.parents("table")[0]);  	
	$(t.parents(".bline")[0]).remove();
	var child_index = 1;
	
	table.children("tbody").children("tr").each(function(){
		var tmp = $(this);
		if(!tmp.hasClass('template')){
			tmp.children("td:first-child").children("span").text(child_index);
			child_index++;
		}
	});
}


function showDialog(obj){
	var td = $(obj).parents("td")[0];
	var div = $(".popup-div",td);
	alert(div.length);
	$(div).dialog("open");
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









//new add function
function addTesting(obj,clz){
	var btn = $(obj)
	var div = $(btn.parents(".option-edit")[0]);
	var round = btn.attr("round");
	var line = btn.attr("line");
	
	var t = $(".template."+clz,div);
	var n = t.clone();
	$('.datePicker',n).attr("id","");
	n.removeClass("template");
	
	$("fieldset",n).each(function(){
		var index = count++;
		var fieldset = $(this);
		$("input,select,textarea",fieldset).each(function(){
			var tmp = $(this);
			var new_name = tmp.attr("name").replace("_x","_"+index);
			tmp.removeClass("hasDatepicker");
			tmp.attr("name",new_name);
		});
		$("input[name^='new_test_round_']",fieldset).val(round);
		$("input[name^='new_test_line_']",fieldset).val(line);
	});
	btn.attr("line",parseInt(line)+1);
	$("span",n).text(round);
	
	$('.datePicker',n).datepicker({
	        changeMonth : true,
	        changeYear : true,
	        dateFormat : dateFormat
	});
	
	var table = $(t.parents("table")[0]);    	
	table.append(n);    	

}


function delTesting(obj){
	var t = $(obj);
	var table = $(t.parents("table")[0]);  	
	$(t.parents(".bline")[0]).remove();
}


function addFitting(obj,clz){
	var btn = $(obj);
	var div = $($(obj).parents(".option-edit")[0]);
	var t = $(".template."+clz,div);
	
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
	
	//update the round for the testing
	var max_round = btn.attr("max_round");
	$("input[name^='internal_new_round_']",n).val(max_round);
	$(".testing_btn",n).attr("round",max_round);
	btn.attr("max_round",parseInt(max_round)+1);
	
	var table = $(t.parents("table")[0]);    	
	table.append(n);    	
	var child_index = 1;
	table.children("tbody").children("tr").each(function(){
		var tmp = $(this);
		if(!tmp.hasClass('template')){
			tmp.children("td:first-child").children("span").text(child_index);
			child_index++;
		}
	});
}

function delFitting(obj){
	var t = $(obj);
	var table = $(t.parents("table")[0]);  	
	$(t.parents(".bline")[0]).remove();
	var btn = $("#internal_fitting_btn");
	var max_round = btn.attr("max_round");
	btn.attr("max_round",parseInt(max_round)-1);
}