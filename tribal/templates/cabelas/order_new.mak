<%inherit file="tribal.templates.master"/>
<%
my_page = tmpl_context.paginators.collections
pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
%>
<%def name="extTitle()">r-pac - Cabelas</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
<link rel="stylesheet" type="text/css" media="screen" href="/css/jquery.lightbox-0.5.css"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.lightbox-0.5.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {
	var type;
	maxSq(".img1")
	$('.gallery').lightBox({fixedNavigation:true}); 
	$("#btn_add_to_job").click(function(){
	 	$(".cboxClass").each(function(){
	 		if($(this).attr("checked") == true){
	 			type = 1;
	 		}
	 	})
		if(type){
			$("#order_form").submit()
		}else{
			alert("Please select!")
		}
	})

})
</script>
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/cabelas/index"><img src="/images/images/menu_cabelas_g.jpg"/></a></td>
  	<td valign="top" align="left"><a href="/cabelas/ordering/new"><img src="/images/images/menu_new_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="/cabelas/ordering/index"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Ordering</div>
<div class='main'>
	<form action="/cabelas/ordering/order" method="POST" id="order_form">
		<table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:100%">
			<thead>
				<tr>
					<td style="border:0px;text-align:left;">
						<P><input type="button" id="btn_add_to_job" value="Add To Order" class="btn"/></p>
					</td>
					<td style="border:0px;text-align:right;" colspan="20">
						${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
					</td>
				</tr>
				<tr>
					<th class="head" style="width:5%;"><input id="header_checkbox" type="checkbox" value="0" onclick="selectAll(this)" /></th>
					<th style="width:12%">Logo</th>
					<th style="width:12%">Product Name</th>
					<th style="width:24%">Box Size</th>
					<th style="width:20%">Price</th>
					<th style="width:20%">Bullet Info</th>
				</tr>
			</thead>
			<tbody>
				%for i in collections:
				<tr>
					<td class="head first"><input type="checkbox" class="cboxClass" value="${i.id}"  name="id"/></td>
					<td>
						%for logo in i.logos:
							<a href="/upload/${logo._file_path}" class="gallery"><img src='/upload/${logo._file_path}' class="img1"></a>
						%endfor
					</td>
					<td>${i.product_desc}</td>
					<td>${i.box_size.name}</td>
					<td>${i.price}</td>
					<td>${i.bullet_info}</td>
				</tr>
				%endfor
				<tr>
					<td colspan="20" style="border:0px;text-align:right;">
						${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
					</td>
				</tr>
			</tbody>
		</table>
	</form>
</div>