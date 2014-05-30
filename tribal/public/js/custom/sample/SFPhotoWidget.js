Namespace.register("SFNamespace.SFPhoto");

/*
var resetFileConvertField=function(){
    resetCheckToFields('#SFFileConvert-file_from_ftp', '', '#SFFileConvert-file_from_ftp_location');
    resetCheckToFields('#SFFileConvert-file_from_files', '', '#SFFileConvert-file_from_files_location');
    resetCheckToFields('#SFFileConvert-output_other', '', '#SFFileConvert-output_other_content');
}
*/

SFNamespace.SFPhoto.obj = {

    id   		 : "SFPhoto",
	
    title        : "Photo Shot",
	
    install 	 : function(){
        $('.datePicker').datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: dateFormat
        });
        validators.push(this);
        
        
        /*
        resetFileConvertField();
        $('#SFFileConvert-file_from_ftp').click(function(){
            resetFileConvertField()
        })
        $('#SFFileConvert-file_from_files').click(function(){
            resetFileConvertField()
        })
        $('#SFFileConvert-output_other').click(function(){
            resetFileConvertField()
        })
        */
        
        
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
        if( $("input[name='SFPhoto-job_purpose']:checked").length < 1 ){
            changeColorList($("input[name='SFPhoto-job_purpose']"));
            msg.push("Task["+this.title+"]Please select the 'Job Purpose'.");
        }
        if( $("input[name='SFPhoto-submit_items']:checked").length < 1 ){
            changeColorList($("input[name='SFPhoto-submit_items']"));
            msg.push("Task["+this.title+"]Please select the 'Submitted Items'.");
        }else if( $("#SFPhoto-submit_other").attr("checked") && !$("#SFPhoto-submit_items_other").val() ){
            changeColorList( $("#SFPhoto-submit_items_other") );
            msg.push("Task["+this.title+"]Please input the content if you select the 'Other' option in 'Submitted Items'.");
        }
        
        if( $("input[name='SFPhoto-output']:checked").length < 1 ){
            changeColorList($("input[name='SFPhoto-output']"));
            msg.push("Task["+this.title+"]Please select the 'Output'.");
        }else if( $("#SFPhoto-output_other").attr("checked") && !$("#SFPhoto-output_other_content").val() ){
            changeColorList( $("#SFPhoto-output_other_content") );
            msg.push("Task["+this.title+"]Please input the content if you select the 'Others' option in 'Output'.");
        }
        
        if( !$("#SFPhoto-expected_date").val() ){
            changeColorList($("#SFPhoto-expected_date"))
            msg.push("Task["+this.title+"]Please input the 'Expected Date'.");
        }
        
        
        //jsonify the shoot info into the hidden field
        var jsonvals = new Array();
        $(".shoot_widget").each(function(){
            if($(this).val()){
                jsonvals.push($(this).attr("ref"));
            }
        });
        $("#SFPhoto-shoot_widgets").val("[" + jsonvals.join(",") + "]");
        
        return msg;
    }
}
