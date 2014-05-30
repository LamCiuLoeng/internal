<%inherit file="tribal.templates.master"/>
<%
from tribal.util.master_helper import populateTranslation1
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
<script type="text/javascript" src="/js/custom/orsay_item3.js"></script>
<script>
    $(function(){
        $(".numeric").numeric();
            % if action=='add':
            $('[title]').tip();
        addPartRow();
        addAppendixPage();
            % else:
            $("body").mask("Loading...");
        initFormVal(location.href.getQuery("id"));
        $("body").unmask();
            % endif
    })
</script>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/orsay/index"><img src="/images/images/menu_orsay_g.jpg"/></a></li>
        <li class='li-center'><a href="#" onclick="toConfirm(3)"><img src="/images/images/menu_confirm_g.jpg"/></a></li>
        <li class='li-center'><a href="/orsay/index" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Orsay&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Item 
	%if season=='s11':
	3
	%else:
	6
	%endif
</div>
<div class='main'>
    <form action="/orsay/item3/saveOrder" id="_form" method="post">
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
            <div class='box4'>
                <table border="0" cellspacing="0" cellpadding="0" style="text-align:center;">
                    <tr><td height="36">&nbsp;</td></tr>
                    <tr><td height="62" valign="top" style="font-size:20px;"><div style="width:92px;margin:0 18px;padding:5px 0;border:1px solid #000;" id="size11">&nbsp;</div></td></tr>
                    <tr><td height="36" style="line-height:18px;font-size:16px;"><span id="size12">&nbsp;</span><br/><span id="size13">&nbsp;</span><td></tr>
                    <tr><td height="115" style="font-size:11px;"><div style="margin:0 18px;" id="article1">&nbsp;</div><td></tr>
                    <tr><td height="36" style="font-size:14px;"><span id="number11">&nbsp;</span> / <span id="number12">&nbsp;</span><br/><span id="number13">&nbsp;</span></td></tr>
                    <tr><td height="72" style="font-size:14px;" id="collection1">&nbsp;</td></tr>
                    <tr><td height="36" style="font-size:14px;" id="location1">&nbsp;</td></tr>
                    <tr><td height="40" style="font-size:18px;font-weight:bold;" id="trademark1">&nbsp;</td></tr>
                </table>
            </div>
            <div class='box4'>
                <table border="0" cellspacing="0" cellpadding="0" style="text-align:left;">
                    <tr><td height="8">&nbsp;</td></tr>
                    <tr><td height="414" style="font-size:9px;line-height:12px;" valign="top">
                            <div style="margin:0 7px 0 10px;">
                                <span id="part1"></span>
                            </div>
                        </td></tr>
                </table>
            </div>
        </div>
        <div class='l' id="careLabelForm">
            <ul class="css-tabs">
            	<li><a href="javascript:void(0)">Care Label Item
	            	%if season=='s11':
					3
					%else:
					6
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
                    <tr><th>Reference Total Order Price:</th><td>&nbsp;</td></tr>
                    <tr><th>Size:<span class="red">*</span></th><td>
                            <select id="size_input" onchange="writeSize()">
                                <option value="0">please select size</option>
                                % for a in sizeList:
                                <option value="${a.id},${a.name},${a.name_euro},${a.name_slo}">${a.name}; EUR ${a.name_euro}; SLO ${a.name_slo}</option>
                                % endfor
                            </select>
                        </td></tr>
                    <tr><th>Article description:<span class="red">*</span></th><td>
                            <select id="article_input" onchange="writeArticle()">
                                <option value="0">please select Article description</option>
                                % for a in articleList:
                                <option value="${a.id},${populateTranslation(a)}">${a.englisch}</option>
                                % endfor
                            </select>
                        </td></tr>
                    <tr><th>Reference code:<span class="red">*</span></th><td><input type='text' id="reference_no" name="reference_no" class="numeric" onblur="writeReferenceNo()" title="Must be 6-digit number."/></td></tr>
                    <tr><th>Reference color code:<span class="red">*</span></th><td><input type='text' id="reference_color_no" name="reference_color_no" class="numeric" onblur="writeReferenceColorNo()" title="Must be 2-digit number."/></td></tr>
                    <tr><th>Order no:<span class="red">*</span></th><td><input type='text' id="order_no" name="order_no" class="numeric" onblur="writeOrderNo()" title="Must be 6-digit number."/></td></tr>
                    <tr><th>Orign collection:<span class="red">*</span></th><td>
                            <select id="orign_collection_input" onchange="writeOrignCollection()">
                                <option value="0">please select orign collection</option>
                                % for a in collectionList:
                                <option value="${a.id},${a.name}">${a.name}</option>
                                % endfor
                            </select>
                        </td></tr>
                    <tr><th>Orign location:<span class="red">*</span></th><td><input type="text" id="orign_location" name="orign_location" onblur="writeOrignLocation()"/></td></tr>
                    <tr><th>Trademark:<span class="red">*</span></th><td>
                            <select name="trademark" id="trademark" onchange="writeTrademark()">
                                <option value="">please select trademark</option>
                                <option value=""></option>
                                <option value="LORSAY&reg;">LORSAY&reg;</option>
                                <option value="ORSAY&reg;">ORSAY&reg;</option>
                            </select>
                    </td></tr>
                    <tr><th>Part:<span class="red">*</span></th><td>
                            <a id="partLink" href="javascript:void(0)" onclick="addPartRow()">add part</a><br/>
                        </td></tr>
                    <tr><th>Appendix:</th><td>
                            <a id="appendixPageLink" href="javascript:void(0)" onclick="addAppendixPage()">add page</a>
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
        <option value="${a.id},${populateTranslation1(a)}">${a.englisch}</option>
        % endfor
    </select>
    <a href="javascript:void(0)" onclick="delPartRow(this)"><span>Delete</span></a>
    <div class='material1'>
        Material: <span style="color:red;">input: 0%  remainder: 100%</span><br/>
        <a href="javascript:void(0)" onclick="addMaterialRow(this)">add material</a>
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
            <option value="${a.id},${populateTranslation1(a)}">${a.englisch}</option>
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
            <option value="${a.id},${a.sub_cat},${populateTranslation1(a)}">${a.englisch}</option>
            % if a.end:
        </optgroup>
        % endif
        % endfor
        </optgroup>
    </select>
    <a href="javascript:void(0)" onclick="delAppendixRow(this)"><span>Delete</span></a>
</div>
<div id="appendixPageDiv" class="none">
    <a href="javascript:void(0)" onclick="delAppendixPage(this)"><span class="r">Delete Page</span></a>
    <a href="javascript:void(0)" onclick="addAppendixRow(this)">add appendix</a>
</div>
<div id="appendixPage">
    <table border="0" cellspacing="0" cellpadding="0" style="text-align:left;">
        <tr><td height="36">&nbsp;</td></tr>
        <tr><td height="397" style="font-size:7px;line-height:8px;" valign="top">
                <div style="margin:0 7px 0 10px;"></div>
            </td></tr>
    </table>
</div>