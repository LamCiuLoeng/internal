<%inherit file="tribal.templates.master"/>
<%
	from tribal.util.mako_filter import b, tp
	from tribal.util.common import Date2Text
	from tribal.util.common import rpacEncrypt
%>
<%def name="extTitle()">r-pac - PEI</%def>
<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<link rel="stylesheet" href="/css/custom/orsay.css" type="text/css" />
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.tools.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/trb_search.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/orsay_item.js" language="javascript"></script>
</%def>
<div class='submenu' id="function-menu">
    <ul>
        <li class='li-start'></li>
        <li class='li-center'><a href="/pei/index"><img src="/images/images/menu_pei_g.jpg"/></a></li>
        <li class='li-center'><a href="#" onclick="toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;PEI&nbsp;&nbsp;&gt;&nbsp;&nbsp;View Order List</div>
<div class="main">
    <div>
        <form action="/pei/search" class="tableform" id="_form" method="post">
			${widget(value=values)|n}
        </form>
        <%
            my_page = tmpl_context.paginators.result
            pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
        %>
        <div class="clear"></div>
        <table class="gridTable" cellpadding="0" cellspacing="0" border="0">
            <thead>
                <tr>
                    <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="6">
						${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                    </td>
                </tr>
                <tr>
                    <th>Buyer PO#</th>
                    <th>Vendor PO#</th>
                    <th>Required Date</th>
                    <th>Total Quantity</th>
                    <th>View Detail</th>
                </tr>
            </thead>
            <tbody>
				% for index,header in enumerate(my_page.items):
				%if index%2==0:
                <tr class="odd">
				%else:
                <tr class="even">
				%endif
                    <td style="border-left:1px solid #ccc">${header.buyerPO}</td>
                    <td>${header.vendorPO}</td>
                    <td>${Date2Text(header.shipDate,)}</td>
                    <td>${header.totalQty}</td>
                    <td><a href="/pei/viewOrder?code=${rpacEncrypt(header.id)}">Detail</a></td>
                </tr>
				%endfor
                <tr>
                    <td style="text-align:right;border-right:0px;border-bottom:0px" colspan="6">
                        ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>