<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Orchestra</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orchestra/${team}/list_order"><img src="/images/images/menu_return_g.jpg"/></a></li>
        <li class='li-center'><a href="/orchestra/${team}/edit_order?id=${order.id}"><img src="/images/images/menu_revise_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Orchestra&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order&nbsp;&nbsp;&gt;&nbsp;&nbsp;Show</div>
<div class='main'>
	<div class="ca_box1">
	    <fieldset class="module aligned">
	        <legend>Bill To</legend>
	        <div class="form-row">
	            <label>Name:</label>${order.billto_name}
	        </div>
	        <div class="form-row">
	            <label>Address:</label>${order.billto_address}
	        </div>
	        <div class="form-row">
	            <label>Contact:</label>${order.billto_contact}
	        </div>
	        <div class="form-row">
	            <label>Telephone:</label>${order.billto_telephone}
	        </div>
	        <div class="form-row last">
	            <label>Email:</label>${order.billto_email}
	        </div>
	    </fieldset>
	</div>
	<div class="ca_box1">
	    <fieldset class="module aligned">
	        <legend>Ship To</legend>
	        <div class="form-row">
	            <label>Name:</label>${order.shipto_name}
	        </div>
	        <div class="form-row">
	            <label>Address:</label>${order.shipto_address}
	        </div>
	        <div class="form-row">
	            <label>Contact:</label>${order.shipto_contact}
	        </div>
	        <div class="form-row">
	            <label>Telephone:</label>${order.shipto_telephone}
	        </div>
	        <div class="form-row last">
	            <label>Email:</label>${order.shipto_email}
	        </div>
	    </fieldset>
	</div>
	<div class="ca_box2">
	    <fieldset class="module aligned">
	    	<legend>Care Labe Development</legend>
	    	<div class="form-row">
	            <label><span class="red">*</span>Item:</label>${order.item.name}
	            %if order.item.info1:
	            & ${order.item.info1}${order.item_info1}
	            %endif
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>Customer PO#:</label>${order.customer_po}
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>Sku:</label>${order.sku}
	        </div>
	        %if team=='HK':
            <div class="form-row">
	            <label><span class="red">*</span>Age&Height:</label>${order.height}
	        </div>
            %elif team=='SH':
            <div class="form-row">
	            <label><span class="red">*</span>Age&Height:</label>${order.height}
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>Age&Head Size:</label>${order.head_size}
	        </div>
            %endif
	        <div class="form-row">
	            <label>Specification:</label>${order.specification}
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>Product Family:</label>${order.product_family.english}<br/>
	            language: ${order.product_family_langs}
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>Origin:</label>${order.origin.name}
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>CA Number:</label>${order.ca_no}
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>Composition:</label>
	            <div class=content>
	            %if order.fabrics:
		            %for fabric_index, i in enumerate(order.fabrics):
		            	<div style='float:left;margin:0 15px 15px 0;background:#fff;'>
				        	%if i:
				        	${i.english}
				        	%endif
				        	<div style='background:#fefe9a;border:1px solid #ddd;padding:3px;'>
				        	%for composition_index, j in enumerate(order.compositions[fabric_index]):
				        	${order.percents[fabric_index][composition_index]}% ${j.english}<br/>
				        	%endfor
				        	</div>
				        </div>
		            %endfor
		        %endif
	           	</div>
	        </div>
	        <div class="form-row">
	            <label><span class="red">*</span>Care Img:</label>
	            <div class=content>
	            %if order.care_imgs:
		            %for i in order.care_imgs:
		            	<img src='${i.path}'>
		            %endfor
	            %endif
	            </div>
	        </div>
	        <div class="form-row last">
	            <label>Care Washing:</label>
	            <div class=content>
	            %if order.care_ids:
	            %for i in order.cares:
	            ${i.english}<br/>
	            %endfor
	            %endif
	            </div>
	        </div>
	    </fieldset>
	</div>
</div>