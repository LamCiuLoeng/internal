Namespace.register("SFNamespace.SFFileConvert");

var resetFileConvertField=function(){
    resetCheckToFields('#SFFileConvert-file_from_ftp', '', '#SFFileConvert-file_from_ftp_location');
    resetCheckToFields('#SFFileConvert-file_from_files', '', '#SFFileConvert-file_from_files_location');
    resetCheckToFields('#SFFileConvert-output_other', '', '#SFFileConvert-output_other_content');
}

SFNamespace.SFFileConvert.obj = {

    id   		 : "SFFileConvert",
	
    title        : "File Convert",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        validators.push(this);
        resetFileConvertField();
        $('#SFFileConvert-file_from_ftp').click(function(){
            resetFileConvertField()
        })
        $('#SFFileConvert-file_from_files').click(function(){
            resetFileConvertField()
        })
        $('#SFFileConvert-output_other').click(function(){
            resetFileConvertField()
        })
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
        if( $("#SFFileConvert-file_from_ftp").attr("checked") && !$("#SFFileConvert-file_from_ftp_location").val() ){
            changeColorList($("#SFFileConvert-file_from_ftp_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option.");
        }
        if( $("#SFFileConvert-file_from_files").attr("checked") && !$("#SFFileConvert-file_from_files_location").val() ){
            changeColorList($("#SFFileConvert-file_from_files_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'Files' option.");
        }
        if( $("#SFFileConvert-file_from_attachment").attr("checked") && !($("#SFFileConvert-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) ){
            msg.push("Task["+this.title+"]Please upload the 'Attachment' if select the 'See per attachment' option.");
            changeColorList($("input[name='SFFileConvert-attachment_name']"))
        }
        if(!$("input[name='SFFileConvert-output']:checked").val()){
            changeColorList($("input[name='SFFileConvert-output']"))
            msg.push("Task["+this.title+"]Please select the 'Output '.");
        }else if( $("#SFFileConvert-output_other").attr("checked") && !$("#SFFileConvert-output_other_content").val() ){
            changeColorList($("#SFFileConvert-output_other_content"))
            msg.push("Task["+this.title+"]Please input the content if select 'Output : Other'.");
        }else if( $("#SFFileConvert-output_pdf").attr("checked") && !$("input[name='SFFileConvert-output_pdf_protection']:checked").val() ){
            changeColorList($("#SFFileConvert-output_pdf_protection"))
            msg.push("Task["+this.title+"]Please select the 'Security File Protection' if select 'Output: PDF'.");
        }
        if( !$("#SFFileConvert-expected_date").val() ){
            changeColorList($("#SFFileConvert-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        return msg;
    }
}
