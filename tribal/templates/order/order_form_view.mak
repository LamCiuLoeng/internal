<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b
%>

<%def name="extTitle()">r-pac - Tribal Sportsware</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/order_form.css" type="text/css" />
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/order/index"><img src="/images/images/menu_trb_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="/order/index"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Tribal Sportsware&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>
	<div style="width:1100px">
  <div class="templat_main_div1">
    <table cellspacing="0" cellpadding="0" border="0" width="100%">
      <tbody>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170">&nbsp;</td>
          <td width="300" colspan="3">&nbsp;</td>
        </tr>
        <tr>
          <td class="STYLE3">&nbsp;</td>
          <td class="STYLE3">BILL TO:</td>
          <td class="bottom_border" colspan="3">${poheader.billTo.company}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>ADDRESS:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.billTo.address}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>CONTACT:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.billTo.attn}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>TELEPHONE:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.billTo.tel}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>FAX:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.billTo.fax}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>E-mail:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.billTo.email}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
          <td colspan="3">&nbsp;</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="templat_main_div2">
    <table cellspacing="0" cellpadding="0" border="0" width="100%">
      <tbody>
        <tr>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
          <td width="220" colspan="3">&nbsp;</td>
        </tr>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170"><span class="STYLE3">SHIP TO:</span></td>
          <td class="bottom_border" colspan="3">${poheader.shipTo.company}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>ADDRESS:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.shipTo.address}</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>CONTACT:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.shipTo.attn}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>TELEPHONE:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.shipTo.tel}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>FAX:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.shipTo.fax}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>E-mail:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.shipTo.email}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
          <td colspan="3">&nbsp;</td>
        </tr>
      </tbody>
    </table>
  </div>


  <div class="templat_main_div1">
    <table cellspacing="0" cellpadding="0" border="0" width="100%">
      <tbody>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170">&nbsp;</td>
          <td width="300" colspan="3">&nbsp;</td>
        </tr>
        <tr>
          <td class="STYLE3">&nbsp;</td>
          <td><strong>Customer POM#:</strong></td>
          <td class="bottom_border" colspan="3">${poheader.customerPO}&nbsp;</td>
        </tr>
      </tbody>
    </table>
  </div>
	</div>
  <div style="clear:both"><br /></div>
  <table cellspacing="0" cellpadding="0" border="0" class="gridTable">
    <thead>
      <tr>
        <td height="30" align="center" width="100" class="wt-td">Cut No</td>
        <td align="center" width="200" class="wt-td">Barcode</td>
        <td align="center" width="200" class="wt-td">Style</td>
        <td align="center" width="70" class="wt-td">Size</td>
        <td align="center" width="150" class="wt-td">Style Desc</td>
        <td align="center" width="150" class="wt-td">Cle Desc</td>
        <td align="center" width="150" class="wt-td">Sourcing Zone</td>
        <td align="center" width="100" class="wt-td">Quantity</td>
      </tr>
    </thead>
    <tbody>

    %for index,item in enumerate(podetails):
    %if index%2==0:
    <tr class="even">
    %else:
    <tr class="odd">
    %endif
      <td height="25" class="t-td">${poheader.header.cutNo}</td>
      <td align="center" class="t-td">${item.detailPO.barcode|b}</td>
      <td align="center" class="t-td">${item.detailPO.style|b}</td>
      <td align="center" class="t-td">${item.detailPO.size|b}</td>
      <td align="center" class="t-td">${item.detailPO.styleDesc|b}</td>
      <td align="center" class="t-td">${item.detailPO.cleDesc|b}</td>
      <td align="center" class="t-td">${item.detailPO.sourcingZone|b}</td>
      <td align="center" class="t-td">${item.quantity|b}</td>
    </tr>
    %endfor
    </tbody>
  </table>