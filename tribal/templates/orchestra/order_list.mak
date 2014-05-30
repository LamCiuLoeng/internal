<%inherit file="tribal.templates.master"/>
<%
from tribal.util.mako_filter import pt
%>
<%def name="extTitle()">r-pac - Orchestra</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.loadmask.min.js"></script>
<script>
var actionBase = '/orchestra/${team}/'
var delOrder = function(id){
	if(confirm('Are you sure to delete this order?')){
		location.href='/orchestra/${team}/delete_order?id='+id
	}
}
var redoOrder = function(){
	if(confirm('Are you sure to redo all selected order?')){
		$("body").mask("Loading...");
		$('#_form').attr('action', actionBase+'redo_order')
		$('#_form').submit()	
	}
}
var downOrder = function(){
	$("body").mask("Loading...");
	$('#_form').attr('action', actionBase+'downloads')
	$('#_form').submit()
}
</script>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orchestra/${team}/index"><img src="/images/images/menu_orchestra_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Orchestra&nbsp;&nbsp;&gt;&nbsp;&nbsp;List Order</div>
<div class='ca_box4'>
	<form method="get" action="/orchestra/${team}/list_order">
		${widget(value=values)|n}
		<div style='clear:both;margin-left:10px;'><input type=submit class=btn value='Search'/></div>
	</form>
</div>
<div class='main'>
	<form method="post" action='/orchestra/${team}/' id='_form'>
	<input type='button' value='Redo Selected Orders' onclick='redoOrder()'/>
	<!--<input type='button' value='Download Selected Orders' onclick='downOrder()'/>-->
	<table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:100%">
		<thead>
			<tr>
				<th style='width:20px;'><input type='checkbox' onclick='selectAll(this)'/></th>
				<th>Customer PO#</th>
				<th>Sku#</th>
				<th>Age</th>
				<th>Specification</th>
				<th>Bill to</th>
				<th>Ship to</th>
				<th>Created By</th>
				<th>Created At</th>
				<th>&nbsp;</th>
			</tr>
		</thead>
		<tbody>
			%for i in orders:
			%if i.team==team:
			<tr>
				<td class="first"><input type='checkbox' name='cb_ids' value='${i.id}'/></td>
				<td><a href='/orchestra/${team}/show_order?id=${i.id}'>${i.customer_po}</a></td>
				<td>${i.sku}</td>
				<td>${i.height}</td>
				<td>${i.specification}</td>
				<td>${i.billto_name}</td>
				<td>${i.shipto_name}</td>
				<td>${i.create_by.display_name}</td>
				<td>${pt(i.create_time)}</td>
				<td><a href='/orchestra/${team}/download?id=${i.id}'>download</a>&nbsp;&nbsp;<a href='javascript:void(0)' onclick='delOrder(${i.id})'>delete</a></td>
			</tr>
			%endif
			%endfor
		</tbody>
	</table>
	</form>
</div>