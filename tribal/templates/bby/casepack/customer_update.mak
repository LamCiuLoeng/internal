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

.ul-session{
	list-style : none;
	padding-left : 0px;
	margin-left: 5px;
}

.ul-session li{
	padding-left : 0px;
	padding-bottom : 5px;
	margin-left : 0px;
	text-align : left;
}


textarea{
	width : 150px;
}

.numeric{
	width : 50px;
}

.datePicker{
	width : 100px;
}

.template,.file_template{display:none;}

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
	
	var count = ${ max(map(lambda r:r.id,header.results) or [0]) +10 }
    
    function addline(){
    	//var btn = $(obj);
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
		$(".filebtn",tmp).attr("bindex",index);
    	$("#table_customer").append(tmp);
		reindex();		
		//alert($(".file_template input[type='file']",tmp).attr("name"));
    }
    
    function delline(obj){
    	var tmp = $(obj);
    	$(tmp.parents("tr")[0]).remove();
    	reindex();
    }
    
    
    function addFile(obj){
    	var btn=$(obj);
    	var td = btn.parents("td")[0];
    	var tmp = $(".file_template",td).clone();
    	//alert($("input[type='file']",tmp).attr("name"));
    	tmp.removeClass("file_template");
    	var index = parseInt(btn.attr("sindex")) + 1;
    	
    	$("input",tmp).each(function(){
    		var t = $(this);
    		var n = t.attr("name");
    		t.attr("name",n.replace("_x","_"+btn.attr("bindex")).replace("_y","_"+index));
    		//alert(t.attr("name"));
    	});
    	
    	btn.attr("sindex",index);
    	$("ul",td).append(tmp);
    	//alert($("input[type='file']",tmp).attr("name"));
    }
    
    function delFile(obj){
    	var t = $(obj);
    	$(t.parents("li")[0]).remove();
    }
    
    function getFileName(obj){
	    var tmp = $(obj);
		var path = tmp.val();
		if( path && path.length > 0){
			var location = path.lastIndexOf("\\") > -1 ?path.lastIndexOf("\\") + 1 : 0;
			var fn = path.substr( location,path.length-location );	
			var li = tmp.parents("li")[0];
			$("input[type='text'][name='"+ tmp.attr("name").replace('attachment_path_','attachment_name_') +"']",li).val(fn);
		}
	}
	
	function ajaxDelFile(type,id,fid,obj){
    	$.getJSON("/bbycasepack/ajaxDeleteFile",
    	          {
    	          	type : type,
    	          	id : id,
    	          	fid : fid
    	          },
    	          function(r){
    	          	if(r.result == "0"){
    	          		alert("Delete the file successfully!");
    	          		$($(obj).parents("li")[0]).remove();
    	          	}else{
    	          		alert("Error when deleting the file!");
    	          	}
    	          });
    }
    
    function toSave(){
    	$(".template").remove();
    	$("form").submit();
    }
    
    function reindex(){
    	var index = 1;
    	$("#table_customer tbody tr:not('.template')").each(function(){
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
            <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
            <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
        </tr>
        </tbody>
    </table>
</div>

            
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Casepack</div>



<!-- Main content begin -->
<div>
    <div id="tabsJ">
		<ul>
			<li><a href="view?id=${header.id}"><span>Item Information</span></a></li>
			<li><a href="factory?id=${header.id}"><span>Factory</span></a></li>
			<li id="current"><a href="customer?id=${header.id}"><span>Customer</span></a></li>
			<li><a href="history?id=${header.id}"><span>History</span></a></li>
		</ul>
    </div>

    <div><br class="clear"/><br /></div>
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
      ${widget(action="",value=values)|n}
    </div>

</div>
   
    <div style="margin: 5px 0px 10px 10px;">
    	<p><input type="button" class="btn" value="Add Line" onclick="addline();"/></p>
    	<form action="/bbycasepack/customer_save" method="post" enctype="multipart/form-data">
    		<input type="hidden" name="id" value="${header.id}"/>
		    <table cellspacing="0" cellpadding="0" border="0" class="gridTable" id="table_customer">
		    	<thead>
	                <tr>
	                    <th style="width:50px">Round</th>
	                    <th style="width:100px">Received Date</th>
	                    <th style="width:100px">Send Out Date</th>
	                    <th style="width:150px">Customer Received Date</th>
	                    <th style="width:100px">Test By</th>
	                    <th style="width:80px">Qty</th>
	                    <th style="width:80px">Pass/Fail</th>
	                    <th style="width:100px">Reported Date</th>
	                    <th style="width:150px">Reason for failure</th>
	                    <th style="width:450px">Attachment</th>
	                    <th style="width:150px">Remark</th>
	                    <th style="width:80px">Action</th>
	                </tr>
	            </thead>
	            <tbody>
	            	%for index,r in enumerate(header.results):
	            		<tr>
	            			<td style="border-left:1px solid #ccc;">&nbsp;${index+1}</td>
	            			<td><input type="text" name="received_date_${r.id}" class="datePicker" value="${r.received_date.strftime('%Y-%m-%d') if r.received_date else ''}"/></td>
	            			<td><input type="text" name="send_out_date_${r.id}" class="datePicker" value="${r.send_out_date.strftime('%Y-%m-%d') if r.send_out_date else ''}"/></td>
	            			<td><input type="text" name="customer_received_date_${r.id}" class="datePicker" value="${r.customer_received_date.strftime('%Y-%m-%d') if r.customer_received_date else ''}"/></td>
	            			<td><input type="text" name="test_by_${r.id}" value="${r.test_by}"/></td>
	            			<td><input type="text" name="qty_${r.id}" class="numeric" value="${r.qty}" style="width:50px"/></td>
	            			<td>
	            				<select name="result_${r.id}">
	            					%for o in ['','PASS','FAIL']:
	            						<option value="${o}" ${tw.attrs([('selected',o==r.result)])}>${o}</option>
	            					%endfor
	            				</select>
	            			</td>
	            			<td><input type="text" name="reported_date_${r.id}" class="datePicker" value="${r.reported_date.strftime('%Y-%m-%d') if r.reported_date else ''}"/></td>
	            			<td>${select_widget("reason_id_%d" %r.id,"BBYFailureReason",r.reason_id)}</td>
	            			<td>
	            				<ul class="ul-session">
	            					%for i in r.getAttachments():
	            						<li><a href="/bbycasepack/download?id=${i.id}">${i.file_name}</a>&nbsp;<input type="button" class="btn" value="Del" onclick="ajaxDelFile('cpr',${r.id},${i.id},this)"/></li>
	            					%endfor
	            					<li class="file_template"><input type="text" name="attachment_name_${r.id}_y"/>&nbsp;<input type="file" name="attachment_path_${r.id}_y" onchange="getFileName(this)"/>&nbsp;<input type="button" class="btn" value="Del" onclick="delFile(this)"/></li>
	            				</ul>
	            				<input type="button" class="btn filebtn" value="Add File" bindex="${r.id}" sindex="${r.getAttachments()[-1].id +10 if r.getAttachments() else 10}" onclick="addFile(this)"/>
	            			</td>
	            			<td><textarea name="remark_${r.id}">${r.remark}</textarea></td>
	            			<td><input type="button" class="btn" value="Del" onclick="delline(this)"/>
	            		</tr>
	            	%endfor
	            	
	            	
	            	<tr class="template">
            			<td style="border-left:1px solid #ccc;"></td>
            			<td><input type="text" name="received_date_x" class="datePicker" value="${f(last_rev_day)}"/></td>
            			<td><input type="text" name="send_out_date_x" class="datePicker" value=""/></td>
            			<td><input type="text" name="customer_received_date_x" class="datePicker" value=""/></td>
            			<td><input type="text" name="test_by_x" value=""/></td>
            			<td><input type="text" name="qty_x" class="numeric" value="" style="width:50px"/></td>
            			<td>
            				<select name="result_x">
            					%for o in ['','PASS','FAIL']:
            						<option value="${o}">${o}</option>
            					%endfor
            				</select>
            			</td>
            			<td><input type="text" name="reported_date_x" class="datePicker" value=""/></td>
            			<td>${select_widget("reason_id_x","BBYFailureReason",None)}</td>
            			<td>
            				<ul class="ul-session">
            					<li class="file_template"><input type="text" name="attachment_name_x_y"/>&nbsp;<input type="file" name="attachment_path_x_y" onchange="getFileName(this)"/>&nbsp;<input type="button" class="btn" value="Del" onclick="delFile(this)"/></li>
            				</ul>
            				<input type="button" class="btn filebtn" value="Add File" bindex="" sindex="10" onclick="addFile(this)"/>
            			</td>
            			<td><textarea name="remar_x"></textarea></td>
            			<td><input type="button" class="btn" value="Del" onclick="delline(this)"/>
            		</tr>
	            </tbody>
		    </table>
	    
	 </div>
    
	

<!-- Main Content end -->

<%def name="f(date_value,date_format='%Y-%m-%d')" filter="trim">
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