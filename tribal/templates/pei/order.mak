<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b
	from tribal.util import const
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


<script type="text/javascript" src="/js/custom/pei/pei_form.js" language="javascript"></script>

</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/pei/index"><img src="/images/images/menu_pei_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toConfirm()"><img src="/images/images/menu_confirm_g.jpg"/></a>    </td>
    <td width="64" valign="top" align="left">
    	% if order_flag == 0:
    	<a href="/pei/index" onclick="return toCancel()">
    	% else:
    	<a href="/pei/index" onclick="return toCancel()">
    	% endif
    		<img src="/images/images/menu_cancel_g.jpg"/>
    	</a>
    </td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">PEI&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>

<form id="orderForm" action="/pei/saveOrder" method="post">
<input type="hidden" id="order_form" name="order_form" value="${form.id}" />
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
                <td>
                <select name="shipCompany" class="input-style1-40fonts" id="shipCompany" onchange="changeShipTo(this)">
	          		%for st in shipTos:
	          		<option value="${st.id}">${st.company|b}</option>
	          		%endfor
	          		<option value="0">Other</option>
          		</select>
          		<div class="other_shipto" style="display: None;">
          			<br />
          			<input name="other_shipto" type="text" class="input-style1" size="30" />
          		</div>
                </td>
              </tr>
              <tr>
                <td align="right">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>
                	<div class="other_shipto" style="display: None;">
          			<br />
          			</div>
                	<textarea name="shipAddress" cols="45" rows="5" class="textarea-style" id="shipAddress" disabled="disabled"></textarea>
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="shipTel" type="text" class="input-style1" id="shipTel" size="30" disabled="disabled" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="shipFax" type="text" class="input-style1" id="shipFax" size="30" disabled="disabled" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="shipAttn" type="text" class="input-style1" id="shipAttn" size="30" disabled="disabled" />
                	&nbsp;&nbsp;
                	<a href="#" onclick="clearInput(this,['vendorPO', 'orderedBy', 'orderedTel'])"><img src="/images/clear_input.jpg"/></a>
                </td>
              </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Customer PO&nbsp;:</td>
                <td>&nbsp;</td>
                <td><input name="vendorPO" type="text" class="required input-style1" id="vendorPO" size="30" /></td>
              </tr>
              <tr>
                <td height="26" align="right">&nbsp;Ordered By&nbsp;:</td>
                <td>&nbsp;</td>
                <td><input name="orderedBy" type="text" class="input-style1" id="orderedBy" size="30" /></td>
              </tr>
               <tr>
			  	<td height="26" align="right">&nbsp;Tel&nbsp;:</td>
                <td>&nbsp;</td>
                <td><input name="orderedTel" type="text" class="input-style1" id="orderedTel" size="30" /></td>
			  </tr>
			  <tr>
			  	<td height="26" align="right">&nbsp;For International Drop Ship&nbsp;:</td>
                <td>&nbsp;</td>
                <td><input name="dropShip" type="radio" value="1"/>True&nbsp;<input name="dropShip" type="radio" value="0" checked />False</td>
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
                <td>
                <select name="billCompany" class="input-style1-40fonts" id="billCompany" onchange="changeBillTo(this)">
	          		%for bt in billTos:
	          		<option value="${bt.id}">${bt.company|b}</option>
	          		%endfor
	          		<option value="0">Other</option>
          		</select>
          		<div class="other_billto" style="display: None;">
          			<br />
          			<input name="other_billto" type="text" class="input-style1" size="30" />
          		</div>
                </td>
              </tr>
              <tr>
                <td align="right">Address&nbsp;:&nbsp;</td>
                <td>&nbsp;</td>
                <td>
                	<div class="other_billto" style="display: None;">
          			<br />
          			</div>
                	<textarea name="billAddress" cols="45" rows="5" class="textarea-style" id="billAddress" disabled="disabled"></textarea>
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Phone&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="billTel" type="text" class="input-style1" id="billTel" size="30" disabled="disabled" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Fax&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="billFax" type="text" class="input-style1" id="billFax" size="30" disabled="disabled" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Contact&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="billAttn" type="text" class="input-style1" id="billAttn" size="30" disabled="disabled" />
                	&nbsp;&nbsp;
                	<a href="#" onclick="clearInput(this,['buyerPO', 'shipVia', 'shipDate'])"><img src="/images/clear_input.jpg"/></a>
                </td>
              </tr>
              <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td height="26" align="right"><img src="/images/search_07.jpg" width="7" height="7" />&nbsp;Buyer PO&nbsp;:</td>
                <td>&nbsp;</td>
                <td>
                	<input name="buyerPO" type="text" class="required input-style1" id="buyerPO" size="30" />
                </td>
              </tr>
              <tr>
                <td height="26" align="right">Ship VIA :</td>
                <td>&nbsp;</td>
                <td>
                	<input name="shipVia" type="text" class="input-style1" id="shipVia" size="30" />
                </td>
              </tr>
			  <tr>
			  	<td height="26" align="right">Required Date :</td>
			  	<td>&nbsp;</td>
			  	<td>
			  		<input name="shipDate" type="text" class="datePicker input-style1" id="shipDate" size="30" />
			  	</td>
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
	<table class="gridTable" border="0" cellpadding="0" cellspacing="0" width="1200">
  <thead>
    <tr>
      <td height="35" align="center" width="200" class="wt-td">Item Code</td>
      <td align="center" width="200" class="wt-td">View</td>
      <td align="center" width="100" class="wt-td">Variables</td>
      <td align="center" width="500" class="wt-td">Description</td>
      <td align="center" width="200" class="wt-td">US$/1000PCS</td>
      <td align="center" width="200" class="wt-td">Quantity</td>
    </tr>
  </thead>
  <tbody>
    %for index,item in enumerate(items):
    %if index%2==0:
    <tr class="even">
    %else:
    <tr class="odd">
    %endif
      <td height="25" class="t-td">${item.itemCode|b}</td>
      <td align="center" class="t-td"><a href="/images/pei/${item.itemCode}.jpg" title="Sample Image" class="thickbox">View Item</a></td>
      % if item.attrs:
      <td align="center" class="t-td"><a href="#" onClick="editVariable(${form.id}, ${item.id})">Edit</a></td>
      % else:
      <td align="center" class="t-td">&nbsp;</td>
      % endif
      <td align="center" class="t-td">${item.itemDesc|b}</td>
      <td align="center" class="t-td"><input type="text" class="numeric" name="price_${item.id}" style="text-align:right;width:200px;"></td>
      <td align="center" class="t-td">
      	<input type="text" class="numeric" name="quantity_${item.id}" style="text-align:right;width:200px;">
      	<input type="hidden" name="variable_${item.id}" />
      </td> 
    </tr>
    %endfor
  </tbody>
</table>
<div style="float: left; padding-left: 900px;">
<br />
<a href="#" onclick="toConfirm()"><img src="/images/images/menu_confirm_g.jpg"/></a>
&nbsp;&nbsp;
<a href="/order/index" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a>
</div>
<div class="shade"><iframe class="T_iframe"></iframe></div>
<div class="item_variable" style="display:none"></div>
</form>