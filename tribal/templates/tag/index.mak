<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
	from tribal.util.tag_util import returnIds, returnFormat
%>

<%def name="extTitle()">r-pac - TAG</%def>

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

<script type="text/javascript" src="/js/custom/tag.js" language="javascript"></script>

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
  	<td width="64" valign="top" align="left"><a href="/tag/index"><img src="/images/images/menu_tag_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="javascript:toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:toExport()"><img src="/images/images/menu_export_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:addSO()"><img src="/images/images/menu_addso_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
        <td width="64" valign="top" align="left"><a href="javascript:toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left">
    	<img height="21" width="23" src="/images/images/menu_last.jpg"/>
    </td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">TAG&nbsp;&nbsp;&gt;&nbsp;&nbsp;Main</div>

<div style="width:1300px;margin:0px;">
	<div style="overflow:hidden;margin:5px 0px 5px 0px">
	<form id="search_form" name="DataTable" class="tableform" method="post" action="index">
		<input type="hidden" name="latest" value="0" />
		${search_form(value=values)|n}
	</form>
	</div>
</div>

<div id="recordsArea">
<form id="record_form" method="post" action="/tag/export">
<input type="hidden" name="item_ids" value="" id="item_ids"/>
<input type="hidden" name="xls_format" value="" id="xls_format"/>
<!--
<div class="gridTable" style="width:800px;margin:6px 0 0 10px;">
    <span style="color:red; font-weight: bold;">*Flapdoodles Export Format:</span>
    <span><input type="radio" name="flap_format" value="Flapdoodles_905">905 &nbsp;</span>
    <span><input type="radio" name="flap_format" value="Flapdoodles_925">925 &nbsp;</span>
    <span><input type="radio" name="flap_format" value="Flapdoodles_940">940 &nbsp;</span>
    <span><input type="radio" name="flap_format" value="Flapdoodles">New &nbsp;</span>
</div>
-->
%if tmpl_context.paginators.collections:
	<table width="90%" class="gridTable" cellpadding="0" cellspacing="0" border="0">
		<%
			label_attrs = [('PO#',"60"), ("Style","30"),('SO NO',"110"), ('SO Remark',"100"), \
                        ('TAG NO',"30"), ('PO UNITS',"30"), ("Brand","20"), ('Attachment Set',"70"), ('Latest Version',"60")]

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
            <%
               ids = returnIds(item[0], item[1], item[2],item[3],item[4],item[6],item[7],item[8])
               format = returnFormat(item[6], item[4])
            %>
            <td><input type="checkbox" name="ids" value="${ids}" alt="${item[6]|b}" ref="${format}" /></td>
			<td>${item[0]|b}</td>
			<td>${item[1]|b}</td>
            <td><span id="so_${ids}">${item[2]|b}</span></td>
            <td><span id="soRemark_${ids}">${item[3]|b}</span></td>
            <td>${item[4]|b}</td>
            <td>${item[5]|b}</td>
			<td>${item[6]|b}</td>
            <td>${item[7]|b}</td>  
            <td>${item[8]|b}</td>                
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
