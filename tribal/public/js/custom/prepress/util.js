Namespace = new Object();
String.prototype.startsWith = function(str){
    return (this.match("^"+str)==str)
}

var ie9 = (function(){
    var undef,
        v = 3,
        div = document.createElement('div'),
        all = div.getElementsByTagName('i');
    while (
        div.innerHTML = '<!--[if gt IE ' + (++v) + ']><i></i><![endif]-->',
        all[0]
    );
    return v >=9 ? true : false;
}());

/*
Array.prototype.remove = function(obj) {
    var a = [];
    for (var i=0; i<this.length; i++) {
        if (this[i] != obj) {
            a.push(this[i]);
        }
    }
    return a;
}
*/
Namespace.register = function(fullNS){
    var nsArray = fullNS.split('.');
    var sEval = "";
    var sNS = "";
    for (var i = 0; i < nsArray.length; i++)
    {
        if (i != 0) sNS += ".";
        sNS += nsArray[i];
        sEval += "if (typeof(" + sNS + ") == 'undefined') " + sNS + " = new Object();"
    }
    if (sEval != "") eval(sEval);
}
/* the validator would add to this array dynamic and when the form submmit, the validators would run to check the form input */
var validators = [];

/* The sub form's nameplace */
var SFNamespace = {};

/* the default date format */
var dateFormat = 'yy-mm-dd';
var lastProgramVal = $.trim($('#program_name').val()).toUpperCase()
var initDesign;
var firstComming = true;



$(document).ready(function() {

	$('.datePicker').attr('readonly', 'true')
    $('.datePicker').datepicker({
        changeMonth : true,
        changeYear : true,
        dateFormat : dateFormat,
        minDate: "+1d",
        showOn: "button",
		buttonImage: "/images/calendar.gif",
		buttonImageOnly: true
    });
    
    $('#href_customer').click(function(){
        $.ajax({
            url: '/sample/ajaxListCustomer',
            success: function(data) {
                $("#dialog-new_customer").html(data);
                $("#dialog-new_customer").dialog('open');
            }
        });
    })
    
    $('#href_item_category').click(function(){
        $.ajax({
            url: '/prepress/ajaxListItemCategory',
            success: function(data) {
            	//$("#dialog-new_item_category").html(data);
                $("#dialog-new_item_category").html(data);
                $("#dialog-new_item_category").dialog('open');
            }
        });
    })
    
    // autocomplete
    $(".ajaxSearchField").each(function(){
		var jqObj = $(this);
        jqObj.autocomplete("/sample/ajaxField", {
        	extraParams: {fieldName: jqObj.attr("name")},
            formatItem: function(item){return item[0]},
            matchCase: false,
            mustMatch: true,
            cacheLength: 1 // not cache  
        }).result(function(event, item){
    	  	if(item[2] == 'customer_name'){
    			$('#customer').val(item[3]);
    		}
    		if(item[2] == 'program_name'){
    			$('#program').val(item[3]);
    			changeProject(item[3]);
    		}
    	})
	});

    $('#program_name').blur(function(){
		if($.trim($(this).val()) == ''){
			$('#program').val('');
			$("#project").html("<option value=''></option>");
		}
		//setTimeout('resetDesignTab()',300)
	});

	
    $('#customer_name').blur(function(){
		if($.trim($(this).val()) == ''){
			$('#customer').val('');
		}
	});

    $('#tabs span.ui-icon-close').live('click', function() {
        removeTab(this)
    })
    $("#service-div input[type='button']").click(function() {
        var s = $(this).prev();
        if(s.val()!='' && toValidate()){
        	addTab(s.val(), s.find("option:selected").text(),true);
        }
    });
});


function changeProject(program_id){
	// var t = $('#program');
	var s = $("#project");
	s.html("<option value=''></option>");
	if(program_id){
		$.getJSON("/sample/ajaxProjectInfo",{"program_id" : program_id},
			function(res){
			 	if(res.flag != "0"){
					alert("Error occur on the server side!");
				}else{
					var d = res.data;
					var html = "<option></option>";
					for(var i=0;i<d.length;i++){
						html += '<option value="'+d[i][0]+'">'+d[i][1]+'</option>';
			 		}
			 		s.html(html);
				}
			}
		);		
	}
}

var tabLabel = {
    "PSSFUpload":"Prepress",
    "PSSFBarcode":"Barcode"
}

var $tabs, tabIndex=0;
var main_id;
var action;
var token;
var is_draft = false;
var is_draft_status = false;
var childrenForms=[];
var getTabIds = function(){
    var tab_ids = []
    $(".ui-tabs-nav > li > a").each(function(){
        tab_ids.push($(this).attr('href').split('#')[1])
    })
    return tab_ids
}


var resetTabLabels = function(){    
    var tabSeq = {};
    var tab_ids = getTabIds();
    for(var i=0;i<tab_ids.length;i++){
        var tab_id = tab_ids[i];
        var form_type = tab_id.split("-")[1];
        if( tabSeq[form_type] ==undefined ){
            tabSeq[form_type] = 0;
            var label = tabLabel[form_type];
        }else{
            tabSeq[form_type]++ ;
            var label = tabLabel[form_type] + "(" + tabSeq[form_type] + ")";
        }
        try{
            $('#iframe-'+tab_id)[0].contentWindow.reset_label(label);
            //$('a[href="#'+tab_id+'"]').text(label);   //to fix here
            if($('a[href="#'+tab_id+'"] u').length>0){
                $('a[href="#'+tab_id+'"] u').text(label);
            }else{
                $('a[href="#'+tab_id+'"]').text(label);
            }
        }catch (e) {
        
        }
        
    }
}


function toDraft(){
	var msg = [];
    var required = [ [ "project_own", "Region" ], [ "team", "Division Team" ]];
    for ( var i = 0; i < required.length; i++) {
        if (!$("#" + required[i][0]).val()) {
            changeColorList($("#" + required[i][0]))
            msg.push("Please fill in the '" + required[i][1] + "'!");
        }
    }
    if (msg.length > 0) {
        var str = "<ul><li>" + msg.join("</li><li>") + "</li></ul>";
        $.prompt(str, {opacity : 0.6, prefix : 'cleanred'});
        return false;
    } else {
    	is_draft = true;
    	var tab_ids = getTabIds();
    	$("body").mask("Loading...");
    	var form_ids = []
        for(var i=0;i<tab_ids.length;i++){
            form_ids.push(tab_ids[i].split('-')[1])
        }
        $('#form_ids').val(form_ids.join('|'))
        $.getJSON('/prepress/saveMainForm?'+$("#mainForm").serialize(), function(req) {
            if (req.flag != "0") {
                location.href='/prepress/index'
            }else{
                for(var i=0;i<tab_ids.length;i++){
                    var json_widget = ['material','shoot'];
                    for(var j=0;j<json_widget.length;j++){
                        var name = json_widget[j];
                        var widget = $('#iframe-'+tab_ids[i]).contents().find("input[id$='"+name+"_widgets']");
                        if(widget.length>0){
                            //jsonify the widget info into the hidden field
                            var jsonvals = new Array();                   
                            $('#iframe-'+tab_ids[i]).contents().find("."+name+"_widget").each(function(){
                                if($(this).val()){
                                    jsonvals.push($(this).attr("ref"));
                                }
                            });                   
                            widget.val("[" + jsonvals.join(",") + "]");
                        }
                    }

                    $('#iframe-'+tab_ids[i])[0].contentWindow.submit_form();                                       
                }
                setTimeout('validateResult()', 100)
            }
        })
    }
}

function deleteDraft() {
    return confirm('Are you sure to delete this draft?');
}


function toValidate(){
	var msg = [];
	var tab_ids = getTabIds();
	if(tab_ids.length>0){
		//msg = msg.concat($('#iframe-'+selectedTab)[0].contentWindow.validate_form())
		for(var i=0;i<tab_ids.length;i++){
	        msg = msg.concat($('#iframe-'+tab_ids[i])[0].contentWindow.validate_form());
	    }
		if(msg.length>0){
			var str = "<ul><li>" + msg.join("</li><li>") + "</li></ul>";
		    $.prompt(str, {
		        opacity : 0.6,
		        prefix : 'cleanred'
		    });
		    return false;
		}
	}
	return true;
}

function toSave() {
    var msg = [];
    var required = [ [ "project_own", "Region" ], [ "project_owner", "Owner Name" ],
        [ "team", "Division Team" ],[ "contact_person", "Contact Person" ],[ "project", "Brand" ],
        ["request_contact_number","Contact Number"]];
    for ( var i = 0; i < required.length; i++) {
        if (!$("#" + required[i][0]).val()) {
            changeColorList($("#" + required[i][0]))
            msg.push("Please fill in the '" + required[i][1] + "'!");
        }
    }
	
    var tab_ids = getTabIds();
    if(tab_ids.length==0)
        msg.push("Please at least add one service!");
    else{
        for(var i=0;i<tab_ids.length;i++){
            msg = msg.concat($('#iframe-'+tab_ids[i])[0].contentWindow.validate_form());
        }
    }
    
    if (msg.length > 0) {
        var str = "<ul><li>" + msg.join("</li><li>") + "</li></ul>";
        $.prompt(str, {
            opacity : 0.6,
            prefix : 'cleanred'
        });
        return false;
    }else{
        toSaveRequest();
    }
    
    
    
	//check whether the form is duplicate
	/*
	$.getJSON("/prepress/checkDuplicate",{
        "project": $("#project").val(),
		"item_code": $("#item_code").val(),
		"time": Date.parse(new Date()),
		'main_id': main_id ? main_id : ''
	},function(r){
		if(r.flag!=0){
			msg.push('This Corporate Brand and Item No# was inputted, please kindly check with your team if someone was entered the same request.');
		}
		if (msg.length > 0) {
	        var str = "<ul><li>" + msg.join("</li><li>") + "</li></ul>";
	        $.prompt(str, {
	            opacity : 0.6,
	            prefix : 'cleanred'
	        });
	        return false;
	    }else{
			toSaveRequest();
		}
	})
	*/
}


function toSaveRequest(){
	$("body").mask("Loading...");
	var tab_ids = getTabIds();
    var form_ids = []
    for(var i=0;i<tab_ids.length;i++){
        form_ids.push(tab_ids[i].split('-')[1])
    }
    $('#form_ids').val(form_ids.join('|'))
    $.getJSON('/prepress/saveMainForm?'+$("#mainForm").serialize(), function(req) {
        if (req.flag != "0") {
            location.href='/prepress/index'
        }else{
            for(var i=0;i<tab_ids.length;i++){
                $('#iframe-'+tab_ids[i])[0].contentWindow.submit_form();
            }
            setTimeout('validateResult()', 100)
        }
    })
}
var directed = false;
function validateResult(){
	if(!directed){
		var tab_ids = getTabIds();
	    var pass_index = 0;
	    var fail_index = 0;
	    for(var i=0;i<tab_ids.length;i++){
	    	if(window.frames['iframe-'+tab_ids[i]].document.body){
		        var html = window.frames['iframe-'+tab_ids[i]].document.body.innerHTML;
		        if(html==''){
		            pass_index++
		        }else if(html=='error'){
		            fail_index++;
		            break;
		        }
	        }
	    }
	    if(fail_index>0){
	    	directed = true;
	    	location.href='/prepress/saveFormFail?token='+token+'&is_draft='+is_draft;
	    }else if(pass_index==tab_ids.length){
	    	directed = true;
	    	location.href='/prepress/saveFormSuccess?action='+action+'&token='+token+'&is_draft='+is_draft;
	    }else{
	    	setTimeout('validateResult()', 100)
	    }
	}
}

function toCancel() {
    if (confirm("Are you sure the leave the request form without saving?"))
        window.location.href = "/prepress/index"
    else return false;
}

function addTab(id, label,is_update) {
    is_update = is_update || false; //default is not removable.
	tabIndex++;
	if(is_update){
	   $tabs.tabs( "option", "tabTemplate","<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close'>Remove Tab</span></li>");
	}else{
	   $tabs.tabs( "option", "tabTemplate","<li><a href='#{href}'>#{label}</a>");
	}
    $tabs.tabs("add", "#tab-" + id + '-' + tabIndex, label);
    showLoading();
}


function removeTab(removeObj) {
    $tabs.tabs('remove', $('li', $tabs).index($(removeObj).parent()))
    resetTabLabels()
}


function excludeCheckbox(obj) {
    var t = $(obj);
    var td = t.parents("td")[0];
    $("input[name$='overall_result']", td).each(function() {
        if ($(this).attr("id") != t.attr("id")) {
            $(this).removeAttr("checked");
        }
    });
}

function getFileName(obj) {
    var tmp = $(obj);
    var path = tmp.val();
    if (path && path.length > 0) {
        var location = path.lastIndexOf("\\") > -1 ? path.lastIndexOf("\\") + 1	: 0;
        var fn = path.substr(location, path.length - location);
        tmp.prev("input[type='text']").val(fn);
    }
}

function addFile(obj) {
	var html = $('<tr>'+$(obj).parent().parent().html()+'</tr>');
	html.find('a').eq(1).removeAttr('style')
	$(obj).parent().parent().after(html)
}

function deleteFile(obj) {
	if(confirm('Are you sure to delete the file ?')){
	    $($(obj).parents("tr")[0]).remove();
	}
}

function deleteDownload(obj,params){
    if(!window.confirm("Are you sure to delete the file?")){
        return ;
    }
    $("body").mask("Loading...");
    	alert("Delete the file successfully!");
        $($(obj).parents("tr")[0]).remove();
        $("body").unmask();
}


var tempradio= null;
function check(checkedRadio)  {
    if(tempradio== checkedRadio){
        tempradio.checked=false;
        tempradio=null;
    } else{
        tempradio= checkedRadio;
    }
}
var showMsg = function(Msg){
    $.prompt(Msg,{
        opacity: 0.6,
        prefix:'cleanblue'
    });
}


var showError = function(Msg){
    $.prompt(Msg,{
        opacity: 0.6,
        prefix:'cleanred'
    });
}


//less the checkBox 
var lessCheckBox = function(list){
    for(x in list){
        $(list[x]).attr("disabled","disabled");
        //$(list[x]).css({"border":"1px solid #e1e1e1","backgroundColor":"#f1f2f2"})
	     if($(list[x]).attr("type") == "text"){
	        $(list[x]).removeAttr("style");
	     }
	     if($(list[x]).attr("type") == "radio" || $(list[x]).attr("type") == "checkbox"){
		        $(list[x]).parent("span.changeColor").css("border","1px solid #ffffff")
		     }
    }
}


var lessCheckBox2 = function(list){
    for(x in list){
        //$(list[x]).attr("disabled","disabled");
        //$(list[x]).css({"border":"1px solid #e1e1e1","backgroundColor":"#f1f2f2"})
	     if($(list[x]).attr("type") == "text"){
	        $(list[x]).removeAttr("style");
	     }
	     if($(list[x]).attr("type") == "radio" || $(list[x]).attr("type") == "checkbox"){
		        $(list[x]).parent("span.changeColor").css("border","1px solid #ffffff")
		     }
    }
}


var lessCheckBox3 = function(list){
    for(x in list){
        //$(list[x]).attr("disabled","disabled");
        //$(list[x]).css({"border":"1px solid #e1e1e1","backgroundColor":"#f1f2f2"})
	     if($(list[x]).attr("type") == "text"){
	        $(list[x]).removeAttr("style");
	        $(list[x]).val("");
	     }
	     if($(list[x]).attr("type") == "radio" || $(list[x]).attr("type") == "checkbox"){
		        $(list[x]).parent("span.changeColor").css("border","1px solid #ffffff")
		        $(list[x]).attr('checked', false);
		     }
	     
    }
}


//if the radio checked the other list work
var workCheckBox = function(obj,list){
    var check = true
    if(obj.attr("type") == "checkbox"){
        if(obj.attr("checked") == false){
            check = false
            for(x in list){
                $(list[x]).attr("disabled","disabled");
            // if($(list[x]).attr("type") == "text"){
            //     $(list[x]).removeAttr("style");
            // }
            }
        }
    }
    if(check){
        for(x in list){
            $(list[x]).removeAttr("disabled")
        //if($(list[x]).attr("type") == "text"){
        //    $(list[x]).css("border","1px solid #006699")
        //}
        }
    }
}


//check the radio
var checkRadio = function(list){
    for(x in list){
        if($(list[x]).attr("checked") == false){
            $(list[x]).attr("checked","checked")
        }
    }
}


//return True or False , if Type not checkbox return value.ֵ
var getTypeResult = function(obj){
    var type = $(obj).attr("type")
    if(type=="checkbox" || type == "radio"){
        if($(obj).attr("checked") == true){
            return true;
        }else{
            return false;
        }
    }else{
        if($(obj).val()){
            return $(obj).val();
        }
        else{
            return false;
        }
    }
}

var validatForm = function(type,list){
    //must input min one text
    var minOne = true
    if(type == 1){
        for (x in list){
            //if hava true break the forloop
            if(getTypeResult(list[x])){
                minOne = true;
                break;
            }else{
                minOne = false;
            }
        }
        if(minOne == false){
            return "<p>You must choose least one!</p>";

        }
    }
    //select one must select other and the list is the map
    var msg = [];
    if(type == 2){
        $.each(list,function(k,v){
            if(getTypeResult(k)){
                for(x in v){
                    if(getTypeResult(v[x]) == false){
                        msg.push("You must input either one!<br />");
                        $(v[x]).css("border","1px solid #ff0000");
                    }
                }
            }
        })
        if(msg.length>0) return msg
    }
    //input can't null
    if(type == 3){
        for (x in list ){
            if(getTypeResult(list[x]) == false){
                return false;
                break;
            }
        }
    }
    //select one,other can't input
    if(type == 4){
        $.each(list,function(k,v){
            if(getTypeResult(k)){
                for(x in v){
                    $(v[k]).attr("disabled","disabled");
                }
            }
        })
    }
}
var disableField=function(field){
    $(field).attr('disabled', true);
    $(field).addClass('disabled');
}


var resetCheckToFields=function(from, value, to){
    resetCheckToFieldsBool(from, value, to, true);
}


var resetCheckToFieldsNoteq=function(from,value,to){
    resetCheckToFieldsBool(from, value, to, false);
}


var resetCheckToFieldsBool=function(from, value, to, isEq){
    if(typeof value=='string') value = [value]
    if(typeof to=='string') to=[to]
    var isPass = false;
    for(var i=0;i<value.length;i++){
        if(isEq){
            if((!value[i] && $(from+':checked').val()) || (value[i] && $(from+':checked').val()==value[i])){
                isPass = true;
                break
            }
        }else{
            isPass = true;
            if(!isEq && value[i] && $(from+':checked').val()==value[i]){
                isPass = false;
                break;
            }
        }
    }
    for(var i=0;i<to.length;i++){
        var field = to[i]
        if(isPass){
            $(field).removeAttr('disabled');
            $(field).removeClass('disabled');
        }else{
        	var fieldType = $(field).attr('type') 
        	if(fieldType=='checkbox' || fieldType=='radio'){
				$(field).attr('checked', false)
			}else if(fieldType=='select-one'){
				$(field).attr('selectedIndex', 0);
			}else if(fieldType=='textarea' || fieldType=='text'){
				$(field).val('')
			}
            $(field).attr('disabled', true);
            $(field).addClass('disabled');
        }
    }
}


function extendJson(des, src, override){
    if(src instanceof Array){
        for(var i = 0, len = src.length; i < len; i++)
             extendJson(des, src[i], override);
    }
    for( var i in src){
        if(override || !(i in des)){
            des[i] = src[i];
        }
    }
    return des;
}
var FieldsUtil = {
	getObjType: function(obj){
		if(typeof(obj)=='boolean')
			return 'Boolean';
		else if(typeof(obj)=='string')
			return 'String';
		else if(typeof(obj)=='number')
			return 'Number';
		else if(typeof(obj)=='object' && obj instanceof Array)
			return 'Array';
	},
	extractFields: function(fields){
		var results = []
		var fields_type = FieldsUtil.getObjType(fields)
		if(fields_type == 'Array'){
			for(var i=0;i<fields.length;i++){
				results = results.concat(FieldsUtil.extractFields(fields[i]))
			}
		}else if(fields_type != 'Boolean'){
			results.push(fields)
		}
		return results
	},
	addBorder: function(fields){
		fields = FieldsUtil.extractFields(fields)
		for(var i=0;i<fields.length;i++){
			var field = $(fields[i])
			var fieldType = field.attr('type')
			var disabled = field.attr('disabled')
			if(!disabled && (fieldType=='checkbox' || fieldType=='radio')){
				if($("input[name="+field.attr('name')+"]:checked").length==0){
					if(!field.hasClass('border_checkbox'))
						$("input[name="+field.attr('name')+"]").addClass('border_checkbox')
				}else{
					$("input[name="+field.attr('name')+"]").removeClass('border_checkbox')
				}
			}else if(fieldType=='select-one'){
				if(!disabled && !field.val()){
					if(!field.parent().hasClass('border_select'))
						field.wrap('<span class="border_select"></span>')
				}else if(field.parent().hasClass('border_select')){
					field.parent().replaceWith(field)
				}
			}else if(!disabled && (fieldType=='textarea' || fieldType=='text')){
				if(!field.val()){
					if(!field.hasClass('border_text'))
						field.addClass('border_text')
				}else{
					field.removeClass('border_text')
				}
			}
		}
	},
	delBorder: function(fields){
		fields = FieldsUtil.extractFields(fields)
		for(var i=0;i<fields.length;i++){
			var field = $(fields[i])
			var fieldType = field.attr('type')
			if(fieldType=='checkbox' || fieldType=='radio'){
				$("input[name="+field.attr('name')+"]").removeClass('border_checkbox')
			}else if(fieldType=='select-one'){
				if(field.parent().hasClass('border_select'))
					field.parent().replaceWith(field)
			}else if(fieldType=='textarea' || fieldType=='text'){
				field.removeClass('border_text')
			}
		}
	},
	bindFields: function(from_fields, to_fields, isRequired){
		var fields = FieldsUtil.extractFields(from_fields).concat(FieldsUtil.extractFields(to_fields))
		for(var i=0;i<fields.length;i++){
			field = $(fields[i])
			var fieldType = field.attr('type')
			if(fieldType=='checkbox' || fieldType=='radio'){
				$('input[name='+field.attr('name')+']').click(function(){
					FieldsUtil.validateFields(from_fields, to_fields, isRequired)
				})
			}else if(fieldType=='select-one'){
				field.change(function(){
					FieldsUtil.validateFields(from_fields, to_fields, isRequired)
				})
			}else if (fieldType=='textarea' || fieldType=='text'){
				field.keydown(function(){
					FieldsUtil.validateFields(from_fields, to_fields, isRequired)
				}).blur(function(){
					FieldsUtil.validateFields(from_fields, to_fields, isRequired)
				})
			}
		}
	},
	judgeFields: function(fields, isRequired, isTop){			
		var results = []
		var fields_type = FieldsUtil.getObjType(fields)
		if(fields_type == 'Boolean'){
			return fields
		}else if(fields_type == 'Array'){
			for(var i=0;i<fields.length;i++){
				if(FieldsUtil.getObjType(fields[i]) == 'Array'){
					var result = FieldsUtil.judgeFields(fields[i], isRequired, false)
					if(result==true || result==1)
						return result
					else
						results.push(result)
				}else{
					results.push(FieldsUtil.judgeFields(fields[i], isRequired, false))
				}
			}
			results.sort()
			if(!isRequired && !isTop){
				if(results[0]==true && results[results.length-1]==true)
					return 1
				else if(results[0]==false && results[results.length-1]==false)
					return -1
				else return 0
			}
			return (results[0]==true && results[results.length-1]==true) || (results[0]==1 && results[results.length-1]==1) || (!isRequired && results[0]==-1 && results[results.length-1]==-1)
		}else if(fields_type == 'String'){
			var field = $(fields)
			var fieldType = field.attr('type')
			if(fieldType=='checkbox' || fieldType=='radio'){
				if(field.length==1 && $("input[name="+field.attr('name')+"]").length>1){
					var result = false;
					$("input[name="+field.attr('name')+"]:checked").each(function(){
						if($(this).val()==field.val()) result = true;
					})
					return result;
				}else{
					return $("input[name="+field.attr('name')+"]:checked").length>0
				}
			}else{
				if($("input[name="+field.attr('name')+"]").length>1){
					var result = false;
					$("input[name="+field.attr('name')+"]:checked").each(function(){
						if($(this).val().length>0) result = true;
					})
					return result;
				}else
					return field.val().length>0
			}
		}
	},
	validateFields: function(from_fields, to_fields, isRequired){
		var judgeFrom = FieldsUtil.judgeFields(from_fields, isRequired, true)
		if(judgeFrom){
			var judgeTo = FieldsUtil.judgeFields(to_fields, isRequired, true)
			if(judgeTo){
				FieldsUtil.delBorder(to_fields)
			}else{
				FieldsUtil.addBorder(to_fields)
			}
		}else{
			FieldsUtil.delBorder(to_fields)
		}
	},
	disableFields: function(from, value, to, init){
		if(typeof value=='string') value = [value]
	    if(typeof to=='string') to=[to]
	    var isPass = false;
	    for(var i=0;i<value.length;i++){
	        if(!$(from).attr('disabled')){
	        	if($(from+':checked').length>1)
	        		$(from+':checked').each(function(){
	        			if($(this).val()==value[i])
	        				isPass = true;
	        		})
	        	else if((!value[i] && $(from+':checked').val()) || (value[i] && $(from+':checked').val()==value[i]))
	        		isPass = true;
	        	if(isPass) break;
	        }
	    }
	    var fieldMap = {}
	    for(var i=0;i<to.length;i++){
	        var field = to[i]
	        if(isPass){
	            $(field).removeAttr('disabled');
	            $(field).removeClass('disabled');
	        }else{
	            $(field).attr('disabled', true);
	            $(field).addClass('disabled');
	            FieldsUtil.delBorder(field)
	        }
	        if(field instanceof Array){
	        	FieldsUtil.disableFields(field[0], field[1], field[2], false)
	        	if(init){
	        		(function(_f, _v, _t){
	        		     $(_f).click(function(){
	        		    	 FieldsUtil.disableFields(_f, _v, _t, false)
	        		     });
	        		})(field[0], field[1], field[2]);
	        	}
	        }
	    }
	},
	addPlusField: function(obj, val){
		if(!val) val = '';
		var html = $('<li>'+$(obj).parent().parent().children().html()+'<a href="javascript:void(0)" onclick="FieldsUtil.delPlusField(this)"><img src="/images/minus.gif" title="Remove Field"/></a></li>');
		html.find('input').val(val)
		html.find('input').numeric();
		html.removeAttr('id')
		$(obj).parent().after(html)
	},
	delPlusField: function(obj){
		$(obj).parent().remove()
	},
	plusFields: function(fields){
		for(var i=0;i<fields.length;i++){
			var field = $(fields[i])
			field.after('<a href="javascript:void(0)" onclick="FieldsUtil.addPlusField(this, null)"><img src=/images/plus.gif title="Add Field"/></a>')
			var value = field.val() 
			if(value){
				if(value.startsWith('{')) value = value.substring(1, value.length)
				if(value.endsWith('}')) value = value.substring(0, value.length-1)
		    	var _vals = value.split(',')
		    	for(var j=0;j<_vals.length;j++){
		    		if(j==0)
		    			field.val(_vals[0])
		    		else
		    			FieldsUtil.addPlusField(field.next(), _vals[-(j-_vals.length)])
		    	}
		    }
		}
	}
}
var initDisableFields=function(from, value, to){
	FieldsUtil.disableFields(from, value, to, true)
	$(from).click(function(){
		FieldsUtil.disableFields(from, value, to, false)
	})
}
var initRedFields=function(from_fields, to_fields, params){
	var isValidate = params['validate']==undefined ? false : params['validate']
	var isBind = params['bind']==undefined ? false : params['bind']
	var isRequired = params['required']==undefined ? true : params['required']

	if(isBind) FieldsUtil.bindFields(from_fields, to_fields, isRequired)
	if(isValidate) FieldsUtil.validateFields(from_fields, to_fields, isRequired)
}
var initPlusFields=function(fields){
	String.prototype.startsWith = function(str){return (this.match("^"+str)==str)}
	String.prototype.endsWith = function(str){return (this.match(str+"$")==str)}
	FieldsUtil.plusFields(fields)
}
var resetAsSampleToFields=function(from, to){
    if(typeof to=='string') to=[to]
    from = $(from);
    var _to = []
    for(var i=0;i<to.length;i++){
        _to.push($(to[i]));
    }
    linkScroll(_to, from);
}


function ajaxSelect(queryString,parname,type){
    $.ajax({
        type:"GET",
        dataType:"json",
        data:{
            "id":queryString,
            "key":parname
        },
        url: "/sample/ajaxRegionTeam",
        success: function(data,textStatus){
            var selectStart;
            var inputStart;
            var position;
            var owner_name = $("#project_owner").val()
            var contact_person = $("#contact_person").val()
            if(data.cur == 'project_own'){
                selectStart = "<select class='input-150px' id='project_owner' name='project_owner'><option value=''></option>";
                inputStart  = "<input name='project_owner' id='project_owner' value='' class='input-150px'>"
                position =   $("#owner_name_p")
			
            }else{
                selectStart = "<select class='input-150px' id='contact_person' name='contact_person'>";
                inputStart  = "<input class='input-150px inputText' value='' id='contact_person' name='contact_person'>"
                position =   $("#contact_person_p")
            }
            if(data.active == 0){
                var users    = data.user
                var temp = []
                temp.push(selectStart)
                for( i in users ){
                    if((data.cur == 'project_own' && owner_name == users[i]['display_name']) || (data.cur == 'team' && contact_person == users[i]['display_name'])){
                        temp.push("<option value='"+users[i]['display_name']+"' selected='selected'>"+users[i]['display_name']+"</option>");
                    }
                    else{
                        temp.push("<option value='"+users[i]['display_name']+"'>"+users[i]['display_name']+"</option>");
                    }
                }
                temp.push("</select>")
                position.html("").append(temp.join(""))
            }
            if(data.active == 1){
                position.html(inputStart)
            }
        }
    });
}


var getParentVendor = function(){
    return $("#customer").val()
}


var getParentProduct = function(){
    return $("#item_description").val()
}


var getText = function(){
    var Vendor_Name   = parent.getParentVendor();
    var Product_Name  = parent.getParentProduct();
    if(Vendor_Name)
        $("#SFTarget-target_vendor_id").val(Vendor_Name);
    if(Product_Name)
        $("#SFTarget-product_name").val(Product_Name);
}


var changeSelect = function(obj){
    var name = obj.attr("name");
    var queryString = obj.val();
    ajaxSelect(queryString,name);
}


var initSelete = function(){
    $("select[name='project_own'],select[name='team']").change(function(){
        changeSelect($(this),'select')
    })
}


var downSelct = function(){
    $("select[name='project_own'],select[name='team']").each(function(){
        changeSelect($(this),'update')
    })
}


var newSelect = function(obj){
    $("select[name='project_own'],select[name='team']").each(function(){
        changeSelect($(this),'update')
    })
    $("#owner_name").val(obj);
    $("#contact_person").val(obj);
}


var times;
var choose = function(obj){
    if(obj.attr('type')=='checkbox' || obj.attr('type')=='radio'){
        $("input[name='"+obj.attr('name')+"']").each(function(){
            $(this).parent("span.changeColor").removeAttr("style")
            $(this).removeAttr("style")
        })
        obj.attr("checked","checked")
    }
}


var changeColorList = function(obj){
	if(obj.constructor==Array){
        for(a in obj){
            for(b in obj[a][0]){
                if(obj[a][0][b].constructor==Array){
                    for(c in obj[a][0][b]){
                        changeColor(obj[a][0][b][c],obj[a][0][b],true);
                    }
            		
                }
                else{
                    changeColor(obj[a][0][b],obj[a][0],obj[a][1]);
                }
            }
        }
    }else{
        changeColor(obj,[],true);
    }
}


var changeColor = function(obj,objList,objType){
    if(obj.attr('type')=='checkbox' || obj.attr('type')=='radio'){
        obj.each(function(){
            if(navigator.userAgent.indexOf("Firefox")>0){
                if($(this).parent("span.changeColor").length>0){
                    $(this).parent("span.changeColor").css({
                        "border":"1px solid #ff0000"
                    })
                }else{
                    $(this).wrap("<span class='changeColor' style='border:1px solid #ff0000;'></span>")
                }
            }
            if(navigator.userAgent.indexOf("MSIE")>0) {
                $(this).css("border","1px solid #ff0000")
            }
            if(!obj.attr("name")=="SFTray-style" ){
            	$(this).unbind("click");
            }
            $(this).bind("click",function(){
                if($(this).attr("checked")){
                    choose($(this));
                }
            })
        })
    }
    else if(obj.attr('type')=='text'){
        obj.css("border","1px solid #ff0000").removeAttr("disabled");
        if(!obj.hasClass('datePicker')){
            obj.unbind("focus blur");
        }
        obj.bind("focus blur",function(event){
            if(event.type == 'focus') {
                var objs = $(this)
                if(objType){
                    times = window.setInterval(function(){
                        checkVals(objs,false);
                    },100);
                }else{
                    times = window.setInterval(function(){
                        checkVals(objList,true);
                    },100);
                }

            }
            if(event.type == 'blur') {
                window.clearInterval(times);
            }
        })
    }

    if($("select[name='"+obj.attr("name")+"']").length>0 || $("textarea[name='"+obj.attr("name")+"']").length>0){
        var curObj = $("select[name='"+obj.attr("name")+"']").length>0?$("select[name='"+obj.attr("name")+"']"):$("textarea[name='"+obj.attr("name")+"']")
        if(curObj.parent("span.changeColor").length>0){
            curObj.parent("span.changeColor").css({
                "border":"1px solid #ff0000"
            })
        }else{
            curObj.wrap("<span class='changeColor' style='border:1px solid #ff0000;'></span>")
        }
        curObj.bind("change click",function(){
            if($(this).val()){
                $(this).parent("span.changeColor").css("border","1px solid #ffffff")
            }
        })
    }
}


var checkVals = function(obj,type){
    if(type){
        var check;
        for(a in obj){
            if(obj[a].val().length>0){
                check = 1;
            }
        }
        if(check == 1){
            for(b in obj){
                obj[b].removeAttr("style")
            }
        }
    }
    else{
        if(obj.val().length>0){
            obj.removeAttr("style")
        }
    }
}

var linkScroll = function(listObj,obj){

    for(a in listObj){
    	listObj[a].unbind("focus blur");
        listObj[a].bind("focus blur",function(event){
            if(event.type == 'focus') {
                var objs = $(this)
                times = window.setInterval(function(){
                    checkSample(objs,obj);
                },100);
            }
            if(event.type == 'blur') {
                window.clearInterval(times);
            }
        })
    }
    obj.unbind("focus blur")
    obj.bind("focus blur",function(event){
        if(event.type == 'focus') {
            var objs = $(this)
            times = window.setInterval(function(){
                checkSample(objs,listObj);
            },100);
        }
        if(event.type == 'blur') {
            window.clearInterval(times);
        }
    })
   
}


var checkSample= function(objs, obj){
    if(objs.attr("checked")||objs.val()){
        if(obj.constructor == Array){
            for(a in obj){
                if(obj[a].attr("type") == "radio" || obj[a].attr("type") == "checkbox"){
                    obj[a].attr("checked",false);
                }
                if(obj[a].attr("type") == "text"){
                    obj[a].val("");
                }
                obj[a].parent("span.changeColor").css("border","1px solid #ffffff")
                obj[a].removeAttr("style")
            }
        }else{
            obj.attr("checked",false);
            obj.parent("span.changeColor").css("border","1px solid #ffffff")
            obj.removeAttr("style")
        }
    }
}


function SetCwinHeight(id){
    var iframeid=document.getElementById(id); //iframe id
    if (document.getElementById){
        if (iframeid && !window.opera){
            if (iframeid.contentDocument && iframeid.contentDocument.body.offsetHeight){
                iframeid.height = iframeid.contentDocument.body.offsetHeight+45;
            }else if(iframeid.Document && iframeid.Document.body.scrollHeight){
                iframeid.height = iframeid.Document.body.scrollHeight+30;
            }
        }
    }
}


function resetIframeHeight(){
    var iframe = document.getElementById('iframe-'+last_panel_id);
    var bHeight = iframe.contentWindow.document.body.scrollHeight;
    var dHeight = iframe.contentWindow.document.documentElement.scrollHeight;
    var height = Math.max(bHeight, dHeight);
    iframe.height =  height;
}


function showLoading(){
    $("body").mask("Loading...");
}


function cancelLoading(){
    $("body").unmask();
}

var timepicker = function(id){
	html =  "<div id='timeDialog_"+id+"' title='Basic dialog' style='display:none'>" 
			+ "<table><tr>"
			+ "<td width='50'>Time</td><td id='ui_tpicker_time_"+id+"'><td>"
			+ "</tr><tr>"
			+ "<td id='ui_tpicker_hour_label'>Hour</td>" 
			+ "<td id='ui_tpicker_hour'><select cid='"+id+"' name='hours_"+id+"' onchange='changeTime(this)'>"
		  	+ "<option value='9'>9</option>"
		  	+ "<option value='10'>10</option>"
		  	+ "<option value='11'>11</option>"
		  	+ "<option value='12'>12</option>"
		  	+ "<option value='13'>13</option>"
		  	+ "<option value='14'>14</option>"
		  	+ "<option value='15'>15</option>"
		  	+ "<option value='16'>16</option>"
		  	+ "<option value='17'>17</option>"
		  	+ "<option value='18'>18</option>"
		  	+ "</select></td></tr><tr>" 
		  	+ "<td id='ui_tpicker_minute_label'>Minute</td><td id='ui_tpicker_minute'>"
		  	+ "<select cid='"+id+"' name='minute_"+id+"'  onchange='changeTime(this)'>"
		  	+ "<option value ='00'>00</option>"
		  	+ "<option value ='30'>30</option>"
		  	+ "</select></td></tr>" 
		  	+ "</div>"
	//$(id).after(html);
	html = $(html);
	$(id).attr('readonly', 'readonly');
	$(id).click(function(){
		openDialog(html, $(id));
	})
 
}

var changeTime = function(obj){
	var type = " am";
	var id = $(obj).attr("cid");
	var hoursValue = $("select[name='hours_"+id+"']").val();
	var minuteValue = $("select[name='minute_"+id+"']").val();
	if(hoursValue && minuteValue){
		if(hoursValue > 11){
			if(hoursValue > 12){
				hoursValue = hoursValue -12;
			} 
			type = " pm";
		}
		var time = hoursValue+":"+minuteValue+type;
		$(id).val(time)
		$("td[id='ui_tpicker_time_"+id+"']").html(time);
	}
}


var openDialog = function(html, id){
	ps = id.position();
	$(function() {
		html.dialog({
			autoOpen: false,
			width:200,
			title:'Choose time',
			height:180,
			position:[ps.left, ps.top+20],
			create: function(event, ui) {
				 
			},
			buttons: {
				"Done": function() {
					$( this ).dialog( "close" );
				}
			}
		});
		html.dialog("open");
		return false;
	});
}

//convert the server time into the localtime
function servertime2localtime(servertime,servertfc,browsertfc){
    var diff = servertfc - browsertfc;
    var op = diff > 0 ? 1 : -1;
    diff = Math.abs(diff);
    var diffHours = Math.floor(diff/60);
    var diffMins = diff % 60;
    var t = servertime.split(":");
    var newHour = parseInt(t[0]) + op * diffHours;
    var newMin = parseInt(t[1]) + op * diffMins;
    
    if(newMin < 0){
        newMin += 60;
        newHour --;
    }
    if(newHour < 0){
        newHour += 24;
    }
    
    return newHour + ":" + newMin;
}


function check_number(v){
    var pattern = /^[\d\.]+$/;
    return pattern.test(v); 
}
