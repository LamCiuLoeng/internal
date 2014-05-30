$(document).ready(function() {
    //downSelct();
    newSelect(user_name);
    initSelete();

    addGroup()

    $("#dialog:ui-dialog").dialog( "destroy" );
    $("#dialog-new_program,#dialog-new_project,#dialog-new_customer,#dialog-new_item_category").dialog({
        height: 250,
        width: 350,
        modal: true,
        autoOpen: false
    });
});