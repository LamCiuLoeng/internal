Namespace.register("SFNamespace.SFUpload");


SFNamespace.SFUpload.obj = {

    id   		 : "SFUpload",
	
    title        : "Upload/Download/File checking",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
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
        //if( !$("[name='SFUpload-job_nature']:checked").val() && !$("[name='SFUpload-checking']:checked").val()){
        //	msg.push("Tab["+this.title+"]Please select the 'Job Nature'.");
        //	changeColorList($("[name='SFUpload-checking']"))
        //}
        //if( $("input[name='SFUpload-file_to']:checked").length < 1 && $("#SFUpload-job_nature_u").attr("checked")){
        //	msg.push("Tab["+this.title+"] 'File to' Please select one.");
        //	changeColorList($("#SFUpload-job_nature_u"))
        //}
        if( $("input[name='SFUpload-checking']:checked").length < 1){
            msg.push("Task["+this.title+"] 'File to' Please select one.");
            changeColorList($("input[name='SFUpload-checking']"))
        }
        if( !$("#SFUpload-expected_date").val() ){
            changeColorList($("#SFUpload-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        if( $("#SFUpload-file_from_ftp").attr("checked") && !$("#SFUpload-from_ftp_location").val() ){
            changeColorList($("#SFUpload-from_ftp_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option in 'File from'.");
        }
        if( $("#SFUpload-file_from_public").attr("checked") && !$("#SFUpload-from_public_location").val() ){
            changeColorList($("#SFUpload-from_public_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'Public' option in 'File from'.");
        }
        if( $("#SFUpload-file_to_ftp").attr("checked") && !$("#SFUpload-to_ftp_location").val() ){
            changeColorList($("#SFUpload-to_ftp_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option in 'File to'.");
        }
        if( $("#SFUpload-file_to_public").attr("checked") && !$("#SFUpload-to_public_location").val() ){
            changeColorList($("#SFUpload-to_public_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'Public' option in 'File to'.");
        }
        //var validOne1 = validatForm(1,["#SFUpload-file_from_ftp","#SFUpload-file_from_public","#SFUpload-file_from_cd"])
        //if(validOne1) msg.push(validOne1)
						
        //var validOne2 = validatForm(1,["#SFUpload-file_to_ftp","#SFUpload-file_to_public","#SFUpload-file_to_cd"])
        //if(validOne2) msg.push(validOne2)
						
        //valid = validatForm(2,{
        //						"#SFUpload-file_from_ftp":["#SFUpload-from_ftp_location"],
        //						"#SFUpload-file_from_public":["#SFUpload-from_public_location"],
        //						"#SFUpload-file_to_ftp":["#SFUpload-to_ftp_location"],
        //						"#SFUpload-file_to_public":["#SFUpload-to_public_location"]
        //						})
        //if(valid) msg.push(valid)
        return msg;
    }
}
