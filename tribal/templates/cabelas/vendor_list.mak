<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Cabelas</%def>
<%def name="extCSS()">
</%def>
<%def name="extJavaScript()">
</%def>
<div id="function-menu">
	<table width="100%" cellspacing="0" cellpadding="0" border="0"><tbody>
		<tr>
			<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
			<td valign="top" align="left"><a href="/cabelas/development"><img src="/images/images/menu_return_g.jpg"/></a></td>
			<td valign="top" align="left"><a href="/cabelas/development/new_vendor"><img src="/images/images/menu_new_g.jpg"/></a></td>
			<td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
			<td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
		</tr>
	</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Vendor Managerment</div>
<div class='main'>
	<table width=100% cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			%if len(result) > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="20">${len(result)} records</td>
			</tr>
			%endif
			<tr>
				<th height="30">Vendor Name</th>
				<th>User Name</th>
				<th>Email</th>
			</tr>
		</thead>
		<tbody>
			%for i in result:
			<tr>
				<td class=first><a href='/cabelas/development/edit_vendor?id=${i.id}'>${i.name}</a></td>
				<td>${i.user.user_name if i.user else '&nbsp;'|n}</td>
				<td>${i.user.email_address if i.user else '&nbsp;'|n}</td>
			</tr>
			%endfor
		</tbody>
	</table>
</div>