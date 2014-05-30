<%inherit file="tribal.templates.master"/>
<%
	from tribal.util.master_helper import populateTranslation
	from tribal.util.mako_filter import b
%>
<%def name="extTitle()">r-pac - Orsay</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/orsay.css"/>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orsay/index"><img src="/images/images/menu_orsay_g.jpg"/></a></li>
        <li class='li-center'><a href="/orsay/editOrder?id=${order.id}"><img src="/images/images/menu_revise_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Orsay&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Item 
	%if order.season=='s11':
	1
	%else:
	4
	%endif
</div>
<div class='main'>
    <div class='box1 bg1'>
        <table class='table1' border="0" cellspacing="0" cellpadding="0">
            <tr><th>Customer</th><td>${order.cust_name}</td></tr>
            <tr><th>ADDRESS(BILL TO)</th><td>${order.billto_address}&nbsp;</td></tr>
            <tr><th>CONTACT(BILL TO)</th><td>${order.billto_contact_sales}&nbsp;</td></tr>
            <tr class="last"><th>TELEPHONE(BILL TO)</th><td>${order.billto_tel_no}&nbsp;</td></tr>
        </table>
    </div>
    <div class='box1 bg2'>
        <table class='table1' border="0" cellspacing="0" cellpadding="0">
            <tr><th>ADDRESS(SHIP TO)</th><td>${order.shipto_address}&nbsp;</td></tr>
            <tr><th>CONTACT(SHIP TO)</th><td>${order.shipto_contact_person | b}&nbsp;</td></tr>
            <tr class="last"><th>TELEPHONE(SHIP TO)</th><td>${order.shipto_tel_no}&nbsp;</td></tr>
        </table>
    </div>
    <hr class='space'>
    <div id="careLabelImage">
        <div class='box2'>
            <div class='blank1'></div>
            <div class='size1' id="size1">
                <div class="size11" id="size11">SIZE ${detail.size.name}</div>
                <div class="size12" id="size12">EUR ${detail.size.name_euro}</div>
                <div class="size13" id="size13">SLO ${detail.size.name_slo}</div>
            </div>
            <div class='article1' id="article1">${populateTranslation(detail.article_desc)}</div>
            <div class='number1' id="number1">
                <div class="number11" id="number11">${detail.reference_no}/${detail.reference_color_no}</div>
                <div class="number12" id="number12">${detail.order_no}</div>
            </div>
            <div class='collection1' id="collection1">${detail.orign_collection.name}</div>
            <div class='location1' id="location1">Made in ${detail.orign_location}</div>
            <div class='trademark1' id="trademark1">${detail.trademark}</div>
        </div>
        <div class='box2'>
            <div class="block1">
                <div class='part1' id="part1">
                    <% i=0 %>
                    % for a in detail.parts:
                    <div class="part11">
                        ${populateTranslation(a)}
                    </div>
                        <% j=0 %>
                        % for b in materials[i]:
                        <div>
                            <div class="material11">${percents[i][j]}%</div>
                             <div class="material12">${populateTranslation(b)}</div>
                            <% j=j+1 %>
                        </div>
                        % endfor
                    <% i=i+1 %>
                    % endfor
                </div>
                <div class='appendix1' id="appendix1">
                    <% i=0 %>
                    % for a in detail.appendixs:
                    <div class="appendix11">${populateTranslation(a)}</div>
                    <% i=i+1 %>
                    % endfor
                </div>
            </div>
            <div class="blank2"></div>
        </div>
    </div>
    <div class='l' id="careLabelForm">
        <ul class="css-tabs">
            <li><a href="javascript:void(0)">Care Label Item 
	        	%if order.season=='s11':
				1
				%else:
				4
				%endif
			</a></li>
        </ul>
        <div class="css-panes">
            <table class='table2' border="0" cellspacing="0" cellpadding="0">
                <tr><th class='first'>Customer Order No:</th><td class='first'>${order.customer_po}</td></tr>
                <tr><th>Total this order Quantity (pieces):</th><td>${order.qty}</td></tr>
                <tr><th>Reference Total Order Price:</th><td>&nbsp;
                        <div id="amt_div" style="display:none">&nbsp;
                            <span class="currenty_flag"></span>
                            <span id="unitPrice"></span> <b>X</b>
                            <span id="qty_show"></span> <b>=</b>
                            <span class="currenty_flag"></span>
                            <span id="amt"></span>
                        </div>
                    </td></tr>
                <tr><th>Size:</th><td>${detail.size.name}; EUR ${detail.size.name_euro}; SLO ${detail.size.name_slo}</td></tr>
                <tr><th>Article description:</th><td>${detail.article_desc.polnisch}</td></tr>
                <tr><th>Reference code:</th><td>${detail.reference_no}</td></tr>
                <tr><th>Reference color code:</th><td>${detail.reference_color_no}</td></tr>
                <tr><th>Order no:</th><td>${detail.order_no}</td></tr>
                <tr><th>Orign collection:</th><td>${detail.orign_collection.name}</td></tr>
                <tr><th>Orign location:</th><td>${detail.orign_location}</td></tr>
                <tr><th>Trademark:</th><td>${detail.trademark}</td></tr>
                <tr><th>Part:</th><td>
                    <% i=0 %>
                    % for a in detail.parts:
                    <div class="part1">
                        %if a:
                        <span style="font-weight:bold">${a.englisch}</span><br/>
                        %endif
                        <% j=0 %>
                        % for b in materials[i]:
                            ${percents[i][j]}% ${b.englisch}<br/>
                            <% j=j+1 %>
                        % endfor
                    <% i=i+1 %>
                    </div>
                    % endfor
                    </td></tr>
                <tr><th>Appendix:</th><td>
                    % for a in detail.appendixs:
                    ${a.englisch}<br/>
                    % endfor
                    </td></tr>
            </table>
        </div>
    </div>
</div>