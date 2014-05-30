<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
	from tribal.util.bby_helper import getMaster
%>

<%def name="extTitle()">r-pac - (BBY)Mockup</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/bby.css" type="text/css" media="screen"/>
<style type="text/css">
<!--
	.bold_font {
		padding-left:20px;
		font-size: 12px;
		line-height: 24px;
		font-weight: bold;
		color: #069;
		text-decoration: none;
	}
	.text_td {
		padding-left:20px;
	}

	td {
		font-family: Tahoma, Geneva, sans-serif;
		font-size: 12px;
		line-height: normal;
		color: #000;
		text-decoration: none;
	}

	.date-session{
		list-style : none;
		padding-left : 0px;
	}
	.date-session li{
		padding-bottom : 3px;
	}
	
	.gridTable ul{
		margin-left:5px;
		padding-left:0px;
		list-style:none;
		text-align:left;
		margin-bottom : 5px;
		margin-top : 5px;
		margin-right : 5px;
	}
	.template{
		display : none;
	}
	
	.ui-widget{
		font-size : 12px;
	}
	
	.gridTable2 thead th{
		background-color : gray;
	}
-->
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>

<script type="text/javascript" src="/js/custom/bby/mockup_detail.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
    //<![CDATA[
	var dateFormat = 'yy-mm-dd';
    $(document).ready(function(){
    	<%	
    		selected = 0
    		for index ,o in enumerate(header.options):
    			if o.final :
    				selected = index
    	%>
    	$( "#tabs" ).tabs({selected : ${selected}});
    	
    	$('.datePicker').datepicker({
	        changeMonth : true,
	        changeYear : true,
	        dateFormat : dateFormat
	      });
	      
	    $(".numeric").numeric();
	    
    });
    
    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
        <tr>
            <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
            <td width="175" valign="top" align="left"><a href="/bbymockup/index"><img src="/images/mainmenu_g.jpg"/></a></td>
            %if not header.is_complete() and not header.is_eol():
	            %if header.status == 21 and can_submit:
	           		<td width="64" valign="top" align="left"><a href="/bbymockup/submit?id=${header.id}" onclick="return toSubmit();"><img src="/images/images/menu_confirm_g.jpg"/></a></td>
            	%endif
            %endif
	        
            <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
            <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
        </tr>
        </tbody>
    </table>
</div>
	       
            

<div class="nav-tree">BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Mockup</div>



<!-- Main content begin -->
<div style="width:1500px;">
	
    	<div id="tabsJ">
	    	<ul>
				<li><a href="item_view?id=${header.id}"><span>Item Information</span></a></li>
				<li id="current"><a href="detail_view?id=${header.id}"><span>Mockup Details</span></a></li>
				<li><a href="vendor_fitting?id=${header.id}"><span>Vendor Fitting</span></a></li>
				<li><a href="history?id=${header.id}"><span>History</span></a></li>
			</ul>
    	</div>
    
	  <div><br class="clear"/><br /></div>
	  
      <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
    	${widget(value=values)|n}
	  </div>
	  
	  
	  <div id="tabs" style="margin: 5px 0px 10px 10px;">	  
  	    %if header.options:
        <ul>
        	%for o in header.options:
				<li><a href="#option-testing-${o.id}">Option - ${o.name}
					%if o.final:
					(Final)
					%endif
					</a>
				</li>
			%endfor
        </ul>
  	    
	  	    %for option in header.options:
			  	<div id="option-testing-${option.id}">
			  		
			  		<div class="option-view">  	
					  	<p><b>Internal Fitting</b></p>
					  	${populate1(option.internal_fittings)}
					  	<br />
					  	
					  	<p><b>Internal Drop Test Report</b></p>
					  	${populate2(testing_data[option.id]["DROP"])}
					  	<br />
					  	
					  	<p><b>Internal Hanging Test Report</b></p>
					  	${populate2(testing_data[option.id]["HANGING"])}
					  	<br />
					  	
					  	%if has_permission("BBY_EDIT"):
						  	<p><input type="button" class="btn" value="Edit" onclick="toEdit(this)"/></p>
		       			%endif
					</div>
					
					
					<div class="option-edit" style="display:none">
						<form action="/bbymockup/save_detail_edit" method="post" enctype="multipart/form-data">
						<input type="hidden" name="option_id" value="${option.id}"/>
						
						<p><input type="button" id="internal_fitting_btn" value="Add round for 'Internal Fitting'" onclick="addFitting(this,'INTERNAL')" class="btn" max_round="${option.get_max_internal_fitting_round()+1}"/></p>
		  				<p class="red"><sup>*</sup> The 'Received Date' field for each line is required, otherwise the related information won't be saved for the system !</p>
					  	${edit1(option.internal_fittings,option)}
					  	<br />
					  	
					  	<!-- <p><input type="button" value="Add round for 'Internal Drop Test Report'" onclick="addline(this,'DROP','table-DROP')" class="btn"/></p> -->
		  				<p class="red"><sup>*</sup> The 'Sent out Date' field for each line is required, otherwise the related information won't be saved for the system !</p>
					  	${edit2(testing_data[option.id]["DROP"],"DROP",option)}
					  	<br />
					  	
					  	<!-- <p><input type="button" value="Add round for 'Internal Hanging Test Report'" onclick="addline(this,'HANGING','table-HANGING')" class="btn"/></p> -->
		  				<p class="red"><sup>*</sup> The 'Sent out Date' field for each line is required, otherwise the related information won't be saved for the system !</p>
					  	${edit2(testing_data[option.id]["HANGING"],"HANGING",option)}
					  	<br />
	

					  	<p><input type="button" class="btn" value="Save" onclick="toSave(this)"/>&nbsp;&nbsp;<input type="button" class="btn" value="Cancel" onclick="toCancel(this)"/></p>
					  	
						</form>				
					</div>
			  	</div>
			%endfor
		%endif
	  </div>
	
</div>
	  						


</div>
<!-- Main Content end -->










<%def name="populate1(l)">
	<table cellspacing="0" cellpadding="0" border="0" class="gridTable" style="width:1300px">
		<thead>
		<tr>
			<th width="30">Round</th>
			<th>Content</th>
		</tr>
		</thead>
		%for row in l:
			<tr>
				<td style="border-left:1px solid #CCCCCC">${row.round}</td>
				<td style="text-align:left;">
					<ul>
						%for c in row.getContent():
							<li>${c}</li>
						%endfor
					</ul>
                    <table cellspacing="0" cellpadding="0" border="0">
                        <thead>
                        	<th width="120">Component</th>
                            <th width="120">Received Date</th>
                            <th width="150">Source</th>
                            <th width="80">Test By</th>
                            <th width="50">Qty</th>
                            <th width="80">PASS/FAIL</th>
                            <th width="120">Reported Date</th>
                            <th width="200">Reasons for Failure</th>
                            <th width="200">Attachment</th>
                            <th width="250">Remarks</th>	
                            <th width="100">Courier</th>	
                            <th width="100">AWB</th>	
                        </thead>
                        <tbody>
                        	%for v in row.details:
                        		<tr>
		                        	<td>${v.component}&nbsp;</td>
		                            <td>${f(v.received_date)}&nbsp;</td>
		                            <td>${v.source}&nbsp;</td>
		                            <td>${v.test_by}&nbsp;</td>
		                            <td>${v.qty}&nbsp;</td>
		                            <td>${v.result}&nbsp;</td>
		                            <td>${f(v.reported_date)}&nbsp;</td>
		                            <td>${v.reason}&nbsp;</td>
		                            <td>
		                                <ul>
		                                    %for att in v.getAttachments() :
		                                        <li><a href="/bbymockup/download?id=${att.id}">${att.file_name}</a> <input type="button" class="btn" value="Del" onclick="ajaxDelFile('I','${v.id}','${att.id}',this)"/></li>
		                                    %endfor
		                                </ul>
		                                &nbsp;
		                            </td>
		                            <td>${v.remark}&nbsp;</td>
		                            <td>${v.courier}&nbsp;</td>
		                            <td>${v.awb}&nbsp;</td>
                        		</tr>
                        	%endfor
                        </tbody>
                    </table>
				</td>
			</tr>
		%endfor
	</table>
</%def>



<%def name="edit1(l,option)">
<table cellspacing="0" cellpadding="0" border="0" class="gridTable table-INTERNAL" style="width:1400px">
    <thead>
        <th style="width:50px;">Round</th>
        <th style="width:5000px;">Content</th>
        <th style="width:100px;">Action</th>
    </thead>
    <tbody>
        %for row in l:
            <tr class="bline">
                <td style="border-left:1px solid #CCCCCC">
                	<span>${row.round}</span>
                	<input type="hidden" name="internal_round_${row.id}" value="${row.id}"/>
                </td>
                <td> 
	                <p style="text-align:left">
	                	<input type="button" value="Add Drop Testing" class="testing_btn btn" round="${row.round}" line="1" onclick="addTesting(this,'DROP')"/>&nbsp;&nbsp;&nbsp;
	                	<input type="button" value="Add Hanging Testing" class="testing_btn btn" round="${row.round}" line="1" onclick="addTesting(this,'HANGING')"/>
	                </p>
                    <ul>
                    <% cs = row.getContent(True) %>
                    %for s in getMaster("BBYMockupContent"):
                        <li><input type="checkbox" name="internal_content_${row.id}" value="${s.id}" id="internal_content_${row.id}_${s.id}" ${tw.attrs([('checked',str(s.id) in row.getContent(True))])}/>
                            <label for="internal_content_${row.id}_${s.id}">${s}</label>
                        </li>
                    %endfor
                    </ul>
                    <table>
                        <thead>
                        	<th>Component</th>
                            <th>Received Date</th>
                            <th>Source</th>
                            <th>Test By</th>
                            <th>Qty</th>
                            <th>PASS/FAIL</th>
                            <th>Reported Date</th>
                            <th>Reasons for Failure</th>
                            <th>Attachment</th>
                            <th>Remarks</th>	
                            <th>Courier</th>	
                            <th>AWB</th>
                        </thead>
                        <tbody>
                        	%for v in row.details:
                        		<tr>
		                        	<td>${v.component}</td>
		                            <td><input type="text" name="internal_received_date_${v.id}" value="${v.received_date.strftime('%Y-%m-%d') if v.received_date else ''}" class="datePicker"/></td>
		                            <td>${select_widget("internal_source_id_%d" %v.id,'BBYSource',v.source_id)}</td>
		                            <td>${select_widget("internal_test_by_id_%d" %v.id,'BBYTeammate',v.test_by_id)}</td>
		                            <td><input type="text" name="internal_qty_${v.id}" value="${v.qty}"/></td>
		                            <td>
		                                <select name="internal_result_${v.id}">
		                                    %for o in ['','PASS','FAIL']:
		                                    <option value="${o}" ${tw.attrs([('selected',o==v.result),])}>${o}</option>
		                                    %endfor
		                                </select>
		                            </td>
		                            <td><input type="text" name="internal_reported_date_${v.id}" value="${v.reported_date.strftime('%Y-%m-%d') if v.reported_date else ''}" class="datePicker"/></td>
		                            <td>${select_widget('internal_reason_id_%d' %v.id,'BBYFailureReason',v.reason_id)}</td>
		                            <td>   
		                                <div class="popup-div">
		                                    <table class="popup-table">
		                                        <tr class="template">
		                                            <td>File Name :</td><td><input type="text" name="internal_attachment_name_${v.id}"/></td>
		                                            <td>File Path :</td><td><input type="file" name="internal_attachment_path_${v.id}" onchange="getFileName(this)"/></td>
		                                            <td><input type="button" value="Del" onclick="delFile(this)" class="btn"/></td>
		                                        </tr>
		                                    </table>
		                                    <p><input type="button" value="Add Line" onclick="addFile(this)" class="btn"/></p>
		                                </div>
		                                
		                            </td>
		                            <td><textarea name="internal_remark_${v.id}"  style="width: 150px;">${v.remark}</textarea></td>
		                            <td>${select_widget('internal_courier_id_%d' %v.id,'BBYCourier',v.courier_id)}</td>
		                            <td><input type="text" name="internal_awb_${v.id}" value="${v.awb}"/></td>
                        		</tr>
                        	%endfor
                        </tbody>
                    </table>
                </td>
                <td><input class="btn" type="button" value="Del Round" onclick="delFitting(this);"/></td>
            </tr> 
        %endfor
                 		
        <tr class="template INTERNAL bline">
            <td style="border-left:1px solid #CCCCCC"><span/>&nbsp;
            </td>
            <td>
                <p style="text-align:left">
                	<input type="button" value="Add Drop Testing" class="testing_btn btn" round="" line="1" onclick="addTesting(this,'DROP')"/>&nbsp;&nbsp;&nbsp;
                	<input type="button" value="Add Hanging Testing" class="testing_btn btn" round="" line="1" onclick="addTesting(this,'HANGING')"/>
                </p>
                <ul>
                    %for s in getMaster("BBYMockupContent"):
                        <li><input type="checkbox" name="internal_new_content_x" value="${s.id}" id="internal_new_content_${s.id}_x"/>
                            <label for="internal_new_content_${s.id}_x">${s}</label>
                        </li>
                    %endfor
                </ul>
            	<input type="hidden" name="internal_new_round_x" value=""/>
                <table>
                    <thead>
                    	<th>Component</th>
                        <th>Received Date</th>
                        <th>Source</th>
                        <th>Test By</th>
                        <th>Qty</th>
                        <th>PASS/FAIL</th>
                        <th>Reported Date</th>
                        <th>Reasons for Failure</th>
                        <th>Attachment</th>
                        <th>Remarks</th>	
                        <th>Courier</th>	
                        <th>AWB</th>
                    </thead>
                    <tbody>
                    	%for c in option.components:
                    	<tr>
	                    	<td>${c}
	                    		<input type="hidden" name="internal_new_component_id_x_${c.id}" value="${c.id}"/>
	                    	</td>
	                        <td><input type="text" name="internal_new_received_date_x_${c.id}" value="" class="datePicker"/></td>
	                        <td>${select_widget("internal_new_source_id_x_%d" %c.id,'BBYSource',None)}</td>
	                        <td>${select_widget("internal_new_test_by_id_x_%d" %c.id,'BBYTeammate',None)}</td>
	                        <td><input type="text" name="internal_new_qty_x_${c.id}" value=""/></td>
	                        <td>
	                            <select name="internal_new_result_x_${c.id}">
	                                %for o in ['','PASS','FAIL']:
	                                <option value="${o}">${o}</option>
	                                %endfor
	                            </select>
	                        </td>
	                        <td><input type="text" name="internal_new_reported_date_x_${c.id}" value="" class="datePicker"/></td>
	                        <td>${select_widget('internal_new_reason_id_x_%d' %c.id,'BBYFailureReason',None)}</td>
	                        <td>
	                            <div class="popup-div">
	                                <table class="popup-table">
	                                    <tr class="template">
	                                        <td>File Name :</td><td><input type="text" name="internal_new_attachment_name_x_${c.id}" value=""/></td>
	                                        <td>File Path :</td><td><input type="file" name="internal_new_attachment_path_x_${c.id}" onchange="getFileName(this)"/></td>
	                                        <td><input type="button" value="Del" onclick="delFile(this)" class="btn"/></td>
	                                    </tr>
	                                </table>
	                                <p><input type="button" value="Add Line" onclick="addFile(this)" class="btn"/></p>
	                            </div>
	                        </td>
	                        <td><textarea name="internal_new_remark_x_${c.id}" style="width: 150px;"></textarea></td>
	                        <td>${select_widget('internal_new_courier_id_x_%d' %c.id,'BBYCourier',None)}</td>
	                        <td><input type="text" name="internal_new_awb_x_${c.id}" value=""/></td>
                        </tr>
                        %endfor
                    </tbody>
                </table>
            </td>
            <td><input class="btn" type="button" value="Del Round" onclick="delFitting(this);"/></td>
        </tr>
    </tbody>
</table>
</%def>
                        



<%def name="populate2(data)">
	<table cellspacing="0" cellpadding="0" border="0" class="gridTable" style="width:1400px">
		<thead>
		<tr>
			<th width="30">Round</th>
			<th>Content</th>						
		</tr>
		</thead>	
		%for round_line,content in data.items():
			<tr>
				<td style="border-left:1px solid #CCCCCC">${round_line.split("_")[0]}</td>
				<td style="text-align:left">
					%for v in content:
						<fieldset>
							<legend><b>${v.component}</b></legend>
							<table>
								<thead>
									<th width="100">Sent out Date</th>
									<th width="150">Source</th>
									<th width="100">Test By</th>
									<th width="50">Qty</th>
									<th width="80">PASS/FAIL</th>
									<th width="100">Reported Date</th>
									<th width="200">Reasons for Failure</th>
									<th width="200">Attachment</th>
									<th>Remarks</th>
								</thead>
								<tr>
									<td>${f(v.send_date)}&nbsp;</td>
									<td>${v.source}&nbsp;</td>
									<td>${v.test_by}&nbsp;</td>
									<td>${v.qty}&nbsp;</td>
									<td>${v.result}&nbsp;</td>
									<td>${f(v.reported_date)}&nbsp;</td>
									<td>${v.reason}&nbsp;</td>
									<td>
										<ul>
											%for att in v.getAttachments() :
												<li><a href="/bbymockup/download?id=${att.id}">${att.file_name}</a><input type="button" class="btn" value="Del" onclick="ajaxDelFile('T','${v.id}','${att.id}',this)"/></li>
											%endfor
										</ul>
										&nbsp;
									</td>
									<td>${v.remark}&nbsp;</td>
								</tr>
							</table>						
						</fieldset>
					%endfor
				</td>
			</tr>
		%endfor
	</table>
</%def>





<%def name="edit2(data,test_type,option)">
	<table cellspacing="0" cellpadding="0" border="0" class="gridTable table-${test_type}" id="${test_type}">
		<thead>
		<tr>
			<th>Round</th>
			<th style="width:5000px;">Content</th>
			<th>Action</th>
		</tr>
		</thead>
			%for round_line,content in data.items():
				<tr>
					<td style="border-left:1px solid #CCCCCC">${round_line.split("_")[0]}</td>
					<td style="text-align:left">
						%for v in content:
							<fieldset class="fieset-css" style="width:500px;display:block">
								<legend><b>${v.component}</b></legend>
								<table>
									<thead>
										<th>Sent out Date</th>
										<th>Source</th>
										<th>Test By</th>
										<th>Qty</th>
										<th>PASS/FAIL</th>
										<th>Reported Date</th>
										<th>Reasons for Failure</th>
										<th>Attachment</th>
										<th>Remarks</th>
		
									</thead>
									<tr class="bline">
										<td><input type="text" name="send_date_${v.id}" value="${v.send_date.strftime('%Y-%m-%d') if v.send_date  else ''}" class="datePicker"/></td>
										<td>${select_widget("source_id_%d"%v.id,'BBYSource',v.source_id)}</td>
										<td>${select_widget("test_by_id_%d"%v.id,'BBYTeammate',v.test_by_id)}</td>
										<td><input type="text" name="qty_${v.id}" value="${v.qty}"/></td>
										<td>
											<select name="result_${v.id}">
												%for o in ['','PASS','FAIL']:
												<option value="${o}" ${tw.attrs([('selected',o==v.result),])}>${o}</option>
												%endfor
											</select>
										</td>
										<td><input type="text" name="reported_date_${v.id}" value="${v.reported_date.strftime('%Y-%m-%d') if v.reported_date else ''}" class="datePicker"/></td>
										<td>${select_widget('reason_id_%d'%v.id,'BBYFailureReason',v.reason_id)}</td>
										<td>		
											<div class="popup-div">
											    <table class="popup-table">
											        <tr class="template">
											            <td>File Name :</td><td><input type="text" name="attachment_name_${v.id}" value=""/></td>
											            <td>File Path :</td><td><input type="file" name="attachment_path_${v.id}" onchange="getFileName(this)"/></td>
											            <td><input type="button" value="Del" onclick="delFile(this)" class="btn"/></td>
											        </tr>
											    </table>
											    <p><input type="button" value="Add Line" onclick="addFile(this)" class="btn"/></p>
											</div>
										</td>
										<td><textarea name="remark_${v.id}">${v.remark}</textarea></td>
									</tr>
								</table>
							</fieldset>
						%endfor
					</td>
					<td><input type="button" class="btn" value="Del Round" onclick="delTesting(this);"/></td>
				</tr>
			%endfor
			<tr class="template ${test_type} bline">
				<td style="border-left:1px solid #CCCCCC"><span/></td>
				<td style="text-align:left">
					%for c in option.components:
						<fieldset class="fieset-css" style="width:500px;display:block">
							<legend><b>${c}</b></legend>
							<input type="hidden" name="new_test_type_x" value="${test_type}"/>
							<input type="hidden" name="new_test_round_x" value=""/>
							<input type="hidden" name="new_test_line_x" value=""/>
							<input type="hidden" name="new_test_component_id_x" value="${c.id}"/>
							
							<table cellspacing="0" cellpadding="0" border="0" class="gridTable">
								<thead>
									<th>Sent out Date</th>
									<th>Source</th>
									<th>Test By</th>
									<th>Qty</th>
									<th>PASS/FAIL</th>
									<th>Reported Date</th>
									<th>Reasons for Failure</th>
									<th>Attachment</th>
									<th>Remarks</th>
					
								</thead>
								<tr>
									<td style="border-left:1px solid #CCCCCC"><input type="text" name="new_send_date_x" value="" class="datePicker" style="width:150px"/></td>
									<td>${select_widget("new_source_id_x",'BBYSource',None)}</td>
									<td>${select_widget("new_test_by_id_x",'BBYTeammate',None)}</td>
									<td><input type="text" name="new_qty_x" value="" style="width:150px"/></td>
									<td>
										<select name="new_result_x" style="width:150px">
											%for o in ['','PASS','FAIL']:
											<option value="${o}">${o}</option>
											%endfor
										</select>
									</td>
									<td><input type="text" name="new_reported_date_x" value="" class="datePicker" style="width:150px"/></td>
									<td>${select_widget('new_reason_id_x','BBYFailureReason',None)}</td>
									<td>
										<div class="popup-div">
											<table class="popup-table">
												<tr class="template">
													<td>File Name :</td><td><input type="text" name="new_attachment_name_x" value=""/></td>
													<td>File Path :</td><td><input type="file" name="new_attachment_path_x" onchange="getFileName(this)"/></td>
													<td><input type="button" value="Del" onclick="delFile(this)" class="btn"/></td>
												</tr>
											</table>
											<p><input type="button" value="Add Line" onclick="addFile(this)" class="btn"/></p>
										</div>
									</td>
									<td><textarea name="new_remark_x" style="width:150px"></textarea></td>
								</tr>
							</table>
						</fieldset>
					%endfor
				</td>
				<td><input type="button" class="btn" value="Del Round" onclick="delTesting(this);"/></td>
			</tr>
	</table>
</%def>




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