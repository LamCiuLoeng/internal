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
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>


<script type="text/javascript" src="/js/custom/trb_search.js" language="javascript"></script>
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
    <td width="64" valign="top" align="left">
    	<a href="javascript:toSearch()">
    		<img src="/images/images/menu_search_g.jpg"/>
    	</a>
    </td>
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Tribal&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order by CUT No</div>
<div style="width:1200px;margin:0px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
		<form name="DataTable" class="tableform" method="post" action="index">
			<div>
				${search_form(value=values)|n}
			</div>
		</form>
	</div>
</div>
<div id="recordsArea">
	<table class="gridTable" cellpadding="0" cellspacing="0" border="0">
		<%
			label_attrs = [('CUT No', '150'), ('Customer PO#',"200"), 
						   ('Order Date',"200"), ('Total Qty', 100)]

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
				${item.orders[0].header.cutNo}
				</td>
				<td>
				<a href="/order/viewOrder?id=${item.id}">${item.orders[0].customerPO}</a>&nbsp;
				</td>
				<td>${Date2Text(item.orders[0].orderDate)|b}</td>
				<td>${item.orders[0].total_qty()|b}</td>
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

<div id="tooltipdiv"></div>