<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Prepress</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/glowbutton.css" type="text/css" media="screen"/>
<style type="text/css">
  .subform-info{
    padding-bottom : 10px;
    padding-left   : 100px;
    padding-right  : 0px;
    padding-top    : 10px;
    margin         : 0px;
    width          : 800px;
    float          : left;
  }
  
  .subform-action{
    width          : 250px;
    padding-top    : 10px;
    padding-right  : 10px;
    margin         : 0px;
    float          : right;
    text-align     : right;
  }
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.color.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.glowbuttons.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		$(document).ready(function(){
        $(":button").each(function(){
          var t = $(this);
          var type = t.attr("action_type");
          if(type=="A"){
            var from_css = "#79B837";
            var to_css = "#C7EB6E";
          }else if(type=="D"){
            var from_css = "#9C0063";
            var to_css = "#D693BD";
          }else if(type=="C"){
            var from_css = "#e2ae01";
            var to_css = "'#555555";
          }else if(type=="S" || type=="P"){
            var from_css = "#016bbd";
            var to_css = "#b1ddff";
          }else if(type=="X"){
            var from_css = "#a31300";
            var to_css = "#ffa498";
          }
          t.glowbuttons({from:from_css,to:to_css,speed: 100})
      });
      
      
      $(".view").click(
        function(){
          var t = $(this);
          if(t.text()=="Open"){
            //$("#"+t.attr("related_tr")).fadeIn();
            $("#"+t.attr("related_tr")).show();
            t.text("Close");
          }else{
            //$("#"+t.attr("related_tr")).fadeOut();
            $("#"+t.attr("related_tr")).hide();
            t.text("Open");
          }
        });
    });		
    
    
    function ajaxMark(subform_id,action){
      var form_ids = [];
      $("#"+subform_id+" tbody input[type='checkbox']:checked").each(function(){
        form_ids.push($(this).val());
      });
      
      if(form_ids.length<1){ alert("Pelase select at lease one record to submit!"); return;}
      

      $("body").mask("Loading...");
      $.getJSON("/prepress/ajaxMark",
        {
          "form_ids" : form_ids.join("|"),
          "action"   : action 
        },function(req){
        if(req["flag"]==1){
          $.prompt("Error occur on the server side!",{opacity: 0.6,prefix:'cleanred'});
        }else if(req["flag"]==2){
          $.prompt("No such action type!",{opacity: 0.6,prefix:'cleanred'});
        }else{
          var result = "";
          switch(req["status"]){
            case 0    : result = "Approved";break; 
            case -1   : result = "Disapproved";break;
            case 2    : result = "Under Development";break;  
            case 3    : result = "Pending";break;  
          }          
          for(var i=0;i<form_ids.length;i++){
            $("#"+form_ids[i]).remove()
          }
          
          if( $("#"+subform_id+" tbody tr").length < 1 ){
           var k = $("#"+subform_id);
           k.remove(); 
           $(".view",k.prev("tr")).remove();
          }
          
          $.prompt("Update the record(s) successfully!",{opacity: 0.6,prefix:'cleanblue'});
          
        }
        $("body").unmask();
      })
    }
    
    
    function selecAll(obj){
      var t = $(obj);
      var p = t.parents("table")[0];
      if(t.attr("checked")){
        $(":checkbox",p).attr("checked",true);
      }else{
        $(":checkbox",p).removeAttr("checked");
      }
    }
    
     
    
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/prepress/index"><img src="/images/images/prepress_g.jpg"/></a></td>

    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Prepress&nbsp;&nbsp;&gt;&nbsp;&nbsp;To Do List</div>



<!-- Main content begin -->
<div style="width:1500px;">

<div style="width:1200px;float:left">

	<div id="recordsArea" style="margin:5px 0px 10px 10px">
	  <%
		my_page = tmpl_context.paginators.result
		pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
	  %>
      <table cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="11">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
			<tr> 
				<th width="200">Job No</th>
	    		<th width="200">Region</th>
	    		<th width="150">Vendor</th>
	    		<th width="150">Project</th>
	    		<th width="120">Item Code</th>
	    		<th width="120">Reqeust Date</th>
	    		<th width="120">Issued By</th>
				<th width="120">View</th>
	    	</tr>
		</thead>
		<tbody>
			% for index,c in enumerate(result):
	    	%if index %2 == 0 :
  				<tr class="even">
  			%else:
  				<tr class="odd">
  			%endif
  				%if statusType==-10:
  				<td style="border-left:1px solid #ccc"><a href="/prepress/updateRequest?id=${c.id}">${str(c)}</a></td>
  				%else:
  				<td style="border-left:1px solid #ccc"><a href="/prepress/viewRequest?id=${c.id}">${str(c)}</a></td>
  				%endif
  				<td>&nbsp;${c.project_own}</td>
  				<td>&nbsp;${c.customer}</td>
  				<td>&nbsp;${c.project}</td>
  				<td>&nbsp;${c.item_code}</td>
  				<td>&nbsp;${c.create_time.strftime("%Y/%m/%d")}</td>
  				<td>&nbsp;${c.create_by}</td>
  				<td>&nbsp;
  					%if statusType!=-10:
  					<a href="#" related_tr="subform_${c.id}" class="view">Open</a>
  					%endif
  				</td>
				</tr>
				<!- subform info  ->
				<tr id="subform_${c.id}" style="display:none">
				  <td colspan="9" style="border-left:1px solid #ccc">
				    <div class="subform-info" id="subform-info-${c.id}">
				      <table cellspacing="0" cellpadding="0" border="0" class="gridTable">
				        <thead>
  				        <tr>
  				          <th width="30">&nbsp;<input type="checkbox" onclick="selecAll(this)" checked="checkeds"/></th>
  				          <th width="200">Request Type</th>
  				          <th width="200">Status</th>
  				          <th width="200">Update Time</th>
  				        </tr>
				        </thead>
				        <tbody>
  				        %for f in c.getChildrenForm():
  				          %if f.status == statusType:
      				        <tr id="${'%s_%d' %(f.__class__.__name__,f.id)}">
      				          <td style="border-left:1px solid #ccc"><input type="checkbox" name="sf_ids" value="${'%s_%d' %(f.__class__.__name__,f.id)}" checked="checked"/></td>
      				          <td>&nbsp;${f.getWidget().label}</td>
      				          <td>&nbsp;${f.showStatus()}</td>  
      				          <td>&nbsp;${f.update_time.strftime("%Y-%m-%d")}</td>
      				        </tr>
      				      %endif
  				        %endfor
				        </tbody>
				      </table>
				    </div>
            <div class="subform-action">
				      <p>				        
                %if statusType == 1:
                    <input type="button" action_type="S" value="Start Work" onclick="ajaxMark('subform_${c.id}','S')"/>&nbsp;
                    <input type="button" action_type="X" value="Cancel" onclick="ajaxMark('subform_${c.id}','X')"/>
                %elif statusType == 2:
                    <input type="button" action_type="C" value="Complete" onclick="ajaxMark('subform_${c.id}','C')"/>&nbsp;
                    <input type="button" action_type="P" value="Pending" onclick="ajaxMark('subform_${c.id}','P')"/>
                    <input type="button" action_type="X" value="Cancel" onclick="ajaxMark('subform_${c.id}','X')"/>
                %elif statusType == 4:
                    <input type="button" action_type="G" value="Restart" onclick="ajaxMark('subform_${c.id}','G')"/>
                %endif
				      </p>              
            </div>
				  </td>
				</tr>
			%endfor
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="11">
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