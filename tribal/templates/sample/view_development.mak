<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Structural/Flexible Development</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>

<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			var dateFormat = 'yy-mm-dd';
    		$('.datePicker').datepicker({firstDay: 1 , dateFormat: dateFormat});
    		$(".status-bar").each(function(){
    		  var t = $(this);
    		  t.progressbar( {value:t.attr("percentage")} );
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
  	<td width="64" valign="top" align="left"><a href="/sample/viewRequest?id=${main.id}"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Structural/Flexible Development&nbsp;&nbsp;&gt;&nbsp;&nbsp;Development Log</div>


<!-- Main content begin -->
<div style="width:1200px;float:left">

	<div class="clear"><br /></div>
	<div id="recordsArea" style="margin:5px 0px 10px 10px">
      <table cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			<tr>
	    		<th width="120" height="30">Job No</th>
	    		<th width="150">Tab ${show_direction('sub_form_id')}</th>
	    		<th width="130">Time ${show_direction('create_time')}</th>
	    		<th width="100">Person ${show_direction('update_by_id')}</th>
	    		<th width="100">Action ${show_direction('action_type')}</th>
	    		<th width="450">Remark</th>
	    	</tr>
		</thead>
		<tbody>
			% for index,d in enumerate(result):
	    	%if index %2 == 0 :
  				<tr class="even">
  			%else:
  				<tr class="odd">
  			%endif
				<td style="border-left:1px solid #ccc">&nbsp;${d.system_no if d.system_no  else d.main.system_no}</td>
				<td>&nbsp;${"" if not d.sub_form_type else "%s [id=%s]" %(d.sub_form.getWidget().label,d.sub_form_id)}</td>
				<td>&nbsp;${d.create_time.strftime("%Y/%m/%d %H:%M:%S")}</td>
				<td>&nbsp;${d.create_by}</td>
				<td>&nbsp;${d.action_type}</td>
				<td style="text-align:left">${d.remark.replace('\n','<br />')|n}</td>
			%endfor
		</tbody>
	</table>
  </div>
</div>	

<!-- Main Content end -->


<%def name="show_direction(f)">
	%if field == f:
		%if direction == 'desc':
			<a href="/sample/viewDevelopmentLog?id=${main.id}&f=${f}&d=asc"><img src="/images/down.png"/></a>
		%else:
			<a href="/sample/viewDevelopmentLog?id=${main.id}&f=${f}&d=desc"><img src="/images/up.png"/></a>
		%endif
	%else:
		<a href="/sample/viewDevelopmentLog?id=${main.id}&f=${f}&d=desc"><img src="/images/updown.gif"/></a>
	%endif
</%def>