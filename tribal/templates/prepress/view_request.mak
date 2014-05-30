<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
	from repoze.what.predicates import in_any_group,in_group,has_permission
	from tribal.util.prepress_helper import checkPSSameTeam
	disable = True
	_d = lambda : tw.attrs([('disabled',disable)])
%>
<%def name="extTitle()">r-pac - Prepress</%def>
<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen,print"/>

<style type="text/css" media="screen,print">
    .hlfont{font:normal 18px Tahoma, Helvetica, sans-serif;color:#069;margin:0;padding:15px 5px;}
    .action-bn{display:inline;float:right;}
    .jobs-div{border:1px solid #A6C9E2;margin-bottom:10px;overflow:hidden;width:850px;padding:10px 10px 0;}
    .one-job-div{width:800px;margin-bottom:10px;overflow:auto;}
    .one-material-div{width:400px;float:left;}
    .one-material-div span{width:80px;float:left;}
    .sample-table{border:#069 solid 1px;margin:15px;}
    .sample-Joblist{font-family:Tahoma, Geneva, sans-serif;font-size:12px;color:#000;text-decoration:none;line-height:20px;padding:10px;}
    .title-JL{font-family:Tahoma, Geneva, sans-serif;font-size:12px;line-height:normal;font-weight:700;color:#C90;text-decoration:none;}
    .sample-content{border:#069 solid 1px;background-color:#FFC;}
    #tabboxs{margin:0; padding:0;}
    #tabboxs li{margin:0; padding: 0; float: left;}
    #tabboxs li input{ line-height: 10px;}
    #jqismooth{width: 600px;}
</style>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.loadmask.min.js"></script>
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js"></script>
<script type="text/javascript" src="/js/jquery.color.js"></script>
<script type="text/javascript" src="/js/jquery.progressbar.js"></script>
<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/jquery-ui-timepicker-addon.js"></script>
<script type="text/javascript" src="/js/custom/prepress/util.js?3"></script>

<script type="text/javascript" src="/js/custom/prepress/prepress_update_request.js?3"></script>

<script type="text/javascript">
    childrenForms = ${childrenForms|n};
    updatedChildrenForms = ${updatedChildrenForms|n};
    action = 'view';
    token = '${token}';
    $(document).ready(function(){   
        $(".status-bar").progressBar();
        $(".numeric").numeric();
        $('#page-div :input').not('#printjobdiv :input').not('#assigndiv :input').each(function(){
            disableField($(this));
        });
        // print-job
        $('#printdialog input[name=printall]').live('click', function(){
        	if($(this).attr("checked") == true){
        		$('#printdialog input[name=tabpos]').each(function(){
					$(this).attr("checked","checked");
        		});
        	}else{
        		$('#printdialog input[name=tabpos]').each(function(){
					$(this).removeAttr("checked");
        		});
        	}
        });
        $('#printdialog input[name=tabpos]').live('click', function(){
        	
        	if($('#printdialog input[name=tabpos]:checked').length 
        		== $('#printdialog input[name=tabpos]').length){
        		$('#printdialog input[name=printall]').attr("checked","checked");
        	}else{
        		$('#printdialog input[name=printall]').removeAttr("checked");
        	}
        });
        
    });
    
    function printjob (){
       var li_html = '';
        $('a', '#tabs ul li').each(function(index){
            li_html += '<li><input name="tabpos" type="checkbox" value="'
                        + index +'-'
                        + $(this).text().replace(/[\\\/\:\*\?\"\<\>\|\s]/g, '_')
                        + '" /><span style="color: #2E8ED4;">'
                        + $(this).text() 
                        + '</span>&nbsp;&nbsp;</li>';
        });
        $('#tabboxs').html(li_html);
    	$.prompt('<div id="printdialog">'+$('#printjobdiv').html()+'</div>', 
    	{
    		 show:'slideDown',
    		 prefix:'jqismooth',
			submit: printjobsubmit,
			buttons: { Ok: true}
		});
    }
   function printjobsubmit(v,m,f){
   		var pos = [];
   		var files = [];
   		var not_pos = false;
   		var not_files = false;
   		$('#printdialog .filemsg').html('');
   		$('#printdialog .printmsg').html('');
        $('#printdialog input[name=tabpos]:checked').each(function(){
        		pos.push($(this).val());
        });
        $('#printdialog input[name=filetypes]:checked').each(function(){
                files.push($(this).val());
        });
        if(files.length<1){
            $('#printdialog .filemsg').html('*Please select one type at least!');
            not_files = true;
        }
        if(pos.length<1){
        	$('#printdialog .printmsg').html('*Please select one tab at least!');
        	not_pos = true;
        }
        if(not_files || not_pos){
            return false;
        }else{
        	$('#printdialog input[name=positions]').val(pos.join('|'));
        	$('#printdialog input[name=file_exts]').val(files.join('-'));
        	$('#printdialog .printmsg').html('Submit...');
        	$('#printdialog form').submit();
        	// $.prompt('<center>Downloading...</center>', {
        		// timeout: 1000
        	// });
		    return true;
        }
   }
   
   function ajaxCancelAll(params){
		if(!confirm('This action would cancel all the tasks which are not completed,are you sure to go ahead?')){
			return false;
		}
	    $("body").mask("Loading...");
	    params['timestr'] = Date.parse(new Date());
	    $.getJSON("/prepress/ajaxMark", params, function (req){
	        if( req.flag == "0" ){
	            alert("The record has been updated successfully!");
	            window.location.reload(true);
	        }else if(req.flag == "2"){
	            alert("No such action!");
	        }else{
	            alert("Error on the serve !");
	        }
	        $("body").unmask();
	    })
	}
	
	var myprompt;
	
	function assign(){
		myprompt = $.prompt('<div id="assigndialog">'+$('#assigndiv').html()+'</div>', 
    	{
    		 show:'slideDown',
    		 prefix:'jqismooth',
			 submit: ajaxAssign,
			 buttons: { "Submit" : true,  "Cancel" : false }
		});
	}
	
	
	function ajaxAssign(){
	    var assign_user_ids = [];
	    $('input[name="user_ids"]:checked').each(function() {
	        assign_user_ids.push($(this).val());
	    });
		if(assign_user_ids.length == 0){
			$('#assigndialog .assignmsg').html('*Please select the Applicable Teamer to assign!');
			return false; 
		}
		var params = {
            'form_id' : ${main.id},
            'assign_user_ids' : assign_user_ids.join("|"),
            't' : Date.parse(new Date())
		}
		$.getJSON("/prepress/ajaxAssign",params,function(r){
			if(r.code != 0){
				alert(r.msg);
			}else{
				alert("The job is assigned successfully!");
				$("#assigntd").remove();
				myprompt.remove();
				window.location.reload(true);
			}
		})
	}
</script>
</%def>

              
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
            <tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="64" valign="top" align="left"><a href="/prepress/index"><img src="/images/images/prepress_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="/prepress/updateRequest?id=${main.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="/prepress/copyRequest?id=${main.id}"><img src="/images/images/menu_copy_g.jpg"/></a></td>
				
				%if has_permission('PREPRESS_ASSIGN') and main.status == 0:
	                <td width="64" valign="top" align="left" id="assigntd"><a href="javascript:assign()"><img src="/images/images/assign_g.jpg"/></a></td>
                %endif
                
                % if len(main.getChildren()) > 0:
                <td width="64" valign="top" align="left"><a href="javascript:printjob()"><img src="/images/images/menu_printjob_g.jpg"/></a></td>
                %endif
                <td width="64" valign="top" align="left"><a href="/prepress/viewDevelopmentLog?id=${main.id}"><img src="/images/images/menu_log_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="/prepress/index"><img src="/images/images/menu_return_g.jpg"/></a></td>

                %if canCancelForms:
                	%if checkPSSameTeam(request.identity['user'],main) or has_permission('PREPRESS_EDIT'):
                		<td width="64" valign="top" align="left"><a href="#" onclick="ajaxCancelAll({form_ids:'${canCancelForms}',action:'X'})"/><img src="/images/images/cancel_all_g.jpg"/></a></td>
                	%endif
                %endif
                <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
                <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
            </tr>
        </tbody>
    </table>
</div>


<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Prepress</div>
<div style="width:1200px;padding-left:0px;">
    <div class="div-900-400">
        <div class="div-300-400" style="margin-left:10px;">
            <table width="100%" border="0" cellspacing="1" style="background:#333333;">
                <tr>
                    <td style="background:#ffffff">
                        <ul>
                            <li>Project Owner</li>
                            <li> </li>
                        </ul>
                        <ul>
                            <li style=""><label for="project_own">Region</label></li>
                            <li><input type="text" value="${main.project_own}" class="input-150px"/></li>
                        </ul>
                        <ul>
                            <li><label for="owner_name">Owner Name</label></li>
                            <li>
                                <input class="input-150px inputText" value="${main.project_owner}" class="input-150px" id="project_owner" name="project_owner">
                            </li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td style="background:#ffffff">
                        <ul>
                            <li>Business Unit</li>
                            <li> </li>
                        </ul>
                        <ul>
                            <li><label for="team">Division Team</label> </li>
                            <li><input type="text" value="${main.team}" class="input-150px"/></li>
                        </ul>
                        <ul>
                            <li><label for="contact_person">Contact Person</label></li>
                            <li><input name="contact_person" id="contact_person" value="${main.contact_person}" class="input-150px"/></li>
                        </ul>
                    </td>
                </tr>
            </table>
            <ul>
                <li><label for="reference_code">Reference Code</label></li>
                <li><input name="reference_code" id="reference_code" value="${main.reference_code}" class="input-150px"/></li>
            </ul>
            <ul>
                <li><label for="customer">Vendor/Customer</label></li>
                <li><input type="text" value="${main.customer}" class="input-150px"/></li>
            </ul>
            <ul>
                <li><label for="project">Brand</label></li>
                <li><input type="text" value="${main.project}" class="input-150px"/></li>
            </ul>
            <ul>
                <li><label for="item_category">Item Category</label></li>
                <li><input type="text" value="${main.item_category}" class="input-150px"/></li>
            </ul>
            <ul>
                <li><label for="item_description">Item Description</label></li>
                <li>
                    <textarea name="item_description" id="item_description" value="" class="input-150px" style="height:120px">${main.item_description}</textarea>
                </li>
            </ul>
            <ul>
                <li><label for="item_code">Item Code</label></li>
                <li>
                    <!-- input name="item_code" id="item_code" value="${main.item_code}" class="input-150px"/ -->
                    <textarea id="item_code" name="item_code" class="input-150px" style="height:120px">${main.item_code}</textarea>
                </li>
            </ul>
        </div>
        <div class="div-300-400">
            <ul>
                <li><label for="job_no">Job No</label></li>
                <li>
                    <input type="text" value="${main}" class="input-150px"/>
                </li>
            </ul>
            <ul>
                <li><label for="request_person">Request Person</label></li>
                <li>
                    <input type="text" value="${main.create_by}" class="input-150px"/>
                </li>
            </ul>
            <ul>
                    <li><label>Contact Number</label></li>
                    <li>
                        <input type="text" value="${main.request_contact_number}" name="request_contact_number" id="request_contact_number" class="input-150px"/>
                    </li>
                </ul>
            <ul>
                <li><label for="team"> Request Person's Team</label></li>
                <li><input type="text" value="${rpt}" class="input-150px"/></li>
            </ul>
            <ul>
                <li><label for="create_time">Request Date</label></li>
                <li>
                    <input type="text" value="${main.create_time.strftime("%Y-%m-%d %H:%M")}" class="input-150px"/>
                </li>
            </ul>
            <ul>
                <li><label for="percentage">Last Update Time</label></li>
                <li>
                    <input type="text" value="${main.update_time.strftime("%Y-%m-%d %H:%M")}" class="input-150px"/>
                </li>
            </ul>
            <ul>
                <li><label for="percentage">Last Update By</label></li>
                <li>
                    <input type="text" value="${main.update_by}" class="input-150px"/>
                </li>
            </ul>
            <ul>
                <li><label for="create_time">E-mail CC to</label></li>
                <li>
                    <textarea id="cc_to" name="cc_to" class="input-150px" style="height:120px">${main.cc_to}</textarea>
                </li>
            </ul>
            <ul>
                <li><label for="percentage">Status</label></li>
                <li style="text-align:center;vertical-align:middle">
                	%if main.status == -9:
                		Cancelled
                	%else:
                		<span class="status-bar">${"%d%%" %(main.percentage*100)}</span>
                	%endif
                </li>
            </ul>
        </div>
        
        <!-- print-job -->
        % if len(main.getChildren()) > 0:
        <div id="printjobdiv" style="margin-left:26px; display: none;"> 
         <form action="/prepress/snapshot" method="post">
         	<input type="hidden" name="snapshot_url"  value='viewRequest?id=${main.id}'/>
         	<input type="hidden" name="positions" value="" />
         	<input type="hidden" name="file_exts" value="" />
         	<input type="hidden" name="jobno"  value="${main}"/>
         	<fieldset style="padding-left: 6px;">
         	<legend><span style="font-weight: bold; color: #456884;">Export to PDF/PNG</span></legend>
         	
         	<table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="margin-bottom:2px;border-bottom: 1px solid #DDDDDD;">
          		<tbody>
          		<tr>
          		 <td>
          		     <input id="filetypes" name="filetypes" type="checkbox" value="pdf" checked="checked" /><span style="color:#2E8ED4;">PDF</span>
          		     <input id="filetypes" name="filetypes" type="checkbox" value="png" checked="checked" /><span style="color:#2E8ED4;">PNG</span>
          		     &nbsp;<span class='filemsg' style="color: #ff0000;"></span>
          		 </td>
          		</tr>    		
           	     </tbody>
             </table>
         	
        	 <table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="">
          		<tbody>
          		<tr>
                 <td><input id="printall" name="printall" type="checkbox" value="all" />Select All
                     &nbsp;<span class='printmsg' style="color: #ff0000;"></span>
                 </td>
               </tr>
           	   
           	   <tr>
           	   	<td>
           	   	    <ul id="tabboxs"></ul>
           	   	</td>
           	   </tr>
               </tbody>
             </table>
         	</fieldset>
         </form>
        </div>
        %endif
        <!-- print-job -->
        
        %if has_permission('PREPRESS_ASSIGN'):
        <div id="assigndiv" style="margin-left:26px; display: none;">
        	<fieldset>
	        	<legend><span style="font-weight: bold; color: #456884;">Assign To Applicable Team</span></legend>
	         	<table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="margin-bottom:2px;border-bottom: 1px solid #DDDDDD;">
	          		<tbody>
	          		<tr>
	          		 <td>
	          		     %for at in app_teams:
	          		        <span>${at}</span><br/>
	          		        %for user in at.users:
	          		            <input name="user_ids" type="checkbox" value="${user.user_id}"/><span style="color:#2E8ED4;">${user}</span><br />
	          		        %endfor
	          		     %endfor
	          		     &nbsp;<span class='assignmsg' style="color: #ff0000;"></span>
	          		 </td>
	          		</tr>
	           	     </tbody>
	             </table>
             </fieldset>
        </div>	
        %endif

        <div class="clear"><br /></div>
    </div>
     
    <div class="clear"><br /></div>
    
    <div id="tabs" style="margin-left:20px;width:900px;">
        <ul></ul>
    </div>

</div>	