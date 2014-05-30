<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Structural/Flexible Development</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/glowbutton.css" type="text/css" media="screen"/>
<style type="text/css">
.subform-info{padding-bottom:10px;padding-left:100px;padding-right:0px;padding-top:10px;margin:0px;width:800px;float:left;}
.subform-action{width:250px;padding-top:10px;padding-right:10px;margin:0px;float:right;text-align:right;}
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.color.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.glowbuttons.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
$(document).ready(function(){
	
})
</script>
</%def>

<div id="function-menu">
	<table width="100%" cellspacing="0" cellpadding="0" border="0">
    	<tr>
		  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
		  	<td width="64" valign="top" align="left"><a href="/sample/index"><img src="/images/images/menu_pd_g.jpg"/></a></td>
		  	<td width="64" valign="top" align="left"><a href="/sample/viewRequest?id=${id}"><img src="/images/images/menu_return_g.jpg"/></a></td>
		  	<td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
		    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  		</tr>
	</table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Structural/Flexible Development&nbsp;&nbsp;&gt;&nbsp;&nbsp;History</div>
<!-- Main content begin -->
<div style="width:1500px;">
<div style="width:1200px;float:left">
	<div id="recordsArea" style="margin:5px 0px 10px 10px">
      <table cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			<tr> 
				<th width="200">Job No</th>
	    		<th width="200">Region</th>
	    		<th width="150">Vendor</th>
	    		<th width="150">Program</th>
	    		<th width="150">Project</th>
	    		<th width="120">Item Code</th>
	    		<th width="120">Reqeust Date</th>
	    		<th width="120">Issued By</th>
	    	</tr>
		</thead>
		<tbody>
			% for index,c in enumerate(result):
	    	%if index %2 == 0 :
			<tr class="even">
  			%else:
			<tr class="odd">
  			%endif
  				<td style="border-left:1px solid #ccc"><a href="/sample/viewHistory?id=${c.id}">${str(c.main)}</a></td>
  				<td>&nbsp;${c.main.project_own}</td>
  				<td>&nbsp;${c.main.customer}</td>
  				<td>&nbsp;${c.main.program}</td>
  				<td>&nbsp;${c.main.project}</td>
  				<td>&nbsp;${c.main.item_code}</td>
  				<td>&nbsp;${c.main.create_time.strftime("%Y/%m/%d")}</td>
  				<td>&nbsp;${c.main.create_by}</td>
			</tr>
			%endfor
		</tbody>
	</table>
  </div>
</div>

</div>