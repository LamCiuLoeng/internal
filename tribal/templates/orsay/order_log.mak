<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>
<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<link rel="stylesheet" href="/css/custom/orsay.css" type="text/css" />
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
<script type="text/javascript" src="/js/custom/jcp_index.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			$("select").change(function(){
				var t = $(this);
				if(t.val()){
					$("form").submit();
				}
			});
		});
	//]]>
</script>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orsay/index"><img src="/images/images/menu_orsay_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Orsay&nbsp;&nbsp;&gt;&nbsp;&nbsp;View Order List</div>
<div style="width:1200px;">
	<div style="overflow:hidden;margin:5px 0px 10px 10px">
		<form action="/orsay/orderLog" method="posh">
			${widget(value=values)|n}
		</form>	
		
		<br style="clear:both"/>
			<%
				my_page = tmpl_context.paginators.result
				pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
			%>
		
			<table class="gridTable" cellpadding="0" cellspacing="0" border="0">
				<thead>
					<tr>
						<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="5">
							${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
						</td>
					</tr>
					<tr>
						<th>Confirmed Time</th>
						<th>Customer PO</th>
						<th>E-mail Subject</th>
						<th>Status</th>
                        <th></th>
					</tr>
				</thead>
				<tbody>
					% for index,r in enumerate(my_page.items):
						%if index%2==0:
						<tr class="odd">
						%else:
						<tr class="even">
						%endif
							<td style="border-left:1px solid #ccc">${Date2Text(r.create_time,)}</td>
							<td>${r.customer_po}</td>
							<td>${r.email_subject}</td>
							<td>${r.status}</td>
							<td><a href="/orsay/viewOrderByID?id=${r.id}">View</a>
							&nbsp;&nbsp;&nbsp;&nbsp;
							<a href="/orsay/editOrder?id=${r.id}">Edit</a>
							&nbsp;&nbsp;&nbsp;&nbsp;
							<a href="/orsay/invoice?id=${r.id}&item_no=${item_no}">Invoice</a></td>
						</tr>
					%endfor
					<tr>
						<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="5">
							${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
						</td>
					</tr>
				</tbody>
			</table>
	</div>
</div>	