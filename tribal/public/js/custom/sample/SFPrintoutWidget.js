Namespace.register("SFNamespace.SFPrintout");
var resetDisableFields = function(){
    initDisableFields('input[name=SFPrintout-file_from]', 'ftp', '#SFPrintout-file_from_ftp_location');
    initDisableFields('input[name=SFPrintout-file_from]', 'files', '#SFPrintout-file_from_files_location');
    initDisableFields('input[name=SFPrintout-file_from]', 'new', '#SFPrintout-file_from_task_name');
    initDisableFields('input[name=SFPrintout-output]', 'woodfree', '#SFPrintout-output_woodfree_pcs');
    initDisableFields('input[name=SFPrintout-output]', 'semi', '#SFPrintout-output_semi_pcs');
    initDisableFields('input[name=SFPrintout-output]', 'label', '#SFPrintout-output_label_pcs');
    initDisableFields('input[name=SFPrintout-output]', 'normal', '#SFPrintout-output_normal_pcs');
    initDisableFields('input[name=SFPrintout-delivery]', 'D', '#SFPrintout-expected_time');
    initDisableFields('input[name=SFPrintout-delivery]', 'Y', '#SFPrintout-expected_date');
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
            ['input[name=SFPrintout-file_from]', 'input[name=SFPrintout-output]'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-file_from][value=ftp]', '#SFPrintout-file_from_ftp_location'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-file_from][value=files]', '#SFPrintout-file_from_files_location'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-file_from][value=new]', '#SFPrintout-file_from_task_name'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-output][value=woodfree]', '#SFPrintout-output_woodfree_pcs'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-output][value=semi]', '#SFPrintout-output_semi_pcs'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-output][value=label]', '#SFPrintout-output_label_pcs'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-output][value=normal]', '#SFPrintout-output_normal_pcs'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-delivery][value=D]', '#SFPrintout-expected_time'], 
            {'bind': isBind, 'validate': isValidate})
    initRedFields(true, 
            ['input[name=SFPrintout-delivery][value=Y]', '#SFPrintout-expected_date'], 
            {'bind': isBind, 'validate': isValidate})
}
SFNamespace.SFPrintout.obj = {
    id: "SFPrintout",
    title: "Printout",
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
    validation: function(){
        resetRedFields()
        var msg = [];
					
        if( $("input[name='SFPrintout-file_from']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'Files From'.");
            //changeColorList($("input[name='SFPrintout-file_from']"))
        }
						
        if( $("#SFPrintout-file_from_ftp").attr("checked") && !$("#SFPrintout-file_from_ftp_location").val() ){
            msg.push("Task["+this.title+"]Please input the 'Location' when selecting the ftp in 'Files From'.");
            //changeColorList($("#SFPrintout-file_from_ftp_location"))
        }
						
        if( $("#SFPrintout-file_from_files").attr("checked") && !$("#SFPrintout-file_from_files_location").val() ){
            msg.push("Task["+this.title+"]Please input the 'Location' when selecting the files in 'Files From'.");
            //changeColorList($("#SFPrintout-file_from_files_location"))
        }
        if( $("#SFPrintout-file_from_new").attr("checked") && !$("#SFPrintout-file_from_task_name").val() ){
            msg.push("Task["+this.title+"]Please input the 'Task Name' when selecting the 'New Design With This Request' in 'Files From'.");
            //changeColorList($("#SFPrintout-file_from_task_name"))
        }
        
        if( $("#SFPrintout-file_from_see_per_attachment").attr("checked") && !($("#SFPrintout-attachment_name").val() || $(".SFPrintout-attachment_link").length>0 ) )
        {
            msg.push("Task["+this.title+"]Please input the 'Attachment'.");
            //changeColorList($("#SFPrintout-attachment_name"))
        }
						
        if($("input[name='SFPrintout-delivery']:checked").length < 1){
            msg.push("Task["+this.title+"]Please input the 'Expected date'.");
            //changeColorList($("input[name='SFPrintout-delivery']"))
        }
						
        if($("input[name='SFPrintout-delivery'][value='Y']:checked").val() && !$("#SFPrintout-expected_date").val() ){
            msg.push("Task["+this.title+"]Please input the 'Expected date'.");
            //changeColorList($("#SFPrintout-expected_date"))
        }
        if($("input[name='SFPrintout-delivery'][value='D']:checked").val()  && !$("#SFPrintout-expected_time").val() ){
            msg.push("Task["+this.title+"]Please input the 'Same Day Delivery'.");
            //changeColorList($("#SFPrintout-expected_time"))
        }
        //var valid = validatForm(1,["#SFPrintout-file_from_ftp","#SFPrintout-file_from_cd","#SFPrintout-file_from_files","#SFPrintout-file_from_new"])
        //if(valid) msg.push(valid)
						
        //var valid1 = validatForm(1,["#SFPrintout-output_dupont","#SFPrintout-output_woodfree","#SFPrintout-output_semi","#SFPrintout-output_label","#SFPrintout-output_normal"])
        //if(valid1) msg.push(valid1)
						
        //valid2 = validatForm(2,{
        //						"#SFPrintout-file_from_ftp":["#SFPrintout-file_from_ftp_location"],
        //						"#SFPrintout-file_from_files":["#SFPrintout-file_from_files_location"],
        //						"#SFPrintout-output_dupont":["#SFPrintout-output_dupont_pcs"],
        //						"#SFPrintout-output_woodfree":["#SFPrintout-output_woodfree_pcs"],
        //						"#SFPrintout-output_semi":["#SFPrintout-output_semi_pcs"],
        //						"#SFPrintout-output_label":["#SFPrintout-output_label_pcs"],
        //						"#SFPrintout-output_normal":["#SFPrintout-output_normal_pcs"]
        //						})
        //if(valid2) msg.push(valid2)

        if( $("input[name='SFPrintout-output']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'Output'.");
            //changeColorList($("input[name='SFPrintout-output']"))
        }

        var kv = [
            ["SFPrintout-output_woodfree", "SFPrintout-output_woodfree_pcs"],
            ["SFPrintout-output_semi", "SFPrintout-output_semi_pcs"],
            ["SFPrintout-output_label", "SFPrintout-output_label_pcs"],
            ["SFPrintout-output_normal", "SFPrintout-output_normal_pcs"]
        ];
        var pcsFill = true;
        for(var j=0;j<kv.length;j++){
            if( $("#"+kv[j][0]).attr("checked") && !$("#"+kv[j][1]).val() ){
                pcsFill = false;
                break;
            }
        }
        if(!pcsFill){
            msg.push("Task["+this.title+"]Please input the 'pcs' corresponding.");
        }

        return msg;
    }
}
