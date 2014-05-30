<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
	from datetime import datetime as dt
	from tribal.util.mako_filter import b,tp
	from repoze.what.predicates import in_any_group,in_group,has_permission
	aa = dt.now() 
%>

<%def name="extTitle()">r-pac - Structural/Flexible Development</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>

<style type="text/css">
    div.cleanred{width:700px;}
    .hlfont{font:normal 18px Tahoma, Helvetica, sans-serif;color:#069;margin:0;padding:15px 5px;}
    .action-bn{display:inline;float:right;}
</style>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js"></script>
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js"></script>

<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/sample/util.js?1"></script>
<script type="text/javascript" src="/js/custom/sample/sample_new_request.js?6"></script>
<script typ="text/javascript">
    action='new'
    token = '${token}'
    var user_name = "${request.identity['user']}"
</script>
</%def>
	    
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody><tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="64" valign="top" align="left"><a href="/sample/index"><img src="/images/images/menu_pd_g.jpg"/></a></td>
                <td width="64" valign="top" align="left" class="save_btn"><a href="#" onclick="toDraft()"><img src="/images/images/menu_save_as_draft_g.jpg"/></a></td>
                <td width="64" valign="top" align="left" class="save_btn"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="#" onclick="toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
                <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
                <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
            </tr>
        </tbody></table>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Structural/Flexible Development</div>
<div style="width:1200px;">
    %if not isWorkTime :
	   <div id="time_alert" style="margin:20px 0px 0px 20px !important;"><p class="red" style="font-size: 14px; font-weight: bold;"><u>Out of business hour,we will follow this request on the next working day.</u></p></div>
    %endif
    
    <div id="ie_alert" style="margin:20px 0px 0px 20px !important; display:none;"><p class="red" style="font-size: 14px; font-weight: bold;">The system *DOES NOT* support your broswer(IE 9) yet , please use other broswer to do your operation!</p></div>
    
    <form action="/sample/saveNewRequest" method="POST" enctype="multipart/form-data" id="mainForm">
    	<input type="hidden" name="token" id="token" value="${token}"/>
        <input type="hidden" name="form_ids" id="form_ids" value=""/>
        <input type="hidden" name="tab_ids" id="tab_ids" value=""/>
        <input type="hidden" id="customer" class="rpachidden" name="customer" value="" />
        <input type="hidden" id="program" class="rpachidden" name="program" value="" />
        <input type='hidden' id='group_no' name='group_no' value='1'/>
        <div class="div-900-400">
            <div class="div-300-400" style="margin-left:10px;">
                <table width="100%" border="0" cellspacing="1" style="background:#333333;">
                    <tr>
                        <td style="background:#ffffff">
                            <ul>
                                <li>Project Owner</li>
                                <li></li>
                            </ul>
                            <ul>
                                <li style=""><label>Region</label></li>
                                <li>
                                    <select name="project_own" id="project_own" class="input-150px">
                                        <option></option>
		  		            			%for r in regions_groups:
		  		            				% if len(regions) > 0 and r.id == regions[0].id:
                                        <option value="${r.id}" ${tw.attrs([('selected',r.id == regions[0].id),])}>${str(r)}</option>
		  		           					% else:
                                        <option value="${r.id}">${str(r)}</option>
		  		           					% endif
		  		           				%endfor
                                    </select>
                                </li>
                            </ul>
                            <ul>
                                <li><label>Owner Name</label></li>
                                <li id='owner_name_p'>
                                    <input name='owner_name' id='project_owner' value='' class='input-150px'>
                                </li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td style="background:#ffffff">
                            <ul>
                                <li>Business Unit</li>
                                <li></li>
                            </ul>
                            <ul>
                                <li><label>Division Team</label></li>
                                <li>

                                    <select name="team" id="team" class="input-150px">
                                        <option></option>
          		            			%for t in teams_groups:
          		            				%if len(teams) > 0 and t.id == teams[0].id:
                                                <option value="${t.id}" ${tw.attrs([('selected',t.id == teams[0].id),])}>${str(t)}</option>
                                   			%else:
                                                <option value="${t.id}">${str(t)}</option>
                                   			% endif
                                   		%endfor
                                    </select>
                                </li>
                            </ul>
                            <ul>
                                <li><label>Contact Person</label></li>
                                <li id="contact_person_p">
                                    <input name="contact_person" id="contact_person" value="" class="input-150px"/>
                                </li>
                            </ul>
                        </td>
                    </tr>
                </table>

                <ul>
                    <li><label>Reference Code</label></li>
                    <li><input name="reference_code" id="reference_code" value="" class="input-150px"/></li>
                </ul>
                <ul>
                    <li>
                        <label>
                        %if has_permission('SAMPLE_PD_EDIT'):
                        	(<a href="javascript:void(0)" id="href_customer">Manage</a>)
                        %endif
                        Vendor/Customer</label>
                        <div id="dialog-new_customer" title="Manage Vendor/Customer"></div>
                    </li>
                    <li>
                        <input type="text" name="customer_name" class="input-150px ajaxSearchField inputText ac_input" id="customer_name" value="" autocomplete="off">
                    </li>
                </ul>
                <ul>
                    <li>
                        <label>
                        	%if has_permission('SAMPLE_PD_EDIT'):
                        		(<a href="javascript:void(0)" id="href_program">Manage</a>)
                        	%endif 
                        	<sup class="red">*</sup>Corporate Customer
                        </label>
                        <div id="dialog-new_program" title="Manage Program"></div>
                    </li>
                    <li>
                        <input type="text" name="program_name" class="input-150px ajaxSearchField inputText ac_input" id="program_name" value="" autocomplete="off">
                    </li>
                </ul>
                <ul>
                    <li>
                        <label>
                        %if has_permission('SAMPLE_PD_EDIT'):
                        	(<a href="javascript:void(0)" id="href_project">Manage</a>)
                        %endif
                        <sup class="red">*</sup>Brand</label>
                        <div id="dialog-new_project" title="Manage Project"></div>
                    </li>
                    <li>
                        <select name="project" id="project" class="input-150px">
                            <option></option>
                        </select>
                    </li>
                </ul>
                <ul>
                    <li>
                        <label>
                        %if has_permission('SAMPLE_PD_EDIT'):
                        	(<a href="javascript:void(0)" id="href_item_category">Manage</a>)
                        %endif
                        <sup class="red">*</sup>Item Category</label>
                        <div id="dialog-new_item_category" title="Manage Item Category"></div>
                    </li>
                    <li>
                        <select name="item_category" id="item_category" class="input-150px">
                            <option></option>
		            			%for t in item_categries:
	                            	<option value="${t.id}">${str(t)}</option>
	                       		%endfor
                        </select>
                    </li>
                </ul>
                <ul>
                    <li><label><sup class="red">*</sup>Item Description</label></li>
                    <li>
                        <textarea name="item_description" id="item_description" value="" class="input-150px" style="height:120px"></textarea>
                    </li>
                </ul>
                <ul>
                    <li><label for="item_code"><sup class="red">*</sup>Item Code</label></li>
                    <li>
                        <!-- input name="item_code" id="item_code" value="" class="input-150px"/ -->
                        <textarea id="item_code" name="item_code" class="input-150px" style="height:120px"></textarea>
                    </li>
                </ul>
            </div>
            <div class="div-300-400">
                <ul>
                    <li><label>Request Person</label></li>
                    <li>
                        <input type="text" value="${request.identity['repoze.who.userid'] }" disabled="true"  class="input-150px"/>
                    </li>
                </ul>
                <ul>
                    <li><label>Request Person's Team</label></li>
                    <li><input type="text"  disabled="true" value="${rpt}" class="input-150px"/></li>
                    <input type="hidden" value="${rpt}" class="input-150px" name="rpt"/>
                    <input type="hidden" value="${request_team}" class="input-150px" name="request_team"/>
                </ul>
                <ul>
                    <li><label>Contact Number</label></li>
                    <li>
                        <input type="text" value="" name="request_contact_number" id="request_contact_number" class="input-150px numeric"/>
                    </li>
                </ul>
                <ul>
                    <li><label>Request Date</label></li>
                    <li>
                        <input type="text" value="${dt.now().strftime("%Y-%m-%d %H:%M")}" disabled="true"  class="input-150px"/>
                    </li>
                </ul>
                <ul>
                    <li><label>Access Rights</label></li>
                    <li style="text-align:left">
                        <select name="cowork_team" id="cowork_team" class="input-150px">
                            <option value=""></option>
                            %for t in teams_groups:
                                <option value="${t.id}">${t}</option>
                            %endfor
                        </select>
                        (If Necessary)
                    </li>
                </ul>                
                <ul>
                    <li><label>E-mail CC to</label></li>
                    <li style="text-align:left">
                        <textarea id="cc_to" name="cc_to" class="input-150px" style="height:120px"></textarea>
                        (Seperate E-mail By (;))
                    </li>
                </ul>
                <ul style='display:none'>
                    <li><label>Options</label></li>
                    <li style="text-align:left" id='group_a'>
                    </li>
                </ul>
            </div>
            <div class="clear"><br /></div>
        </div>
    </form>
    <div class="clear"><br /></div>

    <div style="float: left; width: 1000px;" class="title-page">Kind of Design Services:</div>

    <table cellspacing="0" cellpadding="0" border="0" width="900" style="margin: 0px 0px 0px 20px;" id="service-div">
        <tbody>
            <tr>
                <td height="30" align="center" class="form-page">&nbsp;</td>
                <td>
                    <input type="button" value="Add Task Option" class="btn" onclick='addGroup()'/>
                </td>
            </tr>
            <tr>
                <td height="30" align="center" class="form-page">Output</td>
                <td>
                    <select>
                        <option></option>
                        %for f,l in sorted([("SFPrintout","Printout"),("SFSampling","Sampling"),("SF3DImage","3D Image"),("SFAssembly","Assembly Sheet"),("SFDrop","Drop Test"),("SFUpload","Upload/Download/File checking"),("SFContainer","Container Loading"),("SFFileConvert","File Convert"),("SFPhoto","Photo Shot")],key=lambda a:a[1]):
                        <option value="${f}">${l}</option>
                        %endfor
                    </select>
                    &nbsp;
                    <input type="button" value="add to" class="btn_add btn"/>
                    &nbsp;
                    <select class='group_count_select2'></select>
                </td>
            </tr>
            <tr class="SFOther">
                <td bgcolor="#666666" align="center">&nbsp;</td>
                <td bgcolor="#666666">&nbsp;</td>
            </tr>
            <tr class="SFOther">
                <td height="30" align="center" class="form-page">Structure</td>
                <td>
                    <select>
                        <option></option>
                        %for f,l in [("SFGeneral","General Packaging Design"),("SFBox","Box"),("SFTray","Tray"),("SFFloor","Floor/Pallet Display/Sidekick")]:
                        <option value="${f}">${l}</option>
                        %endfor
                    </select>
                    &nbsp;
                    <input type="button" value="add to" class="btn_add btn"/>
                    &nbsp;
                    <select class='group_count_select2'></select>
                </td>
            </tr>
            <tr class="SFOther">
                <td bgcolor="#666666" align="center">&nbsp;</td>
                <td bgcolor="#666666">&nbsp;</td>
            </tr>
            <tr class="SFOther SFArtwork">
                <td height="30" align="center" class="form-page">Artwork</td>
                <td>
                    <select>
                        <option></option>
                        %for f,l in [("SFLabel","Barcode Label"),("SFArtwork","Artwork")]:
                        <option value="${f}">${l}</option>
                        %endfor
                    </select>
                    &nbsp;
                    <input type="button" value="add to" class="btn_add btn"/>
                    &nbsp;
                    <select class='group_count_select2'></select>
                </td>
            </tr>
            <tr class="SFSpecial">
                <td bgcolor="#666666" align="center">&nbsp;</td>
                <td bgcolor="#666666">&nbsp;</td>
            </tr>
            <tr class="SFSpecial">
                <td height="30" align="center" class="form-page">Structure/Artwork</td>
                <td>
                    <select>
                        <option></option>
                        %for f,l in [("SFAvon","Avon"),("SFTarget","Target")]:
                        <option value="${f}">${l}</option>
                        %endfor
                    </select>
                    &nbsp;
                    <input type="button" value="add to" class="btn_add btn"/>
                    &nbsp;
                    <select class='group_count_select2'></select>
                </td>
            </tr>
            <tr>
                <td>&nbsp;</td>
            </tr>
        </tbody>
    </table>

    <div class="clear"><br /></div>
    <div id="group_div" style="margin-left:20px;width:906px;display:none;">

    </div>
</div>