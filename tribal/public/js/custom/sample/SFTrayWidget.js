Namespace.register("SFNamespace.SFTray");


SFNamespace.SFTray.obj = {

    id   		 : "SFTray",
	
    title        : "Tray Design",
	
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
        if( !$("#SFTray-expected_date").val() ){
            changeColorList($("#SFTray-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        if( $("input[name='SFTray-job_purpose']:checked").length < 1 &&  !$("input[name='SFTray-presentation']:checked").val()){
            msg.push("Task["+this.title+"]Please select the 'Job Purpose'");
            changeColorList([[[$("input[name='SFTray-job_purpose']"),$("input[name='SFTray-presentation']")],true]])
        }

        if( !$("input[name='SFTray-product_dimension_type']:checked").val() ){
            changeColorList($("input[name='SFTray-product_dimension_type']"))
            msg.push("Task["+this.title+"]Please select the 'Size'.");
        }
   
        if($(".material_widget[value!='']").length < 1){
            msg.push("Task["+this.title+"]Please add the 'Material'.");
        }
        
        
        if( !$("input[name='SFTray-stackable']:checked").val() ){
            msg.push("Task["+this.title+"]Please select the 'Stackable'.");
            changeColorList($("input[name='SFTray-stackable']"))
        }
        if( !$("input[name='SFTray-style']:checked").val() ){
            msg.push("Task["+this.title+"]Please select the 'Style'.");
            changeColorList($("input[name='SFTray-style']"))
        }
        if( !$("input[name='SFTray-shipper']:checked").val() ){
            msg.push("Task["+this.title+"]Please select the 'Shipper'.");
            changeColorList($("input[name='SFTray-shipper']"))
        }
        
        if($("#SFTray-product_dimension_type_option").attr("checked")&& !$("#SFTray-product_dimension_option_text").val()){
        	msg.push("Task["+this.title+"]Please input the 'Packaging Option'.");
        }
        
        if ($("#SFTray-product_dimension_type_detail").attr("checked") 
            &&!( (
                (
                    $("#SFTray-product_dimension_w").val()
                    && $("#SFTray-product_dimension_d").val()
                    && $("#SFTray-product_dimension_h").val()
                    && $("input[name='SFTray-product_dimension_unit']:checked").val()
                    )
                || $("input[name='SFTray-product_dimension_as_sample']:checked").length>=1
                )&&
            (
                (
                    $("#SFTray-weight").val()
                    && $("#SFTray-weight_unit").val()
                    )
                || $("input[name='SFTray-product_weight_as_sample']:checked").length>=1
                )
            )
        	  
            ){
            changeColorList([[[[$("#SFTray-product_dimension_w"),$("#SFTray-product_dimension_d"),$("#SFTray-product_dimension_h"),$("input[name='SFTray-product_dimension_unit']")]
                ,$("input[name='SFTray-product_dimension_as_sample'][value='Y']")
                ],false]])
            changeColorList([[[[$("#SFTray-weight"),$("#SFTray-weight_unit")],$("input[name='SFTray-product_weight_as_sample'][value='Y']")
                ],false]])
            msg.push("Task["+this.title+"]Please input the size with unit or 'As Sample' when selecting the Product in 'Size'.");
        }
        if (($("#SFTray-product_dimension_type_pack").attr("checked"))
            &&!(
                $("#SFTray-tray_pack_left").val()
                &&
                $("#SFTray-tray_pack_front").val()
                &&
                $("#SFTray-tray_pack_top").val()
                )
            ){
            changeColorList([[[$("#SFTray-tray_pack_left"),$("#SFTray-tray_pack_front"),$("#SFTray-tray_pack_top")],true]])
            msg.push("Task["+this.title+"]Please input the Pack Count when 'Product Dimension' or 'Size according to the new design with this request' was selected.");
        }

        if ( $("#SFTray-product_dimension_type_specified").attr("checked") && !( $("#SFTray-tray_dimension_w").val() && $("#SFTray-tray_dimension_d").val()&& $("#SFTray-tray_dimension_bh").val() && $("#SFTray-tray_dimension_fh").val() && $("input[name='SFTray-tray_size_unit']:checked").val() )){
        	changeColorList([[[$("#SFTray-tray_dimension_w"),$("#SFTray-tray_dimension_d"),$("#SFTray-tray_dimension_bh"),$("#SFTray-tray_dimension_fh"),$("input[name='SFTray-tray_size_unit']")],true]])
            msg.push("Task["+this.title+"]Please input the size with unit if 'Specified Tray Size' was selected.");
        }
        if ( $("#SFTray-product_dimension_type_specified").attr("checked") && !$("input[name='SFTray-box_size']:checked").val()){
        	changeColorList([[[$("input[name='SFTray-box_size']")],true]])
            msg.push("Task["+this.title+"]Please choose dimension type if 'Specified Tray Size' was selected.");
        }
        if ( $("#SFTray-detail_Dividers").attr("checked") && !$("#SFTray-tray_detail_pcs").val()){
            changeColorList($("#SFTray-tray_detail_pcs"))
            msg.push("Task["+this.title+"]Please input the 'pcs' when selecting the 'Dividers' in 'Tray Style'.");
        }
        if ( $("#SFTray-detail_hook").attr("checked") && !$("#SFTray-tray_detail_hook_qty").val()){
            changeColorList($("#SFTray-tray_detail_hook_qty"))
            msg.push("Task["+this.title+"]Please input the 'pcs' when selecting the 'Hook(s)/Peg(s)' in 'Tray Style'.");
        }
        
        if ( $("#SFTray-detail_Thick").attr("checked") && !$("#SFTray-tray_detail_thickness").val()){
            changeColorList($("#SFTray-tray_detail_thickness"))
            msg.push("Task["+this.title+"]Please input the 'thickness' when selecting the 'Thick side wall' in 'Tray Style'.");
        }
        if ( $("#SFTray-detail_Thick").attr("checked") && $("input[name='SFTray-tray_detail_thickness_unit']:checked").length<1){
            changeColorList($("input[name='SFTray-tray_detail_thickness_unit']"))
            msg.push("Task["+this.title+"]Please select the 'unit' when selecting the 'Thick side wall' in 'Tray Style'.");
        }

        
        
        if( $("input[name='SFTray-shipper'][value='Other']:checked").length == 1 && !$("#SFTray-shipper_other_content").val()){
            changeColorList($("#SFTray-shipper_other_content"))
            msg.push("Task["+this.title+"]Please input the content when selecting the 'Others ' in 'Shipper'.");
        }
        if ($("input[name='SFTray-product_tray_size']:checked").length<1){
            changeColorList($("input[name='SFTray-product_tray_size']"))
            msg.push("Task["+this.title+"]Please select the 'Tray Size'.");
        }        
        
        var tmp =  $("input[name='SFTray-shipper']:checked").val();
        if( (tmp == 'HSC' || tmp == 'RSC' || tmp =='FOL') && $("input[name='SFTray-shipper_loading']:checked").length <1  ){
            changeColorList($("input[name='SFTray-shipper_loading']"));
            msg.push("Task["+this.title+"]Please also select the 'Shipper Loading' where the HSC/RSC/FOL is selected.");
        }
        
        
        //jsonify the material info into the hidden field
		var jsonvals = new Array();
		$(".material_widget").each(function(){
		    if($(this).val()){
		        jsonvals.push($(this).attr("ref"));
		    }
		});
		$("#SFTray-material_widgets").val("[" + jsonvals.join(",") + "]");
        
        return msg;
    }
}
var changeImg = function(){
    if($("input[name='SFTray-style']:checked").length=1){
        var objs = $("input[name='SFTray-style']:checked").val()
        var imgPaths
        if(objs == 'Flat'){
            imgPaths = "/images/pei.jpg";
        }else if(objs == 'PDQ'){
            imgPaths = "/images/bby_mockup.jpg";
        }
        $("#changeImg").html("<img src="+imgPaths+">");
    }
}
