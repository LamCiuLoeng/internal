Namespace.register("SFNamespace.SFBox");

var resetBoxField=function(){
    resetCheckToFields('input[name="SFBox-product_or_box"]', 'product', [
        '#SFBox-product_w',
        '#SFBox-product_d',
        '#SFBox-product_h',
        'input[name="SFBox-product_unit"]',
        '#SFBox-product_weight',
        '#SFBox-product_weight_unit'
        //'input[name="SFBox-product_weight_as_sample"]'
        ]);
    resetCheckToFields('input[name="SFBox-product_or_box"]', 'box', [
        '#SFBox-box_w',
        '#SFBox-box_d',
        '#SFBox-box_h',
        'input[name="SFBox-box_unit"]',
        ]);
        
    /*
    resetCheckToFields('input[name="SFBox-material_type"]', 'folding_cards', [
        'input[name="SFBox-folding_cards_type"]',
        '#SFBox-folding_cards_other',
        'input[name="SFBox-paper_thickness_type"]',
        '#SFBox-paper_thickness',
        'input[name="SFBox-paper_thickness_unit"]',
        '#SFBox-gramage_gsm'
        ]);
    resetCheckToFields('input[name="SFBox-material_type"]', 'corrugated', [
        '#SFBox-flute',
        'input[name="SFBox-flute_type"]',
        '#SFBox-bursting',
        '#SFBox-ect',
        '#SFBox-gramage',
        '#SFBox-flute_type_gsm'
        ]);
    resetCheckToFields('input[name="SFBox-material_type"]', 'other', '#SFBox-material_type_other_content');
    */
    resetCheckToFields('input[name="SFBox-top_closure"]', 'Other', '#SFBox-top_closure_other');
    resetCheckToFields('input[name="SFBox-top_locking"]', 'Other', '#SFBox-top_locking_other');
    resetCheckToFields('input[name="SFBox-bottom_closure"]', 'Other', '#SFBox-bottom_closure_other');
    resetCheckToFieldsNoteq('input[name="SFBox-bottom_closure"]', ['SLB','Auto','RSC','FOL','Open_Bottom'], "input[name='SFBox-bottom_locking']");
    resetCheckToFields('input[name="SFBox-bottom_locking"]', 'Other', '#SFBox-bottom_locking_other');
    resetCheckToFields('input[name="SFBox-insert"]', 'Yes', '#insert_material_tmp');
//resetAsSampleToFields('input[name="SFBox-product_weight_as_sample"]', ['#SFBox-product_w', '#SFBox-product_d', '#SFBox-product_h', 'input[name="SFBox-product_unit"]', '#SFBox-product_weight', 'input[name="SFBox-product_weight_unit"]'])
//resetCheckToFields('input[name="SFBox-window"]', ['Open'], ['#SFBox-window_size_w','#SFBox-window_size_h',"input[name='SFBox-window_size_unit']"]);
//resetCheckToFields('input[name="SFBox-window"]', 'No', ['#SFBox-pvc_thickness','#SFBox-pet_thickness','#SFBox-pp_thickness',"input[name='SFBox-window_with']"]);
//resetCheckToFields('input[name="SFBox-window"]', ['With'], ['#SFBox-window_size_w','#SFBox-window_size_h',"input[name='SFBox-window_size_unit']","input[name='SFBox-window_with']"]);
}

SFNamespace.SFBox.obj = {

    id   		 : "SFBox",

    title        : "Box",

    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        $(".numeric").numeric();
        validators.push(this);
        resetBoxField();
        $('input[name="SFBox-product_or_box"]').click(function(){
            resetBoxField()
        });
        /*
        $('input[name="SFBox-material_type"]').click(function(){
            resetBoxField()
        });
        */
        $('input[name="SFBox-top_closure"]').click(function(){
            resetBoxField()
        });
        $('input[name="SFBox-top_locking"]').click(function(){
            resetBoxField()
        });
        $('input[name="SFBox-bottom_closure"]').click(function(){
            resetBoxField()
        });
        $('input[name="SFBox-bottom_locking"]').click(function(){
            resetBoxField()
        });
        $('input[name="SFBox-insert"]').click(function(){
            resetBoxField()
        });
        $('input[name="SFBox-window_type"]').click(function(){
            resetBoxField()
        });
        $("input[name*='as_sample']").click(function(){
            resetBoxField()
        })
        $("input[name='SFBox-top_closure'],input[name='SFBox-top_locking']").click(function(){
            var v1 = $("input[name='SFBox-top_closure']:checked").val();
            var v2 = $("input[name='SFBox-top_locking']:checked").val();

            if(v1=="Standard" && v2=="No")
                $("#top_closure").attr("src","/images/sample/Standard Slit Lock.jpg");
            else if(v1=="Standard" && v2=="Yes")
                $("#top_closure").attr("src","/images/sample/Standard Slit Lock with Tongue Lock.jpg");
            else if(v1=="Friction" && v2=="No")
                $("#top_closure").attr("src","/images/sample/Friction Tuck.jpg");
            else if(v1=="Friction" && v2=="Yes")
                $("#top_closure").attr("src","/images/sample/Friction Tuck with Tongue Lock.jpg");
            else if(v1=="RSC"){
            	$("#top_closure").attr("src","/images/sample/RSC.jpg");
            }
            else if(v1=="FOL"){
            	$("#top_closure").attr("src","/images/sample/FOL.jpg");
            }
            else
                $("#top_closure").attr("src","/images/blank.png");
        });


        $("input[name='SFBox-bottom_closure'],input[name='SFBox-bottom_locking']").click(function(){
            var v1 = $("input[name='SFBox-bottom_closure']:checked");
            var v2 = $("input[name='SFBox-bottom_locking']:checked");

            if(v1.val()=="Standard" && v2.val()=="No")
                $("#bottom_closure").attr("src","/images/sample/Standard Slit Lock.jpg");
            if(v1.val()=="Standard" && v2.val()=="Yes")
                $("#bottom_closure").attr("src","/images/sample/Standard Slit Lock with Tongue Lock.jpg");
            if(v1.val()=="Friction" && v2.val()=="No")
                $("#bottom_closure").attr("src","/images/sample/Friction Tuck.jpg");
            if(v1.val()=="Friction" && v2.val()=="Yes")
                $("#bottom_closure").attr("src","/images/sample/Friction Tuck with Tongue Lock.jpg");
            
            if(!v1.val()||!v2.val()||v1.val()=='Other'||v2.val()=='Other'){
                $("#bottom_closure").attr("src","/images/blank.png");
            }
            if(v1.val()=='SLB'){
                $("#bottom_closure").attr("src","/images/sample/SLB.jpg");
            }
            if(v1.val()=='Auto'){
                $("#bottom_closure").attr("src","/images/sample/Auto Lock.jpg");
            }
            if(v1.val()=='RSC'){
                $("#bottom_closure").attr("src","/images/sample/RSC.jpg");
            }
            if(v1.val()=='FOL'){
                $("#bottom_closure").attr("src","/images/sample/FOL.jpg");
            }
            if(v1.val()=='Open_Bottom'){
                $("#bottom_closure").attr("src","/images/sample/Open.jpg");
            }
        });

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
        //        if(!$("input[name='SFBox-presentation']:checked").val()){
        //
        //        }
        if( $("input[name='SFBox-presentation']:checked").length < 1 && $("input[name='SFBox-job_perpose']:checked").length < 1){
        	changeColorList([[[$("input[name='SFBox-presentation']"),$("input[name='SFBox-job_perpose']")],true]])
            msg.push("Task["+this.title+"]Please select the 'Job Purpose'.");
        }
        if(!$("input[name='SFBox-product_or_box']:checked").val()){
            changeColorList($("input[name='SFBox-product_or_box']"))
            msg.push("Task["+this.title+"]Please select the 'Product','Box' or 'As Sample' for the 'Job Purpose'.");
        }else if($("input[name='SFBox-product_or_box']:checked").val()=='product'){
        	
            
                var checkBox = 0;
                if(!($('#SFBox-product_w').val() && $('#SFBox-product_d').val() && $('#SFBox-product_h').val() && $("input[name='SFBox-product_unit']:checked").val())){
                    //changeColorList([[[$('#SFBox-product_w'),$('#SFBox-product_d'),$('#SFBox-product_h'),$("input[name='SFBox-product_unit']")],true]])
                    msg.push("Task["+this.title+"]Please input Dimension 'Size' and 'Unit' for the 'Job Purpose: Product'.");
                    checkBox = 1;
                      
                }
                if($("#SFBox-product_weight").val() && !$("#SFBox-product_weight_unit").val()){
                    msg.push("Task["+this.title+"]Please input Weight 'Unit' for the 'Job Purpose: Product'.");
                    checkBox = 1;
                }
                
                /*
                if(checkBox == 1){
                    changeColorList([[[[$('#SFBox-product_w'),$('#SFBox-product_d'),$('#SFBox-product_h'),$("input[name='SFBox-product_unit']"),$("#SFBox-product_weight"),$("#SFBox-product_weight_unit")],
                        $("input[name='SFBox-product_weight_as_sample'][value='Y']")
                        ],false]])
                }
                */
                if(checkBox == 1){
                    changeColorList([[[$('#SFBox-product_w'),$('#SFBox-product_d'),$('#SFBox-product_h'),$("input[name='SFBox-product_unit']"),$("#SFBox-product_weight"),$("#SFBox-product_weight_unit")],false],])
                }
        
        }else if($("input[name='SFBox-product_or_box']:checked").val()=='box'){
            if(!($('#SFBox-box_w').val() && $('#SFBox-box_d').val() && $('#SFBox-box_h').val() && $("input[name='SFBox-box_unit']:checked").val() && $("input[name='SFBox-box_size']:checked").val())){
                changeColorList([[[$('#SFBox-box_w'),$('#SFBox-box_d'),$('#SFBox-box_h'), $("input[name='SFBox-box_unit']"),$("input[name='SFBox-box_size']")],true]])
                msg.push("Task["+this.title+"]Please input Dimension 'Size' and 'Unit' for the 'Job Purpose: Box'.");
            }
        }
        
        /*
        if(!$("input[name='SFBox-material_type']:checked").val())
        {
            changeColorList($("input[name='SFBox-material_type']"))
            msg.push("Task["+this.title+"]Please select the 'Material'.");
        }
        else if($("input[name='SFBox-material_type']:checked").val()=='folding_cards'){
            if(!$("input[name='SFBox-folding_cards_type']:checked").val())
            {	
                changeColorList($("input[name='SFBox-folding_cards_type']"))
                msg.push("Task["+this.title+"]Please select the option for the 'Folding Cards'.");
            }
            else if($("input[name='SFBox-folding_cards_type']:checked").val()=='Other' && !$('#SFBox-folding_cards_other').val())
            {
                changeColorList($('#SFBox-folding_cards_other'))
                msg.push("Task["+this.title+"]Please input the content if select the 'Folding Cards: Other'.");
            }
            if($("input[name='SFBox-paper_thickness_type']:checked").val()=='other' && !($('#SFBox-paper_thickness').val() && $("input[name='SFBox-paper_thickness_unit']:checked").val()) )
            {
                changeColorList([[[$('#SFBox-paper_thickness'),$("input[name='SFBox-paper_thickness_unit']")],true]])
                msg.push("Task["+this.title+"]Please input the content and select 'Unit' if select the 'Paper thickness'.");
            }
            if($("input[name='SFBox-paper_thickness_type']:checked").val()=='gramage' && !$('#SFBox-gramage_gsm').val())
            {
                changeColorList($('#SFBox-gramage_gsm'))
                msg.push("Task["+this.title+"]Please input the content if select the 'Grammage'.");
            }
        }else if($("input[name='SFBox-material_type']:checked").val()=='corrugated'){
            if(!$("input[name='SFBox-flute_type']:checked").val()||!$('#SFBox-flute').val())
            {
                changeColorList($('#SFBox-flute'))
                msg.push("Task["+this.title+"]Please input the content and select 'flut type' for the 'Corrugated'.");
            }
        }else if($("input[name='SFBox-material_type']:checked").val()=='other'){
            if(!$('#SFBox-material_type_other_content').val()){
                changeColorList($('#SFBox-material_type_other_content'))
                msg.push("Task["+this.title+"]Please input the content if select 'Material: Other'.");
            }
        }
        */
        
        //        if( $("input[name='SFBox-floding_cards']:checked").length < 1 && !$("#SFBox-corrugated").val() )
        //            msg.push("Tab["+this.title+"]Please select either 'Folding Cards' or 'Corrugate'.");
        //        else{
        //            if($("input[name='SFBox-floding_cards']:checked").val()){
        //                if(!$('#SFBox-grammage').val() && !$('#SFBox-paper_thickness').val())
        //                    msg.push("Tab["+this.title+"]Please input the 'Folding Cards: Paper thickness' or 'Folding Cards: Gramage'.");
        //                if($('#SFBox-paper_thickness').val() && !$("input[name='SFBox-paper_thickness_unit']:checked").val())
        //                    msg.push("Tab["+this.title+"]Please select 'Unit' for the 'Folding Cards: Paper thickness'.");
        //            }
        //            if($("#SFBox-corrugated").val()){
        //                if(!$("input[name='SFBox-flute']:checked").val())
        //                    msg.push("Tab["+this.title+"]Please select 'Kraft Top' or 'Mottle White Top' or 'CCNB Top' for the 'Corrugate'.");
        //            }
        //        }
        //
        
        
        if($(".material_widget[value!='']").length < 1){
            msg.push("Task["+this.title+"]Please add the 'Material'.");
        }
        
        
        if( $("input[name='SFBox-top_closure']:checked").length < 1 )
        {
            changeColorList($("input[name='SFBox-top_closure']"))
            msg.push("Task["+this.title+"]Please fill in the 'Top Closure'.");
        }
        else if($("input[name='SFBox-top_closure']:checked").val()=='Other'&&!$('#SFBox-top_closure_other').val())
        {
            changeColorList($('#SFBox-top_closure_other'))
            msg.push("Task["+this.title+"]Please input the content if select the 'Top Closure: Other'.");
        }

        if( $("input[name='SFBox-top_locking']:checked").length < 1 && !( $("input[name='SFBox-top_closure'][value='RSC']:checked").length ==1 || $("input[name='SFBox-top_closure'][value='FOL']:checked").length ==1))
        {
            changeColorList($("input[name='SFBox-top_locking']"))
            msg.push("Task["+this.title+"]Please fill in the 'Top Locking'.");
        }
        else if($("input[name='SFBox-top_locking']:checked").val()=='Other'&&!$('#SFBox-top_locking_other').val())
        {
            changeColorList($('#SFBox-top_locking_other'))
            msg.push("Task["+this.title+"]Please input the content if select the 'Top Locking: Other'.");
        }

        if( $("input[name='SFBox-bottom_closure']:checked").length < 1 ){
            changeColorList($("input[name='SFBox-bottom_closure']"))
            msg.push("Task["+this.title+"]Please fill in the 'Bottom Closure'.");
        }
        else if($("input[name='SFBox-bottom_closure']:checked").val()=='Other'&&!$('#SFBox-bottom_closure_other').val())
        {
            changeColorList($('#SFBox-bottom_closure_other'))
            msg.push("Task["+this.title+"]Please input the content if select the 'Bottom Closure: Other'.");
        }

        if( $("input[name='SFBox-bottom_locking']:checked").length < 1 && !($("input[name='SFBox-bottom_closure'][value='Auto']:checked").length == 1 || $("input[name='SFBox-bottom_closure'][value='SLB']:checked").length == 1|| $("input[name='SFBox-bottom_closure'][value='Open_Bottom']:checked").length == 1|| $("input[name='SFBox-bottom_closure'][value='FOL']:checked").length == 1|| $("input[name='SFBox-bottom_closure'][value='RSC']:checked").length == 1) ){
            changeColorList($("input[name='SFBox-bottom_locking']"))
            //changeColorList([[[$("input[name='SFBox-bottom_closure'][value='Auto']"),$("input[name='SFBox-bottom_closure'][value='SLB']")],false]])
            msg.push("Task["+this.title+"]Please fill in the 'Bottom Locking'.");
        }
        else if($("input[name='SFBox-bottom_locking']:checked").val()=='Other'&&!$('#SFBox-bottom_locking_other').val())
        {
            changeColorList($('#SFBox-bottom_locking_other'))
            msg.push("Task["+this.title+"]Please input the content if select the 'Bottom Locking: Other'.");
        }

        if( $("input[name='SFBox-insert']:checked").length < 1 )
        {
            changeColorList($("input[name='SFBox-insert']"))
            msg.push("Task["+this.title+"]Please fill in the 'Insert'.");
        }
        else if($("input[name='SFBox-insert']:checked").val()=='Yes' && !$('#SFBox-insert_material').val())
        {
            changeColorList($('#insert_material_tmp'));
            msg.push("Task["+this.title+"]Please input 'Material' for the 'Insert: Yes'.");
        }

        if( $("input[name='SFBox-loading']:checked").length < 1 )
        {
            changeColorList($("input[name='SFBox-loading']"))
            msg.push("Task["+this.title+"]Please select in the 'Top Loading/Side Loading'.");
        }

        if( $("input[name='SFBox-window_type']:checked").length < 1 )
        {
            changeColorList($("input[name='SFBox-window_type']"))
            msg.push("Task["+this.title+"]Please select in the 'Open Window/No Window/Window with'.");
        }
        else if($("input[name='SFBox-window_type']:checked").val()=='With'){
            if(!$("input[name='SFBox-window_with']:checked").val())
            {
                changeColorList($("input[name='SFBox-window_with']"))
                msg.push("Task["+this.title+"]Please select option if select 'Insert: Window with'.");
            }
            else if($("input[name='SFBox-window_with']:checked").val()=='PVC' && !$('#SFBox-pvc_thickness').val())
            {
                changeColorList($('#SFBox-pvc_thickness'))
                msg.push("Task["+this.title+"]Please input 'Thickness' for the 'Insert: Window with PVC'.");
            }
            else if($("input[name='SFBox-window_with']:checked").val()=='PET' && !$('#SFBox-pet_thickness').val())
            {
                changeColorList($('#SFBox-pet_thickness'))
                msg.push("Task["+this.title+"]Please input 'Thickness' for the 'Insert: Window with PET'.");
            }
            else if($("input[name='SFBox-window_with']:checked").val()=='PP' && !$('#SFBox-pp_thickness').val())
            {
                changeColorList($('#SFBox-pp_thickness'))
                msg.push("Task["+this.title+"]Please input 'Thickness' for the 'Insert: Window with PP'.");
            }
        }
        
        if( $("input[name='SFBox-window_type'][value='With']:checked").length == 1 
        		&& !(
        				($("#SFBox-window_size_w").val() 
        				&& $("#SFBox-window_size_h").val() 
        				&& $("input[name='SFBox-window_size_unit']:checked").length>=1 
        				&& $("input[name='SFBox-window_with']:checked").length>=1
        				)
        				||
        				$("input[name='SFBox-suggested_by_pd_team']:checked").length>=1
        			)
        	){
            changeColorList([[[$("#SFBox-window_size_w"),$("#SFBox-window_size_h"),$("input[name='SFBox-window_size_unit']"),$("input[name='SFBox-suggested_by_pd_team']")],true]])
            msg.push("Task["+this.title+"]Please input  and 'Window Size' and 'Unit' and options(PVC or PET or PP or Other)  if select 'Window with'.");
        }
        if($("input[name='SFBox-window_type'][value='Open']:checked").length == 1 && !($("#SFBox-window_size_w").val() && $("#SFBox-window_size_h").val() && $("input[name='SFBox-window_size_unit']:checked").length>=1 || $("input[name='SFBox-suggested_by_pd_team']:checked").length>0)){
            changeColorList([[[$("#SFBox-window_size_w"),$("#SFBox-window_size_h"),$("input[name='SFBox-window_size_unit']")],true]])
            msg.push("Task["+this.title+"]Please input 'Window Size' and 'Unit' or select 'Window Size: Suggested by PD Team' if select 'Open Window'.");
        }
        //
        //        if( $("input[name='SFBox-flute']:checked").length < 1 )
        //            msg.push("Tab["+this.title+"]Please select the 'Kraft Top/Mottle White Top/CCNB Top'.");

        if( !$("#SFBox-expected_date").val() )
        {
            changeColorList($("#SFBox-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        
        
        //jsonify the material info into the hidden field
		var jsonvals = new Array();
		$(".material_widget").each(function(){
		    if($(this).val()){
		        jsonvals.push($(this).attr("ref"));
		    }
		});
		$("#SFBox-material_widgets").val("[" + jsonvals.join(",") + "]");

        return msg;
    }
}
