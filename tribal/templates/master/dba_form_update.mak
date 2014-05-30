<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.multiSelect.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/nyroModal.css" />

 <style type="text/css">

.width-220 {
    width: 220px;
}
label.error {
    display: block;
}
  </style>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.multiSelect.js"></script>
<script type="text/javascript" src="/js/jquery.nyroModal-1.6.2.min.js"></script>
<script type="text/javascript" src="/js/jquery.validate.min.js"></script>
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    	$(document).ready(function(){
    		$(".jqery_multiSelect").multiSelect();
            $('#update-form').validate({
                rules: { image: { accept: "jpg"}},
                messages: { image: "  **File must be jpg!" }
            });
    	});
    	
		function toSave(){
			$.prompt("Are you sure to confirm these?",
                {opacity: 0.6,
                 prefix:'cleanblue',
                 buttons:{'Yes':true,'No,Go Back':false},
                 focus : 1,
                 callback : function(v,m,f){
                    if(v){
                        $("#update-form").submit();
                    }
                 }
                }
            );
		}
		
		function toUpdate() {
			$("form").attr("action", "/itemcode/updateAttr");
			$("form").submit();
		}
    //]]>
   </script>
</%def>


<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <!-- <td width="176" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_${funcURL}_g.jpg"/></a></td> -->
    <td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    <%doc>
    % if funcURL == 'itemcode':
    <td width="64" valign="top" align="left"><a href="#" onclick="toUpdate()"><img src="/images/images/menu_update_g.jpg"/></a></td>
    % endif
    </%doc>
    <td width="64" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">DBA Item&nbsp;&nbsp;&gt;&nbsp;&nbsp;Update</div>

<div>
    <form id="update-form" action="${saveURL}" method="post" class="dbaitemupdateform required" enctype="multipart/form-data">

	${widget(values)|n}

 <div class="case-list-one">
    <ul>
        <li class="label"><label id="old-image.label" for="old-image" class="fieldlabel">Image</label></li>
        <li>
            <a title="${values.get('item_code')}(${values.get('flatted_size')})" class="nyroModal" href="/images/dba/${values.get('image')}.jpg">
                    <img width="60" height="30" src="/images/dba/${values.get('image')}.jpg">
            </a>
        </li>
    </ul>
    <ul>
        <li class="label"><label id="image.label" for="image" class="fieldlabel">New Image(jpg)</label></li>
        <li>
            <input type="file" id="image" class="width-250" name="image" />
        </li>
    </ul>
</div>

    </form>
</div>

<br />
<br />
<br />



