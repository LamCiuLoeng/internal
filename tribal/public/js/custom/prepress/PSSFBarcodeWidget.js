Namespace.register("SFNamespace.PSSFBarcode");

var resetLabelField=function(){
    resetCheckToFields('#PSSFBarcode-file_from_ftp', '', '#PSSFBarcode-file_from_ftp_location');
    resetCheckToFields('#PSSFBarcode-file_from_files', '', '#PSSFBarcode-file_from_files_location');
    resetCheckToFields('input[name="PSSFBarcode-color"]', 'Others', '#PSSFBarcode-color_other');
    resetCheckToFields('#PSSFBarcode-output_other_type', '', '#PSSFBarcode-output_other_content');
}

SFNamespace.PSSFBarcode.obj = {

    id   		 : "PSSFBarcode",
	
    title        : "Barcode",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetLabelField();
        $('#PSSFBarcode-file_from_ftp').click(function(){
		    resetLabelField()
		})
		$('#PSSFBarcode-file_from_files').click(function(){
		    resetLabelField()
		})
		$('input[name="PSSFBarcode-color"]').click(function(){
		    resetLabelField()
		})
		$('#PSSFBarcode-output_other_type').click(function(){
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
        // the validation for label
        
        if( $("input[name='PSSFBarcode-file_from']:checked").length < 1 ){
		    msg.push("Task["+this.title+"]Please select the 'Files From'.");
		    changeColorList($("input[name='PSSFBarcode-file_from']"))
		}
		if( $("#PSSFBarcode-file_from_ftp").attr("checked") && !$("#PSSFBarcode-file_from_ftp_location").val() ){
		    msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'FTP' option.");
		    changeColorList($("#PSSFBarcode-file_from_ftp_location"))
		}
		if( $("#PSSFBarcode-file_from_files").attr("checked") && !$("#PSSFBarcode-file_from_files_location").val() ){
		    msg.push("Task["+this.title+"']Please input the 'Location' also if you select the 'Files' option.");
		    changeColorList($("#PSSFBarcode-file_from_files_location"))
		}
		if(($('#PSSFBarcode-size_w').val() || $('#PSSFBarcode-size_h').val()) && !($('#PSSFBarcode-size_w').val() && $('#PSSFBarcode-size_h').val() && $("input[name='PSSFBarcode-size_unit']:checked").val())){
		    msg.push("Task["+this.title+"']Please input the size('W','H') and 'Unit' for the 'Size'.");
		    changeColorList([[[$('#PSSFBarcode-size_w'),$("input[name='PSSFBarcode-size_unit']"),$('#PSSFBarcode-size_h')],true]])
		}
		if(!$("#PSSFBarcode-barcode").val()){
		    msg.push("Task["+this.title+"]Please input the 'Bar Code No. & Type'.");
		    changeColorList($("#PSSFBarcode-barcode"))
		}
		if( $("input[name='PSSFBarcode-color']:checked").length < 1 ){
		    msg.push("Task["+this.title+"]Please select the 'Print Color'.");
		    changeColorList($("input[name='PSSFBarcode-color']"))
		}
		else if($("input[name='PSSFBarcode-color']:checked").val()=='Others' && !$('#PSSFBarcode-color_other_content').val())
		{  
		    msg.push("Task["+this.title+"]Please input the content for the 'Print: Other'.");
		    changeColorList($('#PSSFBarcode-color_other_content'))
		}
		if( $("input[name='PSSFBarcode-output']:checked").length < 1 )
		{
		    msg.push("Task["+this.title+"]Please select the 'Output'.");
		    changeColorList($("input[name='PSSFBarcode-output']"))
		}
		else if($('#PSSFBarcode-output_other_type').attr('checked') && !$('#PSSFBarcode-output_other_content').val())
		{
		    msg.push("Task["+this.title+"]Please input the content for the 'Output: Other'.");
		    changeColorList($('#PSSFBarcode-output_other_content'))
		}
		else if($("#PSSFBarcode-output_pdf").attr("checked") && $("input[name='PSSFBarcode-protection']:checked").length < 1){
		    changeColorList($("input[name='PSSFBarcode-protection']"));
		    msg.push("Task["+this.title+"]Please select the 'Security File Protction' if select the 'Output: PDF'.");
		}
		if( $("#PSSFBarcode-file_from_see_per_attachment").attr("checked") && !($("#PSSFBarcode-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) )
		{
		    msg.push("Task["+this.title+"]Please input the 'Attachment'.");
		    changeColorList($("#PSSFBarcode-attachment_name"))
		} 
		
        return msg;
    }
}
