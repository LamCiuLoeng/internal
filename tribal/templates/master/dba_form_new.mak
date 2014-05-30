<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.multiSelect.css" type="text/css" media="screen"/>

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
<!-- <script type="text/javascript" src="/js/jquery.1.7.1.min.js"></script> -->
<script type="text/javascript" src="/js/jquery.validate.min.js"></script>
<script type="text/javascript" src="/js/jquery.multiSelect.js"></script>
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    	$(document).ready(function(){
            $('#new-form').validate({
                rules: { image: { required: true, accept: "jpg"}},
                messages: { image: "  **File must be jpg!" }
            });
    		$(".jqery_multiSelect").multiSelect();
    	});
    	
		function toSave(){
			$.prompt("Are you sure to confirm these?",
                {opacity: 0.6,
                 prefix:'cleanblue',
                 buttons:{'Yes':true,'No,Go Back':false},
                 focus : 1,
                 callback : function(v,m,f){
                    if(v){
                        $("#new-form").submit();
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
    <%doc>
    <td width="176" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_${funcURL}_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    % if funcURL == 'itemcode':
    <td width="64" valign="top" align="left"><a href="#" onclick="toUpdate()"><img src="/images/images/menu_update_g.jpg"/></a></td>
    % endif
    </%doc>
    <td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">DBA Item&nbsp;&nbsp;&gt;&nbsp;&nbsp;New</div>

<div>
	<form id="new-form" action="/dbaitem/saveNew" method="post" class="dbaitemupdateform required" enctype="multipart/form-data">


    <div class="case-list-one">
            <ul>
                <li class="label"><label id="item_code.label" for="item_code" class="fieldlabel">Item Code(ERP)</label></li>
                <li><input type="text" id="item_code" class="width-250 required" name="item_code" value="" /></li>
            </ul>
            <ul>
                <li class="label"><label id="type_id.label" for="type_id" class="fieldlabel">Type</label></li>
                <li><select name="type_id" class="width-250 required" id="type_id">
        % for d in dbaTypeOptons:
        <option value=${d[0]}>${d[1]}</option>
        % endfor
</select></li>
            </ul>

            <ul>
                <li class="label"><label id="image.label" for="image" class="fieldlabel">Image(jpg)</label></li>
                <li><input type="file" id="image" class="width-250 required" name="image" /></li>
            </ul>
           
    </div>
    

    
    <div class="case-list-one">
            <ul>
                <li class="label"><label id="category_id.label" for="category_id" class="fieldlabel">Category</label></li>
                <li><select name="category_id" class="width-250 required" id="category_id">
        <option value=""></option>
        <option value="1">DIM</option>
        <option value="2">PLAYTEX / WONDERBRA / SHOCK ABSORBER</option>
</select></li>
            </ul>
             <ul>
                <li class="label"><label id="flatted_size.label" for="flatted_size" class="fieldlabel">Flatted Size</label></li>
                <li><input type="text" id="flatted_size" class="width-250 required" name="flatted_size" value="" /></li>
            </ul>
            
    </div>
    


</form>

</div>





