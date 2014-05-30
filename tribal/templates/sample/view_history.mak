<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
	from repoze.what.predicates import in_any_group,in_group,has_permission
	from tribal.util.sample_helper import getManagerByTeam
	disable = True
	_d = lambda : tw.attrs([('disabled',disable)])
%>
<%def name="extTitle()">r-pac - Structural/Flexible Development</%def>
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
</style>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.loadmask.min.js"></script>
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js"></script>
<script type="text/javascript" src="/js/jquery.color.js"></script>
<script type="text/javascript" src="/js/jquery.progressbar.js"></script>
<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/jquery-ui-timepicker-addon.js"></script>
<script type="text/javascript" src="/js/custom/sample/util.js?6"></script>
<script type="text/javascript" src="/js/custom/sample/sample_update_request.js?6"></script>
<script type="text/javascript">
    childrenForms = ${childrenForms|n};
    updatedChildrenForms = ${updatedChildrenForms|n};
    action = 'history';
    var history_id = ${id}
    $(document).ready(function(){   
        $(".status-bar").progressBar();
        $('#page-div :input').each(function(){
            disableField($(this));
        });
    });
</script>
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
            <tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="64" valign="top" align="left"><a href="/sample/index"><img src="/images/images/menu_pd_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="/sample/listHistory?id=${main.id}"><img src="/images/images/menu_return_g.jpg"/></a></td>
                <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
                <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
            </tr>
        </tbody>
    </table>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Structural/Flexible Development</div>
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
                <li><label for="program">Corporate Customer</label></li>
                <li><input type="text" value="${main.program}" class="input-150px"/></li>
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
                    <input type="text" value="${main.create_by.user_name}" class="input-150px"/>
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
                <li><label for="create_time">Access Rights</label></li>
                <li><input type="text" value="${cowork_team}" class="input-150px"/></li>
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
            <ul>
                <li><label>Options</label></li>
                <li style='text-align:left' id='group_a'>
                    %for k,v in groupFormDict.iteritems():
                    <a href='javascript:void(0)' id='group_a${k}'>Option ${k}</a><br/>
                    %endfor
                </li>
            </ul>
        </div>
    </div>
    <div class="clear"><br /></div>
    <div id="group_div" style="margin-left:20px;width:906px;">
        <% tabIndex = 0 %>
        %for k,v in groupFormDict.iteritems():
        <div class='box2' id='group_div${k}'>
            <div class='title1'>
                <div class='toggle_right'></div>Option ${k}
            </div>
            <div id='tabs${k}' class='tabs none'>
                <ul>
                    %for i_index, i  in enumerate(v):
                    <% tabID = 'tab-%s-%s-%s-%s' % (i['form_name'], i['group_no'], tabIndex+i_index+1, i['id']) %>
                    <li class="ui-state-default ui-corner-top ui-tabs-selected ui-state-active">
                        <a href="${'#%s' % tabID}">
                            ${i['form_label']}
                        </a>
                    </li>
                    %endfor
                </ul>
                %for i_index, i in enumerate(v):
                <% tabID = 'tab-%s-%s-%s-%s' % (i['form_name'], i['group_no'], tabIndex+i_index+1, i['id']) %>
                <div id="${tabID}" class="ui-tabs-panel ui-widget-content ui-corner-bottom">
                    <iframe id="${'iframe-%s' % tabID}" frameborder="0" width=880 height=1 scrolling="auto"
                        onload="Javascript:SetCwinHeight('${'iframe-%s' % tabID}')"></iframe>
                </div>
                %endfor
            </div>
        </div>
        <% tabIndex += len(v) %>
        %endfor
    </div>
</div>	