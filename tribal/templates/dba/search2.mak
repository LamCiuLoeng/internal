<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text, rpacEncrypt
%>

<%def name="extTitle()">r-pac - PLAYTEX / WONDERBRA / SHOCK ABSORBER</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/thickbox.css" type="text/css" />
<style>
#tooltipdiv {
    display:none;
    background:transparent url(/images/jqueryTools/white_arrow.png);
    font-size:12px;
    height:70px;
    width:160px;
    padding:25px;
}
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.tools.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.columnfilters.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>
<script type="text/javascript" src="/js/thickbox-compressed.js" language="javascript"></script>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    $(document).ready(function(){
        var dateFormat = 'yy-mm-dd';

        $(".datePicker").datepicker({firstDay: 1 , dateFormat: dateFormat});
        $(".v_is_date").attr("jVal",
        "{valid:function (val) {if(val!=''){return /^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$/.test(val) }return true;}, message:'YYYY-MM-DD', styleType:'cover'}");
        $(".tooltip").tooltip('#tooltipdiv');
    });

    var search_url = "/dba2/search";

    function toSearch(){
	var f = $(".tableform");
	$(f).attr("action", search_url).submit();
    }
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
        <!--
  	<td width="64" valign="top" align="left"><a href="/dba2/search"><img src="/images/images/menu_trb_g.jpg"/></a></td>
        -->
    <td width="64" valign="top" align="left">
    	<a href="javascript:toSearch()">
    		<img src="/images/images/menu_search_g.jpg"/>
    	</a>
    </td>
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">PLAYTEX / WONDERBRA / SHOCK ABSORBER&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Search</div>
<div style="width:1200px;margin:0px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
		<form name="DataTable" class="tableform" method="post" action="index">
			<div>
				${search_form(value=values)|n}
			</div>
		</form>
	</div>
</div>
%if collections:
<div id="recordsArea" style="margin:5px 0px 10px 20px">
	<table class="gridTable" cellpadding="0" cellspacing="0" border="0">
		<%
			label_attrs = [('Customer PO#',"200"), ('Customer Name',"280"), ('Created By',"200"), 
                        ('Create Time',"200"), ('Request Ship Date',"100"), ('Delivery Date',"100"),
                          ('SOB#',"160")]
                        my_page = tmpl_context.paginators.collections
			pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
		%>
		<thead>

			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="${len(label_attrs)}">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
			<tr>
				% for label,width in label_attrs:
					<th width="${width}">${label}</th>
				% endfor
			</tr>
		</thead>
		<tbody>
                       % for index,order in enumerate(collections):

			%if index%2==0:
			<tr class="odd" height="26">
			%else:
			<tr class="even" height="26">
			%endif
				<td>
				<a href="/dba2/viewOrder?code=${rpacEncrypt(order.id)}">${order.po}</a>&nbsp;
				</td>
                                <td>${order.customer.name}</td>
                                <td>${order.create_by.user_name|b}</td>
				<td>${Date2Text(order.create_time, '%Y-%m-%d %H:%M:%S')|b}</td>
                                <td>${(order.ship_date if order.ship_date else '')|b}</td>
                                <td>${(order.delivery_date if order.delivery_date else '')|b}</td>
                                <td>${(order.sob if order.sob else '')|b}</td>
			</tr>
			% endfor

			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="${len(label_attrs)}">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
		</tbody>
	</table>
</div>
%endif
<div id="tooltipdiv"></div>