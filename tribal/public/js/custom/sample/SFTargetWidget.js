Namespace.register("SFNamespace.SFTarget");


SFNamespace.SFTarget.obj = {

    id   		 : "SFTarget",
	
    title        : "Target",
	
    install 	 : function(){
    	initPlusFields(['#SFTarget-color_spot_content'])
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
        if( !$("#SFTarget-expected_date").val() ){
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
            changeColorList($("#SFTarget-expected_date"))
        }
        /*if( !$("#SFTarget-promo_id").val() ){
							msg.push("Tab["+this.title+"]Please input the 'Target Promo ID'.");
						}
						if( !$("#SFTarget-dpci").val() ){
							msg.push("Tab["+this.title+"]Please input the 'Target DPCI#'.");
						}
						if( !$("#SFTarget-factory_code").val() ){
							msg.push("Tab["+this.title+"]Please input the 'Factory Code(Artwork)'.");
						}
						if( !$("#SFTarget-product_name").val() ){
							msg.push("Tab["+this.title+"]Please input the 'Product Name'.");
						}
						if( !$("#SFTarget-dimension").val() ){
							msg.push("Tab["+this.title+"]Please input the 'Dimension/Size'.");
						}
						*/
        //if( !$("#SFTarget-target_vendor_id").val()){
//            msg.push("Task["+this.title+"] 'Vendor Name' Please select the one.");
//            changeColorList($("#SFTarget-target_vendor_id"))
//        }
        if( $("input[name='SFTarget-material']:checked").length < 1 ){
            msg.push("Task["+this.title+"] Please select the 'Material'.");
            changeColorList($("input[name='SFTarget-material']"))
        }
        if( $("input[name='SFTarget-insert']:checked").length < 1 ){
            msg.push("Task["+this.title+"] Please select the 'Insert'.");
            changeColorList($("input[name='SFTarget-insert']"))
        }
        if( $("#SFTarget-material_others").attr("checked") && !$("#material_other_tmp").val() ){
            msg.push("Task["+this.title+"]Please input the content also if you select the 'Others' option in 'Material'.");
            changeColorList($("#material_other_tmp"))
        }
        if( $("#SFTarget-submitted_item_others").attr("checked") && !$("#SFTarget-submitted_item_other").val() ){
            msg.push("Task["+this.title+"]Please input the content also if you select the 'Others' option in 'Submitted Items'.");
            changeColorList($("#SFTarget-submitted_item_other"))
        }
        
        /*
        if( $("#SFTarget-requirement_Sampling").attr("checked")){
            if(!$("#SFTarget-sample_qty").val() ){
                changeColorList($("#SFTarget-sample_qty"))
                msg.push("Task["+this.title+"]Please input the content also if you select the 'Sampling' option in 'Requirements'.");
            }
            if(!$("input[name='SFTarget-sample']:checked").val()){
                changeColorList($("input[name='SFTarget-sample']"))
                msg.push("Task["+this.title+"]Please select the options also if you select the 'Sampling' option in 'Requirements'.");
            }
        }
        */
        
        if( $("input[name='SFTarget-submitted_item']:checked").length < 1 ){
            changeColorList($("input[name='SFTarget-submitted_item']"))
            msg.push("Task["+this.title+"]Please select the 'Submitted Items'.");
        }
        //if( $("#SFTarget-submitted_item_other").attr("checked") && !$("#SFTarget-submitted_item_other").val() ){
        //	msg.push("Tab["+this.title+"']Please input the content also if you select the 'Others' option.");
        //}
        if( $("input[name='SFTarget-die']:checked").length < 1 ){
            changeColorList($("input[name='SFTarget-die']"))
            msg.push("Task["+this.title+"]Please select the 'Requirements'.");
        }
        var checkps = true;
        if( $("#SFTarget-requirement_quote").attr("checked") && !($("#SFTarget-file_format").attr("checked") || $("#SFTarget-file_format_eps").attr("checked") || $("#SFTarget-file_format_jpeg").attr("checked") || $("#SFTarget-file_format_ard").attr("checked")) ){
            msg.push("Task["+this.title+"]Please choose at least one when selecting the 'Die line for quote(without fitting)' in 'Requirements'.");
            changeColorList([[[$("#SFTarget-file_format"),$("#SFTarget-file_format_eps"),$("#SFTarget-file_format_jpeg"),$("#SFTarget-file_format_ard")],true]])
        }
						
        if( $("#SFTarget-requirement_production").attr("checked") && !($("#SFTarget-file_format2").attr("checked") || $("#SFTarget-file_format_eps2").attr("checked") || $("#SFTarget-file_format_jpeg2").attr("checked") || $("#SFTarget-file_format_ard2").attr("checked"))){
            msg.push("Task["+this.title+"]Please choose at least one when selecting the 'Die line for production' in 'Requirements'.");
            changeColorList([[[$("#SFTarget-file_format2"),$("#SFTarget-file_format_eps2"),$("#SFTarget-file_format_jpeg2"),$("#SFTarget-file_format_ard2")],true]])
        }
					 
		/*				
        if( $("#SFTarget-requirement_Others").attr("checked") && !$("#SFTarget-requirement_other").val() ){
            msg.push("Task["+this.title+"']Please input the content also if you select the 'Others' option.");
            changeColorList($("#SFTarget-requirement_other"))
        }
        */
        
        
        /*
						if( $("input[name='SFTarget-sample']:checked").length < 1 ){
							msg.push("Tab["+this.title+"]Please select the 'Sampling'.");
						}*/
        if( $("input[name='SFTarget-file_format']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'File Format'.");
            changeColorList($("input[name='SFTarget-file_format']"))
        }
        if( $("input[name='SFTarget-target_format']:checked").length < 1 ){
            msg.push("Task["+this.title+"]Please select the 'With Target format'.");
            changeColorList($("input[name='SFTarget-target_format']"))
        }
        if( $("input[name='SFTarget-file_protection']:checked").length < 1 ){
            changeColorList($("input[name='SFTarget-file_protection']"))
            msg.push("Task["+this.title+"]Please select the 'Security File Protection'.");
        }
        /* Update by CL.Lam on 2012-12-30 ,required by Wind.Kwok on 2012-12-12
         * 
        */
    	if( $("#SFTarget-file_from_ftp").attr("checked") && !$("#SFTarget-file_from_ftp_location").val() )
        {
            changeColorList($("#SFTarget-file_from_ftp_location"))
            msg.push("Task["+this.title+"]Please input the 'Location' also if select the 'FTP' option.");
        }
        if( $("#SFTarget-file_from_files").attr("checked") && !$("#SFTarget-file_from_files_location").val() )
        {
            changeColorList($("#SFTarget-file_from_files_location"))
            msg.push("Task["+this.title+"']Please input the 'Location' also if you select the 'Files' option.");
        }
        if( $("#SFTarget-file_from_attachment").attr("checked") && !($("#SFTarget-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) ){
            msg.push("Task["+this.title+"]Please upload the 'Attachment' if select the 'See per attachment' option.");
            changeColorList($("input[name='SFTarget-attachment_name']"))
        }
        
        if(($('#SFTarget-size_w').val() || $('#SFTarget-size_h').val()) &&
            !($('#SFTarget-size_w').val() && $('#SFTarget-size_h').val() && $("input[name='SFTarget-size_unit']:checked").val()))
            {
            changeColorList([[[$('#SFTarget-size_w'),$('#SFTarget-size_h'),$("input[name='SFTarget-size_unit']")],true]])
            msg.push("Task["+this.title+"]Please input the size('W','H') and 'Unit' for the 'Size'.");
        }
        if ($("#SFTarget-color_spot:checked").val())
        {
        	var _spot_flag = false;
        	$('input[name=SFTarget-color_spot_content]').each(function(){
        		if(!$(this).val()) _spot_flag=true
        	})
        	if(_spot_flag){
        		changeColorList($('input[name=SFTarget-color_spot_content]'))
                msg.push("Task["+this.title+"]Please input all the 'PMS' text filed if select the 'Spot Color'.");
        	}
        }
        
        if($("#SFTarget-color_other:checked").val() && !$('#SFTarget-color_other_content').val())
        {
            changeColorList($('#SFTarget-color_other_content'))
            msg.push("Task["+this.title+"]Please input the 'Other' content if select the 'Color: Other'.");
        }
						
        return msg;
    }
}
