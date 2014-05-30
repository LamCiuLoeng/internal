function job_start(sf_type,sf_id,job_type){
    var params = {
        'sf_id' : sf_id,
        'sf_type' : sf_type,
        'job_type' : job_type,
        'action' : 'START',
        't' : Date.parse(new Date())
    }
    $.getJSON('/prepress/ajaxAction.json',params,function(r){
        if(r.flag != 0 ){
            alert(r.msg)
        }else{
            alert('The job has been started.');
            window.location.reload(true);
        }
    })
}




function job_complete(sf_type,sf_id,job_type){

    complete_div.dialog("option",{ buttons : {
            'Submit': function(){
                var job_item = $("#job_item").val();
                var remark = $("#job_remark").val();
                
                if(!job_item){
                    alert("Please fill in the 'Mins' or 'Items' before submit!");
                    return;
                }else if(!check_number(job_item)){
                    alert("Please input the item correctly ,the value should be number.");
                    return;
                }
                
                $("#job_type").val(job_type);
                $("#completeForm").submit();
            }
        }
    })
    complete_div.dialog('open');
}
    
    

function job_restart(sf_type,sf_id,job_type){
    var params = {
        'sf_id' : sf_id,
        'sf_type' : sf_type,
        'job_type' : job_type,
        'action' : 'RESTART',
        't' : Date.parse(new Date())
    }
    $.getJSON('/prepress/ajaxAction.json',params,function(r){
        if(r.flag != 0 ){
            alert(r.msg)
        }else{
            alert("The record has been restart!");
            window.location.reload(true);
        }
    })
}



function job_pending(sf_type,sf_id,job_type){
    pending_div.dialog("option",{buttons : {
            'Submit': function(){
                var reason = $("#job_reason").val();
                if(!reason){ 
                    alert("Please fill in the reason before submit !");
                    return;
                }else{
                    var params = {
                        'sf_id' : sf_id,
                        'sf_type' : sf_type,
                        'job_type' : job_type,
                        'action' : 'PENDING',
                        'reason' : reason,
                        't' : Date.parse(new Date())
                    }
                    $.getJSON("/prepress/ajaxAction.json",params,function(r){
                        if(r.flag != 0 ){
                            alert(r.msg)
                        }else{
                            alert("The record has been updated successfully!");
                            window.location.reload(true);
                        }
                    })
                }
            }
        } })
    pending_div.dialog('open');
 
}



function job_cancel(){
    
}


var complete_div = null;
var pending_div = null;

$("document").ready(function(){
    complete_div= $("#job-div-complete");
    complete_div.dialog({
        title   : "Please fill in the job's item(s):",
        width   : 400,
        closeText : "Close",
        modal   : true,
        autoOpen: false,
        position: 'top'});
        
        
        
    pending_div = $("#job-div-pending");
    pending_div.dialog({
        title   : "Please fill in the pending reason:",
        width   : 400,
        closeText : "Close",
        modal   : true,
        autoOpen: false,
        position: 'top'});
        
})
