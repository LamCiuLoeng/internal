<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Cabelas</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
</%def>
<%def name="extJavaScript()">
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/cabelas/index"><img src="/images/images/menu_cabelas_g.jpg"/></a></td>
  	<td valign="top" align="left"><a href="/cabelas/development/new"><img src="/images/images/menu_new_g.jpg"/></a></td>
  	<td valign="top" align="left"><a href="/cabelas/development/list_vendor"><img src="/images/images/menu_vendor_managerment_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Development</div>
<form action='/cabelas/development' method=post>
	${developmentSearchForm(value=kw)|n}
	<div style='clear:both;margin-left:10px;'><input type=submit class=btn value='Search'/></div>
</form>
<div class='main'>
	<%
		my_page = tmpl_context.paginators.result
		pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
	%>
	<table width=100% cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border:0px;" colspan="20">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
			<tr>
				<th height="30">Product Name</th>
				<th>Vendor</th>
				<th>Box Size</th>
				<th>Gender</th>
				<th>Status</th>
			</tr>
		</thead>
		<tbody>
			%for i in result:
			<tr>
				<td class=first><a href='/cabelas/development/edit?id=${i.id}'>${i.product_desc}</a></td>
				<td>${i.vendor.name}</td>
				<td>${i.box_size.name if i.box_size else '&nbsp;'|n}</td>
				<td>${i.gender.name if i.gender else '&nbsp;'|n}</td>
				<td>${i.display_status}</td>
			</tr>
			%endfor
		</tbody>
	</table>
</div>