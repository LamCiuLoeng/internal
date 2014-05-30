<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Orsay</%def>
<%def name="extCSS()">
<link rel="stylesheet" href="/css/custom/orsay.css" type="text/css" />
</%def>
<%def name="extJavaScript()">
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/orsay/index"><img src="/images/images/menu_orsay_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Orsay</div>
<div
	<div class='box5'>
        <span class='head'>Welcome your visit, Please select</span>
        <ul id="sitemap">
            <li>1. Place NEW Order
                <ul style="margin-left:30px;">
                    <li><a href='/orsay/item1?season=s11'>Item 1</a></li>
                    <li><a href='/orsay/item2?season=s11'>Item 2</a></li>
                    <li><a href='/orsay/item3?season=s11'>Item 3</a></li>
                    <li><a href='/orsay/item1?season=s12'>Item 4</a></li>
                    <li><a href='/orsay/item2?season=s12'>Item 5</a></li>
                    <li><a href='/orsay/item3?season=s12'>Item 6</a></li>
                </ul>
            </li>
            <li><a href="/orsay/orderLog" class="STYLE3">2. Review Confirmed Order Status</a></li>
        </ul>
	</div>
</div>	