Namespace.register("SFNamespace.SFContainer");

var resetContainerField=function(){
    resetCheckToFields('input[name="SFContainer-size_according"]', 'out', ['#SFContainer-outer_w','#SFContainer-outer_d','#SFContainer-outer_h','input[name="SFContainer-outer_unit"]','input[name="SFContainer-outer_as_sample"]']);
    resetCheckToFields('input[name="SFContainer-pallet"]', 'with', ['#SFContainer-pallet_w','#SFContainer-pallet_d','#SFContainer-pallet_h','input[name="SFContainer-pallet_unit"]']);
    resetCheckToFields('#SFContainer-info_other_type', '', '#SFContainer-info_other');
//resetAsSampleToFields('input[name="SFContainer-weight_as_sample"]', ['#SFContainer-weight', 'input[name="SFContainer-weight_unit"]'])
//resetAsSampleToFields('input[name="SFContainer-outer_as_sample"]', ['#SFContainer-outer_w', '#SFContainer-outer_d', '#SFContainer-outer_h', 'input[name="SFContainer-outer_unit"]'])
}

SFNamespace.SFContainer.obj = {

    id   		 : "SFContainer",
	
    title        : "Container Loading",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetContainerField();
        $("input[name='SFContainer-size_according']").click(function(){
            resetContainerField()
        })
        $("input[name='SFContainer-pallet']").click(function(){
            resetContainerField()
        })
        $("#SFContainer-info_other_type").click(function(){
            resetContainerField()
        })
        $("input[name*='as_sample']").click(function(){
            resetContainerField()
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
        /*
						if( !$("input[name='SFContainer-weight_unit']:checked").val() ){
							msg.push("Tab["+this.title+"]Please select the 'unit' for the 'Weight'.");
						}
						if( !$("input[name='SFContainer-pallet']:checked").val() ){
                            msg.push("Tab["+this.title+"]Please select the 'Pallet'.");
                        }
						if( !$("#SFContainer-size_according").attr("checked") ){
							var allFill = true;
							$("input[name^='SFContainer-outer']").each(function(){
								if( !$(this).val() ){ allFill = false; }
							});
							if( !allFill ){ msg.push("Tab["+this.title+"]Please fill in all the fields for 'Overall outer size'."); }
							
							if( !$("input[name='SFContainer-weight_unit']:checked").val() ){ 
								msg.push("Tab["+this.title+"]Please select the 'unit' for the 'Overall outer size'."); 
							}
						}
                        if( !$("#SFContainer-size_according").attr("checked") && (!$("#SFContainer-outer_w").val()||!$("#SFContainer-outer_d").val()||!$("#SFContainer-outer_h").val()) ){
                            msg.push("Tab["+this.title+"]Please select either 'Overall outer siz' or 'Size according'.");
                        }

                        if( !$("input[name='SFContainer-orientation']:checked").val() )
                            msg.push("Tab["+this.title+"]Please select the 'Product Orientation'.");

            */
        if($("#SFContainer-weight").val()&&!($("#SFContainer-weight_unit").val())){
            changeColorList($("#SFContainer-weight_unit"))
            msg.push("Task["+this.title+"]Please select the 'unit' for the 'Weight'.");
        }

        if(!$("input[name='SFContainer-size_according']:checked").val()){
            changeColorList($("input[name='SFContainer-size_according']"))
            msg.push("Task["+this.title+"]Please select the 'Loading Info : size'.");
        }else if($("input[name='SFContainer-size_according']:checked").val()=='out'){
            if(!$('input[name="SFContainer-outer_as_sample"]:checked').val() && !($("#SFContainer-outer_w").val() && $("#SFContainer-outer_d").val() && $("#SFContainer-outer_h").val() && $("input[name='SFContainer-outer_unit']:checked").val())){
                msg.push("Task["+this.title+"]Please either input the size('W','D','H') and 'Unit' or select 'As Sample' if select 'Overall outer size'.");
                changeColorList([[[[$("#SFContainer-outer_w"),$("#SFContainer-outer_d"),$("#SFContainer-outer_h"),$("input[name='SFContainer-outer_unit']"),$("input[name='SFContainer-size_according']")],$("input[name='SFContainer-outer_as_sample']")
                    ],false]])
            }
        }
        if(!$("input[name='SFContainer-pallet']:checked").val())
        {
            changeColorList($("input[name='SFContainer-pallet']"))
            msg.push("Task["+this.title+"]Please select the 'Pallet'.");
        }
        else if( $("input[name='SFContainer-pallet']:checked").val()=='with'
            && !($('#SFContainer-pallet_w').val()&&$('#SFContainer-pallet_d').val()&&$('#SFContainer-pallet_h').val()&&$("input[name='SFContainer-pallet_unit']:checked").val()))
            {
            changeColorList([[[$('#SFContainer-pallet_w'),$('#SFContainer-pallet_d'),$('#SFContainer-pallet_h'),$("input[name='SFContainer-pallet_unit']")],true]])
            msg.push("Task["+this.title+"]Please input the size('W','D','H') and 'Unit' if select 'with pallet'.");
        }

        if(!$("input[name='SFContainer-orientation']:checked").val())
        {
            changeColorList($("input[name='SFContainer-orientation']"))
            msg.push("Task["+this.title+"]Please select the 'Product Orientation'.");
        }

        if( !$("input[name='SFContainer-info']:checked").val() )
        {
            changeColorList($("input[name='SFContainer-info']"))
            msg.push("Task["+this.title+"]Please select the 'Container Info'.");
        }
        else if($('#SFContainer-info_other_type:checked').val() && !$('#SFContainer-info_other').val())
        {
            changeColorList($('#SFContainer-info_other'))
            msg.push("Task["+this.title+"]Please input the content if select 'Container Info : Others'.");
        }
        
        if( !$("#SFContainer-expected_date").val() )
        {
            changeColorList($("#SFContainer-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }

        return msg;
    }
}
