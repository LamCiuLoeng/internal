<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b
        from tribal.util.common import Date2Text, rpacEncrypt
        from datetime import datetime as dt
        from tribal.util.dba_util import nextMonth
%>

<%def name="extTitle()">r-pac - PLAYTEX / WONDERBRA / SHOCK ABSORBER</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/order_form.css" type="text/css" />
<link rel="stylesheet" href="/css/nyroModal.css" />
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.nyroModal-1.6.2.min.js"></script>
<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/custom/dba.js"></script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="64" valign="top" align="left"><a href="/dba2/search"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="64" valign="top" align="left">
        <a href="/dba2/updateOrder?code=${rpacEncrypt(order.id)}&ids=${ids}"><img src="/images/images/menu_revise_g.jpg"/></a>
    </td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">PLAYTEX / WONDERBRA / SHOCK ABSORBER&nbsp;&nbsp;&gt;&nbsp;&nbsp;View Order</div>
<div style="width:1100px">
  <div class="templat_main_div1" style="height:130px;">
    <table cellspacing="0" cellpadding="0" border="0" width="100%">
      <tbody>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170">&nbsp;</td>
          <td width="300" colspan="3">&nbsp;</td>
        </tr>
         <tr>
          <td class="STYLE3">&nbsp;</td>
          <td valign="top">BILL TO:</td>
          <td colspan="3">${order.bill_to}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
          <td colspan="3">&nbsp;</td>
        </tr>
      </tbody>
    </table>
  </div>

 <div class="templat_main_div2" style="min-height:130px;">
    <table cellspacing="0" cellpadding="0" border="0" width="100%">
      <tbody>
        <tr>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
          <td width="220" colspan="3">&nbsp;</td>
        </tr>
        <tr>
          <td width="10">&nbsp;</td>
          <td width="170" valign="top">SHIP TO:</td>
          <td class="bottom_border" colspan="3">${order.ship_to}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><span style="color:red; font-weight: bolder; ">Special Request Ship Date:</span></td>
          <td class="bottom_border" colspan="3"><span style="color:red; font-weight: bolder; ">${order.ship_date if order.ship_date else ''}</span>&nbsp;</td>
        </tr>
        
        <tr>
          <td>&nbsp;</td>
          <td><span style="color:#1B80CE; font-weight: bolder; font-size: 14px; ">Delivery Date:</span></td>
          <td colspan="3"><span style="color:#1B80CE; font-weight: bolder; font-size: 14px;">${order.delivery_date if order.delivery_date else ''}</span>&nbsp;</td>
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
          <td>&nbsp;</td>
          <td><strong>SOB#:</strong></td>
          <td class="bottom_border" colspan="3">${order.sob if order.sob else ''}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>Customer PO#:</strong></td>
          <td class="bottom_border" colspan="3">${order.po}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>Customer Name:</strong></td>
          <td class="bottom_border" colspan="3">${order.customer.name}&nbsp;</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>Create Time:</strong></td>
          <td class="bottom_border" colspan="3">${Date2Text(order.create_time, '%Y-%m-%d %H:%M:%S')|b}</td>
        </tr>
         <tr>
          <td>&nbsp;</td>
          <td><strong>Created By:</strong></td>
          <td class="bottom_border" colspan="3">${order.create_by.user_name|b}</td>
        </tr>
         <tr>
          <td>&nbsp;</td>
          <td><strong>Update Time:</strong></td>
          <td class="bottom_border" colspan="3">${Date2Text(order.update_time, '%Y-%m-%d %H:%M:%S')|b}</td>
        </tr>
        <tr>
          <td>&nbsp;</td>
          <td><strong>Updated By:</strong></td>
          <td colspan="3">${order.update_by.user_name|b}</td>
        </tr>
      </tbody>
    </table>
  </div>

<div class="templat_main_div2" style="height:90px; border: red dashed 1px;">
    <table cellspacing="0" cellpadding="0" border="0" width="100%">
      <tbody>
        <tr>
            <td valign="top">
                <p style=" color: red;font-weight: bolder;">&nbsp;&nbsp;Attention:<br />
                   &nbsp;&nbsp;Normal orders will deliver on 15th of the month.
                   For the POs entered with <br />
                   &nbsp;&nbsp;"Special Request Ship Date",
                    it would further confirm by r-pac.
                </p>
            </td>
        </tr>
      </tbody>
    </table>
 </div>

</div>
  <div style="clear:both"><br /></div>
 <div style="margin:5px 1px 10px 10px">
     <%
        my_page = tmpl_context.paginators.orderDetails
        pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
    %>
  <table cellspacing="0" cellpadding="0" border="0" class="gridTable">
    <thead>
         %if my_page.item_count > 0 :
        <tr>
          <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="100">
            ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
          </td>
        </tr>
        %endif
      <tr>
        <td height="30" align="center" width="140" class="wt-td">Item Code</td>
        <td align="center" width="180" class="wt-td">Qty(Firm PO, ${Date2Text(order.create_time, '%b/%Y')})</td>
        <td align="center" width="320" class="wt-td">
            Forecast Qty (For reference only, ${nextMonth(order.create_time)})
        </td>
        <td align="center" width="290" class="wt-td">Category</td>
        <td align="center" width="210" class="wt-td">Type</td>
        <td align="center" width="200" class="wt-td">Image</td>
        <td align="center" width="200" class="wt-td">Flatted Size</td>
      </tr>
    </thead>
    <tbody>

    %for index,d in enumerate(orderDetails):
    %if index%2==0:
    <tr class="even">
    %else:
    <tr class="odd">
    %endif
      <td height="25" class="t-td">${d.item.item_code}</td>
      <td align="center" class="t-td">${d.commited_qty}</td>
      <td align="center" class="t-td">${d.forecast_qty}</td>
      <td align="center" class="t-td">${d.item.category.name}</td>
      <td align="center" class="t-td">${d.item.type.name}</td>
      <td align="center" class="t-td">
          <a href="/images/dba/${d.item.image}.jpg" class="nyroModal" title="${d.item.item_code}(${d.item.flatted_size})">
             <img width="60" height="30" src="/images/dba/${d.item.image}.jpg" />
          </a>
      </td>
      <td>${d.item.flatted_size|b}</td>
    </tr>
    %endfor
     %if my_page.item_count > 0 :
        <tr>
          <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="100">
            ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
          </td>
        </tr>
        %endif
    </tbody>
  </table>
 </div>