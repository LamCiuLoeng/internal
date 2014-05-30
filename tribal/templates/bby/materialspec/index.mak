<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - PEI</%def>
<%def name="extCSS()">
<link rel="stylesheet" href="/css/custom/orsay.css" type="text/css" />
</%def>
<%def name="extJavaScript()">
<script language="JavaScript" type="text/javascript">
	function toOrder() {
		if( $("#itemclass").val() == '' ){
			$.prompt("Please select a form to continue!",{opacity: 0.6,prefix:'cleanred'});
			return false;
		}else{
			$("form").submit();
		}
	}
</script>
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/pei/index"><img src="/images/images/menu_pei_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;PEI</div>
<div
	<div class='box5'>
        <span class='head'>Welcome customer, Please select</span>
        <form name="DataTable" class="tableform" method="post" action="/pei/order">
        <ul id="sitemap">
            <li><label for="orderForm" id="orderForm">Place NEW order: </label></li>
            <li>
        		<select name="itemclass" id="itemclass">
        			<option value=""></option>
        		%for item in forms:
        			<option value="${item.id}">${item.name}</option>
        		%endfor
        		</select>
      		</li>
        </ul>
        <div style="padding-left: 170px;">
        <input value="Continue" style="width: 150px; color: rgb(0, 0, 0);" type="button" onclick="toOrder()" />
        </div>
        </form>
	</div>
</div>	