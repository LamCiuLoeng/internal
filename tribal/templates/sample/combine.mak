<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - Structural/Flexible Development - Combine</%def>

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
<script type="text/javascript" src="/js/jquery.progressbar.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>


<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
			var dateFormat = 'yy-mm-dd';
    		$('.datePicker').datepicker({firstDay: 1 , dateFormat: dateFormat});
            $("input[name='ids']").bind('click',addTo);
		});

		function selectall(obj,name){
            var t = $(obj);
            if(t.attr('checked')){
                $("input[type='checkbox'][name='"+name+"']").attr('checked','checked');
            }else{
                $("input[type='checkbox'][name='"+name+"']").removeAttr('checked');
            }
            addTo();
        }

		
		function toSearch(){
			$(".searchform").submit();
		}

        function toCombine(){
            if($("#target :selected").length < 1){
                alert('Please select the job to combine to!');
                return false;
            }
            if(!$("#reason").val()){
                alert('Please into the reason why to combine the jobs !');
                return false;
            }
        
            if(window.confirm('Are you sure to combine the jobs ? That is irreversible operation!!')){
                $(".combineform").submit();
            }else{
                return false;
            }
        }
        
        function addTo(){
            var html = '';
            $("input[name='ids']:checked").each(function(){
                var t = $(this);
                html += '<option value="'+t.val()+'">'+t.attr('ref')+'</option">';
            });
            $("#target").html(html);
        }
		
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/sample/index"><img src="/images/images/menu_pd_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="#" onclick="toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Structural/Flexible Development&nbsp;&nbsp;&gt;&nbsp;&nbsp;Combine</div>



<!-- Main content begin -->
<div style="width:1500px;">

<div style="width:1200px;float:left">
	<div style="overflow:hidden;margin:5px 0px 10px 10px">			
		<form action="/sample/combine" method="post" class="required searchform">
		<div class="case-list-one" style="width:1200px">
		    <ul style="width:1100px">
                <li class="label"><label for="jobs" class="fieldlabel">Job Number</label></li>
                <li style="width:900px">
                    <input type="text" id="jobs" style="width:750px" class="inputText" name="jobs" value="${values.get('jobs','')}">
                    &nbsp;&nbsp;(Splited with ",")
                </li>
            </ul>
		</div>
		</form>
	</div>
	<div class="clear"><br /></div>
	<div id="recordsArea" style="margin:5px 0px 10px 10px">
	  <form action="/sample/combineSave" method="post" class="required combineform">
	  <p>Combine into :
	     <select name="target" id="target"></select>
	  Reason : <textarea name="reason" id="reason"></textarea>
	     <input type="button" value="Confirm To Combine" onclick="toCombine()"/>
	  </p>
      <table cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			<tr>
			    <th>&nbsp;<input type="checkbox" onclick="selectall(this,'ids')"/></th>
				<th width="180" height="30">Job No</th>
	    		<th width="100">Region</th>
	    		<th width="150">Vendor/Customer</th>
	    		<th width="150">Corporate Customer</th>
	    		<th width="150">Brand</th>
	    		<th width="120">Reqeustor</th>
	    		<th width="120">Reqeust Date</th>
	    	</tr>
		</thead>
		<tbody>
			% for index,h in enumerate(result):
		    	%if index %2 == 0 :
					<tr class="even">
				%else:
					<tr class="odd">
				%endif					
					%if h.active == 1 :
					   <td style="border-left:1px solid #ccc">&nbsp;</td>
					   <td><a href="/sample/viewRequest?id=${h.id}" style="color: red;">${str(h)}</a></td>
					%else:
					   <td style="border-left:1px solid #ccc"><input type="checkbox" name="ids" value="${h.id}" ref="${str(h)}"/></td>
					   <td><a href="/sample/viewRequest?id=${h.id}">${str(h)}</a></td>
					%endif
					<td>&nbsp;${h.project_own}</td>
					<td>&nbsp;${h.customer}</td>
					<td>&nbsp;${h.program}</td>
					<td>&nbsp;${h.project}</td>
					<td>&nbsp;${h.create_by}</td>
					<td>&nbsp;${h.create_time.strftime("%Y/%m/%d %H:%M")}</td>
			%endfor

		</tbody>
	</table>
	</form>
  </div>
</div>	


</div>
<!-- Main Content end -->