<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
	from tribal.util.bby_helper import getMaster
%>

<%def name="extTitle()">r-pac - (BBY)Casepack</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/bby.css" type="text/css" media="screen"/>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>

<style>
.gridTable2 thead th{
	background-color : gray;
}
.template {display:none}

textarea{
	width : 150px;
}

.numeric{
	width : 50px;
}

.datePicker{
	width : 100px;
}

</style>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    var dateFormat = 'yy-mm-dd';
    $(document).ready(function(){
    		$(".numeric").numeric();
    		
			$('.datePicker').datepicker({
		        changeMonth : true,
		        changeYear : true,
		        dateFormat : dateFormat
		      });
		});
    
    var count = 0;
    
    function addline(obj){
    	var btn = $(obj);
    	var tmp = $(".template").clone();
        $('.datePicker', tmp).attr("id","");
		tmp.removeClass("template");
    	
    	var index = count++;
    	
		$("input,select,textarea",tmp).each(function(){
			var t = $(this);
			var n = t.attr("name")
			t.removeClass("hasDatepicker");
			t.attr("name",n.replace("_x","_"+index));
		});
        
        $('.datePicker',tmp).datepicker({
		        changeMonth : true,
		        changeYear : true,
		        dateFormat : dateFormat
		});
		
		$(".numeric",tmp).numeric();
    	$("#table_factory").append(tmp);
		reindex();
    }
    
    function delline(obj){
    	var tmp = $(obj);
    	$(tmp.parents("tr")[0]).remove();
    	reindex()
    }
    
    function toSave(){
    	$(".template").remove();
    	$("form").submit();
    }
    
    function toCancel(){
    	if(!confirm("Are you sure to leave the page without saving your revise?")){
    		return false;
    	}
    	return true;
    }
    
    function reindex(){
    	var index = 1;
    	$("#table_factory tbody tr:not('.template')").each(function(){
    		$("td:first-child",this).text(index++);
    	});
    }
    
    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
        <tr>
            <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
            <td width="175" valign="top" align="left"><a href="/bbycasepack/index"><img src="/images/mainmenu_g.jpg"/></a></td>
            <td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
            <td width="64" valign="top" align="left"><a href="/bbycasepack/factory?id=${header.id}" onclick="return toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
            <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
            <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
        </tr>
        </tbody>
    </table>
</div>

            
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Casepack</div>



<!-- Main content begin -->
<div style="width:1500px;">
    <div id="tabsJ">
	<ul>
		<li><a href="view?id=${header.id}"><span>Item Information</span></a></li>
		<li id="current"><a href="factory?id=${header.id}"><span>Factory</span></a></li>
		<li><a href="customer?id=${header.id}"><span>Customer</span></a></li>
		<li><a href="history?id=${header.id}"><span>History</span></a></li>
	</ul>
    </div>

    <div><br class="clear"/><br /></div>
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
      ${widget(action="",value=values)|n}
    </div>
    
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
    	<form action="/bbycasepack/factory_save" method="POST">
	    	<input type="hidden" name="id" value="${header.id}"/>
	    	<table cellspacing="0" cellpadding="0" border="0" class="gridTable">
	    		<thead>
	                <tr>
	                    <th style="width:50px">Round</th>
	                    <th>Content</th>
	                </tr>
	            </thead>
	            <tbody>
	            	%for round,round_data in result.items():
	            	<tr>
	            		<td style="border-left:1px solid #ccc;">&nbsp;${round}</td>
	            		<td>
	            			%for cid,c in  round_data.items():
		            			<fieldset class="fieset-css">
		            				<legend><b>${c['component']}</b></legend>
		            				<table cellspacing="0" cellpadding="0" border="0" class="gridTable gridTable2">
		            					<thead>
		            						<tr>
							                    <th style="width:100px">Sender</th>
							                    <th style="width:150px">E-mail Date</th>
							                    <th style="width:150px">Factory</th>
							                    <th style="width:150px">Required Date</th>
							                    <th style="width:80px">Qty</th>
							                    <th style="width:150px">Ship To</th>
							                    <th style="width:100px">Sent Out Date</th>
							                    <th style="width:150px">Couier</th>
							                    <th style="width:100px">AWB#</th>
							                    <th style="width:180px">Casepack Received Date</th>
							                    <th style="width:150px">Remark</th>
							                    <th style="width:70px">Cancel</th>
							                    <th style="width:70px">Approval</th>
						                    </tr>
		            					</thead>
		            					<tbody>
		            						%for r in c['data']:
			            						<tr>
							            			<td style="border-left:1px solid #ccc;">&nbsp;${r.create_by}</td>
							            			<td>&nbsp;${f(r.create_time,'%Y-%m-%d %H:%M:%S')}</td>
							            			<td>&nbsp;${r.factory}</td>
							            			<td>&nbsp;${f(r.required_date)}</td>
							            			<td>&nbsp;${r.qty}</td>
							            			<td>&nbsp;${r.ship_to}</td>
							            			<td><input type="text" name="send_date_${r.id}"  class="datePicker" value="${r.send_date.strftime('%Y-%m-%d') if r.send_date else ''}"/></td>
							            			<td>${select_widget("courier_id_%d" %r.id,"BBYCourier",r.courier_id)}</td>
							            			<td><input type="text" name="awb_${r.id}" value="${r.awb}"/></td>
							            			<td><input type="text" name="received_date_${r.id}" class="datePicker" value="${r.received_date.strftime('%Y-%m-%d') if r.received_date else ''}"/></td>
							            			<td><textarea name="remark_${r.id}">${r.remark}</textarea></td>
							            			<td><input type="checkbox" name="cancel_${r.id}" value="YES" ${tw.attrs([('checked',r.approve=='YES')])}/>YES</td>
							            			<td><input type="checkbox" name="approve_${r.id}" value="YES" ${tw.attrs([('checked',r.approve=='YES')])}/>YES</td>
			            						</tr>
		            						%endfor
		            					</tbody>
		            				</table>
		            			</fieldset>
	            			%endfor
	            		</td>
	            	</tr>
	            	%endfor
	            </tbody>
	    	</table>
	    </form>    					
    </div>
    
</div>
	            	
<!-- Main Content end -->

<%def name="f(date_value,date_format='%Y-%m-%d')">
	%if date_value:
		${date_value.strftime(date_format)}
	%endif
</%def>


<%def name="select_widget(name,master,value)">
	<select name="${name}" style="width:150px">
		<option></option>
		%for m in getMaster(master):
			<option value="${m.id}" ${tw.attrs([('selected',m.id==value),])}>${m}</option>
		%endfor
	</select>
</%def>