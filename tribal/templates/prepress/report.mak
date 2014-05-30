<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - Prepress</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			var dateFormat = 'yy-mm-dd';
    		$('.datePicker').datepicker({firstDay: 1 , 
    									dateFormat: dateFormat
    									//minDate : new Date(2011, 0,1),
    									//maxDate : new Date(2011, 11,31)
    									});
   });
   
   function toExport(){
	   
	   
	   $("form").submit();

   }
            
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/prepress/report"><img src="/images/images/prepress_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="#" onclick="toExport()"><img src="/images/images/menu_export_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Report&nbsp;&nbsp;&gt;&nbsp;&nbsp;Prepress</div>



<!-- Main content begin -->

<div style="width:1200px;float:left">

	<div style="overflow:hidden;margin:5px 0px 10px 10px">

<form class="required reportform" method="post" action="/prepress/export">

    <div class="case-list-one">
    		<ul>
    			<li class="label"><label class="fieldlabel" for="create_time_from" id="create_time_from.label">Request Completed(from)</label></li>
    			<li><input type="text" value="" id="create_time_from" class="datePicker width-250 inputText" name="create_time_from"></li>
    		</ul>
    		<ul>
    			<li class="label"><label class="fieldlabel" for="report_type" id="report_type.label">Report Type</label></li>
    			<li>
    				<select id="report_type" class="width-250" name="report_type">
					        <option value="SUMMARY">Summary</option>
					        <!-- <option value="DESIGNER_STATISTICS">Designer Statistics</option> -->
					</select>
				</li>
    		</ul>
    </div>
	

	
    <div class="case-list-one">
		<ul>
			<li class="label"><label class="fieldlabel" for="create_time_to" id="create_time_to.label">Request Completed(to)</label></li>
			<li><input type="text" value="" id="create_time_to" class="datePicker width-250 inputText" name="create_time_to"</li>
		</ul>
    </div>
	<br class="clear"/>

	
	<br class="clear"/>
	<div class="case-list-one" id="team_div" style="display:none">
        <ul>
            <li class="label"><label class="fieldlabel">Division Team</label></li>
            <li>
                <select id="team_id" class="width-250" name="team_id">
                    % for t in teams :
                        <option value="${t.id}">${t}</option>
                    % endfor 
                </select>
            </li>
        </ul>
    </div>

</form>

	</div>
	
</div>	

<!-- Main Content end -->