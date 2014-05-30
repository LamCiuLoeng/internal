Namespace.register("SFNamespace.SFBestBuy");

var resetBestbuyField=function(){
    resetCheckToFields('#SFBestBuy-submit_items_other_type', '', '#SFBestBuy-submit_items_other');
    resetCheckToFields('#SFBestBuy-material_type_window_type', '', [
        '#SFBestBuy-window_size_w',
        '#SFBestBuy-window_size_d',
        'input[name="SFBestBuy-window_size_unit"]',
        ]);
    resetCheckToFields('#SFBestBuy-material_type_other_type', '', '#SFBestBuy-material_other');
    //resetCheckToFields('#SFBestBuy-job_type_sampling_type', '', '#SFBestBuy-job_type_sampling');
    //resetCheckToFields('#SFBestBuy-job_type_printout_type', '', '#SFBestBuy-job_type_printout');
    //resetCheckToFields('#SFBestBuy-job_type_other_type', '', '#SFBestBuy-job_type_other');
    //resetAsSampleToFields('input[name="SFBestBuy-size_as_sample"]', ['#SFBestBuy-size_w', '#SFBestBuy-size_d', '#SFBestBuy-size_h', 'input[name="SFBestBuy-size_unit"]', 'input[name="SFBestBuy-size_type"]'])
    //resetAsSampleToFields('input[name="SFBestBuy-weight_as_sample"]', ['#SFBestBuy-weight', 'input[name="SFBestBuy-weight_unit"]'])
   // resetAsSampleToFields('input[name="SFBestBuy-material_as_sample"]', '#SFBestBuy-material')
}

SFNamespace.SFBestBuy.obj = {

    id   		 : "SFBestBuy",
	
    title        : "Best Buy",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetBestbuyField();
        $("#SFBestBuy-submit_items_other_type").click(function(){
            resetBestbuyField()
        })
        $("#SFBestBuy-material_type_window_type").click(function(){
            resetBestbuyField()
        })
        $("#SFBestBuy-material_type_other_type").click(function(){
            resetBestbuyField()
        })
        
        /*
        $("#SFBestBuy-job_type_sampling_type").click(function(){
            resetBestbuyField()
        })
        $("#SFBestBuy-job_type_printout_type").click(function(){
            resetBestbuyField()
        })
        $("#SFBestBuy-job_type_other_type").click(function(){
            resetBestbuyField()
        })
        */
        
        $("input[name*='as_sample']").click(function(){
            resetBestbuyField()
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
        
        if( $("input[name='SFBestBuy-job_presentation']:checked").length < 1 && $("input[name='SFBestBuy-job_purpose']:checked").length < 1){
            changeColorList([[[$("input[name='SFBestBuy-job_presentation']"),$("input[name='SFBestBuy-job_purpose']")],true]])
            msg.push("Task["+this.title+"]Please select the 'Job Purpose'.");
        }
        
        if( $("input[name='SFBestBuy-submit_items']:checked").length < 1 ){
            changeColorList($("input[name='SFBestBuy-submit_items']"))
            msg.push("Task["+this.title+"]Please select the 'Submitted Items'.");
        }
        else if( $("#SFBestBuy-submit_items_other_type").attr("checked") && !$("#SFBestBuy-submit_items_other").val() ){
            changeColorList($("#SFBestBuy-submit_items_other"))
            msg.push("Task["+this.title+"]Please input the content if select 'Submitted Items : Others'.");
        }

        //        if( $("input[name='SFBestBuy-size_type']:checked").length < 1 ){
        //            changeColorList($("input[name='SFBestBuy-size_type']"))
        //            msg.push("Tab["+this.title+"]Please either input the contents and select the 'Unit' for the 'Product Size' or select 'As Sample'.");
        //        }
        //        else if(!$("input[name='SFBestBuy-size_as_sample']:checked").val()
        //            && !($('#SFBestBuy-size_w').val() && $('#SFBestBuy-size_d').val() && $('#SFBestBuy-size_h').val() && $("input[name='SFBestBuy-size_unit']:checked").val()
        //                && ($("input[name='SFBestBuy-size_type']:checked").val()=='Product' || $("input[name='SFBestBuy-size_type']:checked").val()=='Packaging'))){
        //            changeColorList([[[$('#SFBestBuy-size_w'),$('#SFBestBuy-size_d'),$('#SFBestBuy-size_h'),$("input[name='SFBestBuy-size_unit']")],true]])
        //            changeColorList([[[$("input[name='SFBestBuy-size_type']"),$("input[name='SFBestBuy-size_type']")],false]])
        //            msg.push("Tab["+this.title+"]Please either input the size('W','D','H') and 'Unit' and select 'Product Size/Packaging Size' or select 'As Sample'.");
        //        }
        if(!$("input[name='SFBestBuy-size_as_sample']:checked").val()){
            if( $("input[name='SFBestBuy-size_type']:checked").length < 1 ){
                changeColorList([[[[
                                    $('#SFBestBuy-size_w'),
                                    $("input[name='SFBestBuy-size_unit']"),
                                    $("input[name='SFBestBuy-size_type']"),
                                    $('#SFBestBuy-size_d'),
                                   $('#SFBestBuy-size_h')
                                   ],$("input[name='SFBestBuy-size_as_sample']")
                                   ],false]])
                                   
                msg.push("Task["+this.title+"]Please either input the contents and select the 'Unit' for the 'Product Size' or select 'As Sample'.");
            }else if(!($('#SFBestBuy-size_w').val() && $('#SFBestBuy-size_d').val() && $('#SFBestBuy-size_h').val() && $("input[name='SFBestBuy-size_unit']:checked").val())){
                
                msg.push("Task["+this.title+"]Please either input the size('W','D','H') and 'Unit' and select 'Product Size/Packaging Size' or select 'As Sample'.");
            }
        }
        
        if(!$("input[name='SFBestBuy-weight_as_sample']:checked").val() && !($('#SFBestBuy-weight').val() && $("#SFBestBuy-weight_unit").val())){
        	changeColorList([[[[$('#SFBestBuy-weight'),$("#SFBestBuy-weight_unit")],$("input[name='SFBestBuy-weight_as_sample']")
                               ],false]])
            msg.push("Task["+this.title+"]Please select the 'Unit' for the 'Packaging Weight' or select 'As Sample'.");
        }
        if(!($('#SFBestBuy-material').val() || $("input[name='SFBestBuy-material_as_sample']:checked").val())){
            changeColorList([[[[$('#SFBestBuy-material')],$("input[name='SFBestBuy-material_as_sample']")
                               ],false]])
            msg.push("Task["+this.title+"]Please either input the 'Packaging Material' or select 'As Sample'.");
        }
        if( $("input[name='SFBestBuy-material_type']:checked").length < 1 ){
            changeColorList($("input[name='SFBestBuy-material_type']"))
            msg.push("Task["+this.title+"]Please select the 'Packaging Style'.");
        }
        else{
            if( $("#SFBestBuy-material_type_other_type").attr("checked") && !$("#SFBestBuy-material_other").val() ){
                changeColorList($("#SFBestBuy-material_other"))
                msg.push("Task["+this.title+"]Please input the content if select 'Packaging Style : Other'.");
            }
            if( $("#SFBestBuy-material_type_window_type").attr("checked")
                && !($('#SFBestBuy-window_size_w').val() && $('#SFBestBuy-window_size_d').val() && $("input[name='SFBestBuy-window_size_unit']:checked").val())
                && ($('#SFBestBuy-window_size_w').val() || $('#SFBestBuy-window_size_d').val() || $("input[name='SFBestBuy-window_size_unit']:checked").val())){
                changeColorList([[[$('#SFBestBuy-window_size_w'), $('#SFBestBuy-window_size_d'),$("input[name='SFBestBuy-window_size_unit']")],true]])
                msg.push("Task["+this.title+"]Please complete input the size('W','D') and 'Unit' for the 'Packaging Style : Window Box'.");
            }
        }

        /*
        if( $("input[name='SFBestBuy-job_type']:checked").length < 1 ){
            changeColorList($("input[name='SFBestBuy-job_type']"))
            msg.push("Task["+this.title+"]Please select the 'Job type'.");
        }        
        else{
            if( $("#SFBestBuy-job_type_sampling_type").attr("checked") && !$("#SFBestBuy-job_type_sampling").val() ){
                changeColorList($("#SFBestBuy-job_type_sampling"))
                msg.push("Task["+this.title+"]Please input the pcs content if select 'Job type : Sampling'.");
            }
            if( $("#SFBestBuy-job_type_printout_type").attr("checked") && !$("#SFBestBuy-job_type_printout").val() ){
                changeColorList($("#SFBestBuy-job_type_printout"))
                msg.push("Task["+this.title+"]Please input the pcs content if select 'Job type : Printout'.");
            }
            if( $("#SFBestBuy-job_type_other_type").attr("checked") && !$("#SFBestBuy-job_type_other").val() ){
                changeColorList($("#SFBestBuy-job_type_other"))
                msg.push("Task["+this.title+"]Please input the content if select 'Job type : Others'.");
            }
        }
        */

        if( !$("#SFBestBuy-expected_date").val() ){
            changeColorList($("#SFBestBuy-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }

        //        if( $("input[name='SFBestBuy-size_type'][value='Product']").attr("checked") || $("input[name='SFBestBuy-size_type'][value='Packaging']") ){
        //            if( !$("#SFBestBuy-size_w").val() || !$("#SFBestBuy-size_h").val() || !$("#SFBestBuy-size_d").val() ){
        //                msg.push("Tab["+this.title+"]Please input the 'Product Size' if select the 'Product Size/Packaging Size'.");
        //            }
        //        }
        //        if( !$("#SFBestBuy-size_w").val() || !$("#SFBestBuy-size_d").val() || !$("#SFBestBuy-size_h").val()){
        //            msg.push("Tab["+this.title+"]Please input the whole 'Size' info.");
        //        }
        //        if(($('#SFBestBuy-window_size_w').val() || $('#SFBestBuy-window_size_d').val()) &&
        //            !($('#SFBestBuy-window_size_w').val() && $('#SFBestBuy-window_size_d').val() && $("input[name='SFBestBuy-window_size_unit']:checked").val()))
        //            msg.push("Tab["+this.title+"]Please input the size('W','D') and 'Unit'.");
        //        if( !$("#SFBestBuy-material").val()){
        //            msg.push("Tab["+this.title+"]Please input the 'Material'.");
        //        }
        
        if( $("input[name='SFBestBuy-requirement']:checked").length < 1 ){
            changeColorList($("input[name='SFBestBuy-requirement']"))
            msg.push("Task["+this.title+"]Please select the 'Requirements'.");
        }
        
        
        return msg;
    }
}
