Namespace.register("SFNamespace.SFLabel");

var resetLabelField=function(){
    resetCheckToFields('#SFLabel-file_from_ftp', '', '#SFLabel-file_from_ftp_location');
    resetCheckToFields('#SFLabel-file_from_files', '', '#SFLabel-file_from_files_location');
    resetCheckToFields('input[name="SFLabel-color"]', 'Others', '#SFLabel-color_other');
    resetCheckToFields('#SFLabel-output_other_type', '', '#SFLabel-output_other_content');
}

SFNamespace.SFLabel.obj = {

    id   		 : "SFLabel",
	
    title        : "Label",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetLabelField();
        $('#SFLabel-file_from_ftp').click(function(){
            resetLabelField()
        })
        $('#SFLabel-file_from_files').click(function(){
            resetLabelField()
        })
        $('input[name="SFLabel-color"]').click(function(){
            resetLabelField()
        })
        $('#SFLabel-output_other_type').click(function(){
            resetLabelField()
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

        if( $("input[name='SFLabel-file_from']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'Files From'.");
            changeColorList($("input[name='SFLabel-file_from']"))
        }
        if( $("#SFLabel-file_from_ftp").attr("checked") && !$("#SFLabel-file_from_ftp_location").val() ){
            msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option.");
            changeColorList($("#SFLabel-file_from_ftp_location"))
        }
        if( $("#SFLabel-file_from_files").attr("checked") && !$("#SFLabel-file_from_files_location").val() ){
            msg.push("Task["+this.title+"']Please input the 'Location' also if you select the 'Files' option.");
            changeColorList($("#SFLabel-file_from_files_location"))
        }
        if( $("#SFLabel-output_other").attr("checked") && !$("#SFLabel-output_other_content").val() ){
            msg.push("Task["+this.title+"']Please input the content also if you select the 'Other' in Output.");
            changeColorList($("#SFLabel-output_other_content"))
        }
        if(($('#SFLabel-size_w').val() || $('#SFLabel-size_h').val()) && !($('#SFLabel-size_w').val() && $('#SFLabel-size_h').val() && $("input[name='SFLabel-size_unit']:checked").val())){
            msg.push("Task["+this.title+"']Please input the size('W','H') and 'Unit' for the 'Size'.");
            changeColorList([[[$('#SFLabel-size_w'),$("input[name='SFLabel-size_unit']"),$('#SFLabel-size_h')],true]])
        }
        
        if(!$("#SFLabel-barcode").val()){
            msg.push("Task["+this.title+"]Please input the 'Bar Code No. & Type'.");
            changeColorList($("#SFLabel-barcode"))
        }
        if( $("input[name='SFLabel-color']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'Print Color'.");
            changeColorList($("input[name='SFLabel-color']"))
        }
        else if($("input[name='SFLabel-color']:checked").val()=='Others' && !$('#SFLabel-color_other').val())
        {  
            msg.push("Task["+this.title+"]Please input the content for the 'Print: Other'.");
            changeColorList($('#SFLabel-color_other'))
        }
        if( $("input[name='SFLabel-output']:checked").length < 1 )
        {
            msg.push("Task["+this.title+"]Please select the 'Output'.");
            changeColorList($("input[name='SFLabel-output']"))
        }
        else if($('#SFLabel-output_other_type').attr('checked') && !$('#SFLabel-output_other_content').val())
        {
            msg.push("Task["+this.title+"]Please input the content for the 'Output: Other'.");
            changeColorList($('#SFLabel-output_other_content'))
        }
        else if($("#SFLabel-output_pdf").attr("checked") && $("input[name='SFLabel-protection']:checked").length < 1){
            changeColorList($("input[name='SFLabel-protection']"));
            msg.push("Task["+this.title+"]Please select the 'Security File Protction' if select the 'Output: PDF'.");
        }
        
        
        if( $("#SFLabel-file_from_see_per_attachment").attr("checked") && !($("#SFLabel-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) )
        {
            msg.push("Task["+this.title+"]Please input the 'Attachment'.");
            changeColorList($("#SFLabel-attachment_name"))
        }
        
        if( !$("#SFLabel-expected_date").val() )
        {
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
            changeColorList($("#SFLabel-expected_date"))
        }
        return msg;
    }
}
