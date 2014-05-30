var childrenForms, selected;
$(document).ready(function(){
    if(action=='update'||action=='copy'){
        downSelct();
        initSelete();
    }
    resetGroup()
    resetTab()
    resetTabLabels()
    if(action != 'view' || (action=='view' && !selected)){
        openGroupDiv($('#group_div1 > .title1').children())
    }
});