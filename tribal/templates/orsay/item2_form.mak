<%inherit file="tribal.templates.master"/>
<%
	from tribal.util.master_helper import populateTranslation
%>
<%def name="extTitle()">r-pac - Orsay</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/jquery.loadmask.css"/>
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/orsay.css"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js"></script>
<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js"></script>
<script type="text/javascript" src="/js/custom/orsay_item.js"></script>
<script type="text/javascript" src="/js/custom/orsay_item2.js"></script>
<script>
$(function(){
$(".numeric").numeric();
% if action=='add':

% else:
    $("body").mask("Loading...");
    $.getJSON("/orsay/item2/ajaxOrderInfo",{"id":location.href.getQuery("id")}, function(res){
        var detail = res.detail;
        var order = res.order;
        $('#order_id').val(order.id);
        $('#detail_id').val(detail.id);
        $('#company_code').val(order.company_code)
        $('#cust_name').val(order.cust_name)
        $('#cust_code').val(order.cust_code)
        $('#billto_address').val(order.billto_address)
        $('#billto_contact_sales').val(order.billto_contact_sales)
        $('#billto_tel_no').val(order.billto_tel_no)
        $('#shipto_address').val(order.shipto_address)
        $('#shipto_contact_person').val(order.shipto_contact_person)
        $('#shipto_tel_no').val(order.shipto_tel_no)
        $('#customer_po').val(order.customer_po);
        $('#qty').val(order.qty);
        var washings = ['washing', 'bleeding', 'various', 'ironing', 'accessories']
        for(var i=0;i<washings.length;i++){
            var type = washings[i]
            var obj = detail[type];
            $("#"+type).val(obj.id)
            $("#"+type+"_img").attr("src", '/images/care_label/'+obj.flag);
            $("#"+type+"_content").text(getTransaction(obj));
        }
    })
    $("body").unmask();
% endif
})
</script>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orsay/index"><img src="/images/images/menu_orsay_g.jpg"/></a></li>
        <li class='li-center'><a href="#" onclick="toConfirm(2)"><img src="/images/images/menu_confirm_g.jpg"/></a></li>
        <li class='li-center'><a href="/orsay/index" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Orsay&nbsp;&nbsp;&gt;&nbsp;&nbsp;Item 
	%if season=='s11':
	2
	%else:
	5
	%endif
</div>
<div class='main'>
    <form action="/orsay/item2/saveOrder" id="_form" method="post">
        <input type="hidden" name="token" value="${token}"/>
        <input type="hidden" id="order_id" name="order_id"/>
        <input type="hidden" id="detail_id" name="detail_id"/>
        <input type="hidden" id="action" name="action" value="${action}"/>
        <input type="hidden" id="season" name="season" value="${season}"/>
        <input type="hidden" id="company_code" name="company_code"/>
        <input type="hidden" id="cust_name" name="cust_name"/>
        <div class='box1 bg1'>
            <table class='table1' border="0" cellspacing="0" cellpadding="0">
                <tr><th>Customer</th><td>
                        <select name="cust_code" id="cust_code" onchange="getCustomerInfo(this)">
                            <option value=""></option>
                            %for c in customerList:
                            <option value="${c[0]}">${c[1]}</option>
                            %endfor
                        </select>
                    </td></tr>
                <tr><th>ADDRESS(BILL TO)</th><td><textarea name="billto_address" id="billto_address"></textarea></td></tr>
                <tr><th>CONTACT(BILL TO)</th><td><input type="text" name="billto_contact_sales" id="billto_contact_sales"/></td></tr>
                <tr class="last"><th>ADDRESS(BILL TO)</th><td><input type="text" name="billto_tel_no" id="billto_tel_no"/></td></tr>
            </table>
        </div>
        <div class='box1 bg2'>
            <table class='table1' border="0" cellspacing="0" cellpadding="0">
                <tr><th>ADDRESS(SHIP TO)</th><td><textarea name="shipto_address" id="shipto_address"></textarea></td></tr>
                <tr><th>CONTACT(SHIP TO)</th><td><input type="text" name="shipto_contact_person" id="shipto_contact_person"/></td></tr>
                <tr class="last"><th>TELEPHONE(SHIP TO)</th><td><input type="text" name="shipto_tel_no" id="shipto_tel_no"/></td></tr>
            </table>
        </div>
        <hr class='space'>
        <div id="careLabelImage">
            <div class="box3">
                <div class="blank1"></div>
                <div class="notice1">
                    <div class="notice11"><img src="/images/blank.png" id="washing_img"/></div>
                    <div class="notice12" id="washing_content"></div>
                </div>
                <div class="notice1">
                    <div class="notice11"><img src="/images/blank.png" id="bleeding_img"/></div>
                    <div class="notice12" id="bleeding_content"></div>
                </div>
                <div class="notice1">
                    <div class="notice11"><img src="/images/blank.png" id="various_img"/></div>
                    <div class="notice12" id="various_content"></div>
                </div>
                <div class="notice1">
                    <div class="notice11"><img src="/images/blank.png" id="ironing_img"/></div>
                    <div class="notice12" id="ironing_content"></div>
                </div>
                <div class="notice1">
                    <div class="notice11"><img src="/images/blank.png" id="accessories_img"/></div>
                    <div class="notice12" id="accessories_content"></div>
                </div>
            </div>
            <div class="box3">
                <div class="text1" style='line-height:19px;'>
                    <span>ORSAY GmbH<br/>Im Lossenfeld 12<br/>77731 WILLSTÄTT<br/>Germany<br /><br/>
						Ordipol Sp.z.o.o<br/>Ul. Logistyczna 1<br/>55-040 Bielany<br/>Wrocławskie,
						%if season=='s11':
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
						%if season=='s12':
						<br/><br />
						Ukrasay LLC
						<br/>Ukraine
						%endif
                </div>
            </div>
        </div>
        <div class='l' id="careLabelForm">
            <ul class="css-tabs">
                <li><a href="javascript:void(0)">Care Label Item 
                	%if season=='s11':
					2
					%else:
					5
					%endif
				</a></li>
            </ul>
            <div class="css-panes">
                <table class='table2' border="0" cellspacing="0" cellpadding="0">
                    <tr><th class='first'>Customer Order No:</th><td class='first'>
                            <input type="text" name="customer_po" id="customer_po" />
                        </td></tr>
                    <tr><th>Total this order Quantity (pieces):</th><td>
                            <input type="text" name="qty" id="qty" class="numeric" />
                        </td></tr>
                    <tr><th>Reference Total Order Price:</th><td>&nbsp;
                            <div id="amt_div" style="display:none">&nbsp;
                                <span class="currenty_flag"></span>
                                <span id="unitPrice"></span> <b>X</b>
                                <span id="qty_show"></span> <b>=</b>
                                <span class="currenty_flag"></span>
                                <span id="amt"></span>
                            </div>
                        </td></tr>
                    <tr><th>Washing</th>
                        <td>
                            <select name="washing" id="washing" class="wi-select">
                                <option value=""></option>
                                %for o in washing["Washing"]:
                                <option value="${o.id}">${o.englisch}</option>
                                %endfor
                            </select>
                        </td></tr>
                    <tr>
                        <th>Bleeding</th>
                        <td>
                            <select name="bleeding" id="bleeding" class="wi-select">
                                <option value=""></option>
                                %for o in washing["Bleeding"]:
                                <option value="${o.id}">${o.englisch}</option>
                                %endfor
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th>Various</th>
                        <td>
                            <select name="various" id="various" class="wi-select">
                                <option value=""></option>
                                %for o in washing["Various"]:
                                <option value="${o.id}">${o.englisch}</option>
                                %endfor
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th>Ironing</th>
                        <td>
                            <select name="ironing" id="ironing" class="wi-select">
                                <option value=""></option>
                                %for o in washing["Ironing"]:
                                <option value="${o.id}">${o.englisch}</option>
                                %endfor
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th>Accessories</th>
                        <td>
                            <select name="accessories" id="accessories" class="wi-select">
                                <option value=""></option>
                                %for o in washing["Accessories"]:
                                <option value="${o.id}">${o.englisch}</option>
                                %endfor
                            </select>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </form>
</div>