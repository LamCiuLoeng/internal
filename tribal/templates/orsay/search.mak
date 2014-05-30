<%inherit file="tribal.templates.master"/>
<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>
<%def name="extTitle()">r-pac - Orsay</%def>
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
        <li class='li-center'><a href="/orsay/index"><img src="/images/images/menu_orsay_g.jpg"/></a></li>
        <li class='li-center'><a href="#" onclick="toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></li>
        <li class='li-end'></li>
    </ul>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Orsay&nbsp;&nbsp;&gt;&nbsp;&nbsp;View Order List</div>
<div class="main">
    <div>
        <form action="/orsay/search" class="tableform" id="_form" method="post">
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
                    <th>Customer</th>
                    <th>Customer POPO#</th>
                    <th>Total Qty</th>
                    <th>E-mail Subject</th>
                    <th>Confirmed Time</th>
                    <th>View Detail</th>
                </tr>
            </thead>
            <tbody>
				% for index,r in enumerate(my_page.items):
				%if index%2==0:
                <tr class="odd">
				%else:
                <tr class="even">
				%endif
                    <td style="border-left:1px solid #ccc">${r.cust_name}</td>
                    <td>${r.customer_po}</td>
                    <td>${r.qty}</td>
                    <td>${r.email_subject}</td>
                    <td>${Date2Text(r.create_time,)}</td>
                    <td><a href="/orsay/viewOrderByID?id=${r.id}">Detail</a></td>
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