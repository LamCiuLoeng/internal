Namespace.register("SFNamespace.SF3DImage");

var reset3DField=function(){
    resetCheckToFields('#SF3DImage-file_from_ftp', '', '#SF3DImage-file_from_ftp_location');
    resetCheckToFields('#SF3DImage-file_from_files', '', '#SF3DImage-file_from_files_location');
}

SFNamespace.SF3DImage.obj = {

    id   		 : "SF3DImage",
	
    title        : "3D image",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        validators.push(this);
        reset3DField();
        $("#SF3DImage-file_from_ftp").click(function(){reset3DField();})
        $("#SF3DImage-file_from_files").click(function(){reset3DField();})
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
        if( $("input[name='SF3DImage-file_from']:checked").length < 1 ){
        	changeColorList($("input[name='SF3DImage-file_from']"))
        	msg.push("Task["+this.title+"]Please select the 'Files From'.");
        }else{
            if( $("#SF3DImage-file_from_ftp").attr("checked") && !$("#SF3DImage-file_from_ftp_location").val() ){
                changeColorList($("#SF3DImage-file_from_ftp_location"))
                msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option.");
            }
            if( $("#SF3DImage-file_from_files").attr("checked") && !$("#SF3DImage-file_from_files_location").val() ){
                changeColorList($("#SF3DImage-file_from_files_location"))
                msg.push("Task["+this.title+"']Please input the 'Location' also if you select the 'Files' option.");
            }
            if( $("#SF3DImage-file_from_attachment").attr("checked") && !($("#SF3DImage-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) ){
                msg.push("Task["+this.title+"]Please upload the 'Attachment' if select the 'See per attachment' option.");
                changeColorList($("input[name='SF3DImage-attachment_name']"))
            }
        }
        if( $("input[name='SF3DImage-output']:checked").length < 1 ){
        	changeColorList($("input[name='SF3DImage-output']"))
        	msg.push("Task["+this.title+"]Please select the 'Output'.");
        }
        if( $("input[name='SF3DImage-details']:checked").length < 1 ){
            changeColorList($("input[name='SF3DImage-details']"))
            msg.push("Task["+this.title+"]Please select the 'Details'.");
        }
        if( !$("#SF3DImage-expected_date").val() ){
        	changeColorList($("#SF3DImage-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        return msg;
    }
}
