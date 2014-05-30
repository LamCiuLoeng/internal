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
   		
    		$(".status-bar").each(function(){
    		  $(this).progressBar();
    		});
    		
    		// don't use this function yet
    		 $(".ajaxSearchField").each(function(){
		        var jqObj = $(this);
		        jqObj.autocomplete("/sample/ajaxField", {
		        	extraParams: {fieldName: jqObj.attr("name")},
		            formatItem: function(item){return item[0]},
		            matchCase: false,
		            mustMatch: true 
		        }).result(function(event, item){
		    	  	if(item[2] == 'customer_name'){
		    			$('#customer').val(item[3]);
		    		}
		    		if(item[2] == 'program_name'){
		    			$('#program').val(item[3]);
		    			changeProject(item[3]);
		    		}
		    	});
		
		    });
		    
		    $('#customer_name').blur(function(){
		    	if($.trim($(this).val()) == ''){
		    		$('#customer').val('');
		    	}
		    });
		    
		    $('#program_name').blur(function(){
		    	if($.trim($(this).val()) == ''){
		    		$('#program').val('');
		    		$("#project").html("<option value=''></option>");
		    	}
		    });
		    
		    
		    %if project_list:
		    	%for p in project_list:
		    		%if str(p.id) == values['project']:
		    			$("#project").append("<option value='${p.id}' selected='selected'>${p}</option>");
		    		%else:
		    			$("#project").append("<option value='${p.id}'>${p}</option>");
		    		%endif
		    	%endfor
		    %endif
		    

			refreshToDoList();
			setInterval(refreshToDoList,1000*60*5); //5min
	
		});
	
		function changeProject(program_id){
			// var t = $('#program');
			var s = $("#project");
			s.html("<option value=''></option>");
			if(program_id){
				$.getJSON("/prepress/ajaxProjectInfo",
						 {"program_id" : program_id},
						 function(res){
						 	if(res.flag != "0"){
						 		alert("Error occur on the server side!");
						 	}else{
						 		var d = res.data;
						 		var html = "<option></option>";
						 		for(var i=0;i<d.length;i++){
						 			html += '<option value="'+d[i][0]+'">'+d[i][1]+'</option>';
						 		}
						 		s.html(html);
						 	}
						 }
				);		
		  }
		}
		
		
		function toSearch(){
			//alert($('#customer').val());
			$("form").submit();
		}
		
		function toSort(f,d){
			$("#field").val(f);
			$("#direction").val(d);
			$("form").submit();
		}

		function refreshToDoList(){
			$.getJSON("/prepress/ajaxTodoList",
			          {time : (new Date()).getTime()},
					  function(req){
					  	if(req.flag == "1"){
							//alert("Error when loading the to-do list.");
						  }else{
						  	$("#todo-draft-count").text(req["draft_count"]);
  							$("#todo-draft .every-request").remove();
  							for(var i=0;i<req["draft"].length;i++){
  								$("#todo-draft").append('<li class="every-request"><a href="/prepress/updateRequest?id='+req["draft"][i][0]+'">'+req["draft"][i][1]+'</a></li>');
  							}
  							
  							$("#todo-new-count").text(req["new_count"]);
  							$("#todo-new .every-request").remove();
  							for(var i=0;i<req["new"].length;i++){
  								$("#todo-new").append('<li class="every-request"><a href="/prepress/viewRequest?id='+req["new"][i][0]+'">'+req["new"][i][1]+'</a></li>');
  							}
						
							$("#todo-cancel-count").text(req["cancel_count"]);
							$("#todo-cancel .every-request").remove();
							for(var i=0;i<req["cancel"].length;i++){
								$("#todo-cancel").append('<li class="every-request"><a href="/prepress/viewRequest?id='+req["cancel"][i][0]+'">'+req["cancel"][i][1]+'</a></li>');
							}
							
							$("#todo-pending-count").text(req["pending_count"]);
				              $("#todo-pending .every-request").remove();
				              for(var i=0;i<req["pending"].length;i++){
				                $("#todo-pending").append('<li class="every-request"><a href="/prepress/viewRequest?id='+req["pending"][i][0]+'">'+req["pending"][i][1]+'</a></li>');
				              }
						    
						    $("#todo-dev-count").text(req["dev_count"]);
				              $("#todo-dev .every-request").remove();
				              for(var i=0;i<req["dev"].length;i++){
				                $("#todo-dev").append('<li class="every-request"><a href="/prepress/viewRequest?id='+req["dev"][i][0]+'">'+req["dev"][i][1]+'</a></li>');
				              }
						    
						    }
					  });
		}
		
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/prepress/index"><img src="/images/images/prepress_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="#" onclick="toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="/prepress/newRequest"><img src="/images/images/menu_new_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Prepress</div>



<!-- Main content begin -->
<div style="width:1500px;">

<div class="div-todolist">
  <table width="180" cellspacing="0" cellpadding="0" border="0">
    <tbody><tr>
      <td height="25" bgcolor="#ffffcc" align="center" class="title-page" style="border-bottom:1px solid #ccc;">TO DO LIST</td>
    </tr>
    
    <tr>
      <td height="30" align="center" class="todoliset-menu" background="/images/TDLBG.jpg">Draft List(<span id="todo-draft-count"></span>)</td>
    </tr>
    <tr>
      <td>
	  	<ol id="todo-draft">
	  	  <li><a href="/prepress/viewToDoList?statusType=-10">View All Request</a></li>
	  	</ol>
	  </td>
    </tr>
    
    <tr>
      <td height="30" align="center" class="todoliset-menu" background="/images/TDLBG.jpg">Outstanding List(<span id="todo-new-count"></span>)</td>
    </tr>
    <tr>
      <td>
	  	<ol id="todo-new">
	  	  <li><a href="/prepress/viewToDoList?statusType=0">View All Request</a></li>
	  	</ol>
	  </td>
    </tr>

    <tr>
      <td height="30" align="center" class="todoliset-menu" background="/images/TDLBG.jpg">Cancelled(<span id="todo-cancel-count"></span>)</td>
    </tr>
    <tr>
      <td>
	  	<ol id="todo-cancel">
	  	  <li><a href="/prepress/viewToDoList?statusType=9">View All Request</a></li>
	  	</ol>
	  </td>
    </tr>
    <tr>
      <td height="30" align="center" class="todoliset-menu" background="/images/TDLBG.jpg">Under Development(<span id="todo-dev-count"></span>)</td>
    </tr>
    <tr>
      <td>
	  	<ol id="todo-dev">
	  	  <li><a href="/prepress/viewToDoList?statusType=2">View All Request</a></li>
	  	</ol>
	  </td>
    </tr>
  </tbody>
  </table>
</div>


<div style="width:1200px;float:left">
	<div style="overflow:hidden;margin:5px 0px 10px 10px">			
		${widget(value=values,action="/prepress/index")|n}
	</div>
	<div class="clear"><br /></div>
	<div id="recordsArea" style="margin:5px 0px 10px 10px">
	  <%
		my_page = tmpl_context.paginators.result
		pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
	  %>
      <table cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="20">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
			<tr> 
				<th width="180" height="30">Job No ${show_direction('system_no')}</th>
	    		<th width="100">Region ${show_direction('project_own_id')}</th>
	    		<th width="150">Vendor/Customer ${show_direction('customer_id')}</th>
	    		<th width="150">Brand ${show_direction('project_id')}</th>
	    		<th width="120">Item Code</th>
	    		<th width="120">Reqeust Date ${show_direction('create_time')}</th>
				<th width="200">Status</th>
	    	</tr>
		</thead>
		<tbody>
			%if len(result) < 1:
				<tr>
					<td colspan="8" style="border-left:1px solid #ccc">No match request found!</td>
				</tr>
			%else:
				% for index,h in enumerate(result):
		    	%if index %2 == 0 :
					<tr class="even">
				%else:
					<tr class="odd">
				%endif
					<td style="border-left:1px solid #ccc">
						%if h.status == -9:
							<a href="/prepress/viewRequest?id=${h.id}" style="color: red;">${str(h)}</a>
						%elif h.status == -10:
							<a href="/prepress/updateRequest?id=${h.id}&is_draft=true" style="color: black;">${str(h)}</a>
						%else:
							<a href="/prepress/viewRequest?id=${h.id}">${str(h)}</a>
						%endif
					</td>
					<td>&nbsp;${h.project_own}</td>
					<td>&nbsp;${h.customer}</td>
					<td>&nbsp;${h.project}</td>
					<td>&nbsp;${h.item_code}</td>
					<td>&nbsp;${h.create_time.strftime("%Y/%m/%d %H:%M")}</td>
				    <td style="text-align:left;">&nbsp;
				    	%if h.status == -9:
				    		Cancelled
				    	%else:
				    		<span class="status-bar">${"%d%%" % (h.percentage*100)}</span>
				    	%endif
				    </td>
				%endfor
			%endif
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="20">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
		</tbody>
	</table>
  </div>
</div>	


</div>
<!-- Main Content end -->




<%def name="show_direction(f)">
	%if values.get('field',None) == f:
		%if values.get('direction',None) == 'desc':
			<a href="#" onclick="toSort('${f}','asc')"><img src="/images/down.png"/></a>
		%else:
			<a href="#" onclick="toSort('${f}','desc')"><img src="/images/up.png"/></a>
		%endif
	%else:
		<a href="#" onclick="toSort('${f}','desc')"><img src="/images/updown.gif"/></a>
	%endif
</%def>