<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
	from datetime import datetime as dt
	from tribal.util.mako_filter import b,tp
%>
<%def name="extTitle()">r-pac - Prepress</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/impromt.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>
<!-- link rel="stylesheet" href="/css/jquery.multiSelect.css" type="text/css" media="screen"/ -->
<style type="text/css">
    div.cleanred{width:700px;}
    .hlfont{font:normal 18px Tahoma, Helvetica, sans-serif;color:#069;margin:0;padding:15px 5px;}
    .action-bn{display:inline;float:right;}
</style>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.loadmask.min.js"></script>
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js"></script>
<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/jquery-ui-timepicker-addon.js"></script>
<!-- script type="text/javascript" src="/js/jquery.multiSelect.js"></script -->
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/prepress/util.js?5"></script>
<script type="text/javascript" src="/js/custom/prepress/prepress_update_request.js?1"></script>
<script typ="text/javascript">
    childrenForms = ${childrenForms|n};
    updatedChildrenForms = [];
    action = 'copy'
    token = '${token}'
    $(document).ready(function(){
        downSelct();
        initSelete();
        
        $(".numeric").numeric();
        //$("#cc_to").multiSelect();
        $("#cc_to").each(function(){
	        var jqObj = $(this);
	        jqObj.autocomplete("/sample/ajaxField", {
	        	extraParams: {fieldName: 'user'},
	            formatItem: function(item){return item[0]},
	            matchCase: false,
	            mustMatch: false,
	            multiple: true, 
	            multipleSeparator: ';',
	            formatResult : function(row){
	            	return row[1];
	            }
	        });

	    });
	    
	    if(ie9){
	       $("#ie_alert").show();
	       $(".save_btn").hide();
	    }
	    
    })
</script>
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody><tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="64" valign="top" align="left"><a href="/prepress/index"><img src="/images/images/prepress_g.jpg"/></a></td>
                <td width="64" valign="top" align="left" class="save_btn"><a href="#" onclick="toDraft()"><img src="/images/images/menu_save_as_draft_g.jpg"/></a></td>
                <td width="64" valign="top" align="left" class="save_btn"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="#" onclick="toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
                <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
                <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
            </tr>
        </tbody></table>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Prepress</div>
<div style="width:1200px;">
	%if not isWorkTime :
       <div id="time_alert" style="margin:20px 0px 0px 20px !important;"><p class="red" style="font-size: 14px; font-weight: bold;"><u>Out of business hour,we will follow this request on the next working day.</u></p></div>
    %endif
    
    <div id="ie_alert" style="margin:20px 0px 0px 20px !important; display:none;"><p class="red" style="font-size: 14px; font-weight: bold;">The system *DOES NOT* support your broswer(IE 9) yet , please use other broswer to do your operation!</p></div>
    
    <form action="/prepress/saveNewRequest" method="POST" enctype="multipart/form-data" id="mainForm">
    	<input type="hidden" name="token" id="token" value="${token}"/>
        <input type="hidden" name="form_ids" id="form_ids" value=""/>
        <input type="hidden" id="customer" class="rpachidden" name="customer" value="${main.customer_id if main.customer else ''}" />
        <div class="div-900-400">
            <div class="div-300-400" style="margin-left:10px;">
                <table width="100%" border="0" cellspacing="1" style="background:#333333;">
                    <tr>
                        <td style="background:#ffffff"><ul>
                                <li>Project Owner</li>
                                <li> </li>
                            </ul>
                            <ul>
                                <li style=""><label for="project_own">Region</label></li>
                                <li>
                                    <select name="project_own" id="project_own" class="input-150px">
                                        <option></option>
                                        %for r in regions_groups:
                                        %if r.id == main.project_own_id:
                                        <option value="${r.id}" ${tw.attrs([('selected',r.id == main.project_own_id),])}>${str(r)}</option>
                                        %else:
                                        <option value="${r.id}">${str(r)}</option>
                                        %endif
                                        %endfor
                                    </select>
                                </li>
                            </ul>
                            <ul>
                                <li><label for="owner_name">Owner Name</label></li>
                                <li id='owner_name_p'>
                                    <input class="input-150px inputText" value="${main.project_owner}" class="input-150px" id="project_owner" name="project_owner">
                                </li>
                            </ul>

                        </td>
                    </tr>
                    <tr>
                        <td style="background:#ffffff"><ul>
                                <li>Business Unit</li>
                                <li> </li></ul>

                            <ul>
                                <li><label for="team">Division Team</label></li>
                                <li>
                                    <select name="team" id="team" class="input-150px">
                                        <option></option>
        				%for t in teams_groups:
        						%if t.id == main.team_id:
                                        <option value="${t.id}" ${tw.attrs([('selected',t.id == main.team_id)])}>${str(t)}</option>
        						%else:
                                        <option value="${t.id}">${str(t)}</option>
        						%endif
        				%endfor
                                    </select>
                                </li>
                            </ul>
                            <ul>
                                <li><label for="contact_person">Contact Person</label></li>
                                <li id="contact_person_p"><input name="contact_person" id="contact_person" value="${main.contact_person}" class="input-150px"/></li>
                            </ul>


                        </td>
                    </tr>
                </table>

                <ul>
                    <li><label for="reference_code">Reference Code</label></li>
                    <li>
                        <input name="reference_code" id="reference_code" value="${main.reference_code}" class="input-150px"/>
                    </li>
                </ul>
                <ul>
                    <li><label for="customer">Vendor/Customer</label></li>
                    <li>
                        <input type="text" name="customer_name" class="input-150px ajaxSearchField inputText ac_input" id="customer_name" value="${main.customer.name if main.customer else ''}" autocomplete="off">
                    </li>
                </ul>
                <ul>
                    <li><label for="project">Brand</label></li>
                    <li>
                        <input type="text" name="project" class="input-150px inputText ac_input" id="project" value="${main.project if main.project else ''}" autocomplete="off">
                    </li>
                </ul>
                <ul>
                    <li><label for="item_category">Item Category</label></li>
                    <li>
                        <select name="item_category" id="item_category" class="input-150px">
                            <option></option>
			      			    %for p in item_categories:
			                            <option value="${p.id}" ${tw.attrs([('selected',p.id == main.item_category_id)])}>${str(p)}</option>
			      				%endfor
                        </select>
                    </li>
                </ul>
                <ul>
                    <li><label for="item_description">Item Description</label></li>
                    <li><textarea name="item_description" id="item_description" class="input-150px">${main.item_description}</textarea></li>
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
                    <li><label for="request_person">Request Person</label></li>
                    <li>
                        <input type="text" value="${request.identity['repoze.who.userid'] }" disabled="true"  class="input-150px"/>
                        <input type="hidden" id="request_person_name" value="${request.identity['user']}" disabled="true"  class="input-150px"/>
                    </li>
                </ul>
                <ul>
                    <li><label>Contact Number</label></li>
                    <li>
                        <input type="text" value="" name="request_contact_number" id="request_contact_number" class="input-150px numeric"/>
                    </li>
                </ul>
                <ul>
                    <li><label for="request_person">Request Person's Team</label></li>
                    <li><input type="text"  disabled="true" value="${rpt}" class="input-150px"/></li>
                    <input type="hidden" value="${rpt}" class="input-150px" name="rpt"/>
                    <input type="hidden" value="${request_team}" class="input-150px" name="request_team"/>
                </ul>
                <ul>
                    <li><label for="create_time">Request Date</label></li>
                    <li>
                        <input type="text" value="${dt.now().strftime("%Y-%m-%d %H:%M")}" disabled="true"  class="input-150px"/>
                    </li>
                </ul>
                <ul>
                    <li><label for="create_time">E-mail CC to</label></li>
                    <li style="text-align:left">
                        <textarea id="cc_to" name="cc_to" class="input-150px" style="height:120px">${main.cc_to}</textarea>
                        <br />
                        (Seperate E-mail By (;)) 
                    </li>
                </ul>
            </div>
            <div class="clear"><br /></div>
        </div>
    </form>
    <div class="clear"><br /></div>

    <table cellspacing="0" cellpadding="0" border="0" width="900" style="margin: 0px 0px 0px 20px;" id="service-div">
        <tbody>
            <tr class="SFOther">
                <td bgcolor="#666666" align="center">&nbsp;</td>
                <td bgcolor="#666666">&nbsp;</td>
            </tr>
            <tr class="SFOther">
                <td height="30" align="center" class="form-page">Kind of Design Services:</td>
                <td>
                    <select>
                        <option></option>
                        %for f,l in [("PSSFUpload","Prepress"),("PSSFBarcode","Barcode"),]:
                        <option value="${f}">${l}</option>
                        %endfor
                    </select>
                    <input type="button" value="add" class="btn_add btn"/>
                </td>
            </tr>
            
            <tr>
                <td>&nbsp;</td>
            </tr>
        </tbody>
    </table>

    <div class="clear"><br /></div>
    <div id="tabs" style="margin-left:20px;width:900px;">
        <ul></ul>
    </div>
</div>