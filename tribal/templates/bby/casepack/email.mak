<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
	from tribal.util.bby_helper import getMaster
%>
<style type="text/css">
<!--
td{
	font-family: Tahoma, Geneva, sans-serif;
	font-size: 12px;
	line-height: normal;
	color: #000;
	text-decoration: none;
}
.j-tab{
	padding:0px 10px 0px 10px;
	text-align:right;
	background-color:#4e7596;
	font-family: Tahoma, Geneva, sans-serif;
	font-size: 14px;
	font-weight: bold;
	color: #FFF;
	text-decoration: none;
}
.j-tab1{
	padding:0px 10px 0px 10px;
	text-align:center;
	background-color:#4e7596;
	font-family: Tahoma, Geneva, sans-serif;
	font-size: 12px;
	font-weight: bold;
	color: #FFF;
	text-decoration: none;
}
.t_area{ 
width:400px; 
overflow-y:visible;
background-color:#FFC;
border:#069 solid 1px;
} 

-->
</style>

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

<style>
.gridTable2 thead th{
	background-color : gray;
}
</style>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    $(document).ready(function(){
    	$("#component_ul :checkbox").click(function(){
    		var t = $(this);
    		var id = t.attr("format_id");
    		if(t.attr("checked")){
    			var msg = isSelectOK();
	    		if(msg.length<1){
	    			$("#component_tr_"+id).fadeIn();
		    		fillComponentSpan();
		    		changeEmailContent();	
	    		}else{
	    			alert(msg.join("\n"));
	    			t.removeAttr("checked");
	    		}
    		}else{
    			$("#component_tr_"+id).fadeOut();
    			fillComponentSpan();
		    	changeEmailContent();
    		}	
    	});
    });
    
    function changeEmailContent(){
    	var cs = $("#component_ul :checked");
    	$("tr[id^='office_qty_tr_']").hide();
    	if(cs.length <1){
    		$("#span_factory").text("");
	    	$("#ship_to_address_vendor").text("");
	    	$("#ship_to_phone_vendor").val("");
	    	$("#send_to").val("");
	    	//$("#span_shipto_remark").text("");
	    	//alert('tohide');
    	}else{
    		cs.each(function(){
	    		//var tmp = component_info[$(cs[0]).val()];
	    		
	    		var tmp = component_info[$(this).val()];
	    		
		    	$("#span_factory").text(tmp['factory']);
		    	$("#ship_to_address_vendor").text(tmp['ship_address']);
		    	$("#ship_to_phone_vendor").val(tmp['ship_phone']);
		    	$("#send_to").val(tmp['email']);

		    	//alert("tr[id^='office_qty_tr_"+$(this).val()+"_']");
		    	$("tr[id^='office_qty_tr_"+$(this).val()+"_']").show();
    		});
    		
    	}
    }
    
    
	var check_email = /^[a-z]([a-z0-9]*[-_\.]?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2})?$/i;
    function checkEmailStr(str){
    	var ss = str.split(";")
    	for(var i=0;i<ss.length;i++){
    		if(!check_email.test(ss[i])){
    			return false;
    		}
    	}
    	return true;
    }
    
    function toSubmit(){
    	var msg = Array();
    	var check_str = /^[a-z0-9@;.\-_]+$/i
    	
    	var components = $("#component_ul :checked");
    	var offices = $("#office_ul :checked");
    	if(components.length<1){ msg.push("Please select at lease one component!"); }
		if(offices.length<1){ msg.push("Please select at lease one office!"); }
    	
    	if(!$("#send_to").val()){ 
    		msg.push("The 'To' field could not be blank!"); 
    	}else{
        	if(!check_str.test($("#send_to").val())){ 
        		msg.push("The 'To' field include the invalid char!"); 
        	}else if(!checkEmailStr($("#send_to").val())){ 
        		msg.push("The 'To' field is not a valid e-mail format!"); 
        	}
    	}       	
    	
    	if(!$("#cc_to").val()){ 
    		msg.push("The 'Cc' field could not be blank!"); 
    	}else{
        	if(!check_str.test($("#cc_to").val())){ 
        		msg.push("The 'Cc' field include the invalid char!"); 
        	}else if(!checkEmailStr($("#cc_to").val())){ 
        		msg.push("The 'Cc' field is not a valid e-mail format!"); 
        	}
    	}
    	
    	var isQtyFilled = true;
    	for(var i=0;i<components.length;i++){
    		var c = $(components[i]);
    		for(var j=0;j<offices.length;j++){
    			var o = $(offices[j]);
    			if(!$("input[name='qty_"+o.val()+"_"+c.val()+"']").val()){
    				isQtyFilled = false;
    				break;
    			}
    		}
			if(!isQtyFilled){ break; }    		
    	}
    	if(!isQtyFilled){ msg.push("Please fill in the related qty!") }
    		        	          	        	
    	if(msg.length>0){
    		$.prompt(msg.join("<br />"),{opacity: 0.6,prefix:'cleanred'});
    		return;
    	}else{
    		if(confirm("Are you sure to send out this e-mail?")){
        		$("form").submit();
        	}
    	}
    }
  
    
    function changeSeq(obj){
    	var t = $(obj);
    	var ids = [];
    	var o = $(":selected",t)
    	if(o.attr("li_ids")){
    		ids = o.attr("li_ids").split("|");
    	}
    	$("#component_ul li").each(function(){
    		var tmp = $(this);
    		var id = tmp.attr("component_id");
    		
    		var flag = false;
    		for(var j=0;j<ids.length;j++){
    			if(ids[j]==id){
    				flag = true;
    				break;
    			}
    		}
    	
    	
    		if(flag){
    			tmp.slideUp();
    		}else{
    			tmp.slideDown();
    		}
    		$(":checkbox",tmp).removeAttr("checked")
    		$("tr[id^='component_tr_']").fadeOut();
    	})
    }
    
    function fillComponentSpan(){
    	var cs = [];
    	$("#component_ul :checked").each(function(){
    		cs.push($(this).siblings(".component_spec").text());
    	});
    	if(cs){
	    	$("#span_components").text(cs.join(","));
    	}else{
    		$("#span_components").text("");
    	}
    }
    
    function isSelectOK(){
    	var cs = $("#component_ul :checked");
    	var msg = [];
    	if(cs.length < 2){ return msg; }
    	
    	for(var i=1;i<cs.length;i++){
    		var pre = component_info[$(cs[i-1]).val()];
    		var cur = component_info[$(cs[i]).val()];
    		if(pre['factory_id'] != cur['factory_id']){ msg.push("Not all the factories are the same!"); }
    		if(pre['shipto_id'] != cur['shipto_id']){ msg.push("Not all the shipto addresses are the same!"); }
    	}
		return msg;
    }
    
    
    function changeOffice(obj,type){
    	var t = $(obj);
    	if(t.attr("checked")){
    		$("#div_"+type).fadeIn();
    	}else{
    		$("#div_"+type).fadeOut();
    	}
    }
    
    function change_att(obj){
    	var t= $(":selected",obj);
    	var div = t.parents("div")[0];
    	$("input[name^='ship_to_phone']",div).val(t.attr("phone"));
    }
    
    var component_info = {}
    %for c,d in component_casepack:
    	component_info[${c.id}] = {
    						        "factory_id" : "${c.factory_id}",
    							    "factory" : "${c.factory}",
    							    "shipto_id" : "${d.ship_to_id if d.ship_to_id else ''}",
    								"ship_address" : "${d.ship_to.address if d.ship_to else ''}",
    								"ship_phone" : "${' '.join(filter(bool,[d.ship_to.tel,d.ship_to.ext,d.ship_to.mobile])) if d.ship_to else ''}",
    							  	"email" : "${';'.join([detail.email for detail in c.factory.details])  if c.factory else ''}",
    							    "remark" : "${d.remark}"
    							  }
    %endfor
    
    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
        <tr>
            <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
            <td width="175" valign="top" align="left"><a href="/bbycasepack/index"><img src="/images/mainmenu_g.jpg"/></a></td>
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
    	<form action="/bbycasepack/email_save" method="POST">
    		<input type="hidden" name="id" value="${header.id}"/>				
			<table cellspacing="0" cellpadding="3" border="1">
				<tr>	    	
	    			<td class="j-tab">Round</td>
   			    	<td style="padding:20px">
    				  <select name="seq" onchange="changeSeq(this)" class="t_area">
	    					<option value="NEW">New Record</option>
	    					%for k in sorted(seqs.keys()):
	    						<option value="${k}" li_ids="${'|'.join(seqs[k]['cids'])}">${k} - Last Update : ${f(seqs[k]['last_date'])}</option>
	    					%endfor
	    				</select>
	    				
	    			</td>
	    		</tr>
	    		<tr>
	    			<td class="j-tab">Component</td>
   			    <td>
    				  <div>
	    					<ul id="component_ul">
	    						%for cc in component_casepack:
	    							%if cc[0].factory_id and cc[1]:
		    							<li component_id="${cc[0].format_id}">
		    								<input type="checkbox" name="component_ids" value="${cc[0].id}" component_name="${cc[0].format}" format_id="${cc[0].format_id}"/><span class="component_spec">${cc[0].format}</span> (Factory : ${cc[0].factory})
		    							</li>
	    							%endif
	    						%endfor
	    					</ul>
	    					
	    				</div>
	    			</td>
	    		</tr>
	    		<tr>
	    			<td class="j-tab">Receivers</td>
	    			<td>
	    				<ul id="office_ul">
	    					<li><input type="checkbox" name="rpac_office" value="vendor" id="rpac_office_vendor" onclick="changeOffice(this,'vendor')"/><label for="rpac_office_vendor">Vendor</label></li>
	    					<li><input type="checkbox" name="rpac_office" value="hko" checked="checked" id="rpac_office_hko" onclick="changeOffice(this,'hko')"/><label for="rpac_office_hko">r-pac HK office</label></li>
	    					<li><input type="checkbox" name="rpac_office" value="szo" checked="checked" id="rpac_office_szo" onclick="changeOffice(this,'szo')"/><label for="rpac_office_szo">r-pac SZ office</label></li>
	    				</ul>
	    			</td>
	    		</tr>
				<tr>
					<td class="j-tab">To</td>
			    <td style="padding:20px">
					  <textarea name="send_to" id="send_to" style="width:600px" class="t_area"></textarea>
						<p>Please seperate multi e-mail address with semicolon (";") , example : <b>aa@aa.com;bb@bb.com</b></p>
					</td>
				<tr>
				<tr>
					<td class="j-tab">Cc</td>
			    <td style="padding:20px">
					  <textarea name="cc_to" id="cc_to" style="width:600px" class="t_area">${";".join(cc_list)}</textarea>
						<p>Please seperate multi e-mail address with semicolon (";") ,example : <b>aa@aa.com;bb@bb.com</b></p>
					</td>
				</tr>
				<tr>
					<td class="j-tab">Content</td>
			    <td style="padding:20px">
					  <div>
							<p>Dear <b><span id="span_factory"></span></b> Team:</p>
							<p>The <b><span id="span_components"></span></b> of <b>${header.sku}</b> is approved, please help to prepare case pack sample with correct LOGO TEMPLATE.</p>
							<table cellspacing="0" cellpadding="3" border="1">
								<thead>
									<tr>
										<th class="j-tab1">Components</th>
										<th class="j-tab1">Material Name</th>
										<th class="j-tab1">Spec</th>
										<th class="j-tab1">Front Color</th>
										<th class="j-tab1">Back Color</th>
										<th class="j-tab1">Finished Size</th>
										<th class="j-tab1">Closure</th>
										<th class="j-tab1">Display Mode</th>
										<!-- <th class="j-tab1">Qty</th> -->
										<th class="j-tab1">Required Ready Date</th>
									</tr>
								</thead>
								<tbody>
									%for cc2 in component_casepack:
									<tr id="component_tr_${cc2[0].format_id}" style="display:none">
										<td>&nbsp;${cc2[0].format}</td>
										<td>&nbsp;${cc2[0].material}</td>
										<td>&nbsp;${cc2[0].coating}</td>
										<td>&nbsp;${cc2[0].front_color}</td>
										<td>&nbsp;${cc2[0].back_color}</td>
										<td>&nbsp;${cc2[0].finished_size}</td>
										<td>&nbsp;${cc2[0].closure}</td>
										<td>&nbsp;${cc2[0].display_mode}</td>
										<!-- <td>&nbsp;${cc2[1].qty}</td> -->
										<td>&nbsp;${f(cc2[1].required_date)}</td>
									</tr>
									%endfor
								<tbody>
							</table>
							<br />
							<%
								vendor_values = {}
								for cc3 in component_casepack:
									vendor_values['qty_%d' % cc3[0].id] = cc3[1].qty
							%>
							
							${email_session('vendor',vendor_values)}
							${email_session('hko',dict(address='HKO'))}
							${email_session('szo',dict(address='SZO'))}
						</div>
					</td>
				</tr>
				<tr>
					<td class="j-tab">Attachment</td>
			  <td>
						%if attachments:
					  <div>
							<ul>
								%for a in attachments:
									<li><input type="checkbox" name="attachment" value="${a['file_id']}"/>${a['file_name']}</li>
								%endfor
							</ul>
						</div>
						%endif
				  </td>
				</tr>
				<tr>
					<td colspan="2" style="text-align:right;">
						<input type="button" class="btn" value="Send" onclick="toSubmit()"/>&nbsp;&nbsp;
						<input type="button" class="btn" value="Cancel"/>
					</td>
				</tr>
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


<%def name="email_session(postfix,values={})">
	%if postfix == 'vendor':
		<div id="div_${postfix}" style="display:none">
	%else:
		<div id="div_${postfix}">
	%endif
		
		<table cellspacing="0" cellpadding="3" border="1">
			<tr>
				<td width="150">Address</td>
				<td><textarea type="text" name="ship_to_address_${postfix}" id="ship_to_address_${postfix}" class="t_area">${values.get('address','')}</textarea> </td>
			</tr>
			<tr>
				<td>Attention</td>
				<td>
					%if postfix != 'vendor' :
						<select name="ship_to_att_${postfix}" id="ship_to_att_${postfix}" class="t_area" onchange="change_att(this)">
							<option value="" phone=""></option>
							%for m in getMaster('BBYTeammate'):
								<option value="${str(m)}" phone="${m.tel}">${m}</option>
							%endfor
						</select>
					%else:
						<input type="text" name="ship_to_att_${postfix}" id="ship_to_att_${postfix}" value="${values.get('att','')}" class="t_area"/>
					%endif
				</td>
			</tr>
			<tr>
				<td>Phone</td>
				<td><input type="text" name="ship_to_phone_${postfix}" id="ship_to_phone_${postfix}" value="${values.get('phone','')}" class="t_area"/></td>
			</tr>
			%for cc in component_casepack:
				<tr id="office_qty_tr_${cc[0].id}_${postfix}" style="display:none">
					<td>Qty (${cc[0]})</td>
					<td><input type="text" name="qty_${postfix}_${cc[0].id}" value="${values.get('qty_%d' %cc[0].id,'')}" class="t_area"/></td>
				</tr>
			%endfor
		</table>
		
		<p>Please advise courier name and AWB# once sent.<br />
		   If you have any difficulty or concern, please advise ASAP.<br />
		   Please see attached to the approved dieline and your quotation for further details.</p>
		<hr/>
	</div>
</%def>