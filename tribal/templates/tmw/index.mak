<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - TMW</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/flora.datepicker.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<style>
.highlight{
   color:white;
   background-color:green;
}
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.tools.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/ui.datepicker.js" language="javascript"></script>

<script type="text/javascript" src="/js/custom/tmw.js" language="javascript"></script>

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
  	<!-- <td width="64" valign="top" align="left"><a href="/tag/index"><img src="/images/images/menu_tag_g.jpg"/></a></td> -->
  	<td width="64" valign="top" align="left"><a href="javascript:toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:toExport()"><img src="/images/images/menu_export_g.jpg"/></a></td>
        <!-- <td width="64" valign="top" align="left"><a href="javascript:addSO()"><img src="/images/images/menu_addso_g.jpg"/></a></td> -->
        <!-- <td width="64" valign="top" align="left"><a href="javascript:toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td> -->
        <!-- <td width="64" valign="top" align="left"><a href="javascript:toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td> -->
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">TMW&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main</div>

<div style="width:1300px;margin:0px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
	<form id="search_form" name="DataTable" class="tableform" method="post" action="index">
		<input type="hidden" name="latest" value="0" />
		${search_form(value=values)|n}
	</form>
	</div>
</div>

<div id="recordsArea">
<form id="record_form" method="post" action="/tmw/export">
<input type="hidden" name="item_ids" value="" id="item_ids"/>

%if tmpl_context.paginators.collections:
	<table width="100%" class="gridTable" cellpadding="0" cellspacing="0" border="0">
		<%
			label_attrs = [('Filename',"40"), ('TAG.FORMAT',"60"), ("QTY","30"),('POFILE.ID',"60"), ('VENDOR.ID',"100"), \
                    ('VENDOR.NAME',"60"), ('TICKET.NAME',"30"), ("SZN.TAG","20"), ('ITEMCODE',"70"), ('ENGLISH.SIZE',"60"),
                    ('RETAIL.PRICE',"60"), ('COMP.PRICE',"60"), ('CDF.DESC',"60"), ('LOT',"60"), ('MODEL',"60"),
                    ('COUNTRY.OF.ORIGIN',"60"), ('COLOR.DESC',"60"), ('TAG.VENDOR',"60"), ('INSEAM',"60"),
                ]

			my_page = tmpl_context.paginators.collections
			pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
		%>
		<thead>
			%if my_page.item_count > 0 :
			<tr>

				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="3">
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
			<td>${item.filename|b}</td>
            <td>${item.tag_format|b}</td>
            <td>${item.qty|b}</td>        
            <td>${item.pofile_id|b}</td>
            <td>${item.vendor_id|b}</td>
            <td>${item.vendor_name|b}</td>
            <td>${item.ticket_name|b}</td>
            <td>${item.szn_tag|b}</td>
            <td>${item.item_code|b}</td>
            <td>${item.english_size|b}</td>
            <td>${item.retail_price|b}</td>
            <td>${item.comp_price|b}</td>
            <td>${item.cdf_desc|b}</td>
            <td>${item.lot|b}</td>
            <td>${item.model|b}</td>
            <td>${item.country_of_origin|b}</td>
            <td>${item.color_desc|b}</td>
            <td>${item.tag_vendor|b}</td>
            <td>${item.inseam|b}</td>
			</tr>
			% endfor

			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="3">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} record s</span>
				</td>
			</tr>
			%endif
		</tbody>
	</table>
</form>
</div>
%endif
