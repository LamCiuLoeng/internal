Namespace.register("SFNamespace.SFGeneral");

var resetGeneralField=function(){

    resetCheckToFields('#SFGeneral-submit_item_other_type', '', '#SFGeneral-submit_item_other');
    resetCheckToFields('#SFGeneral-item_type_other_cb', '', '#SFGeneral-item_type_other');
    /*
    resetCheckToFields('input[name="SFGeneral-material_type"]', 'folding_cards', [
        'input[name="SFGeneral-folding_cards_type"]',
        '#SFGeneral-folding_cards_other',
        'input[name="SFGeneral-paper_thickness_type"]',
        '#SFGeneral-paper_thickness',
        'input[name="SFGeneral-paper_thickness_unit"]',
        '#SFGeneral-gramage_gsm'
        ]);
    resetCheckToFields('input[name="SFGeneral-material_type"]', 'corrugated', [
        '#SFGeneral-flute',
        'input[name="SFGeneral-flute_type"]',
        '#SFGeneral-bursting',
        '#SFGeneral-ect',
        '#SFGeneral-gramage',
        '#SFGeneral-flute_type_gsm'
        ]);
    resetCheckToFields('input[name="SFGeneral-material_type"]', 'other', '#SFGeneral-material_type_other_content');
    */
	//resetAsSampleToFields('input[name="SFGeneral-size_as_sample"]', ['#SFGeneral-size_w', '#SFGeneral-size_d', '#SFGeneral-size_h', 'input[name="SFGeneral-size_unit"]', 'input[name="SFGeneral-size_type"]'])
	//resetAsSampleToFields('input[name="SFGeneral-weight_as_sample"]', ['#SFGeneral-weight', 'input[name="SFGeneral-weight_unit"]'])
}

SFNamespace.SFGeneral.obj = {

    id   		 : "SFGeneral",
	
    title        : "General packaging design",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        validators.push(this);
        resetGeneralField();
        $('#SFGeneral-submit_item_other_type').click(function(){
            resetGeneralField()
        })
        $('#SFGeneral-item_type_other_cb').click(function(){
            resetGeneralField()
        })
        /*
        $('input[name="SFGeneral-material_type"]').click(function(){
            resetGeneralField()
        });
        */
        $("input[name*='as_sample']").click(function(){
            resetGeneralField()
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
        if( $("input[name='SFGeneral-job_presentation']:checked").length < 1 && $("input[name='SFGeneral-job_purpose']:checked").length < 1){
        	changeColorList([[[$("input[name='SFGeneral-job_presentation']"),$("input[name='SFGeneral-job_purpose']")],true]])
            msg.push("Task["+this.title+"]Please select the 'Job Purpose'.");
        }
        /*
        if(!$("input[name='SFGeneral-material_type']:checked").val()){
            changeColorList($("input[name='SFGeneral-material_type']"))
            msg.push("Task["+this.title+"]Please select the 'Material'.");
        }
        else if($("input[name='SFGeneral-material_type']:checked").val()=='folding_cards'){
            if(!$("input[name='SFGeneral-folding_cards_type']:checked").val()){
                changeColorList($("input[name='SFGeneral-folding_cards_type']"))
                msg.push("Task["+this.title+"]Please select the option for the 'Folding Cards'.");
            }
            else if($("input[name='SFGeneral-folding_cards_type']:checked").val()=='Other' && !$('#SFGeneral-folding_cards_other').val()){
                changeColorList($('#SFGeneral-folding_cards_other'))
                msg.push("Task["+this.title+"]Please input the content if select the 'Folding Cards: Other'.");
            }
            if($("input[name='SFGeneral-paper_thickness_type']:checked").val()=='other' && !($('#SFGeneral-paper_thickness').val() && $("input[name='SFGeneral-paper_thickness_unit']:checked").val()) ){
                changeColorList([[[$('#SFGeneral-paper_thickness'), $("input[name='SFGeneral-paper_thickness_unit']")],true]])
                msg.push("Task["+this.title+"]Please input the content and select 'Unit' if select the 'Paper thickness'.");
            }
            if($("input[name='SFGeneral-paper_thickness_type']:checked").val()=='gramage' && !$('#SFGeneral-gramage_gsm').val()){
                changeColorList($('#SFGeneral-gramage_gsm'))
                msg.push("Task["+this.title+"]Please input the content if select the 'Grammage'.");
            }
        }else if($("input[name='SFGeneral-material_type']:checked").val()=='corrugated'){
            if(!$("input[name='SFGeneral-flute_type']:checked").val()||!$('#SFGeneral-flute').val()){
                changeColorList([[[$("input[name='SFGeneral-flute_type']"), $('#SFGeneral-flute')],false]])
                msg.push("Task["+this.title+"]Please input the content and select 'flut type' for the 'Corrugated'.");
            }
        }else if($("input[name='SFGeneral-material_type']:checked").val()=='other'){
            if(!$('#SFGeneral-material_type_other_content').val()){
                changeColorList($('#SFGeneral-material_type_other_content'))
                msg.push("Task["+this.title+"]Please input the content if select 'Material: Other'.");
            }
        }
        */

        if($(".material_widget[value!='']").length < 1){
            msg.push("Task["+this.title+"]Please add the 'Material'.");
        }

        if( $("input[name='SFGeneral-submit_item']:checked").length < 1 ){
            changeColorList($("input[name='SFGeneral-submit_item']"))
            msg.push("Task["+this.title+"]Please select the 'Submitted Items'.");
        }
        else if( $("#SFGeneral-submit_item_other_type").attr("checked") && !$("#SFGeneral-submit_item_other").val() ){
            changeColorList($("#SFGeneral-submit_item_other"))
            msg.push("Task["+this.title+"]Please input the content if select the 'Submitted Items: Others'.");
        }
        if(!$("input[name='SFGeneral-size_as_sample']:checked").val()
            && !($("#SFGeneral-size_w").val() && $("#SFGeneral-size_d").val() && $("#SFGeneral-size_h").val() && $("input[name='SFGeneral-size_unit']:checked").val() && $("input[name='SFGeneral-size_type']:checked").val())
            ){
            msg.push("Task["+this.title+"]Please either input the 'Size' and 'Unit' and 'Size Type' or select 'As Sample' for the 'Product Details: Size'.");
            changeColorList([[[[$("#SFGeneral-size_w"), $("#SFGeneral-size_d"),$("#SFGeneral-size_h"),$("input[name='SFGeneral-size_unit']"),$("input[name='SFGeneral-size_type']")],
                $("input[name='SFGeneral-size_as_sample']")
                ],false]])
        }
        if(!$("input[name='SFGeneral-weight_as_sample']:checked").val() && (
            !($('#SFGeneral-weight').val() && $("#SFGeneral-weight_unit").val())
            )){
            msg.push("Task["+this.title+"]Please either input content and select 'Unit' or select 'As Sample' for the 'Packaging Weight'.");
            changeColorList([[[[$('#SFGeneral-weight'), $("#SFGeneral-weight_unit")],
                $("input[name='SFGeneral-weight_as_sample']")
                ],false]])
        }
        if( $("input[name='SFGeneral-item_type']:checked").length < 1 ){
            changeColorList($("input[name='SFGeneral-item_type']"))
            msg.push("Task["+this.title+"]Please select the 'Packaging Style'.");
        }
        else if( $("#SFGeneral-item_type_other_cb").attr("checked") && !$("#SFGeneral-item_type_other").val() ){
            changeColorList($("#SFGeneral-item_type_other"))
            msg.push("Task["+this.title+"]Please input the content if select the 'Packaging Style: Others'.");
        }
        //}
        //        if( $("input[name='SFGeneral-material_type'][value='provided']:checked").length==1 && !$("#SFGeneral-material_type_content").val() )
        //            msg.push("Tab["+this.title+"]Please input the content if select the 'Material : Material provided'.");
        //
        if( !$("#SFGeneral-expected_date").val() ){
            changeColorList($("#SFGeneral-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        
        
        //jsonify the material info into the hidden field
		var jsonvals = new Array();
		$(".material_widget").each(function(){
		    if($(this).val()){
		        jsonvals.push($(this).attr("ref"));
		    }
		});
		$("#SFGeneral-material_widgets").val("[" + jsonvals.join(",") + "]");
        
        return msg;
    }
}
