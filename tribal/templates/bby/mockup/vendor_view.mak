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

    .fieset-css{
        margin : 10px;
        padding : 5px;
        text-align : left;
        border : 1px solid blue;
    }
    -->
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>


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
    <%
        ids = [v.id for o in header.options for v in o.vendor_fittings]
        max_id = max(ids) + 100 if ids else 100
    %>
    var max_id = ${max_id};
    //]]>
</script>


<script type="text/javascript" src="/js/custom/bby/mockup_vendor.js" language="javascript"></script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
            <tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="175" valign="top" align="left"><a href="/bbymockup/index"><img src="/images/mainmenu_g.jpg"/></a></td>
                %if not header.is_complete() and not header.is_eol():
	            %if header.status == 21 and can_submit:
                <td width="64" valign="top" align="left"><a href="/bbymockup/submit?id=${header.id}" onclick="toSubmit()"><img alt="" src="/images/images/menu_confirm_g.jpg"/></a></td>
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
            <li><a href="detail_view?id=${header.id}"><span>Mockup Details</span></a></li>
            <li  id="current"><a href="vendor_fitting?id=${header.id}"><span>Vendor Fitting</span></a></li>
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
                ${populate3(result[option.id])}<br />
                
                <table width="800" border="1" cellpadding="3" cellspacing="0">
				    <tr>
				        <td bgcolor="#FFFFFF" class="title-td" width="250">Signed Sample Received Date</td>
				        <td>${option.sample_received_date.strftime('%Y-%m-%d') if option.sample_received_date else ''}&nbsp;</td>
				    </tr>
				    <tr>
				        <td bgcolor="#FFFFFF" class="title-td">Attachment</td>
				        <td>
				            <ul>
				                %for a in option.getAttachments():
				                    <li><a href="/bbymockup/download?id=${a.id}">${a.file_name}</a>&nbsp;&nbsp;<input type="button" class="btn" value="Del" onclick="ajaxDelFile('O','${option.id}','${a.id}',this)"/></li>
				                %endfor
				            </ul>
				        </td>
				    </tr>  	
				</table>
				%if has_permission("BBY_EDIT"):
                	<p><input type="button" class="btn" value="Edit" onclick="toEdit(this)"/></p>
                %endif
                <br />
                
                %if len(result[option.id]):
                <fieldset class="fieset-css" style="width:500px">
                    <legend><b>Generate PDF</b></legend>
                    
                    <table cellspacing="3" cellpadding="3" border="1">
                    	<thead>
                    		<tr>
                    			<td></td><td>File Name</td><td>Create By</td><td>Create Time</td><td>Action</td>
                    		</tr>
                    		%for idx,att in enumerate(option.get_pdf_attachments()) :
                    			<tr>
                                    <td>${idx+1}</td>
                    				<td><a href="/bbymockup/download?id=${att.id}">${att.file_name}</a></td>
                    				<td>${att.upload_by}</td>
                    				<td>${f(att.create_time)}</td>
                    				<td><input type="button" class="btn" value="Del" onclick="ajaxDelPdfFile('O','${option.id}','${att.id}',this)"/></td>
                    			</tr>
                    		%endfor
                    	</thead>
                    </table>
					<br />
                    <form action="/bbymockup/genVendorFittingPDF">
                        <input type="hidden" name="option_id" value="${option.id}" />
                        Description of Packaging Revisions from Previous Round:<br/>
                        <input type="textfiled" name="packaging_description" style="width:400px" /><br/>
                        Score of the Packaging Assembly:<br />
                        <select name="score" id="score">
                        	<option value=""></option>
                        	<option value="1: Easy to assemble">1: Easy to assemble</option>
                        	<option value="2: Moderately easy to assemble">2: Moderately easy to assemble</option>
                        	<option value="3: Average, not fast or difficult">3: Average, not fast or difficult</option>
                        	<option value="4: Somewhat challenging">4: Somewhat challenging</option>
                        	<option value="5: Extremely difficult">5: Extremely difficult</option>
                        </select>
                        <br />
                        Packaging Supplier or Service Provider Comments:<br/>
                        <textarea name="packaging_comment" style="width:400px;height:40px;"></textarea><br/>
                        <input type="submit" class="btn" value="Generate PDF" />
                    </form>
                </fieldset>
                %endif
            </div>


            <div class="option-edit" style="display:none">
                <form action="/bbymockup/vendor_fitting_save" method="post" enctype="multipart/form-data">
                    <input type="hidden" name="option_id" value="${option.id}"/>
                    <p><input type="button" value="Add round for 'Vendors' Fitting'" onclick="addline(this,'VENDOR','table-VENDOR')" class="btn"/></p>
                    <p class="red"><sup>*</sup> Both the 'Source' and 'Sent out Date' field for each line are required, otherwise the related information won't be saved for the system !</p>
					  	${edit3(option,result[option.id])}
                    <br />
                    <table width="800" border="1" cellpadding="3" cellspacing="0">
					    <tr>
					        <td bgcolor="#FFFFFF" class="title-td" width="250">Signed Sample Received Date</td>
					        <td><input type="text" name="sample_received_date" value="${option.sample_received_date.strftime('%Y-%m-%d') if option.sample_received_date else ''}" class="datePicker"/></td>
					    </tr>
					    <tr>
					        <td bgcolor="#FFFFFF" class="title-td">Attachment</td>
					        <td>
					            
					            <div class="popup-div">
					                <table class="popup-table">
					                    <tr class="template">
					                        <td>File Name :</td><td><input type="text" name="mock_attachment_name" value=""/></td>
					                        <td>File Path :</td><td><input type="file" name="mock_attachment_path"  onchange="getFileName(this)"/></td>
					                        <td><input type="button" value="Del" onclick="delFile(this)" class="btn"/></td>
					                    </tr>
					                </table>
					                <p><input type="button" value="Add Line" onclick="addFile(this)" class="btn"/></p>
					            </div>
					        </td>
					    </tr>  	
					</table>
					<br />
                    <p><input type="button" class="btn" value="Save" onclick="toSave(this)"/>&nbsp;&nbsp;<input type="button" class="btn" value="Cancel" onclick="toCancel(this)"/></p>

                </form>
            </div>
        </div>
			%endfor
		%endif
    </div>

</div>

<!-- Main Content end -->












<%def name="populate3(vendor_fitting)">
<table cellspacing="0" cellpadding="0" border="0" class="gridTable" style="width:1400px">
    <thead>
        <tr>
            <th width="30">Round</th>
            <th>Content</th>
        </tr>
    </thead>
		%for round,fit in vendor_fitting.items():
    <tr>
        <td style="border-left:1px solid #CCCCCC">${round}</td>
        <td>
			%for component_id,component_info in fit['data'].items():
            <fieldset class="fieset-css">
                <legend><b>${component_info['component']}</b></legend>
                <table cellspacing="0" cellpadding="0" border="0" class="gridTable gridTable2">
                    <thead>
                        <tr>
                            <th width="150" style="border-left:1px solid #CCCCCC">Source</th>
                            <th width="100">Sent out Date</th>
                            <th width="50">Qty</th>
                            <th width="80">Courier</th>
                            <th width="80">AWB</th>
                            <th width="100">Received Date</th>
                            <th width="100">Reported Date</th>
                            <th width="200">Attachment</th>
                            <th width="200">Remarks</th>
                            <th width="50">Confirmed</th>
                        </tr>
                    </thead>
                    <tbody>
						%for v in component_info['data']:
                        <tr>
                            <td style="border-left:1px solid #CCCCCC">${v.source}&nbsp;</td>
                            <td>${f(v.send_date)}&nbsp;</td>
                            <td>${v.qty}&nbsp;</td>
                            <td>${v.courier}&nbsp;</td>
                            <td>${v.awb}&nbsp;</td>
                            <td>${f(v.receive_date)}&nbsp;</td>
                            <td>${f(v.reported_date)}&nbsp;</td>
                            <td>
                                <ul>
									%for att in v.getAttachments() :
                                    	<li><a href="/bbymockup/download?id=${att.id}">${att.file_name}</a>&nbsp;&nbsp;&nbsp;<input type="button" class="btn" value="Del" onclick="ajaxDelFile('V','${v.id}','${att.id}',this)"/></li>
									%endfor
                                </ul>
                                &nbsp;
                            </td>
                            <td>${v.remark}&nbsp;</td>
                            <td>${v.confirm}</td>
                        </tr>
						%endfor
                    </tbody>
                </table>
            </fieldset>
					%endfor
        </td>
    </tr>
		%endfor
</table>
</%def>





<%def name="edit3(option,vendor_fitting)">
<table cellspacing="0" cellpadding="0" border="0" class="gridTable table-VENDOR" style="width:1400px">
    <thead>
        <tr>
            <th width="30">Round</th>
            <th>Content</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
		%for round,fit in vendor_fitting.items():
        <tr>
            <td style="border-left:1px solid #CCCCCC"><span>${round}</span></td>
            <td>
                %for c in option.components:
                
                <fieldset class="fieset-css">
                    <legend><b>${c}</b> <input type="button" class="btn" value="Add" onclick="addsline(this,'component${c.id}')"/></legend>
                    <table cellspacing="0" cellpadding="0" border="0" class="gridTable gridTable2">
                        <thead>
                            <tr>
                                <th width="150">Source</th>
                                <th width="100">Sent out Date</th>
                                <th width="50">Qty</th>
                                <th width="80">Courier</th>
                                <th width="80">AWB</th>
                                <th width="100">Received Date</th>
                                <th width="100">Reported Date</th>
                                <th width="200">Attachment</th>
                                <th width="200">Remarks</th>
                                <th width="50">Confirmed</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            %if c.id in  fit['data']:
                            %for v in fit['data'][c.id]['data']:
                            <tr>
                                <td style="border-left:1px solid #CCCCCC">
                                    <input type="hidden" name="round_${v.id}" value="${v.round}"/>
                                    <input type="hidden" name="component_id_${v.id}" value="${v.component_id}"/>
                                    ${select_widget("source_id_%d" %v.id,"BBYSource",v.source_id)}
                                </td>
                                <td><input type="text" class="datePicker" name="send_date_${v.id}" value="${f(v.send_date)}"/></td>
                                <td><input type="text" name="qty_${v.id}" value="${v.qty}" class="numeric"/></td>
                                <td>${select_widget("courier_id_%d" %v.id,"BBYCourier",v.courier_id)}</td>
                                <td><input type="text" name="awb_${v.id}" value="${v.awb}"/></td>
                                <td><input type="text" class="datePicker" name="receive_date_${v.id}" value="${f(v.receive_date)}"/></td>
                                <td><input type="text" class="datePicker" name="reported_date_${v.id}" value="${f(v.reported_date)}"/></td>
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
                                <td><input type="checkbox" name="confirm_${v.id}" value="YES" ${tw.attrs([("checked",v.confirm),])}/>&nbsp;YES</td>
                                <td><input type="button" class="btn" value="Del" onclick="deletesline(this)"/></td>
                            </tr>
                            %endfor
                            %endif
                            
                            <% default_val = default[option.id].get(c.id,None) %>
                            <tr class="template component${c.id}">
                                <td style="border-left:1px solid #CCCCCC">
                                    <input type="hidden" name="round_x" value="${round}"/>
                                    <input type="hidden" name="component_id_x" value="${c.id}"/>
									${select_widget("source_id_x","BBYSource",default_val.source_id if default_val else None)}
                                </td>
                                <td><input type="text" name="send_date_x" value="${f(default_val.reported_date) if default_val else ''}" class="datePicker"/></td>
                                <td><input type="text" name="qty_x" value="" class="numeric"/></td>
                                <td>${select_widget("courier_id_x","BBYCourier",None)}</td>
                                <td><input type="text" name="awb_x" value=""/></td>
                                <td><input type="text" name="receive_date_x" value="" class="datePicker"/></td>
                                <td><input type="text" name="reported_date_x" value="" class="datePicker"/></td>
                                <td>
                                    <div class="popup-div">
                                        <table class="popup-table">
                                            <tr class="template">
                                                <td>File Name :</td><td><input type="text" name="attachment_name_x" value=""/></td>
                                                <td>File Path :</td><td><input type="file" name="attachment_path_x" onchange="getFileName(this)"/></td>
                                                <td><input type="button" value="Del" onclick="delFile(this)" class="btn"/></td>
                                            </tr>
                                        </table>
                                        <p><input type="button" value="Add Line" onclick="addFile(this)" class="btn"/></p>
                                    </div>
                                </td>
                                <td><textarea name="remark_x"></textarea></td>
                                <td><input type="checkbox" name="confirm_x" value="YES"/>&nbsp;YES</td>
                                <td><input type="button" class="btn" value="Del" onclick="deletesline(this)" onclick="deletesline(this)"/></td>
                            </tr>
                        </tbody>
                    </table>
                </fieldset>
                %endfor
            </td>
            <td><input type="button" class="btn" value="Del round" onclick="deletebline(this)"/></td>
        </tr>
        %endfor


        <tr class="template VENDOR">
            <td style="border-left:1px solid #CCCCCC"><span></span></td>
            <td>
				%for c in option.components:
				<% default_val = default[option.id].get(c.id,None) %>				
                <fieldset class="fieset-css">
                    <legend><b>${c}</b> <input type="button" class="btn" value="Add" onclick="addsline(this,'component${c.id}')"/></legend>
                    <table cellspacing="0" cellpadding="0" border="0" class="gridTable gridTable2">
                        <thead>
                            <tr>
                                <th width="150">Source</th>
                                <th width="100">Sent out Date</th>
                                <th width="50">Qty</th>
                                <th width="80">Courier</th>
                                <th width="80">AWB</th>
                                <th width="100">Received Date</th>
                                <th width="100">Reported Date</th>
                                <th width="200">Attachment</th>
                                <th width="200">Remarks</th>
                                <th width="50">Confirmed</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="template component${c.id}">
                                <td style="border-left:1px solid #CCCCCC">
                                    <input type="hidden" name="round_x" value=""/>
                                    <input type="hidden" name="component_id_x" value="${c.id}"/>
									${select_widget("source_id_x","BBYSource",default_val.source_id if default_val else None)}
                                </td>
                                <td><input type="text" name="send_date_x" value="${f(default_val.reported_date) if default_val else ''}" class="datePicker"/></td>
                                <td><input type="text" name="qty_x" value="" class="numeric"/></td>
                                <td>${select_widget("courier_id_x","BBYCourier",None)}</td>
                                <td><input type="text" name="awb_x" value=""/></td>
                                <td><input type="text" name="receive_date_x" value="" class="datePicker"/></td>
                                <td><input type="text" name="reported_date_x" value="" class="datePicker"/></td>
                                <td>
                                    <div class="popup-div">
                                        <table class="popup-table">
                                            <tr class="template">
                                                <td>File Name :</td><td><input type="text" name="attachment_name_x" value=""/></td>
                                                <td>File Path :</td><td><input type="file" name="attachment_path_x" onchange="getFileName(this)"/></td>
                                                <td><input type="button" value="Del" onclick="delFile(this)" class="btn"/></td>
                                            </tr>
                                        </table>
                                        <p><input type="button" value="Add Line" onclick="addFile(this)" class="btn"/></p>
                                    </div>
                                </td>
                                <td><textarea name="remark_x"></textarea></td>
                                <td><input type="checkbox" name="confirm_x" value="YES"/>&nbsp;YES</td>
                                <td><input type="button" class="btn" value="Del" onclick="deletesline(this)"/></td>
                            </tr>
                        </tbody>
                    </table>
                </fieldset>
                <br />
					%endfor
            </td>
            <td><input type="button" class="btn" value="Del round" onclick="deletebline(this)"/></td>
        </tr>

    </tbody>
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