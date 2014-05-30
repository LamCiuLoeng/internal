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


<script type="text/javascript" src="/js/custom/jcp_form.js" language="javascript"></script>

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

<div class="nav-tree">JCPenney&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>

<form id="orderForm" action="/order/saveOrder" method="post">
	<input type="hidden" name="poId" value="${poheader.id}"/>
  
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
        <tr>
          <td class="STYLE3">&nbsp;</td>
          <td><strong>Fiber content:</strong></td>
          <td class="bottom_border" colspan="3">
          	% for name in range(1, 7):
          	<select name="fc_${name}">
          		% for i in range(1, 10):
        		<option value="${i}">${i}</option>
        		% endfor
      		</select>
          	% endfor
        	<%
        		items = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        				 "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"]
        	%>
        	<select name="fc_7">
        		% for item in items:
          		<option value="${item}">${item}</option>
          		% endfor
        	</select>
        	&nbsp;&nbsp;
        	<a class="thickbox" href="/order/ajaxInstruction?cls=fc&val=111111A">(Detail)</a>
          </td>
        </tr>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170">&nbsp;</td>
          <td width="300" colspan="3">&nbsp;</td>
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
          <td width="170"><strong><label for="poNo"><span class="STYLE3">Country of production for packaging:</span></label></strong></td>
          <td class="bottom_border" colspan="3">
          	<select name="sendEmailTo" id="sendEmailTo" class="input-width required-field">
				<option></option>
				%for c in countries:
					<option value="${c.id}">${c.name}</option>
				%endfor
          </td>
        </tr>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170"><strong>Washing Instructions:</strong></td>
          <td class="bottom_border" colspan="3">
          	% for name in range(1, 7):
          	<select name="wi_${name}">
          		% for i in range(1, 10):
        		<option value="${i}">${i}</option>
        		% endfor
      		</select>
          	% endfor
        	<%
        		items = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        				 "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD"]
        	%>
        	<select name="wi_7">
        		% for item in items:
          		<option value="${item}">${item}</option>
          		% endfor
        	</select>
        	&nbsp;&nbsp;
        	<a class="thickbox" href="/order/ajaxInstruction?cls=wi&val=111111A">(Detail)</a>
          </td>
        </tr>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170"><strong>Label System:</strong></td>
          <td width="300" colspan="3"><input type="text" title="input format: 1A21B4" name="labelCode" id="labelCode" class="input-width" style="text-align:right" /></td>
        </tr>
      </tbody>
     </table>
  </div>

  </div>	

  <div style="clear:both"><br /></div>
  <table cellspacing="0" cellpadding="0" border="0" width="1500"  class="gridTable">
    <thead>
      <tr>
        <td height="35" align="center" width="80" class="wt-td">Stock</td>
        <td align="center" width="60" class="wt-td">Sub</td>
        <td align="center" width="60" class="wt-td">Lot</td>
        <td align="center" width="60" class="wt-td">Line</td>
        <td align="center" width="70" class="wt-td">Size Code</td>
        <td align="center" width="120" class="wt-td">Lot Description</td>
        <td align="center" width="120" class="wt-td">Color</td>
        <td align="center" width="60" class="wt-td">Size</td>
        <td align="center" width="90" class="wt-td">Cat/Sku</td>
        <td align="center" width="150" class="wt-td">Product ID/Style#</td>
        <td align="center" width="120" class="wt-td">UPC *</td>
        <td align="center" width="105" class="wt-td">Retail</td>
        <td align="center" width="105" class="wt-td">Quantity ** </td>
<!--
        <td align="center" width="80" class="wt-td">Misc1</td>
        <td align="center" width="80" class="wt-td">Misc2</td>
-->
      </tr>
    </thead>
    <tbody>

    %for index,item in enumerate(podetails):
    %if index%2==0:
    <tr class="even">
    %else:
    <tr class="odd">
    %endif
      <td height="25" class="t-td">${poheader.stock|b}</td>
      <td align="center" class="t-td">${poheader.sub|b}</td>
      <td align="center" class="t-td">${poheader.lot|b}</td>
      <td align="center" class="t-td">${poheader.line|b}</td>
      <td align="center" class="t-td">${item.sizeCode|b}</td>
      <td align="center" class="t-td">${poheader.lotDescription|b}</td>
      <td align="center" class="t-td">${item.colorCode|b}</td>
      <td align="center" class="t-td">${item.size|b}</td>
      <td align="center" class="t-td">${poheader.cat|b}</td>
      <td align="center" class="t-td">${item.styleNo|b}</td>
      <td align="center" class="t-td">${item.upc|b}</td>
      <td align="center" class="t-td"><input type="text" size="14" name="retail_${item.id}" style="text-align:right"></td>
      % if order_flag == 0:
      <td align="center" class="bt-td"><input type="text" size="14" name="quantity_${item.id}" class="numeric" value="${item.quantity}" style="text-align:right"></td>
      % else:
      <td align="center" class="bt-td"><input type="text" size="14" name="quantity_${item.id}" class="numeric" style="text-align:right"></td>
      % endif
<!--
      <td align="center" class="t-td">&nbsp;</td>
      <td align="center" class="t-td">&nbsp;</td>
-->
    </tr>
    %endfor
    </tbody>
  </table>

</form>

