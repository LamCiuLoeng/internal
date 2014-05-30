<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b
%>

<%def name="extTitle()">r-pac - Tribal</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/order_form.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
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
<script type="text/javascript" src="/js/order_form_edit.js" language="javascript"></script>

<%
	billToStr = "var billToInfo = {" + ",".join(['''
		'%d':{'company':'%s','address':'%s','attn':'%s','tel':'%s','fax':'%s','email':'%s'}
	''' %(bt.id,bt.company,bt.address,bt.attn,bt.tel,bt.fax,bt.email)  for bt in billTos]) + "};"

	shipToStr = "var shipToInfo = {" + ",".join(['''
		'%d':{'company':'%s','address':'%s','attn':'%s','tel':'%s','fax':'%s','email':'%s'}
	''' %(st.id,st.company,st.address,st.attn,st.tel,st.fax,st.email) for st in shipTos]) + "};"

%>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
    	${billToStr}
    	${shipToStr}
	//]]>
</script>


<script type="text/javascript" src="/js/custom/trb_form.js" language="javascript"></script>

</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/order/index"><img src="/images/images/menu_trb_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toConfirm()"><img src="/images/images/menu_confirm_g.jpg"/></a>    </td>
    <td width="64" valign="top" align="left">
    	% if order_flag == 0:
    	<a href="/order/index" onclick="return toCancel()">
    	% else:
    	<a href="/order/index" onclick="return toCancel()">
    	% endif
    		<img src="/images/images/menu_cancel_g.jpg"/>
    	</a>
    </td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Tribal Sportsware&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>

<form id="orderForm" action="/order/saveOrder" method="post">
	<input type="hidden" name="msgID" value="${msgHeader.id}"/>
  
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
          <td class="bottom_border" colspan="3">
          	<select name="billCompany" id="billCompany" class="input-width" onchange="changeBillTo(this)">
          		%for bt in billTos:
          			<option value="${bt.id}">${bt.company}</option>
          		%endfor
          	</select>
          </td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>ADDRESS:</strong></td>
          <td class="bottom_border" colspan="3"><textarea name="billAddress" id="billAddress" class="input-width"></textarea></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>CONTACT:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="billAttn" id="billAttn"  class="input-width"/></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>TELEPHONE:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="billTel" id="billTel"  class="input-width"/></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>FAX:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="billFax" id="billFax"  class="input-width"/></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>E-mail:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="billEmail" id="billEmail"  class="input-width"/></td>
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
          <td class="bottom_border" colspan="3">
          	<select name="shipCompany" id="shipCompany"  class="input-width" onchange="changeShipTo(this)">
          		%for st in shipTos:
          			<option value="${st.id}">${st.company}</option>
          		%endfor
          	</select>
          </td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>ADDRESS:</strong></td>
          <td class="bottom_border" colspan="3"><textarea name="shipAddress" id="shipAddress" class="input-width"></textarea></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>CONTACT:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="shipAttn" id="shipAttn"  class="input-width"/></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>TELEPHONE:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="shipTel" id="shipTel"  class="input-width"/></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>FAX:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="shipFax" id="shipFax"  class="input-width"/></td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>E-mail:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="shipEmail" id="shipEmail"  class="input-width"/></td>
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
          <td width="10">&nbsp;</td>
          <td width="170"><strong><label for="poNo"><span class="STYLE3">Customer PO#</span></label>:</strong></td>
          <td class="bottom_border" colspan="3"><input type="text" name="customerPO" id="poNo" class="input-width required-field" value="${custom_po}"/></td>
        </tr>
       </tbody>
     </table>
  </div>
  </div>
  <div style="clear:both"><br /></div>
  <table cellspacing="0" cellpadding="0" border="0" width="1200"  class="gridTable">
    <thead>
      <tr>
        <td height="35" align="center" width="50" class="wt-td">Cut No</td>
        <td align="center" width="50" class="wt-td">Barcode</td>
        <td align="center" width="50" class="wt-td">Style</td>
        <td align="center" width="50" class="wt-td">Size</td>
        <td align="center" width="50" class="wt-td">Style Desc</td>
        <td align="center" width="50" class="wt-td">Cle Desc</td>
        <td align="center" width="50" class="wt-td">Sourcing Zone</td>
        <td align="center" width="80" class="wt-td">Quantity</td>
      </tr>
    </thead>
    <tbody>

    %for index,item in enumerate(msgDetail):
    %if index%2==0:
    <tr class="even">
    %else:
    <tr class="odd">
    %endif
      <td height="25" class="t-td">${msgHeader.cutNo}</td>
      <td align="center" class="t-td">${item.barcode|b}</td>
      <td align="center" class="t-td">${item.style|b}</td>
      <td align="center" class="t-td">${item.size|b}</td>
      <td align="center" class="t-td">${item.styleDesc|b}</td>
      <td align="center" class="t-td">${item.cleDesc|b}</td>
      <td align="center" class="t-td">${item.sourcingZone|b}</td>
      <td align="center" class="t-td"><input type="text" size="10" name="quantity_${item.id}" class="numeric" value="${item.quantity}" style="text-align:right"></td>
    </tr>
    %endfor
    </tbody>
  </table>

</form>

