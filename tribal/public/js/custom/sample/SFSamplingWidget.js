Namespace.register("SFNamespace.SFSampling");
var resetDisableFields = function(){
	initDisableFields('input[name=SFSampling-file_from]', 'ftp', '#SFSampling-file_from_ftp_location');
	initDisableFields('input[name=SFSampling-file_from]', 'files', '#SFSampling-file_from_files_location');
	initDisableFields('input[name=SFSampling-file_from]', 'New_design_with_this_request', '#SFSampling-file_from_task_name');
	initDisableFields('input[name=SFSampling-output]', 'white', '#SFSampling-output_white_pcs');
	initDisableFields('input[name=SFSampling-output]', 'woodfree', '#SFSampling-output_woodfree_pcs');
	initDisableFields('input[name=SFSampling-output]', 'semi', '#SFSampling-output_semi_pcs');
	initDisableFields('input[name=SFSampling-output]', 'label', '#SFSampling-output_label_pcs');
	initDisableFields('input[name=SFSampling-delivery]', 'D', '#SFSampling-expected_time');
	initDisableFields('input[name=SFSampling-delivery]', 'Y', '#SFSampling-expected_date');
}
var bindOnce = false;
var resetRedFields=function(){
	var isBind, isValidate
	if(!bindOnce){
		isBind = true;
		isValidate = true;
		bindOnce = true;
	}else{
		isBind = false;
		isValidate = true;
	}
	initRedFields(true, 
			['input[name=SFSampling-file_from]', 'input[name=SFSampling-output]'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-file_from][value=ftp]', '#SFSampling-file_from_ftp_location'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-file_from][value=files]', '#SFSampling-file_from_files_location'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-file_from][value=New_design_with_this_request]', '#SFSampling-file_from_task_name'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-output][value=white]', '#SFSampling-output_white_pcs'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-output][value=woodfree]', '#SFSampling-output_woodfree_pcs'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-output][value=semi]', '#SFSampling-output_semi_pcs'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-output][value=label]', '#SFSampling-output_label_pcs'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-delivery][value=D]', '#SFSampling-expected_time'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true, 
			['input[name=SFSampling-delivery][value=Y]', '#SFSampling-expected_date'], 
			{'bind': isBind, 'validate': isValidate})
}
SFNamespace.SFSampling.obj = {
    id: "SFSampling",
    title: "Sampling",
    install: function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetDisableFields()
    },
    uninstall: function(){
        for(var i=0;i<validators.length;i++){
            if( this.id==validators[i].id ){
                validators.splice(i,1);
                break;
            }
        }
    },
    validation   : function(){
    	resetRedFields()
        var msg = [];
        if( $("input[name='SFSampling-delivery']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'Expected date'.");
            //changeColorList($("input[name='SFSampling-delivery']"))
        }				
        if( $("input[name='SFSampling-delivery'][value='D']:checked").length == 1 && !$("#SFSampling-expected_time").val() ){
            msg.push("Task["+this.title+"]Please input the 'Same Day Delivery'.");
            //changeColorList($("#SFSampling-expected_time"))
        }
        if( $("input[name='SFSampling-delivery'][value='Y']:checked").length == 1 && !$("#SFSampling-expected_date").val() ){
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
            //changeColorList($("#SFSampling-expected_date"))
        }
        if( $("input[name='SFSampling-file_from']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'Files From'.");
            //changeColorList($("input[name='SFSampling-file_from']"))
        }
						
        if( $("#SFSampling-file_from_ftp").attr("checked") && !$("#SFSampling-file_from_ftp_location").val() ){
            msg.push("Task["+this.title+"]Please input the 'Location' when selecting the ftp in 'Files From'.");
            //changeColorList($("#SFSampling-file_from_ftp_location"))
        }
						
        if( $("#SFSampling-file_from_files").attr("checked") && !$("#SFSampling-file_from_files_location").val() ){
            msg.push("Task["+this.title+"]Please input the 'Location' when selecting the files in 'Files From'.");
            //changeColorList($("#SFSampling-file_from_files_location"))
        }
        if( $("#SFSampling-New_design_with_this_request").attr("checked") && !$("#SFSampling-file_from_task_name").val() ){
            msg.push("Task["+this.title+"]Please input the 'Task Name' when selecting the 'New Design With This Request' in 'Files From'.");
            //changeColorList($("#SFSampling-file_from_task_name"))
        }
        /*
		if( $("#SFSampling-material_Other").attr("checked") && !$("#SFSampling-material_Others").val() ){
			msg.push("Task["+this.title+"] Please input the content also if you select the 'Others' option.");
			changeColorList($("#SFSampling-material_Others"))
		}
		*/
			
        if( $("input[name='SFSampling-output']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'Output'.");
            //changeColorList($("input[name='SFSampling-output']"))
        }
		
		/*
        if( $("input[name='SFSampling-material_type']:checked").length < 1 ){
        	msg.push("Task["+this.title+"]Please select the 'Material'.");
        	changeColorList($("input[name='SFSampling-material_type']"))
        }
		*/
		
		if($(".material_widget[value!='']").length < 1){
		    msg.push("Task["+this.title+"]Please add the 'Material'.");
		}
		
		
        //var valid = validatForm(1,["#SFSampling-paper_thickness","#SFSampling-gramage"])
		//if(valid) msg.push(valid)
		
		//var valid1 = validatForm(3,["#SFSampling-flute_type_gsm"])
		//if(valid1) msg.push(valid1)
						
        var kv = [["SFSampling-output_white","SFSampling-output_white_pcs"],
        ["SFSampling-output_woodfree","SFSampling-output_woodfree_pcs"],
        ["SFSampling-output_semi","SFSampling-output_semi_pcs"],
        ["SFSampling-output_label","SFSampling-output_label_pcs"]];
        var pcsFill = true;
        for(var j=0;j<kv.length;j++){
            if( $("#"+kv[j][0]).attr("checked") && !$("#"+kv[j][1]).val() ){
                pcsFill = false;
                //changeColorList($("#"+kv[j][1]))
                break;
            }
        }
        if(!pcsFill){
        	//changeColorList($("#SFSampling-output_label_pcs"))
            msg.push("Task["+this.title+"]Please input the 'pcs'.");
        }
        
        /*
		if($("#SFSampling-material_type_cards").attr("checked")){				
	        if( $("input[name='SFSampling-material']:checked").length < 1){
	            msg.push("Task["+this.title+"]Please select the 'Folding Cards'.");
	            changeColorList($("input[name='SFSampling-material']"))
	        }
	        if($("input[name='SFSampling-paper_thickness_type']:checked").length < 1){
	            msg.push("Task["+this.title+"]Please select the 'Paper thickness' or 'Grammage'");
	            changeColorList($("input[name='SFSampling-paper_thickness_type']"))
	        }
			if($("#SFSampling-gramage").attr("checked")){
				if( !$("#SFSampling-gramage").val()){
					msg.push("Task["+this.title+"]Please input the content also if you select the 'Grammage' option.");
					changeColorList($("#SFSampling-gramage"))
				}
			}
			if($("#SFSampling-paper_thicknesss").attr("checked")){
				if( !$("#SFSampling-paper_thickness").val()){
					msg.push("Task["+this.title+"]Please input the content also if you select the 'Paper thickness' option.");
					changeColorList($("#SFSampling-paper_thickness"))
				}else if(!$("input[name='SFSampling-paper_thickness_unit']:checked").val()){
					msg.push("Task["+this.title+"]Please select the options also if you select the 'Paper thickness' option.");
					changeColorList($("input[name='SFSampling-paper_thickness_unit']"))
				}
			}
		}

		if($("#SFSampling-material_corrugated").attr("checked")){				
	        if( !$("#SFSampling-flute").val()){
	            msg.push("Task["+this.title+"]Please input the 'Flute'..");
	            changeColorList($("#SFSampling-flute"))
	        }
	        if($("input[name='SFSampling-flute_type']:checked").length < 1){
	            msg.push("Task["+this.title+"]Please select the options also if you select the 'Corrugated' option.");
	            changeColorList($("input[name='SFSampling-flute_type']"))
	        }
	        //if(!($("#SFSampling-bursting").val() || $("#SFSampling-ect").val() || $("#SFSampling-gramages").val())){
	        //	msg.push("Tab["+this.title+"]Please input the options also if you select the 'Corrugated' option.");
	        //	changeColorList([[[$("#SFSampling-bursting"),$("#SFSampling-ect"),$("#SFSampling-gramages")],false]])
	        //}
		}
		*/
		
        //if($("input[name='SFSampling-material_type'][value='provided']:checked").length==1 && !$("#SFSampling-material_type_content").val()){
        //	msg.push("Tab["+this.title+"]Please input the content also if you select the 'Material :Material provided'");
        //	 changeColorList($("#SFSampling-material_type_content"))
        //}
        if( $("#SFSampling-file_from_see_per_attachment").attr("checked") && !($("#SFSampling-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) )
        {
        	msg.push("Task["+this.title+"]Please input the 'Attachment'.");
        	//changeColorList($("#SFSampling-attachment_name"))
        }
        
        /*
        if($("#SFSampling-material_type_other").attr("checked")){		
        	if(!$("#SFSampling-material_type_other_content").val()){
        		msg.push("Task["+this.title+"]Please fill in the content if you select the 'other' option.'.");
        		changeColorList($("#SFSampling-material_type_other_content"));
        	}
        }
        */
        
        //jsonify the material info into the hidden field
        var jsonvals = new Array();
        $(".material_widget").each(function(){
            if($(this).val()){
                jsonvals.push($(this).attr("ref"));
            }
        });
        $("#SFSampling-material_widgets").val("[" + jsonvals.join(",") + "]");
        return msg;
    }
}
