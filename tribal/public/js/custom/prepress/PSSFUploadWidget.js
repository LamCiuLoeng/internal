Namespace.register("SFNamespace.PSSFUpload");

SFNamespace.PSSFUpload.obj = {

    id   		 : "PSSFUpload",
	
    title        : "Prepress",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
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
        if( $("input[name='PSSFUpload-checking']:checked").length < 1){
            msg.push("Task["+this.title+"] 'File to' Please select one.");
            changeColorList($("input[name='PSSFUpload-checking']"))
        }
        if( !$("#PSSFUpload-expected_date").val() ){
            changeColorList($("#PSSFUpload-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        if( $("#PSSFUpload-file_from_ftp").attr("checked") && !$("#PSSFUpload-from_ftp_location").val() ){
            changeColorList($("#PSSFUpload-from_ftp_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option in 'File from'.");
        }
        if( $("#PSSFUpload-file_from_public").attr("checked") && !$("#PSSFUpload-from_public_location").val() ){
            changeColorList($("#PSSFUpload-from_public_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'Public' option in 'File from'.");
        }
        if( $("#PSSFUpload-file_to_ftp").attr("checked") && !$("#PSSFUpload-to_ftp_location").val() ){
            changeColorList($("#PSSFUpload-to_ftp_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option in 'File to'.");
        }
        if( $("#PSSFUpload-file_to_public").attr("checked") && !$("#PSSFUpload-to_public_location").val() ){
            changeColorList($("#PSSFUpload-to_public_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'Public' option in 'File to'.");
        }
        
        if( $("input[name='PSSFUpload-output']:checked").length < 1 )
		{
		    msg.push("Task["+this.title+"]Please select the 'Output'.");
		    changeColorList($("input[name='PSSFUpload-output']"))
		}
		else if($('#PSSFUpload-output_other_type').attr('checked') && !$('#PSSFUpload-output_other_content').val())
		{
		    msg.push("Task["+this.title+"]Please input the content for the 'Output: Other'.");
		    changeColorList($('#PSSFUpload-output_other_content'))
		}
		else if($("#PSSFUpload-output_pdf").attr("checked") && $("input[name='PSSFUpload-protection']:checked").length < 1){
		    changeColorList($("input[name='PSSFUpload-protection']"));
		    msg.push("Task["+this.title+"]Please select the 'Security File Protction' if select the 'Output: PDF'.");
		}
             
        return msg;
    }
}
