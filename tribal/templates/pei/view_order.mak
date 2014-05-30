<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b
	from tribal.util.common import rpacEncrypt
	from repoze.what.predicates import in_group
%>

<%def name="extTitle()">r-pac - PEI</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/order_form.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<link rel="stylesheet" href="/css/pei_variables.css" type="text/css" />
<style type="text/css">
	.input-width{
		width : 300px
	}
	
	#warning {
		font:italic small-caps bold 16px/1.2em Arial;
	}
</style>

</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
<script type="text/javascript" src="/js/fancyzoom.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.validate.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/pei/pei_form.js" language="javascript"></script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/pei/index"><img src="/images/images/menu_pei_g.jpg"/></a></td>
  	<!--td width="64" valign="top" align="left"><a href="/pei/cancelOrder?code=${rpacEncrypt(header.id)}"><img src="/images/images/menu_cancel_g.jpg"/></a></td-->
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">PEI&nbsp;&nbsp;&gt;&nbsp;&nbsp;View Order</div>

  <table width="1000" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td width="15">&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
      <tr>
        <td width="850" align="left" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
          <tr>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="70"><strong>&nbsp;&nbsp;&nbsp;&nbsp;Ship To&nbsp;:</strong></td>
                <td><img src="/images/search_10.jpg" width="330" height="2" /></td>
              </tr>
            </table></td>
            <td><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="70"><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Bill To&nbsp;:</strong></td>
                <td><img src="/images/search_10.jpg" width="330" height="2" /></td>
              </tr>
            </table></td>
          </tr>
          <tr>
            <td width="50%"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="120">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right">Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td>&nbsp;${shipTo.company|b}</td>
              </tr>
              <tr>
                <td align="right">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;${shipTo.address|b}</td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${shipTo.tel|b}</td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${shipTo.fax|b}</td>
              </tr>
              <tr>
                <td height="26" align="right">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${shipTo.attn|b}</td>
              </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right">Customer PO&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${header.vendorPO|b}</td>
              </tr>
              <tr>
                <td height="26" align="right">Ordered By&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${header.orderedBy|b}</td>
              </tr>
               <tr>
			  	<td height="26" align="right">Tel&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${header.orderedTel|b}</td>
			  </tr>
			  <tr>
			  	<td height="26" align="right">For International Drop Ship&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	% if header.dropShip == True:
                	True
                	% else:
                	False
                	% endif
                </td>
			  </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
            </table></td>
            <td width="50%" valign="top"><table width="100%" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td width="120">&nbsp;</td>
                <td width="10">&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right">Company&nbsp;: </td>
                <td>&nbsp;</td>
                <td>&nbsp;${billTo.company|b}</td>
              </tr>
              <tr>
                <td align="right">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;${billTo.address|b}
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${billTo.tel|b}</td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${billTo.fax|b}</td>
              </tr>
              <tr>
                <td height="26" align="right">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${billTo.attn|b}</td>
              </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right">&nbsp;Buyer PO&nbsp;:</td>
                <td>&nbsp;</td>
                <td>&nbsp;${header.buyerPO|b}</td>
              </tr>
              <tr>
                <td height="26" align="right">Ship VIA :</td>
                <td>&nbsp;</td>
                <td>&nbsp;${header.shipVia|b}</td>
              </tr>
			  <tr>
			  	<td height="26" align="right">Required Date :</td>
			  	<td>&nbsp;</td>
			  	<td>&nbsp;${header.shipDate.strftime('%Y-%m-%d')|b}</td>
			  </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
            </table></td>
          </tr>
        </table></td>
      </tr>
    </table></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td><img src="/images/search_10.jpg" width="970" height="1" /></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
</table>

	<br />
  
  <table cellspacing="0" cellpadding="0" border="0" class="gridTable">
    <thead>
      <tr>

        <td height="35" align="center" width="200" class="wt-td">Item Code</td>
        <td align="center" width="150" class="wt-td">View</td>
        <td align="center" width="150" class="wt-td">Variables</td>
        <td align="center" width="800" class="wt-td">Description</td>
        <td align="center" width="200" class="wt-td">US$/1000PCS</td>
        <td align="center" width="200" class="wt-td">Quantity</td>
  	
      </tr>
    </thead>
    <tbody>
    <%
    	details.sort(key = lambda x: x.id)
    %>
	% for item in details:
   <tr>
      <td height="25" class="t-td">${item.item.itemCode|b}&nbsp;</td>
      <td align="center" class="t-td"><a href="/images/pei/${item.item.itemCode}.jpg" title="Sample Image" class="thickbox">View Item</a></td>
      % if item.item.attrs:
      <td align="center" class="t-td"><a href="#" onClick="viewVariable(${header.id}, ${item.item.itemClass.id}, ${item.item.id})">Variable</a></td>
      % else:
      <td align="center" class="t-td">&nbsp;</td>
      % endif
      <td align="center" class="t-td">${item.item.itemDesc|b}&nbsp;</td>
      <td align="center" class="t-td">${item.price|b}&nbsp;</td>
      <td align="center" class="bt-td">${item.quantity|b}&nbsp;</td>
    </tr>
    % endfor
    </tbody>
  </table>
<div class="shade"><iframe class="T_iframe"></iframe></div>
<div class="item_variable" style="display:none"></div>