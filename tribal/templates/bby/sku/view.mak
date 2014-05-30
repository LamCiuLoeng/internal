<%inherit file="tribal.templates.master"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>



<%def name="extTitle()">r-pac</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/colorbox.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/bby.css" type="text/css" media="screen"/>
	<style type="text/css">
	<!--
	td {
		font-family: Tahoma, Geneva, sans-serif;
		font-size: 12px;
		line-height: normal;
		color: #000;
		text-decoration: none;
		border-color : black;
	}

	.date-session{
		list-style : none;
		padding-left : 0px;
	}
	.date-session li{
		padding : 3px;
		margin-bottom : 3px;
		overflow : auto;
	}
	.confirm{
		border : 1px solid gray;
	}
	.enlarge{
		cursor : url(/images/magnify.cur);
	}
	-->
	</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.colorbox-min.js" language="javascript"></script>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			$("a[rel='sku_imgs']").colorbox({maxWidth:'800px',maxHeight:'800px'});
		});
		
		function toSubmit(){
		  return confirm("Are you sure to submit the record?");
		}
		
		function toCancel(){
		  return confirm("Are you sure to cancel the record?");
		}
		
		function toHold(){
		  return confirm("Are you sure to hold the record?");
		}
		
		function toCopy(){
		  return confirm("Are you sure to copy this record to create a new one?");
		}
		
		function toDelete(){
		  return confirm("[Warning] Are you sure to delete this record ? All the info will be lost !");
		}
		
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="175" valign="top" align="left"><a href="/sku/index"><img src="/images/mainmenu_g.jpg"/></a></td>
  	%if has_permission("BBY_EDIT"):	
  		%if obj.is_complete() or obj.is_eol():
  			%if has_permission("BBY_EDIT_COMPLETE"):
  			   <td width="64" valign="top" align="left"><a href="/sku/update?id=${obj.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
  			%endif
  		%elif obj.is_cancel():
  			<td width="64" valign="top" align="left"><a href="/sku/action?id=${obj.id}&t=ACTIVE"><img src="/images/images/menu_active_g.jpg"/></a></td>
  		%else:
  			<td width="64" valign="top" align="left"><a href="/sku/update?id=${obj.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
            <td width="64" valign="top" align="left"><a href="/sku/submit?id=${obj.id}" onclick="return toSubmit();"><img src="/images/images/menu_submit_g.jpg"/></a></td>		
  			%if obj.is_on_hold():
  				<td width="64" valign="top" align="left"><a href="/sku/action?id=${obj.id}&t=UNLOCK"><img src="/images/images/menu_unlock_g.jpg"/></a></td>
  			%else:
	  			<td width="64" valign="top" align="left"><a href="/sku/action?id=${obj.id}&t=CANCEL" onclick="return toCancel();"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
  				<td width="64" valign="top" align="left"><a href="/sku/action?id=${obj.id}&t=ON_HOLD" onclick="return toHold();"><img src="/images/images/menu_hold_g.jpg"/></a></td>
			%endif
		%endif
		<td width="64" valign="top" align="left"><a href="/sku/copy?id=${obj.id}" onclick="return toCopy();"><img src="/images/images/menu_copy_g.jpg"/></a></td>
		<td width="64" valign="top" align="left"><a href="/sku/delete?id=${obj.id}" onclick="return toDelete();"><img src="/images/images/menu_delete_g.jpg"/></a></td>	
  	%endif
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;New SKU</div>



<!-- Main content begin -->
	<div id="tabsJ">
		<ul>
			<li id="current"><a href="view?id=${obj.id}"/><span>Item Information</span></a></li>
			<li><a href="pcr?id=${obj.id}"/><span>PCR</span></a></li>
			<li><a href="history?id=${obj.id}"/><span>History</span></a></li>
		</ul>
	</div>
	<div><br class="clear"/></div>
	
<div style="overflow:hidden;margin:5px 0px 10px 10px">
		
	<div style="width:1200px;">
		<div style="float:left;width:860px">
		  
		    
	        %if obj.is_eol():
                <table border="1" cellpadding="3" cellspacing="0" class="eol">
            %else:
                <table border="1" cellpadding="3" cellspacing="0">
            %endif
				<tr>
					<td width="150" height="30"  class="title-td">SKU#</td>
					<td>${obj.sku}&nbsp;
					    %if obj.is_eol():
					       <b><span class="red">(EOL)</span></b>
						%elif obj.is_complete():
							<b><span class="red">(COMPLETED)</span></b>
						%elif obj.is_cancel():
							<b><span class="red">(CANCEL)</span></b>
						%elif obj.is_on_hold():
							<b><span class="red">(ON HOLD)</span></b>
						%endif
					</td>
					<td width="150" class="title-td">Brand</td>
					<td width="250">${obj.brand}&nbsp;</td>
				</tr>
				<tr>
					<td width="150" height="30"  class="title-td">Agent</td>
					<td width="250">${obj.agent}&nbsp;</td>
					<td width="150" class="title-td">Vendor</td>
					<td width="250">${obj.vendor}&nbsp;</td>
				</tr>
				<tr>
					<td width="150" height="30"  class="title-td">Package Format</td>
					<td>${obj.packaging_format}&nbsp;</td>
					<td width="150" class="title-td">UPC#</td>
					<td>${obj.upc_no}&nbsp;</td>
				</tr>
				<tr>
					<td width="150" height="30"  class="title-td">Closure</td>
					<td>${obj.closure}&nbsp;</td>
					<td width="150" class="title-td">Display Mode</td>
					<td>${obj.display_mode}&nbsp;</td>
				</tr>
				<tr>
					<td width="150" height="30" class="title-td">IOQ</td>
					<td>${obj.ioq}&nbsp;</td>
					<td width="150"class="title-td">AOQ</td>
					<td>${obj.aoq}&nbsp;</td>
				</tr>
				<tr>
					<td width="150" height="30"  class="title-td">Product Descrption</td>
					<td colspan="3">${obj.product_description}&nbsp;</td>
				</tr>
				<tr>
					<td width="150" height="30"  class="title-td">PD</td>
					<td>${obj.pd}&nbsp;</td>
					<td class="title-td">AE</td>
					<td>${obj.ae}&nbsp;</td>
				</tr>
				<tr>
					<td width="150" height="30"  class="title-td">Formed Size</td>
					<td colspan="3">${obj.formed_size}&nbsp;&nbsp;(L * W * H  Unit:inch)</td>
				</tr>
				<tr>
					<td width="150" height="30"  class="title-td">Asia Packaging Team Contact</td>
					<td>${obj.bby_asia_contact}&nbsp;</td>
					<td class="title-td">US Packaging Team Contact</td>
					<td>${obj.bby_us_contact}&nbsp;</td>
				</tr>
			</table>
		</div>
		<div style="float:right;width:300px;text-align:center">
			%for index,img in enumerate(images):
				%if index == 0:
				<a href="/upload/${img._file_path.replace('\\','/')}" rel="sku_imgs" title="${img.file_name}">
				%else:
				<a href="/upload/${img._file_path.replace('\\','/')}" rel="sku_imgs" title="${img.file_name}" style="display:none">
				%endif
				<img src="/upload/${img._file_path.replace('\\','/')}" width="200" height="200" title="Click to see the enlarge photo." class="sku_images" style="cursor:url(/images/magnify.cur)"/></a>
			%endfor
			%if images:
				<p>Totals ${len(images)} images</p>
			%endif
		</div>
		<br class="clear"/>
	</div>
		<br />
		
		<table border="1" cellpadding="3" cellspacing="0">
			<tr>
				<td class="title-td" style="width:180px">Item</td>
				<td class="title-td" style="width:120px">Date</td>
				<td class="title-td" style="width:250px">Attachment</td>
				<td class="title-td" style="width:250px">Remark</td>
				<td class="title-td" style="width:50px">Confirm</td>
			</tr>
			
			%for row in obj.sku_info:
				${show_row(row)}
			%endfor
			
		</table>
<!-- Main Content end -->



<%def name="show_row(v)">
	<tr>
		<td rowspan="${len(v.row_detail) or 1}">${v.row_name}&nbsp;</td>
		%if v.row_detail:
			${show_detail(v.row_detail[0])}
		%else:
			<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
		%endif
	</tr>
		
	%if v.row_detail:
		%for r in v.row_detail[1:]:
			<tr>
			${show_detail(r)}
			</tr>
		%endfor
	%endif
</%def>


<%def name="show_detail(r)">
	${show_td(r)}${r["date"]}&nbsp;</td>
	${show_td(r)}
		%if r["files"]:
			%for f in r['files']:
				<a href="/sku/download?id=${f["file_id"]}">${f["file_name"]}</a>&nbsp;&nbsp;
			%endfor
		%endif
		&nbsp;
	</td>
	${show_td(r)}${r["remark"]}&nbsp;</td>
	${show_td(r)}
		%if r["confirm"]:
			YES
		%endif
		&nbsp;
	</td>
</%def>

<%def name="show_td(c)">
	%if c['confirm']:
		<td class="confirm">
	%else:
		<td>
	%endif
</%def>