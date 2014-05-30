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
	2
	%else:
	5
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
        <div class="box3">
            <div class="blank1"></div>
            %for attr in ["washing","bleeding","various","ironing","accessories"]:
            <div class="notice1">
                <div class="notice11"><img src="/images/care_label/${getattr(detail,attr).flag}"/></div>
                <div class="notice12">${populateTranslation(getattr(detail,attr),"&nbsp;")|n}</div>
            </div>
            %endfor
        </div>
        <div class="box3">
            <div class="text1">
                <span>ORSAY GmbH<br/>Im Lossenfeld 12<br/>77731 WILLSTÄTT<br/>Germany<br /><br/>
						Ordipol Sp.z.o.o<br/>Ul. Logistyczna 1<br/>55-040 Bielany<br/>Wrocławskie,
						%if order.season=='s11':
						<br/>
						%endif
						Poland</span>
                <br/><br />
						Ordia Handelsges.<br/>MbH, Austria<br/><br />
						Ditres AG, Switzerland<br/><br />
						Ordiczech s.r.o.<br/>Czech Republic<br/><br />
						MDO Kft., Hungary<br/><br />
						Ordislovak S.R.O.<br/>Slovakia<br/><br />
						SMS Romania SRL<br/>Romania
            </div>
        </div>
    </div>
    <div class='l' id="careLabelForm">
        <ul class="css-tabs">
            <li><a href="javascript:void(0)">Care Label Item 
            	%if order.season=='s11':
				2
				%else:
				5
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
                <tr><th>Washing</th><td>${detail.washing.englisch}</td></tr>
                <tr><th>Bleeding</th><td>${detail.bleeding.englisch}</td></tr>
                <tr><th>Ironing</th><td>${detail.ironing.englisch}</td></tr>
                <tr><th>Accessories</th><td>${detail.accessories.englisch}</td></tr>
                <tr><th>Various</th><td>${detail.various.englisch}</td></tr>
            </table>
        </div>
    </div>
</div>
