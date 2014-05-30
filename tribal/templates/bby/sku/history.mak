<%inherit file="tribal.templates.master"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - (BBY)New SKU</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/bby.css" type="text/css" media="screen"/>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){

		});
		
		function toCancel(){
		  return confirm("Are you sure to cancel the record?");
		}
		
		function toHold(){
		  return confirm("Are you sure to hold the record?");
		}
		
		function toCopy(){
		  return confirm("Are you sure to copy this record to create a new one?");
		}
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="175" valign="top" align="left"><a href="/sku/index"><img src="/images/mainmenu_g.jpg"/></a></td>
  	%if has_permission("BBY_EDIT"):	
  		%if header.is_complete():
  			
  		%elif header.is_cancel():
  			<td width="64" valign="top" align="left"><a href="/sku/action?id=${header.id}&t=ACTIVE"><img src="/images/images/menu_active_g.jpg"/></a></td>
  		%else:
  			<td width="64" valign="top" align="left"><a href="/sku/update?id=${header.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
            <td width="64" valign="top" align="left"><a href="/sku/submit?id=${header.id}" onclick="return toSubmit();"><img src="/images/images/menu_submit_g.jpg"/></a></td>		
  			%if header.is_on_hold():
  				<td width="64" valign="top" align="left"><a href="/sku/action?id=${header.id}&t=UNLOCK"><img src="/images/images/menu_unlock_g.jpg"/></a></td>
  			%else:
	  			<td width="64" valign="top" align="left"><a href="/sku/action?id=${header.id}&t=CANCEL" onclick="return toCancel();"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
  				<td width="64" valign="top" align="left"><a href="/sku/action?id=${header.id}&t=ON_HOLD" onclick="return toHold();"><img src="/images/images/menu_hold_g.jpg"/></a></td>
			%endif
		%endif
		<td width="64" valign="top" align="left"><a href="/sku/copy?id=${header.id}" onclick="return toCopy();"><img src="/images/images/menu_copy_g.jpg"/></a></td>
  	%endif
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;New SKU</div>



<!-- Main content begin -->
<div style="width:1500px;">
	<div id="tabsJ">
		<ul>
			<li><a href="view?id=${header.id}"/><span>Item Information</span></a></li>
			<li><a href="pcr?id=${header.id}"/><span>PCR</span></a></li>
			<li id="current"><a href="history?id=${header.id}"/><span>History</span></a></li>
		</ul>
	</div>
	
	<div style="padding-left:20px;">
		<%include file="tribal.templates.bby.history_session" args="header=header,history=history"/>
	</div>

</div>
<!-- Main Content end -->