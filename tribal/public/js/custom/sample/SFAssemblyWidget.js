Namespace.register("SFNamespace.SFAssembly");

var resetAssemblyField=function(){
    resetCheckToFields('#SFAssembly-file_from_ftp', '', '#SFAssembly-file_from_ftp_location');
    resetCheckToFields('#SFAssembly-file_from_files', '', '#SFAssembly-file_from_files_location');
}

SFNamespace.SFAssembly.obj = {

    id   		 : "SFAssembly",
	
    title        : "Assembly Sheet",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        validators.push(this);
        resetAssemblyField();
        $('#SFAssembly-file_from_ftp').click(function(){resetAssemblyField();})
        $('#SFAssembly-file_from_files').click(function(){resetAssemblyField();})
    },
	
    uninstall 	 : function(){
        for(var i=0;i<validators.length;i++){
            if( this.id==validators[i].id ){
                validators.splice(i,1);
                break;
            }
        }
    },
	
    validation   : function(){
        var msg = [];
        if(!$('input[name="SFAssembly-file_from"]:checked').val()){
            changeColorList($("[name='SFAssembly-file_from']"))
            msg.push("Task["+this.title+"]Please select the 'Files from'.");
        }else{
            if( $("#SFAssembly-file_from_ftp").attr("checked") && !$("#SFAssembly-file_from_ftp_location").val() ){
                changeColorList($("#SFAssembly-file_from_ftp_location"))
                msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option.");
            }
            if( $("#SFAssembly-file_from_files").attr("checked") && !$("#SFAssembly-file_from_files_location").val() ){
                changeColorList($("#SFAssembly-file_from_files_location"))
                msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'Files' option.");
            }
            if( $("#SFAssembly-file_from_attachment").attr("checked") && !($("#SFAssembly-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) ){
                msg.push("Task["+this.title+"]Please upload the 'Attachment' if select the 'See per attachment' option.");
                changeColorList($("input[name='SFAssembly-attachment_name']"))
            }
        }
        if( !$("[name='SFAssembly-output']:checked").val() ){
            changeColorList($("[name='SFAssembly-output']"))
            msg.push("Task["+this.title+"]Please select the 'Output'.");
        }
        if( !$("#SFAssembly-expected_date").val() ){
            changeColorList($("#SFAssembly-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        return msg;
    }
}
