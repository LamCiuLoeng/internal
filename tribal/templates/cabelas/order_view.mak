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
	$('.gallery').lightBox(); 
})
</script>
</%def>
<div id="function-menu">
	<table width="100%" cellspacing="0" cellpadding="0" border="0"><tbody>
		<tr>
			<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
			<td width="64" valign="top" align="left"><a href="/cabelas/index"><img src="/images/images/menu_cabelas_g.jpg"/></a></td>
			<td width="64" valign="top" align="left"><a href="/cabelas/ordering/index"><img src="/images/images/menu_return_g.jpg"/></a></td>
			<td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
			<td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
		</tr>
	</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Ordering</div>
<div class=main>
	<form action="/cabelas/ordering/confirm" method="POST" id="order_confirm">
		<table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:100%">
			<thead>
				<tr>
					<td colspan="80" style="border:0px;text-align:left;">
					</td>
				</tr>
				<tr>
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
					<td class='first'>
						%for logo in i.logos:
						<a href="/upload/${logo._file_path}" class="gallery"><img src='/upload/${logo._file_path}' class="img1"></a>
						%endfor
					</td>
					<td>${i.product_desc}</td>
					<td><input type="text" value="${qty_dict.get(i.id)}" name="qty_${i.id}"></td>
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
				 <div class="case-list-one">
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="bill_to_id" id="bill_to_id.label">Bill To</label></li>
				    			<li>${order.bill_to.address}</li>
				    		</ul>
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="name" id="name.label">Company</label></li>
				    			<li>${order.name}</li>
				    		</ul>
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="fax" id="fax.label">Fax</label></li>
				    			<li>${order.fax}</li>
				    		</ul>
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="contact" id="contact.label">Contact</label></li>
				    			<li>${order.contact}</li>
				    		</ul>
				    </div>
				
					
				    <div class="case-list-one">
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="ship_to_id" id="ship_to_id.label">Ship To</label></li>
				    			<li>${order.ship_to.address}</li>
				    		</ul>
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="telephone" id="telephone.label">Telephone</label></li>
				    			<li>${order.telephone}</li>
				    		</ul>
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="rcm_dcm" id="rcm_dcm.label">RCM / DCM</label></li>
				    			<li>${order.rcm_dcm}</li>
				    		</ul>
				    		<ul>
				    			<li class="label"><label class="fieldlabel" for="address" id="address.label">Address</label></li>
				    			<li>${order.address}</li>
				    		</ul>
				    </div>
				 
			</fieldset>
		</div>
	 
	</form>
</div>