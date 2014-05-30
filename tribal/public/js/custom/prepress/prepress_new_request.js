var last_panel_id;
$(document).ready(function() {
    $tabs = $("#tabs").tabs({
        tabTemplate: "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close'>Remove Tab</span></li>",
        "add" : function(event, ui) {
            var iframeId = 'iframe-'+ui.panel.id
            var url = '/prepress/getSubForm?tab_id='+ui.panel.id+'&action='+action+'&token='+token;
            $(ui.panel).append('<iframe src="'+url+'" id="'+iframeId+'" name="'+iframeId+'" onload="Javascript:SetCwinHeight(\''+iframeId+'\')" frameborder="0" width=880 height=1 scrolling="auto"></iframe>');
            $tabs.tabs('select', '#' + ui.panel.id);
        }
    });
    $("#dialog:ui-dialog").dialog( "destroy" );
    $("#dialog-new_program,#dialog-new_project,#dialog-new_customer,#dialog-new_item_category").dialog({
        height: 250,
        width: 350,
        modal: true,
        autoOpen: false
    });
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