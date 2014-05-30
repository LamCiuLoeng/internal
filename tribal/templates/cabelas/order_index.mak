<%inherit file="tribal.templates.master"/>
<%
my_page = tmpl_context.paginators.collections
pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
%>
<%def name="extTitle()">r-pac - Cabelas</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js"></script>
<script type="text/javascript" src="/js/jquery-ui-timepicker-addon.js"></script>
<script type="text/javascript">
$(document).ready(function() {
	initDateNoImg();
})
</script>
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/cabelas/index"><img src="/images/images/menu_cabelas_g.jpg"/></a></td>
  	<td valign="top" align="left"><a href="/cabelas/ordering/new"><img src="/images/images/menu_new_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Ordering</div>
<form action='/cabelas/ordering/index' method=post>
	${OrderingSearchForm(value=kw)|n}
	<div style='clear:both;margin-left:10px;'><input type=submit class=btn value='Search'/></div>
</form>
<div class='main'>
		<table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:100%">
			<thead>
				<tr>
					<td style="border:0px;text-align:right;" colspan="20">
						${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
					</td>
				</tr>
				<tr>
					<th style="width:12%">No.</th>
					<th style="width:24%">Bill To</th>
					<th style="width:20%">Ship To</th>
					<th style="width:20%">Create Time</th>
				</tr>
			</thead>
			<tbody>
				%for i in collections:
				<% labels = i.lables() %>
				<tr>
					<td class='first'><a href="/cabelas/ordering/view?id=${i.id}">${i.number}</a></td>
					<td> ${i.bill_to.address}</td>
					<td> ${i.ship_to.address}</td>
					<td> ${str(i.create_time)[:16]}</td>
				</tr>
				%endfor
				<tr>
					<td colspan="20" style="border:0px;text-align:right;">
						${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
					</td>
				</tr>
			</tbody>
		</table>
	
</div>