Namespace.register("SFNamespace.SFAvon");
var resetDisableFields = function(){
	initDisableFields('input[name="SFAvon-top"]', 'Other', '#SFAvon-top_other');
	initDisableFields('input[name="SFAvon-white_box"]', 'Y', '#SFAvon-white_box_qty');
	initDisableFields('input[name="SFAvon-dimension_type"]', 'product', 
			['#SFAvon-product_width','#SFAvon-product_depth','#SFAvon-product_height','input[name=SFAvon-product_unit]','input[name=SFAvon-product_as_sample]']);
	initDisableFields('input[name="SFAvon-dimension_type"]', 'styrofoam', 
			['#SFAvon-dimension_width','#SFAvon-dimension_depth','#SFAvon-dimension_height','input[name=SFAvon-dimension_unit]','input[name=SFAvon-dimension_as_sample]']);
	initDisableFields('input[name="SFAvon-dimension_type"]', 'box', 
			['#SFAvon-box_width','#SFAvon-box_depth','#SFAvon-box_height','input[name=SFAvon-box_unit]','input[name=SFAvon-box_as_sample]', 'input[name=SFAvon-box_size]']);
//
//	var set_dc4 = $('.fset_dc4 :input')
//	initDisableFields('input[name=SFAvon-category]', ['Insert', 'Bubble', 'Polybag', 'GB', 'MP'], set_dc4)

	var set_mp = $('#fset_mp :input');
	set_mp.push(['input[name=SFAvon-quantity]', 'Fixed', 'input[name=SFAvon-quantity_pcs]'])
	set_mp.push(['input[name=SFAvon-country]', 'Other', '#SFAvon-country_other'])
	initDisableFields('input[name=SFAvon-category]', 'MP', set_mp)

    var set_artwork = $('.fset_artwork :input')
    set_artwork.push(['input[name=SFAvon-artwork_color]', 'spot', 'input[name=SFAvon-artwork_color_spot_content]'])
    set_artwork.push(['input[name=SFAvon-artwork_color]', 'other', '#SFAvon-artwork_color_other_content'])
    initDisableFields('input[name=SFAvon-category]', 'Artwork', set_artwork)
    
    var set_barcode = $('.fset_barcode :input')
    set_barcode.push(['input[name=SFAvon-label_color]', 'Others', '#SFAvon-label_color_other'])
    initDisableFields('input[name=SFAvon-category]', 'Barcode', set_barcode)
    
    var set_artwork_barcde = $('.fset_artwork_barcode :input')
    set_artwork_barcde.push(['input[name=SFAvon-artwork_file_from]', 'ftp', '#SFAvon-artwork_file_from_ftp_location'])
    set_artwork_barcde.push(['input[name=SFAvon-artwork_file_from]', 'files', '#SFAvon-artwork_file_from_files_location'])
    set_artwork_barcde.push(['input[name=SFAvon-artwork_output]', 'pdf', 'input[name=SFAvon-artwork_protection]'])
    set_artwork_barcde.push(['input[name=SFAvon-artwork_output]', 'other', '#SFAvon-artwork_output_other_content'])
    initDisableFields('input[name=SFAvon-category]', ['Artwork', 'Barcode'], set_artwork_barcde)
}
var bindOnce = false;
var resetRedFields=function(){
	var isBind, isValidate
	if(!bindOnce){
		isBind = true;
		isValidate = true;
		bindOnce = true;
	}else
		isBind = false;
	initRedFields(true, 
			['input[name=SFAvon-category]', '#SFAvon-expected_date'], 
			{'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-dimension_type][value=product]', 
			[['#SFAvon-product_width', '#SFAvon-product_depth', '#SFAvon-product_height', 'input[name=SFAvon-product_unit]'], ['input[name=SFAvon-product_as_sample]']],
			{'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-dimension_type][value=styrofoam]', 
			[['#SFAvon-dimension_width', '#SFAvon-dimension_depth', '#SFAvon-dimension_height', 'input[name=SFAvon-dimension_unit]'], ['input[name=SFAvon-dimension_as_sample]']],
			{'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-dimension_type][value=box]', 
			[['#SFAvon-box_width', '#SFAvon-box_depth', '#SFAvon-box_height', 'input[name=SFAvon-box_unit]', 'input[name=SFAvon-box_size]'], ['input[name=SFAvon-box_as_sample]']],
			{'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-top][value=Other]', '#SFAvon-top_other', 
			{'bind': isBind, 'validate': isValidate})
	initRedFields(true,
			[['#SFAvon-mp_width', '#SFAvon-mp_depth', '#SFAvon-mp_height', 'input[name=SFAvon-mp_size]', 'input[name=SFAvon-mp_unit]']],
			{'bind': isBind, 'validate': isValidate, 'required': false})
	initRedFields([['input[name=SFAvon-category][value=Insert]'], 
	               ['input[name=SFAvon-category][value=Bubble]'], 
	               ['input[name=SFAvon-category][value=Polybag]'], 
	               ['input[name=SFAvon-category][value=GB]'], 
	               ['input[name=SFAvon-category][value=MP]']], 
			['input[name=SFAvon-sample]', 'input[name=SFAvon-artwork]', 'input[name=SFAvon-dimension_type]', '.material_widget'],
			{'bind': isBind, 'validate': isValidate})
	initRedFields([['input[name=SFAvon-category][value=Insert]'], 
	               ['input[name=SFAvon-category][value=Bubble]'], 
	               ['input[name=SFAvon-category][value=Polybag]'], 
	               ['input[name=SFAvon-category][value=GB]'], 
	               ['input[name=SFAvon-category][value=MP]']], 
			[['#SFAvon-product_weight', '#SFAvon-product_weight_unit'],['input[name=SFAvon-product_weight_as_sample]']],
			{'bind': isBind, 'validate': isValidate})

	initRedFields('input[name=SFAvon-quantity][value=Fixed]', 'input[name=SFAvon-quantity_pcs]', {'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-country][value=Other]', '#SFAvon-country_other', {'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-category][value=MP]', 
			['input[name=SFAvon-quantity]', 'input[name=SFAvon-country]', 'input[name=SFAvon-product]'],
			{'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-category][value=GB]', 
			['input[name=SFAvon-top]', 'input[name=SFAvon-dimension_type][value=box]'],
			{'bind': isBind, 'validate': isValidate})
	initRedFields([['input[name=SFAvon-category][value=Artwork]'], ['input[name=SFAvon-category][value=Barcode]']], 
			['input[name=SFAvon-artwork_file_from]', 'input[name=SFAvon-artwork_output]'],
			{'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-artwork_file_from][value=ftp]', '#SFAvon-artwork_file_from_ftp_location', {'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-artwork_file_from][value=files]', '#SFAvon-artwork_file_from_files_location', {'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-artwork_output][value=pdf]', 'input[name=SFAvon-artwork_protection]', {'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-artwork_output][value=other]', '#SFAvon-artwork_output_other_content', {'bind': isBind, 'validate': isValidate})
	
	initRedFields(true, 
			[['#SFAvon-artwork_size_w', '#SFAvon-artwork_size_h', 'input[name=SFAvon-artwork_size_unit]']],
			{'bind': isBind, 'validate': isValidate, 'required': false})
	initRedFields('#SFAvon-artwork_color_spot', 'input[name=SFAvon-artwork_color_spot_content]', {'bind': isBind, 'validate': isValidate})
	initRedFields('#SFAvon-artwork_color_other', '#SFAvon-artwork_color_other_content', {'bind': isBind, 'validate': isValidate})
	
	initRedFields(true, [['#SFAvon-label_size_w', '#SFAvon-label_size_h', 'input[name=SFAvon-label_size_unit]']], 
			{'bind': isBind, 'validate': isValidate, 'required': false}) 
	initRedFields('input[name=SFAvon-category][value=Barcode]', 
			['#SFAvon-label_barcode', 'input[name=SFAvon-label_color]'],
			{'bind': isBind, 'validate': isValidate})
	initRedFields('input[name=SFAvon-label_color][value=Others]', '#SFAvon-label_color_other', {'bind': isBind, 'validate': isValidate})
}
var bindOnce = false;
SFNamespace.SFAvon.obj = {
    id: "SFAvon",
    title: "Avon",
    install: function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        initPlusFields(['#SFAvon-quantity_pcs', '#SFAvon-artwork_color_spot_content'])
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
        if( !$("input[name='SFAvon-category']:checked").val()){
            //changeColorList($("input[name='SFAvon-category']"))
            msg.push("Task["+this.title+"]Please select the 'Design Category'.");
        }else if($('input[name=SFAvon-category][value=Insert]').attr('checked') || 
        		$('input[name=SFAvon-category][value=Bubble]').attr('checked') || 
        		$('input[name=SFAvon-category][value=Polybag]').attr('checked') || 
        		$('input[name=SFAvon-category][value=GB]').attr('checked') || 
        		$('input[name=SFAvon-category][value=MP]').attr('checked')){
        	if($(".material_widget[value!='']").length < 1){
                msg.push("Task["+this.title+"]Please add the 'Material'.");
            }

            if( $("input[name='SFAvon-sample']:checked").length < 1 ){
                //changeColorList($("input[name='SFAvon-sample']"))
                msg.push("Task["+this.title+"]Please select the 'Sample Reference'.");
            }
            if( $("input[name='SFAvon-artwork']:checked").length < 1 ){
                //changeColorList($("input[name='SFAvon-artwork']"))
                msg.push("Task["+this.title+"]Please select the 'Artworks'.");
            }
            if( $("input[name='SFAvon-dimension_type']:checked").length < 1 ){
                //changeColorList($("input[name='SFAvon-dimension_type']"))
                msg.push("Task["+this.title+"]Please select the 'Dimension'.");
            }else{
                var d = $("input[name='SFAvon-dimension_type']:checked").val();
                if(d=='product'){
                    if(!($('#SFAvon-product_width').val() && $('#SFAvon-product_depth').val() && $('#SFAvon-product_height').val() && $("input[name='SFAvon-product_unit']:checked").val()) && !$("input[name='SFAvon-product_as_sample']:checked").val()){
//                        changeColorList([[[[$("input[name='SFAvon-product_as_sample']"),$('#SFAvon-product_width'),$('#SFAvon-product_depth'),$('#SFAvon-product_height'),$("input[name='SFAvon-product_unit']")]
//                            ,$("input[name='SFAvon-product_as_sample']")
//                            ],false]])
                        msg.push("Task["+this.title+"]Please either input the content and select the 'Unit' for the 'Product Dimensions' or select 'As Sample'.");
                    }
                }else if(d=='styrofoam'){
                    if(!$("input[name='SFAvon-dimension_as_sample']:checked").val() && 
                        !($('#SFAvon-dimension_width').val() && $('#SFAvon-dimension_depth').val() && $('#SFAvon-dimension_height').val() && $("input[name='SFAvon-dimension_unit']:checked").val()) ){
//                        changeColorList([[[[$("input[name='SFAvon-dimension_as_sample']"),$('#SFAvon-dimension_width'),$('#SFAvon-dimension_depth'),$('#SFAvon-dimension_height'),$("input[name='SFAvon-dimension_unit']")]
//                            ,$("input[name='SFAvon-dimension_as_sample']")
//                            ],false]])
                        msg.push("Task["+this.title+"]Please complete input content for the 'Styrofoam Dimension' or select 'As Sample'.");
                    }
                }else if(d=='box'){
                    if(!$("input[name='SFAvon-box_as_sample']:checked").val() && 
                        !($('#SFAvon-box_width').val() && $('#SFAvon-box_depth').val() && $('#SFAvon-box_height').val() && $("input[name='SFAvon-box_unit']:checked").val() && $("input[name='SFAvon-box_size']:checked").val()) ){
//                        changeColorList([[[[$("input[name='SFAvon-box_as_sample']"),$('#SFAvon-dimension_width'),$('#SFAvon-box_depth'),$('#SFAvon-box_height'),$("input[name='SFAvon-box_unit']"),$("input[name='SFAvon-box_size']")]
//                            ,$("input[name='SFAvon-box_as_sample']")
//                            ],false]])
                        msg.push("Task["+this.title+"]Please either input the contents, select the 'Unit' and 'Diemension' for the 'Box Dimensions' or select 'As Sample'.");
                    }
                }
            }
            if(!($('#SFAvon-product_weight').val() && $("#SFAvon-product_weight_unit").val()) && !$("input[name='SFAvon-product_weight_as_sample']:checked").val()){
//                changeColorList([[[[$("input[name='SFAvon-product_weight_as_sample']"), $('#SFAvon-product_weight'), $("#SFAvon-product_weight_unit")]
//                    ,$("input[name='SFAvon-product_weight_as_sample']")
//                    ],false]])
                msg.push("Task["+this.title+"]Please either input the content and select the 'Unit' for the 'Product Weight' or select 'As Sample'.");
            }
        }

        if( $("input[name='SFAvon-top']:checked").val()=='Other' && !$("#SFAvon-top_other").val()){
//            changeColorList($("#SFAvon-top_other"))
            msg.push("Task["+this.title+"]Please input the 'Other' if select the 'Top & Bottom Closure: Other'.");
        }
        if(($('#SFAvon-mp_width').val() || $('#SFAvon-mp_depth').val() || $('#SFAvon-mp_height').val() || $("input[name='SFAvon-mp_size']:checked").val() || $("input[name='SFAvon-mp_unit']:checked").val())
            &&!($('#SFAvon-mp_width').val() && $('#SFAvon-mp_depth').val() && $('#SFAvon-mp_height').val() && $("input[name='SFAvon-mp_size']:checked").val() &&  $("input[name='SFAvon-mp_unit']:checked").val())){
//            changeColorList([[[$('#SFAvon-mp_width'),$('#SFAvon-mp_depth'),$('#SFAvon-mp_height'), $("input[name='SFAvon-mp_size']"),$("input[name='SFAvon-mp_unit']")],true]])
            //changeColorList([[[$('#SFAvon-mp_width'),$('#SFAvon-mp_depth'),$('#SFAvon-mp_height'), $("input[name='SFAvon-mp_size']"),$("input[name='SFAvon-mp_unit']")],false]])
            msg.push("Task["+this.title+"]Please complete input content for the 'Specified MP Size'.");
        }
        if( $("input[name='SFAvon-quantity']:checked").val()=='Fixed' ){
        	var flag = true;
        	$("input[name=SFAvon-quantity_pcs]").each(function(){
        		if(!$(this).val()) flag = false
        		//changeColorList($(this))
        	})
        	if(!flag) msg.push("Task["+this.title+"]Please input the 'Quantity' for the 'Fixed' option.");
        }
        if( $("input[name='SFAvon-country']:checked").val()=='Other' && !$("#SFAvon-country_other").val() ){
            //changeColorList($("#SFAvon-country_other"))
            msg.push("Task["+this.title+"]Please input the 'Other' if select 'Country: Other'.");
        }
                
        
        if($("#SFAvon-category_mp").attr('checked')){
            if($("input[name='SFAvon-country']:checked").length < 1){
                //changeColorList($("input[name='SFAvon-country']"))
                msg.push("Task["+this.title+"]Please select 'Country' if the 'MP' is checked.");
            }
            if($("input[name='SFAvon-product']:checked").length < 1){
                //changeColorList($("input[name='SFAvon-product']"))
                msg.push("Task["+this.title+"]Please select 'Product Orientation' if the 'MP' is checked.");
            }
            if($("input[name='SFAvon-quantity']:checked").length < 1){
                //changeColorList($("input[name='SFAvon-quantity']"))
                msg.push("Task["+this.title+"]Please select 'Quantity' if the 'MP' is checked.");
            }
        }

        if($("#SFAvon-category_gb").attr('checked')){
            if($("input[name='SFAvon-top']:checked").length < 1){
                //changeColorList($("input[name='SFAvon-top']"))
                msg.push("Task["+this.title+"]Please select 'Top & Bottom Closure' if the 'GB' is checked.");
            }
            if(!$("input[name='SFAvon-box_as_sample']:checked").val() && !($('#SFAvon-box_width').val() && $('#SFAvon-box_depth').val() && $('#SFAvon-box_height').val() && $("input[name='SFAvon-box_unit']:checked").val() && $("input[name='SFAvon-box_size']:checked").val())){
//                changeColorList([[[[$("input[name='SFAvon-box_as_sample']"),$('#SFAvon-box_width'),$('#SFAvon-box_depth'),$('#SFAvon-box_height'),$("input[name='SFAvon-box_unit']"),$("input[name='SFAvon-box_size']")]
//                    ,$("input[name='SFAvon-box_as_sample']")
//                    ],false]])
                msg.push("Task["+this.title+"]Please complete input the 'Box Dimensions' content or select 'As Sample' if the 'GB' is checked.");
            }
        }
        if($("#SFAvon-category_artwork").attr('checked') || $('#SFAvon-category_barcode').attr('checked')){
        	if( $("input[name='SFAvon-artwork_file_from']:checked").length < 1 ){
                //changeColorList($("input[name='SFAvon-artwork_file_from']"))
                msg.push("Task["+this.title+"]Please select the 'Files From'.");
            }else{
                if( $("#SFAvon-artwork_file_from_ftp").attr("checked") && !$("#SFAvon-artwork_file_from_ftp_location").val() ){
                    //changeColorList($("#SFAvon-artwork_file_from_ftp_location"))
                    msg.push("Task["+this.title+"]Please input the 'Location' if select the 'FTP' option.");
                }
                if( $("#SFAvon-artwork_file_from_files").attr("checked") && !$("#SFAvon-artwork_file_from_files_location").val() ){
                    //changeColorList($("#SFAvon-artwork_file_from_files_location"))
                    msg.push("Task["+this.title+"']Please input the 'Location' if you select the 'Files' option.");
                }
                if( $("#SFAvon-artwork_file_from_attachment").attr("checked") && !($("#SFAvon-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) ){
                    //changeColorList($("input[name='SFAvon-artwork_attachment_name']"))
                    msg.push("Task["+this.title+"]Please upload the 'Attachment' if select the 'See per attachment' option.");
                }
            }
        	if( $("input[name='SFAvon-artwork_output']:checked").length < 1 ){
                //changeColorList($("input[name='SFAvon-artwork_output']"))
                msg.push("Task["+this.title+"]Please select the 'Output'.");
            }else if($("#SFAvon-artwork_output_other").attr("checked") &&　!$('#SFAvon-artwork_output_other_content').val()){
                //changeColorList($('#SFAvon-artwork_output_other_content'))
                msg.push("Task["+this.title+"]Please input the 'Other' content if select the 'Output: Other'.");
            }else if($("#SFAvon-artwork_output_pdf").attr("checked") && $("input[name='SFAvon-artwork_protection']:checked").length < 1){
                //changeColorList($("input[name='SFAvon-artwork_protection']"));
                msg.push("Task["+this.title+"]Please select the 'Security File Protction' if select the 'Output: PDF'.");
            }

        	if($("#SFAvon-category_artwork").attr('checked')){
        		if(($('#SFAvon-artwork_size_w').val() || $('#SFAvon-artwork_size_h').val()) &&
                        !($('#SFAvon-artwork_size_w').val() && $('#SFAvon-artwork_size_h').val() && $("input[name='SFAvon-artwork_size_unit']:checked").val())){
                        //changeColorList([[[$('#SFAvon-artwork_size_w'),$('#SFAvon-artwork_size_h'),$("input[name='SFAvon-artwork_size_unit']")],true]])
                        msg.push("Task["+this.title+"]Please input the size('W','H') and 'Unit' for the 'Artwork Size'.");
                    }
                    if ($("#SFAvon-artwork_color_spot:checked").val()){
                    	var _spot_flag = false;
                    	$('input[name=SFAvon-artwork_color_spot_content]').each(function(){
                    		if(!$(this).val()) _spot_flag=true
                    	})
                    	if(_spot_flag){
                    		//changeColorList($('input[name=SFAvon-artwork_color_spot_content]'))
                            msg.push("Task["+this.title+"]Please input all the 'PMS' text filed if select the 'Spot Color'.");
                    	}
                    }
                    if($("#SFAvon-artwork_color_other:checked").val() && !$('#SFAvon-artwork_color_other_content').val()){
                        //changeColorList($('#SFAvon-artwork_color_other_content'))
                        msg.push("Task["+this.title+"]Please input the 'Other' content if select the 'Color: Other'.");
                    }
        	}
        	if($("#SFAvon-category_barcode").attr('checked')){
        		if(($('#SFAvon-label_size_w').val() || $('#SFAvon-label_size_h').val()) && !($('#SFAvon-label_size_w').val() && $('#SFAvon-label_size_h').val() && $("input[name='SFAvon-label_size_unit']:checked").val())){
                    msg.push("Task["+this.title+"]Please input the size('W','H') and 'Unit' for the 'Barcode Size'.");
                    //changeColorList([[[$('#SFAvon-label_size_w'),$("input[name='SFAvon-label_size_unit']"),$('#SFAvon-label_size_h')],true]])
                }
                if(!$("#SFAvon-label_barcode").val()){
                    msg.push("Task["+this.title+"]Please input the 'Bar Code No. & Type'.");
                    //changeColorList($("#SFAvon-label_barcode"))
                }
                if( $("input[name='SFAvon-label_color']:checked").length < 1 ){
                    msg.push("Task["+this.title+"]Please select the 'Print Color'.");
                    //changeColorList($("input[name='SFAvon-label_color']"))
                }else if($("input[name='SFAvon-label_color']:checked").val()=='Others' && !$('#SFAvon-label_color_other').val()){
                    msg.push("Task["+this.title+"]Please input the content for the 'Print: Other'.");
                    //changeColorList($('#SFAvon-label_color_other'))
                }
        	}
        }

        if( !$("#SFAvon-expected_date").val() ){
            //changeColorList($("#SFAvon-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }

        //jsonify the material info into the hidden field
		var jsonvals = new Array();
		$(".material_widget").each(function(){
		    if($(this).val()){
		        jsonvals.push($(this).attr("ref"));
		    }
		});
		$("#SFAvon-material_widgets").val("[" + jsonvals.join(",") + "]");
        return msg;
    }
}