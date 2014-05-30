<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - LEMMI</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<style>

.highlight{
   color:white;
   background-color:green;
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.tools.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>

<script type="text/javascript" src="/js/custom/lemmi.js" language="javascript"></script>

<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
	    	// highlight select
	    	$(".gridTable tbody td :checkbox").click(function() {
			    // chk = $(":checkbox",$(this).parents('tr'));
			    if($(this).attr("checked")==false){
					$(this).attr("checked",false);
				    var sid = $(this).parents('tr').attr("sid");
				    sid = parseInt(sid);
				    if(sid%2==0){
			    	      $(this).parents('tr').removeClass();
				      $(this).parents('tr').addClass('odd');
				    }else{
				      $(this).parents('tr').removeClass('highlight');
				    }
			    }else{
			    	$(":checkbox",$(this).parents('tr')).attr("checked",true);
			    	$(this).parents('tr').removeClass();
			    	$(this).parents('tr').addClass('highlight');
			    }
       		});
		});
               
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/lemmi/index"><img src="/images/images/menu_index_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="javascript:toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:toExport()"><img src="/images/images/menu_export_g.jpg"/></a></td>
     <!--
        <td width="64" valign="top" align="left"><a href="javascript:addSO()"><img src="/images/images/menu_addso_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
     -->
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">LEMMI&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main</div>

<div style="width:1300px;margin:0px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
	<form id="search_form" name="DataTable" class="tableform" method="post" action="index">
		<input type="hidden" name="latest" value="0" />
		${search_form(value=values)|n}
	</form>
	</div>
</div>

<div id="recordsArea">
<form id="record_form" method="post" action="/lemmi/export">
<input type="hidden" name="item_ids" value="" id="item_ids"/>

%if tmpl_context.paginators.collections:
	<table width="90%" class="gridTable" cellpadding="0" cellspacing="0" border="0">
		<%
			label_attrs = [('OrderNumber',"40"), ('Type',"30"), ('Sender',"40"), 
			                 ('Created',"30"),('DispatchDate',"20"), 
			                 ('CountryOfOrigin',"20"), ('VendorNumber',"30"), 
			                 ('CompanyName', '40'), ('SourceFile', '40')]
			my_page = tmpl_context.paginators.collections
			pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
		%>
		<thead>
			%if my_page.item_count > 0 :
			<tr>

				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="${len(label_attrs) + 1}">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
			<tr>
				<th width="8"><input type="checkbox" value="all" /></th>
				% for label,width in label_attrs:
					<th width="${width}">${label}</th>
				% endfor
			</tr>
		</thead>
		<tbody>
			% for index,item in enumerate(my_page.items):

			%if index%2==0:
			<tr class="odd" height="25" sid="${index}">
			%else:
			<tr class="even" height="25" sid="${index}">
			%endif
            <td><input type="checkbox" name="ids" value="${item.id}" /></td>
			<td>${item.orderNumber|b}</td>
			<td>${item.type|b}</td>  
			<td>${item.sender|b}</td>  
			<td>${Date2Text(item.created, dateTimeFormat='%Y-%m-%d %H:%M:%S')|b}</td>   
			<td>${Date2Text(item.dispatchDate)|b}</td>   
			<td>${item.countryOfOrigin|b}</td>  
			<td>${item.vendorNumber|b}</td>  
			<td>${item.companyName|b}</td> 
			<td>${item.filename|b}</td>                          
			</tr>
			% endfor

			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="${len(label_attrs) + 1}">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
		</tbody>
	</table>
</form>
</div>
%endif
