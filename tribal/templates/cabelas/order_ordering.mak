<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Cabelas</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
<link rel="stylesheet" type="text/css" media="screen" href="/css/jquery.lightbox-0.5.css"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.lightbox-0.5.min.js"></script>
<script type="text/javascript">
$(document).ready(function() {
	maxSq(".img1")
	$('.gallery').lightBox({fixedNavigation:true}); 
	$("#btn_remove_to_job").click(function(){
		if(!confirm('Are you sure?')) { return false; }
		else{
			remove();
		}
	})
	$("#bill_to_id").val(${billto});
	$("#ship_to_id").val(${shipto});
	
})
var remove = function(){
	$(".cboxClass").each(function(){
		 if($(this).attr("checked") == true){
			$(this).parent("td").parent("tr").remove();
		 }
		
	})
}
</script>
</%def>
<div id="function-menu">
	<table width="100%" cellspacing="0" cellpadding="0" border="0"><tbody>
		<tr>
			<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
			<td width="64" valign="top" align="left"><a href="/cabelas/index"><img src="/images/images/menu_cabelas_g.jpg"/></a></td>
			<td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
			<td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
		</tr>
	</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Ordering</div>
<div class=main>
	<form action="/cabelas/ordering/confirm" method="POST" id="order_confirm">
		% if vendor:
		<input type="hidden" value="${vendor.id}" name="vendor_id">
		% endif
		<table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:100%">
			<thead>
				<tr>
					<td colspan="80" style="border:0px;text-align:left;">
						<input type="button" id="btn_remove_to_job" value="Remove" class="btn"  />
					</td>
				</tr>
				<tr>
					<th class="head" style="width:5%;"><input id="header_checkbox" type="checkbox" value="0" onclick="selectAll(this)" /></th>
					<th style="width:12%">Logo</th>
					<th style="width:12%">Product Name</th>
					<th style="width:12%">Qty</th>
					<th style="width:24%">Box Size</th>
					<th style="width:20%">Price</th>
					<th style="width:20%">Bullet Info</th>
				</tr>
			</thead>
			<tbody>
				%for i in collections:
				<tr>
					<td class="head first"><input type="checkbox" class="cboxClass" value="${i.id}" />
						<input type="hidden" name="id" value="${i.id}"/>
					</td>
					<td>
						%for logo in i.logos:
						<a href="/upload/${logo._file_path}" class="gallery"><img src='/upload/${logo._file_path}' class="img1"></a>
						%endfor
					</td>
					<td>${i.product_desc}</td>
					<td><input type="text" value="0" name="qty_${i.id}"></td>
					<td>${i.box_size.name}</td>
					<td>${i.price}</td>
					<td>${i.bullet_info}</td>
				</tr>
				%endfor
			</tbody>
		</table>
		<div class="ca_box2" style='margin-top:20px;'>
			<fieldset class="module aligned">
				<legend>Information</legend>
				${orderingConfirmForm(value=kw)|n}
			</fieldset>
		</div>
		<div class="submit-row">
			<input type="submit" value="Submit" name="submit" onclick="javascript:if(!confirm('Are you sure?')) { return false; }"  class="default">
		</div>
	</form>
</div>