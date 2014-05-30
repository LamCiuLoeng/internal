<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Structural/Flexible Development</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.progressbar.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			var dateFormat = 'yy-mm-dd';
    		$(".status-bar").each(function(){
          $(this).progressBar();
        });
			
		});

	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/sample/index"><img src="/images/images/menu_pd_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Structural/Flexible Development&nbsp;&nbsp;&gt;&nbsp;&nbsp;History</div>


<!-- Main content begin -->
<div style="width:1200px;float:left">

	<div class="clear"><br /></div>
	<div id="recordsArea" style="margin:5px 0px 10px 10px">
      <table cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			<tr> 
	    		<th width="50">Version</th>
				  <th width="180">Job No</th>
	    		<th width="150">Vendor/Customer</th>
	    		<th width="150">Program</th>
	    		<th width="150">Project</th>
	    		<th width="120">Item Code</th>
	    		<th width="120">Reqeust Date</th>
	    		<th width="120">Issued By</th>
				  <th width="150">Status</th>
	    	</tr>
		</thead>
		<tbody>
			% for index,h in enumerate(result):
	    	%if index %2 == 0 :
  				<tr class="even">
  			%else:
  				<tr class="odd">
  			%endif
				<td style="border-left:1px solid #ccc">&nbsp;${h.revision}</td>
				<td><a target="_blank" href="/sample/viewRequest?id=${h.id}">${str(h)}</a></td>
				<td>&nbsp;${h.customer}</td>
				<td>&nbsp;${h.program}</td>
				<td>&nbsp;${h.project}</td>
				<td>&nbsp;${h.item_code}</td>
				<td>&nbsp;${h.create_time.strftime("%Y/%m/%d %H:%M")}</td>
				<td>&nbsp;${h.create_by}</td>
		    <td>&nbsp;<span class="status-bar">${"%d%%" % (h.percentage*100)}</span></td>
		    %endfor
		</tbody>
	</table>
  </div>
</div>	

<!-- Main Content end -->