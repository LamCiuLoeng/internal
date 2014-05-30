<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - Tribal</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<style>
#tooltipdiv {
    display:none;
    background:transparent url(/images/jqueryTools/white_arrow.png);
    font-size:12px;
    height:70px;
    width:160px;
    padding:25px;
}
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.tools.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<!-- <script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script> -->
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>


<script type="text/javascript" src="/js/custom/trb_index.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			$(".tooltip").tooltip('#tooltipdiv');
		});
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/order/index"><img src="/images/images/menu_trb_g.jpg"/></a></td>
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Tribal Sportsware&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main</div>
<div style="width:1200px;margin-left:100px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
		<form name="DataTable" class="tableform" method="post" action="index">
		<table>
			<tr>
			<td>&nbsp;</td>
			<td>
				<div class="case-list-one">
					<ul>
						<li class="label"><label for="DataTable_customerPO" class="fieldlabel">Customer PO#</label></li>
						<li><input type="text" id="DataTable_customerPO" name="customerPO" fieldname="customerPO" style="width: 250px;" /></li>
					</ul>
				</div>
			</td>
			</tr>
			<tr>
				<td>&nbsp;<td>
				<td>&nbsp;</td>
			</tr>
			<tr>
			<td>&nbsp;</td>
			<td>
			<div class="case-list-one">
				<ul>
					<li class="label">
						<label for="DataTable_pom" class="fieldlabel">Cut NO#</label>
					</li>
					<li>
						<%!
							from tribal.util.page_helper import getCutNo
							
							headers = getCutNo()
						%>
						<select name="cutNo" id="cutNo" class="input-width" style="width: 250px;">
							<option value="">&nbsp;</option>
          				%for header in headers:
          					<option value="${header.cutNo}">${header.cutNo}</option>
          				%endfor
          				</select>
						<!--
						<input type="text" id="DataTable_pom" name="cutNo" fieldname="cutNo" class="ajaxSearchField" style="width: 250px;" />
						-->
					</li>
				</ul>
			</div>
			</td>
			</tr>
			<tr>
				<td colspan="2" style="text-align:right"><input type="submit" value="Place Order" style="width:150px;color:#000;" /></td>
			</tr>
		</table>
		</form>
	</div>
</div>
<div id="recordsArea">


%if tmpl_context.paginators.collections:
	<table class="gridTable" cellpadding="0" cellspacing="0" border="0">
		<%
			label_attrs = [('Cut NO#',"80"), ('Barcode',"120"), ('Style',"100"), ('Size',"100"), \
						   ('Style Desc',"100"), ('Cle Desc',"100"),('Sourcing Zone',"100"), ('Quantity',"100")]

			my_page = tmpl_context.paginators.collections
			pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
		%>
		<thead>
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="${len(label_attrs)}">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
			<tr>
				% for label,width in label_attrs:
					<th width="${width}">${label}</th>
				% endfor
			</tr>
		</thead>
		<tbody>
			% for index,item in enumerate(my_page.items):

			%if index%2==0:
			<tr class="odd">
			%else:
			<tr class="even">
			%endif
				<td>
				%if len(item.orders) > 0:
					<a href="/order/viewOrder?id=${item.id}">
					%if not item.poNo:
					Manual
					%else:
					${item.poNo}
					%endif
					</a>
				%else:
					<a href="/order/poOrder?id=${item.id}">${item.poNo}</a>&nbsp;
				%endif
				</td>
				<td><a href="/images/jcpenney/${item.stock}.jpg" class="thickbox">${item.stock}</a>&nbsp;</td>
				<td>${item.sub|b}</td>
				<td>${item.lot|b}</td>
				<td>${item.lotDescription|b}</td>
				<td>${item.line|b}</td>
				<td>${item.cat|b}</td>
				<td>${Date2Text(item.poDate)|b}</td>
			</tr>
			% endfor

			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="${len(label_attrs)}">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
		</tbody>
	</table>
</div>

%endif

<div id="tooltipdiv"></div>