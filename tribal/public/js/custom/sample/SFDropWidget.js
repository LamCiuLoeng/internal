Namespace.register("SFNamespace.SFDrop");

var resetDropField=function(){
    resetCheckToFields('#SFDrop-submit_items_dieline', '', '#SFDrop-submit_items_location');
    resetCheckToFields('input[name="SFDrop-condition"]', 'other', '#SFDrop-condition_other_content');
}

SFNamespace.SFDrop.obj = {

    id   		 : "SFDrop",
	
    title        : "Drop Test",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        validators.push(this);
        resetDropField();
        $('#SFDrop-submit_items_dieline').click(function(){resetDropField()})
        $('input[name="SFDrop-condition"]').click(function(){resetDropField()})
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
        if($("input[name='SFDrop-submit_items']:checked").length < 1){
        	changeColorList($("input[name='SFDrop-submit_items']"))
            msg.push("Task["+this.title+"]Please select the 'Submitted Items'.");
        }
        if( $("#SFDrop-submit_items_dieline").attr("checked") && !$("#SFDrop-submit_items_location").val() ){
        	changeColorList($("#SFDrop-submit_items_location"))
        	msg.push("Task["+this.title+"]Please input the 'Location' also if you select the 'Die-line Files' option.");
        }
        if( $("#SFDrop-submit_items_attachment").attr("checked") && !($("#SFDrop-attachment_name").val() || $("img[title='Delete this file.']").length>0 ) ){
        	msg.push("Task["+this.title+"]Please upload the 'Attachment' if select the 'See per attachment' option.");
        	changeColorList($("input[name='SFDrop-attachment_name']"))
        }
        if( !$("[name='SFDrop-test_info']:checked").val() ){
        	changeColorList($("[name='SFDrop-test_info']"))
        	msg.push("Task["+this.title+"]Please select the 'Test Info'.");
        }
        if( !$("[name='SFDrop-condition']:checked").val() ){
        	changeColorList($("[name='SFDrop-condition']"))
        	msg.push("Task["+this.title+"]Please select the 'Conditions'.");
        }
        if( $("#SFDrop-condition_other").attr("checked") && !$("#SFDrop-condition_other_content").val() ){
        	changeColorList($("#SFDrop-condition_other_content"))
        	msg.push("Task["+this.title+"]Please input the content if you select the 'Other' option in 'Conditions'.");
        }
        if( !$("#SFDrop-expected_date").val() ){
        	changeColorList($("#SFDrop-expected_date"))
        	msg.push("Task["+this.title+"]Please input the 'Expected date/time'.");
        }
        return msg;
    }
}
