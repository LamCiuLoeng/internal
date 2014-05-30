Namespace.register("SFNamespace.SFArtwork");

var resetArtworkField=function(){
    resetCheckToFields('#SFArtwork-file_from_ftp', '', '#SFArtwork-file_from_ftp_location');
    resetCheckToFields('#SFArtwork-file_from_files', '', '#SFArtwork-file_from_files_location');
    resetCheckToFields('#SFArtwork-color_spot', '', 'input[name=SFArtwork-color_spot_content]');
    resetCheckToFields('#SFArtwork-color_other', '', '#SFArtwork-color_other_content');
    resetCheckToFields('#SFArtwork-output_other', '', '#SFArtwork-output_other_content');
}

SFNamespace.SFArtwork.obj = {

    id   		 : "SFArtwork",
	
    title        : "Artwork",
	
    install 	 : function(){
        initPlusFields(['#SFArtwork-color_spot_content'])
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetArtworkField();
        $("#SFArtwork-file_from_ftp").click(function(){resetArtworkField();})
        $("#SFArtwork-file_from_files").click(function(){resetArtworkField();})
        $("#SFArtwork-color_spot").click(function(){resetArtworkField();})
        $("#SFArtwork-color_other").click(function(){resetArtworkField();})
        $("#SFArtwork-output_other").click(function(){resetArtworkField();})
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
        if( $("input[name='SFArtwork-file_from']:checked").length < 1 )
        {
            changeColorList($("input[name='SFArtwork-file_from']"))
            msg.push("Task["+this.title+"]Please select the 'Files From'.");
        }
        else{
            if( $("#SFArtwork-file_from_ftp").attr("checked") && !$("#SFArtwork-file_from_ftp_location").val() )
            {
                changeColorList($("#SFArtwork-file_from_ftp_location"))
                msg.push("Task["+this.title+"]Please input the 'Location' also if select the 'FTP' option.");
            }
            if( $("#SFArtwork-file_from_files").attr("checked") && !$("#SFArtwork-file_from_files_location").val() )
            {
                changeColorList($("#SFArtwork-file_from_files_location"))
                msg.push("Task["+this.title+"']Please input the 'Location' also if you select the 'Files' option.");
            }
            if( $("#SFArtwork-file_from_attachment").attr("checked") && !($("#SFArtwork-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) ){
                msg.push("Task["+this.title+"]Please upload the 'Attachment' if select the 'See per attachment' option.");
                changeColorList($("input[name='SFArtwork-attachment_name']"))
            }
        }
        
        if(($('#SFArtwork-size_w').val() || $('#SFArtwork-size_h').val()) &&
            !($('#SFArtwork-size_w').val() && $('#SFArtwork-size_h').val() && $("input[name='SFArtwork-size_unit']:checked").val()))
            {
            changeColorList([[[$('#SFArtwork-size_w'),$('#SFArtwork-size_h'),$("input[name='SFArtwork-size_unit']")],true]])
            msg.push("Task["+this.title+"]Please input the size('W','H') and 'Unit' for the 'Size'.");
        }
        if ($("#SFArtwork-color_spot:checked").val())
        {
        	var _spot_flag = false;
        	$('input[name=SFArtwork-color_spot_content]').each(function(){
        		if(!$(this).val()) _spot_flag=true
        	})
        	if(_spot_flag){
        		changeColorList($('input[name=SFArtwork-color_spot_content]'))
                msg.push("Task["+this.title+"]Please input all the 'PMS' text filed if select the 'Spot Color'.");
        	}
        }
        if($("#SFArtwork-color_other:checked").val() && !$('#SFArtwork-color_other_content').val())
        {
            changeColorList($('#SFArtwork-color_other_content'))
            msg.push("Task["+this.title+"]Please input the 'Other' content if select the 'Color: Other'.");
        }
        if( $("input[name='SFArtwork-output']:checked").length < 1 )
        {
            changeColorList($("input[name='SFArtwork-output']"))
            msg.push("Task["+this.title+"]Please select the 'Output'.");
        }
        else if($("#SFArtwork-output_other").attr("checked") &&　!$('#SFArtwork-output_other_content').val())
        {
            changeColorList($('#SFArtwork-output_other_content'))
            msg.push("Task["+this.title+"]Please input the 'Other' content if select the 'Output: Other'.");
        }
        else if($("#SFArtwork-output_pdf").attr("checked") && $("input[name='SFArtwork-protection']:checked").length < 1){
            changeColorList($("input[name='SFArtwork-protection']"));
            msg.push("Task["+this.title+"]Please select the 'Security File Protction' if select the 'Output: PDF'.");
        }
        
        
        if( !$("#SFArtwork-expected_date").val() ){
            changeColorList($("#SFArtwork-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        return msg;
    }
}
