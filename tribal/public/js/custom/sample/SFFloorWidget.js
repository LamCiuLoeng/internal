Namespace.register("SFNamespace.SFFloor");

var resetFloorField=function(){
    resetCheckToFields('input[name="SFFloor-dimension_type"]', 'detail', ['#SFFloor-dimension_w','#SFFloor-dimension_d','#SFFloor-dimension_h',
        'input[name="SFFloor-dimension_unit"]', 'input[name="SFFloor-dimension_as_sample"]', '#SFFloor-weight', '#SFFloor-weight_unit', 'input[name="SFFloor-weight_as_sample"]']);
    
    resetCheckToFields('input[name="SFFloor-dimension_type"]','option',['#SFFloor-dimension_type_option_text'])
    resetCheckToFields('input[name="SFFloor-pallet_size"]', 'full', ['input[name="SFFloor-full_pallet"]','#SFFloor-full_pallet_height_limit','input[name="SFFloor-full_pallet_height_limit_unit"]']);
    resetCheckToFields('input[name="SFFloor-pallet_size"]', 'half', ['input[name="SFFloor-half_pallet"]','#SFFloor-half_pallet_height_limit','input[name="SFFloor-half_pallet_height_limit_unit"]']);
    resetCheckToFields('input[name="SFFloor-pallet_size"]', 'pack', ['#SFFloor-display_pack_left', '#SFFloor-display_pack_front', '#SFFloor-display_pack_top']);
    resetCheckToFields('input[name="SFFloor-pallet_size"]', 'other', ['#SFFloor-other_size_w','#SFFloor-other_size_d','#SFFloor-other_size_h','input[name="SFFloor-other_size_unit"]']);
    resetCheckToFields('input[name="SFFloor-facing"]', 'other', '#SFFloor-facing_other');
    resetCheckToFields('#SFFloor-detail_type_header', '', ['#SFFloor-detail_height', 'input[name="SFFloor-detail_height_unit"]']);
    resetCheckToFields('#SFFloor-detail_type_hook', '', ['#SFFloor-detail_type_hook_qty',]);
    resetCheckToFields('#SFFloor-detail_type_other', '', '#SFFloor-detail_type_other_content');

}

SFNamespace.SFFloor.obj = {

    id   		 : "SFFloor",

    title        : "Floor/Pallet Display/Sidekick",

    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetFloorField();
        $('input[name="SFFloor-dimension_type"]').click(function(){
            resetFloorField()
        })

        $('input[name="SFFloor-pallet_size"]').click(function(){
            resetFloorField()
        })
        $('input[name="SFFloor-facing"]').click(function(){
            resetFloorField()
        })
        $('#SFFloor-detail_type_header').click(function(){
            resetFloorField()
        })
        $('#SFFloor-detail_type_hook').click(function(){
            resetFloorField()
        })
        $('#SFFloor-detail_type_other').click(function(){
            resetFloorField()
        })

        $("input[name='SFFloor-shipper_type1']").click(function(){
            $("input[name='SFFloor-shipper_type2']").removeAttr("checked");
        });
        $("input[name='SFFloor-shipper_type2']").click(function(){
            $("input[name='SFFloor-shipper_type1']").removeAttr("checked");
        });
        $("input[name*='as_sample']").click(function(){
            resetFloorField()
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

        if(!$("input[name='SFFloor-job_purpose']:checked").val() && !$("#SFFloor-presentation:checked").val()){
            changeColorList([[[$("input[name='SFFloor-job_purpose']"),$("#SFFloor-presentation")],true]])
            msg.push("Task["+this.title+"]Please select the 'Job Purpose'.");
        }
        if( $("input[name='SFFloor-dimension_type']:checked").length < 1){
            changeColorList([[[$("input[name='SFFloor-dimension_type']")],false]])
            msg.push("Task["+this.title+"]Please select the 'Product Details'.");
        }else if( $("input[name='SFFloor-dimension_type'][value='option']").attr("checked") ){
        	if(!$("#SFFloor-dimension_type_option_text").val()){
        		msg.push("Task["+this.title+"]Please input the 'Refer to Packaging Option'.");
        	}
        }else if($("input[name='SFFloor-dimension_type'][value='detail']").attr("checked")){
            if(!($('#SFFloor-dimension_w').val() && $('#SFFloor-dimension_d').val() && $('#SFFloor-dimension_h').val() && $("input[name='SFFloor-dimension_unit']:checked").val()) && !$("input[name='SFFloor-dimension_as_sample']:checked").val()){
                changeColorList([[[[$('#SFFloor-dimension_w'),$('#SFFloor-dimension_d'),$('#SFFloor-dimension_h'),$("input[name='SFFloor-dimension_unit']")],
                    $("input[name='SFFloor-dimension_as_sample'][value='Y']")
                    ],false]])
                msg.push("Task["+this.title+"]Please either input the size('W','D','H') and 'Unit' or select 'As Sample' for the 'Dimension'.");
            }
            if(!($('#SFFloor-weight').val() && $("#SFFloor-weight_unit").val()) && !$("input[name='SFFloor-weight_as_sample']:checked").val() ){
                changeColorList([[[[$('#SFFloor-weight'),$("#SFFloor-weight_unit")],
                    $("input[name='SFFloor-weight_as_sample'][value='Y']")
                    ],false]])
                msg.push("Task["+this.title+"]Please select the 'Unit' or 'As Sample' for the 'Weight'.");
            }
        }
        
        
        if($(".material_widget[value!='']").length < 1){
            msg.push("Task["+this.title+"]Please add the 'Material'.");
        }
        
        if(!$("input[name='SFFloor-pallet_size']:checked").val()){
            changeColorList($("input[name='SFFloor-pallet_size']"))
            msg.push("Task["+this.title+"]Please select the 'Pallet Size'.");
        }else if($("input[name='SFFloor-pallet_size']:checked").val() == 'full'){
            if(!$("input[name='SFFloor-full_pallet']:checked").val()){
                changeColorList($("input[name='SFFloor-full_pallet']"))
                msg.push("Task["+this.title+"]Please select the option for the 'Full Pallet'.");
            }
        }else if($("input[name='SFFloor-pallet_size']:checked").val() == 'half'){
            if(!$("input[name='SFFloor-half_pallet']:checked").val()){
                changeColorList($("input[name='SFFloor-half_pallet']"))
                msg.push("Task["+this.title+"]Please select the option for the 'Half Pallet'.");
            }
        }else if($("input[name='SFFloor-pallet_size']:checked").val() == 'pack'){
            if( !$("#SFFloor-display_pack_left").val() || !$("#SFFloor-display_pack_front").val() || !$("#SFFloor-display_pack_top").val() ){
                changeColorList([[[$("#SFFloor-display_pack_left"),$("#SFFloor-display_pack_front"),$("#SFFloor-display_pack_top")],false]])
                msg.push("Task["+this.title+"]Please input the pcs if select the 'Display size according to pack count'.");
            }
        }else if($("input[name='SFFloor-pallet_size']:checked").val() == 'other'){
            if(!$("#SFFloor-other_size_w").val() || !$("#SFFloor-other_size_d").val() || !$("#SFFloor-other_size_h").val() || !$("input[name='SFFloor-other_size_unit']:checked").val()){
                changeColorList([[[$("#SFFloor-other_size_w"),$("#SFFloor-other_size_d"),$("#SFFloor-other_size_h"),$("input[name='SFFloor-other_size_unit']")],true]])
                msg.push("Task["+this.title+"]Please input the size('Width', 'Depth', 'Height') and 'unit' if select 'Other specified size'.");
            }
        }

        if($('#SFFloor-front_lip_height').val() && !$("input[name='SFFloor-front_lip_unit']:checked").val()){
            changeColorList($("input[name='SFFloor-front_lip_unit']"))
            msg.push("Task["+this.title+"]Please select the 'Unit' for the 'Front lip height'.");
        }
        if(!$("#SFFloor-shelves_left").val() || !$("#SFFloor-shelves_top").val()){
            changeColorList([[[$("#SFFloor-shelves_left"),$("#SFFloor-shelves_top")],true]])
            msg.push("Task["+this.title+"]Please input the 'No. of shelves'.");
        }

        if( $("input[name='SFFloor-style']:checked").length < 1 ){
            changeColorList($("input[name='SFFloor-style']"))
            msg.push("Task["+this.title+"]Please select the 'Style'.");
        }

        if( $("input[name='SFFloor-facing']:checked").length < 1 ){
            changeColorList($("input[name='SFFloor-facing']"))
            msg.push("Task["+this.title+"]Please select the 'Facing'.");
        }
        else if($("input[name='SFFloor-facing']:checked").val()=='other' && !$('#SFFloor-facing_other').val()){
            changeColorList($('#SFFloor-facing_other'))
            msg.push("Task["+this.title+"]Please input the content if select the 'Facing: Others'.");
        }
        if( $("input[name='SFFloor-detail_type']:checked").length < 1 ){
            changeColorList($("input[name='SFFloor-detail_type']"))
            msg.push("Task["+this.title+"]Please select the 'Details'.");
        }
        else{
            if($("#SFFloor-detail_type_header").attr('checked')==true && !($('#SFFloor-detail_height').val() && $("input[name='SFFloor-detail_height_unit']:checked").val())){
                changeColorList([[[$('#SFFloor-detail_height'),$("input[name='SFFloor-detail_height_unit']")],true]])
                msg.push("Task["+this.title+"]Please input 'height' and 'unit' if select 'Details: Header'.");
            }
            else if($("#SFFloor-detail_type_other").attr('checked')==true && !$('#SFFloor-detail_type_other_content').val()){
                changeColorList($('#SFFloor-detail_type_other_content'))
                msg.push("Task["+this.title+"]Please input the content if select 'Details: Other'.");
            }
            else if($("#SFFloor-detail_type_hook").attr('checked')==true && !$('#SFFloor-detail_type_hook_qty').val()){
                changeColorList($('#SFFloor-detail_type_hook_qty'));
                msg.push("Task["+this.title+"]Please input the pcs if select 'Details: Hook(s)/Peg(s)'.");
            }
        }
        
        if( $("input[name='SFFloor-shipper_type1']:checked").length < 1 &&  $("input[name='SFFloor-shipper_type2']:checked").length < 1){
            changeColorList($("input[name='SFFloor-shipper_type2']"))
            msg.push("Task["+this.title+"]Please select the 'Shipper '.");
        }
        if( $("input[name='SFFloor-transit']:checked").length < 1 ){
            changeColorList($("input[name='SFFloor-transit']"))
            msg.push("Task["+this.title+"]Please select the 'Transit'.");
        }

        if( !$("#SFFloor-expected_date").val() ){
            changeColorList($("#SFFloor-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        
        
        //jsonify the material info into the hidden field
		var jsonvals = new Array();
		$(".material_widget").each(function(){
		    if($(this).val()){
		        jsonvals.push($(this).attr("ref"));
		    }
		});
		$("#SFFloor-material_widgets").val("[" + jsonvals.join(",") + "]");
        
        return msg;
    }
}
