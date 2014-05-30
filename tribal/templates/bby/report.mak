<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - BBY</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			var dateFormat = 'yy-mm-dd';
    		$('.datePicker').datepicker({firstDay: 1 , dateFormat: dateFormat});
   });
   
   function toExport(){
     $("form").submit();
     
   }
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="175" valign="top" align="left"><a href="${current_url}"><img src="/images/mainmenu_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="#" onclick="toExport()"><img src="/images/images/menu_export_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Report&nbsp;&nbsp;&gt;&nbsp;&nbsp;${current_nav}</div>



<!-- Main content begin -->

<div style="width:1200px;float:left">
	<div style="overflow:hidden;margin:5px 0px 10px 10px">
			
		${widget(action=action)|n}

	</div>
</div>	

<!-- Main Content end -->