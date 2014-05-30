var last_panel_id;
$(document).ready(function(){
    var sub_id = false;
    var from_add = false;
    $tabs = $("#tabs").tabs({
        tabTemplate: "<li><a href='#{href}'>#{label}</a>",
        "add" : function(event, ui) {
            
            from_add = true;
            var iframeId = 'iframe-'+ui.panel.id
            var url;
            if(action=='history'){
            	url = '/prepress/getHistorySubForm?tab_id='+ui.panel.id+'&history_id='+history_id;
            }else{
            	url = '/prepress/getSubForm?tab_id='+ui.panel.id+'&action='+action+'&token='+token+'&is_draft='+is_draft_status;
                if(sub_id) url= url + '&sub_id='+sub_id;
            }
            $(ui.panel).append('<iframe src="'+url+'" id="'+iframeId+'" name="'+iframeId+'" onload="Javascript:SetCwinHeight(\''+iframeId+'\')" frameborder="0" width=880 height=1 scrolling="auto"></iframe>');
            $tabs.tabs('select', '#' + ui.panel.id);
        }
        ,'show':function(event, ui){
            if(!from_add){
                last_panel_id = ui.panel.id
                setTimeout('resetIframeHeight()', 100)
            }
            from_add = false;
        }
    });
    
    //fix the indexOf in IE
	if (!Array.indexOf) {
	  Array.prototype.indexOf = function (obj, start) {
	    for (var i = (start || 0); i < this.length; i++) {
	      if (this[i] == obj) {
	        return i;
	      }
	    }
	    return -1;
	  }
	}
    for(var i=0;i<childrenForms.length;i++){
        var obj_id = childrenForms[i].split('-')[0];
        sub_id = childrenForms[i].split('-')[1];
        if(action=='view'){
            if(updatedChildrenForms.indexOf(childrenForms[i])>=0){
            	addTab(obj_id, '<u>'+tabLabel[obj_id]+'</u>');
            }else{
    	        addTab(obj_id, tabLabel[obj_id]);
            }
        }else if(action=='copy' || is_draft_status){
            addTab(obj_id, tabLabel[obj_id],true);
        }else{
        	
            addTab(obj_id, tabLabel[obj_id]);
        }
    }

    sub_id = false;

    $("#request_type_new").click(function() {
        $("#original_version").attr("disabled", true);
        $(".history").slideUp();
    });
    $("#request_type_revision").click(function() {
        $("#original_version").removeAttr("disabled");
        $(".history").slideDown();
    });
    $("#original_version").change(function() {
        $("#history-link").attr("href", "/prepress/viewVersions?system_no="+ $(this).val());
    });
    
});