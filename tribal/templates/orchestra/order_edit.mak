<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Orchestra</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/inlines.min.js"></script>
<script type="text/javascript" src="/js/custom/orchestra.js?1"></script>
<script>
var customers_json = ${customers_json|n};
</script>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orchestra/${team}/show_order?id=${order.id}"><img src="/images/images/menu_return_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Orchestra&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order&nbsp;&nbsp;&gt;&nbsp;&nbsp;New</div>
<div class='main'>
    <form action="/orchestra/${team}/save_order" id="_form" method="post">
    	<input type='hidden' name='id' id='id' value='${order.id}'/>
    	<input type='hidden' name='care_img_ids' id='care_img_ids'/>
    	<div class="ca_box1">
            <fieldset class="module aligned">
                <legend>Bill To</legend>
                <div class="form-row">
                    <label>Customer:</label>
                    <select name='billto_customer_id' onchange='changeCustomer(this)'>
                    	<option></option>
                		%for i in customers:
                		%if i.team==team:
                		<option value='${i.id}' ${'selected=true' if order.billto_customer_id==i.id else ''}>${i.name}</option>
                		%endif
                		%endfor
                	</select>
                </div>
                <div class="form-row">
                    <label>Name:</label>
                    <input type="text" name="billto_name" id="billto_name" value='${order.billto_name}'/>
                </div>
                <div class="form-row">
                    <label>Address:</label>
                    <textarea name="billto_address" id="billto_address">${order.billto_address}</textarea>
                </div>
                <div class="form-row">
                    <label>Contact:</label>
                    <input type="text" name="billto_contact" id="billto_contact" value='${order.billto_contact}'/>
                </div>
                <div class="form-row">
                    <label>Telephone:</label>
                    <input type="text" name="billto_telephone" id="billto_telephone" value='${order.billto_telephone}'/>
                </div>
                <div class="form-row last">
                    <label>Email:</label>
                    <input type="text" name="billto_email" id="billto_email" value='${order.billto_email}'/>
                </div>
            </fieldset>
        </div>
        <div class="ca_box1">
            <fieldset class="module aligned">
                <legend>Ship To</legend>
                <div class="form-row">
                    <label>Customer:</label>
                    <select name='shipto_customer_id' onchange='changeCustomer(this)'>
                    	<option></option>
                		%for i in customers:
                		%if i.team==team:
                		<option value='${i.id}' ${'selected=true' if order.shipto_customer_id==i.id else ''}>${i.name}</option>
                		%endif
                		%endfor
                	</select>
                </div>
                <div class="form-row">
                    <label>Name:</label>
                    <input type="text" name="shipto_name" id="shipto_name" value='${order.shipto_name}'/>
                </div>
                <div class="form-row">
                    <label>Address:</label>
                    <textarea name="shipto_address" id="shipto_address">${order.shipto_address}</textarea>
                </div>
                <div class="form-row">
                    <label>Contact:</label>
                    <input type="text" name="shipto_contact" id="shipto_contact" value='${order.shipto_contact}'/>
                </div>
                <div class="form-row">
                    <label>Telephone:</label>
                    <input type="text" name="shipto_telephone" id="shipto_telephone" value='${order.shipto_telephone}'/>
                </div>
                <div class="form-row last">
                    <label>Email:</label>
                    <input type="text" name="shipto_email" id="shipto_email" value='${order.shipto_email}'/>
                </div>
            </fieldset>
        </div>
		<div class="ca_box2">
            <fieldset class="module aligned">
            	<legend>Care Labe Development</legend>
		    	<div class="form-row">
		    		<label><span class="red">*</span>Item:</label>
		    		<select name='item_id' id='item_id' onchange='changeItem()' class='required'/>
		    			%for i in items:
		    			%if i.team==team or not i.team:
		    			<option value='${i.id}' ${'selected=true' if order.item_id==i.id else ''}>${i.name}
		    				%if i.info1:
		    					& ${i.info1}
		    				%endif
		    			</option>
		    			%endif
		    			%endfor
		    		</select>
		    		<input type='text' name='item_info1' value='${order.item_info1}' class='required'/>
		        </div>
            	<div class="form-row">
            		<label><span class="red">*</span>Customer PO#:</label>
		    		<input type='text' name='customer_po' value='${order.customer_po}'/>
		    	</div>
                <div class="form-row">
                    <label><span class="red">*</span>Sku:</label>
                    <input type="text" name="sku" id="sku" class='required' value='${order.sku}'/>
                </div>
                
                %if team=='HK':
                <div class="form-row">
                    <label><span class="red">*</span>Age&Height:</label>
                    <input type="text" name="height" id="height" value='${order.height}'/>
                </div>
                %elif team=='SH':
                <div class="form-row">
                    <label>Age&Height:</label>
                    <input type="text" name="height" id="height" value='${order.height}'/>
                </div>
                <div class="form-row">
                    <label>Age&Head Size:</label>
                    <input type="text" name="head_size" id="head_size" value='${order.head_size}'/>
                </div>
                %endif
                <div class="form-row">
                    <label>Specification:</label>
                    <input type="text" name="specification" id="specification" value='${order.specification}'/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Product Family:</label>
                    <div class='content'>
                    	<% pre_pf = None %>
	                    <select name='product_family_id' class='required'>
	                    	%for index,i in enumerate(product_familys):
	                    		%if i.type!=pre_pf:
	                    		</optgroup>
	                    		%endif
	                    		%if not pre_pf or i.type!=pre_pf:
	                    		<optgroup label="${i.type}">
	                    		%endif
	                    		<option value='${i.id}' ${'selected=true' if order.product_family_id==i.id else ''}>${i.english}</option>
	                    		%if index==len(product_familys)-1:
	                    		</optgroup>
	                    		%endif
	                    		<% pre_pf = i.type %>
	                    	%endfor
	                   </select><br/>
	                    <input type='checkbox' name='product_family_langs' value='french' class='required' ${'checked=true' if 'french' in order.product_family_langs.split(',') else ''}>French
	                    <input type='checkbox' name='product_family_langs' value='english' class='required' ${'checked=true' if 'english' in order.product_family_langs.split(',') else ''}/>English
	                    <input type='checkbox' name='product_family_langs' value='arabic' class='required' ${'checked=true' if 'arabic' in order.product_family_langs.split(',') else ''}/>Arabic
	                </div>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Origin:</label>
                    <select name='origin_id' class='required'>
                    	%for i in origins:
                    		<option value='${i.id}' ${'selected=true' if order.origin_id==i.id else ''}>${i.english}</option>
                    	%endfor
                    </select>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>CA Number:</label>
                    <input type="text" name="ca_no" id="ca_no" class="numeric required" value='${order.ca_no}'/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Composition:</label>
                    <div class='content' id='fabric-group'>
                		<input type="hidden" name="fabric_set-TOTAL_FORMS" value="${len(order.fabrics)}" id="id_fabric_set-TOTAL_FORMS" />
                		<input type="hidden" name="fabric_set-MAX_NUM_FORMS" id="id_fabric_set-MAX_NUM_FORMS" />
                		%if order.fabrics:
				            %for fabric_index, fabric in enumerate(order.fabrics):
				            <div class="inline-related dynamic-form" style='float:left;margin:0 15px 15px 0;background:#fff;'>
			            		<select name='fabric_set-${fabric_index}-fabric_ids' style='width:200px;'>
		                    		<option></option>
			                    	%for i in fabrics:
			                    		%if i:
			                    		<option value='${i.id}' ${'selected=true' if (fabric and i.id==fabric.id) else ''}>${i.english}</option>
			                    		%endif
			                    	%endfor
			                    </select>&nbsp;&nbsp;&nbsp;&nbsp;
			                    <a class="deletelink" href="javascript:void(0)" onclick="delFabric(this)"></a>
			                    <div style='background:#fefe9a;border:1px solid #ddd;padding:3px;'>
			                    	%for composition_index, composition in enumerate(order.compositions[fabric_index]):
						        	<div>
				                		<input type='text' name='fabric_set-${fabric_index}-composition_percents' class='required' style='width:25px;text-align:right;' value='${order.percents[fabric_index][composition_index]}'/>%
				                        <select name='fabric_set-${fabric_index}-composition_ids' style='width:200px;'>
				                        	%for i in compositions:
				                        		<option value='${i.id}' ${'selected=true' if (composition and i.id==composition.id) else ''}>${i.english}</option>
				                        	%endfor
				                        </select>
				                        &nbsp;&nbsp;&nbsp;&nbsp;
				                    </div>
						        	%endfor
				                    <a href='javascript:void(0)' onclick='addComposition(this)' class='a_add_composition'>Add Composition</a>
			                    </div>
					        </div>
				            %endfor
				        %endif
                    	<div class="empty-form inline-related" id="fabric_set-empty" style='float:left;margin:0 15px 15px 0;background:#fff;'>
	                    	<select name='fabric_set-__prefix__-fabric_ids' style='width:200px;'>
	                    		<option></option>
		                    	%for i in fabrics:
		                    		<option value='${i.id}'>${i.english}</option>
		                    	%endfor
		                    </select>&nbsp;&nbsp;&nbsp;&nbsp;
		                    <a class="deletelink" href="javascript:void(0)" onclick="delFabric(this)"></a>
		                    <div style='background:#fefe9a;border:1px solid #ddd;padding:3px;'>
			                    <div>
			                		<input type='text' name='fabric_set-__prefix__-composition_percents' class='required' style='width:25px;text-align:right;'/>%
			                        <select name='fabric_set-__prefix__-composition_ids' style='width:200px;'>
			                        	%for i in compositions:
			                        		<option value='${i.id}'>${i.english}</option>
			                        	%endfor
			                        </select>
			                        &nbsp;&nbsp;&nbsp;&nbsp;
			                    </div>
			                    <a href='javascript:void(0)' onclick='addComposition(this)' class='a_add_composition'>Add Composition</a>
		                    </div>
	                    </div>
                    </div>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Care Img:</label>
                    <div class='content'>
                    	<h4>Wash:</h4>
                    	<ul class='ul1'>
                    	%for i in care_imgs:
                    		%if team==i.team and (i.type == 'washing' or i.type == 'wash'):
	                    	<li><input type='radio' name='_care_img_wash' value='${i.id}' class='required' ${'checked=true' if str(i.id) in order.care_img_ids.split(',') else ''}/>&nbsp;<img src='${i.path}'></li>
	                    	%endif
	                    %endfor
	                    </ul>
	                    <hr class=thin>
	                    <h4>Bleach:</h4>
                    	<ul class='ul1'>
                    	%for i in care_imgs:
                    		%if team==i.team and (i.type == 'bleaching' or i.type == 'bleach'):
	                    	<li><input type='radio' name='_care_img_bleach' value='${i.id}' class='required' ${'checked=true' if str(i.id) in order.care_img_ids.split(',') else ''}/>&nbsp;<img src='${i.path}'></li>
	                    	%endif
	                    %endfor
	                    </ul>
	                    <hr class=thin>
	                    <h4>Dry:</h4>
                    	<ul class='ul1'>
                    	%for i in care_imgs:
                    		%if team==i.team and (i.type == 'drying' or i.type == 'dry'):
	                    	<li><input type='radio' name='_care_img_dry' value='${i.id}' class='required' ${'checked=true' if str(i.id) in order.care_img_ids.split(',') else ''}/>&nbsp;<img src='${i.path}'></li>
	                    	%endif
	                    %endfor
	                    </ul>
	                    <hr class=thin>
	                    <h4>Iron:</h4>
                    	<ul class='ul1'>
                    	%for i in care_imgs:
                    		%if team==i.team and (i.type == 'ironing' or i.type == 'iron'):
	                    	<li><input type='radio' name='_care_img_iron' value='${i.id}' class='required' ${'checked=true' if str(i.id) in order.care_img_ids.split(',') else ''}/>&nbsp;<img src='${i.path}'></li>
	                    	%endif
	                    %endfor
	                    </ul>
	                    <hr class=thin>
	                    <h4>Dry Clean:</h4>
                    	<ul class='ul1'>
                    	%for i in care_imgs:
                    		%if team==i.team and (i.type == 'cleaning' or i.type == 'clean'):
	                    	<li><input type='radio' name='_care_img_clean' value='${i.id}' class='required' ${'checked=true' if str(i.id) in order.care_img_ids.split(',') else ''}/>&nbsp;<img src='${i.path}'></li>
	                    	%endif
	                    %endfor
	                    </ul>
                    </div>
                </div>
                <div class="form-row last">
                    <label>Care Washing:</label>
                    <div class='content'>
                    	%if order.care_ids:
                    	%for care_index,care in enumerate(order.cares):
                    	<div>
	                        <select name='care_ids'>
	                        	<option></option>
	                        	%for i in cares:
	                        		<option value='${i.id}' ${'selected=true' if care.id==i.id else ''}>${i.english}</option>
	                        	%endfor
	                        </select>&nbsp;&nbsp;&nbsp;&nbsp;
	                        %if care_index>0:
	                        <a class="deletelink" href="javascript:void(0)" onclick="delCare(this)"></a>
	                        %endif
                    	</div>
                    	%endfor
                    	%else:
                    	<div>
	                        <select name='care_ids'>
	                        	<option></option>
	                        	%for i in cares:
	                        		<option value='${i.id}'>${i.english}</option>
	                        	%endfor
	                        </select>&nbsp;&nbsp;&nbsp;&nbsp;
                    	</div>
                    	%endif
                    	<a href='javascript:void(0)' onclick='addCare(this)' id='a_add_care'>Add Care translation</a>
                    </div>
                </div>
            </fieldset>
        </div>
        <div class="submit-row" >
            <input type="button" value="Save" class="default" name="_create" onclick='toConfirm()'/>
            <input type="button" value="Save as New" class="default" name="_create" onclick='toCreate()'/>
        </div>
    </form>
</div>