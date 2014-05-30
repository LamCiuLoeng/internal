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
<script type="text/javascript" src="/js/jquery.tip.js"></script>
<script type="text/javascript" src="/js/custom/orsay_item.js"></script>
<script type="text/javascript" src="/js/custom/orsay_item1.js"></script>
<script>
$(function(){
$(".numeric").numeric();
% if action=='add':
    $('[title]').tip();
    addPartRow1();
    addAppendixRow();
% else:
    $("body").mask("Loading...");
    $.getJSON("/orsay/item1/ajaxOrderInfo",{"id":location.href.getQuery("id")}, function(res){
        var detail = res.detail;
        var order = res.order;
        var percents = res.percents;
        var materials = res.materials;
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
        changeSelect($('#size_input'), detail.size_id)
        changeSelect($('#article_desc_input'), detail.article_desc_id)
        $('#reference_no').val(detail.reference_no)
        $('#reference_color_no').val(detail.reference_color_no)
        $('#order_no').val(detail.order_no)
        changeSelect($('#orign_collection_input'), detail.orign_collection_id)
        $('#orign_location').val(detail.orign_location)
        $('#trademark').val(detail.trademark)
        var part_ids = detail.part_ids.split(',');
        for(var i=0;i<part_ids.length;i++){
            addPartRow();
            var part = $('#partLink').prev();
            changeSelect($(' > select', part), part_ids[i]);
            var materialLink = $(' > div > a', part);
            for(var j=0;j<materials[i].length;j++){
                addMaterialRow(materialLink);
                var material = materialLink.prev();
                changeSelect($(' > select', material), materials[i][j].id);
                $(' > input', material).val(percents[i][j]);
            }
        }
        var appendix_ids = detail.appendix_ids.split(',');
        for(var i=0;i<appendix_ids.length;i++){
            addAppendixRow();
            var appendix = $('#appendixLink').prev();
            changeSelect($(' > select', appendix), appendix_ids[i]);
        }
        changeSize()
        changeArticle()
        changeReferenceNo()
        changeReferenceNo()
        changeOrderNo()
        changeOrignCollection()
        changeOrignLocation()
        changeTrademark()
        writePart();
        writeAppendix();
    });
    $("body").unmask();
% endif
})
</script>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orsay/index"><img src="/images/images/menu_orsay_g.jpg"/></a></li>
        <li class='li-center'><a href="#" onclick="toConfirm(1)"><img src="/images/images/menu_confirm_g.jpg"/></a></li>
        <li class='li-center'><a href="/orsay/index" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Orsay&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Item 
	%if season=='s11':
	1
	%else:
	4
	%endif
</div>
<div class='main'>
    <form action="/orsay/item1/saveOrder" id="_form" method="post">
        <input type="hidden" name="token" value="${token}"/>
        <input type="hidden" id="order_id" name="order_id"/>
        <input type="hidden" id="detail_id" name="detail_id"/>
        <input type="hidden" id="action" name="action" value="${action}"/>
        <input type="hidden" id="season" name="season" value="${season}"/>
        <input type="hidden" id="company_code" name="company_code"/>
        <input type="hidden" id="cust_name" name="cust_name"/>
        <input type="hidden" id="size_id" name="size_id"/>
        <input type="hidden" id="article_desc_id" name="article_desc_id"/>
        <input type="hidden" id="orign_collection_id" name="orign_collection_id"/>
        <input type="hidden" id="part_ids" name="part_ids"/>
        <input type="hidden" id="material_ids" name="material_ids"/>
        <input type="hidden" id="material_percents" name="material_percents"/>
        <input type="hidden" id="appendix_ids" name="appendix_ids"/>
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
                <tr class="last"><th>TELEPHONE(BILL TO)</th><td><input type="text" name="billto_tel_no" id="billto_tel_no"/></td></tr>
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
            <div class='box2'>
                <div class='blank1'></div>
                <div class='size1' id="size1">
                    <div class="size11" id="size11"></div>
                    <div class="size12" id="size12"></div>
                    <div class="size13" id="size13"></div>
                </div>
                <div class='article1' id="article1"></div>
                <div class='number1' id="number1">
                    <div class="number11" id="number11"></div>
                    <div class="number12" id="number12"></div>
                </div>
                <div class='collection1' id="collection1"></div>
                <div class='location1' id="location1"></div>
                <div class='trademark1' id="trademark1"></div>
            </div>
            <div class='box2'>
                <div class="block1">
                    <div class='part1' id="part1"></div>
                    <div class='appendix1' id="appendix1"></div>
                </div>
                <div class="blank2"></div>
            </div>
        </div>
        <div class='l' id="careLabelForm">
            <ul class="css-tabs">
                <li><a href="javascript:void(0)">Care Label Item 
                	%if season=='s11':
					1
					%else:
					4
					%endif
				</a></li>
            </ul>
            <div class="css-panes">
                <table class='table2' border="0" cellspacing="0" cellpadding="0">
                    <tr><th class='first'>Customer Order No:<span class="red">*</span></th><td class='first'>
                            <input type="text" name="customer_po" id="customer_po" />
                        </td></tr>
                    <tr><th>Total this order Quantity (pieces):<span class="red">*</span></th><td>
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
                    <tr><th>Size:<span class="red">*</span></th><td>
                            <select id="size_input" onchange="changeSize()">
                                <option value="0">please select size</option>
                                % for a in sizeList:
                                <option value="${a.id},${a.name},${a.name_euro},${a.name_slo}">${a.name}; EUR ${a.name_euro}; SLO ${a.name_slo}</option>
                                % endfor
                            </select>
                        </td></tr>
                    <tr><th>Article description:<span class="red">*</span></th><td>
                            <select id="article_desc_input" onchange="changeArticle()">
                                <option value="0">please select Article description</option>
                                % for a in articleList:
                                <option value="${a.id},${populateTranslation(a)}">${a.englisch}</option>
                                % endfor
                            </select>
                        </td></tr>
                    <tr><th>Reference code:<span class="red">*</span></th><td><input type='text' id="reference_no" name="reference_no" class="numeric" onblur="changeReferenceNo()" title="Must be 6-digit number."/></td></tr>
                    <tr><th>Reference color code:<span class="red">*</span></th><td><input type='text' id="reference_color_no" name="reference_color_no" class="numeric" onblur="changeReferenceNo()" title="Must be 2-digit number."/></td></tr>
                    <tr><th>Order no:<span class="red">*</span></th><td><input type='text' id="order_no" name="order_no" class="numeric" onblur="changeOrderNo()" title="Must be 6-digit number."/></td></tr>
                    <tr><th>Orign collection:<span class="red">*</span></th><td>
                            <select id="orign_collection_input" onchange="changeOrignCollection()">
                                <option value="0">please select origh collection</option>
                                % for a in collectionList:
                                <option value="${a.id},${a.name}">${a.name}</option>
                                % endfor
                            </select>
                        </td></tr>
                    <tr><th>Orign location:<span class="red">*</span></th><td><input type="text" id="orign_location" name="orign_location" onblur="changeOrignLocation()"/></td></tr>
                    <tr><th>Trademark:<span class="red">*</span></th><td>
                            <select name="trademark" id="trademark" onchange="changeTrademark()">
                                <option value="">please select trademark</option>
                                <option value=""></option>
                                <option value="LORSAY&reg;">LORSAY&reg;</option>
                                <option value="ORSAY&reg;">ORSAY&reg;</option>
                            </select>
                    </td></tr>
                    <tr><th>Part:<span class="red">*</span></th><td>
                            <a id="partLink" href="javascript:void(0)" onclick="addPartRow()">add more part</a><br/>
                        </td></tr>
                    <tr><th>Appendix:</th><td>
                            <a id="appendixLink" href="javascript:void(0)" onclick="addAppendixRow()">add more appendix</a><br/>
                        </td></tr>
                </table>
            </div>
        </div>
    </form>
</div>
<div id="partDiv" class="none">
    <select class="partClass1" onchange="changePart(this)">
        <option value="0">please select part</option>
        % for a in partList:
        <option value="${a.id},${populateTranslation(a)}">${a.englisch}</option>
        % endfor
    </select>
    <a href="javascript:void(0)" onclick="delPartRow(this)"><span>Delete</span></a>
    <div class='material1'>
        Material: <span style="color:red;">input: 0%  remainder: 100%</span><br/>
        <a href="javascript:void(0)" onclick="addMaterialRow(this)">add more material</a>
    </div>
</div>
<div id="materialDiv" class="none">
    <input type='text' class="numeric" onblur="changeMaterialPercent(this)" />%
    <select onchange="changeMaterial(this)">
        <option value="0">please select material</option>
        % for a in materialList:
            % if a.begin:
                <optgroup label="${a.kurzel}">
            % endif
            <option value="${a.id},${populateTranslation(a)}">${a.englisch}</option>
            % if a.end:
                </optgroup>
            % endif
        % endfor
    </select>
    <a href="javascript:void(0)" onclick="delMaterialRow(this)"><span>Delete</span></a>
</div>
<div id="appendixDiv" class="none">
    <select class="appendixClass1" onchange="changeAppendix(this)">
        <option value="0">please select appendix</option>
        % for a in appendixList:
        % if a.begin:
        <optgroup label="${a.sub_cat}">
        % endif
        <option value="${a.id},${a.sub_cat},${populateTranslation(a)}">${a.englisch}</option>
        % if a.end:
        </optgroup>
        % endif
        % endfor
        </optgroup>
    </select>
    <a href="javascript:void(0)" onclick="delAppendixRow(this)"><span>Delete</span></a>
</div>