<%
	from repoze.what.predicates import in_any_group,in_group,has_permission
	from tribal.util.prepress_helper import checkPSSameTeam
%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-Equiv="Cache-Control" Content="no-cache">
<meta http-Equiv="Pragma" Content="no-cache">
<meta http-Equiv="Expires" Content="0">

<title>r-pac - Prepress</title>
<link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
<link href="/css/screen.css" rel="stylesheet" type="text/css" media="screen,print"/>
<link href="/css/all.css" rel="stylesheet" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/impromt.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen,print"/>


<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen,print"/>
<link rel="stylesheet" href="/css/glowbutton.css" type="text/css" media="screen,print"/>


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
<script type="text/javascript" src="/js/jquery-1.3.2.js" type="text/javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>

<script type="text/javascript" src="/js/custom/prepress/util.js?2" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-ui-timepicker-addon.js" language="javascript"></script>

%if action=='view':
<script type="text/javascript" src="/js/jquery.progressbar.js" language="javascript"></script>
<!-- 
<script type="text/javascript" src="/js/custom/prepress/prepress_view_request_sub.js?2" language="javascript"></script>
-->
%endif

<script type="text/javascript" src="${js_url}?3" language="javascript"></script>
<script typ="text/javascript">
    var tab_id, obj_id;
    action = '${action}';
    token = '${token}';
    $(document).ready(function(){
        tab_id = $('#tab_id').val();
        obj_id = tab_id.split('-')[1]
        var index = tab_id.split('-')[2]
        SFNamespace[obj_id].obj.id = SFNamespace[obj_id].obj.id + '-' + index
        //SFNamespace[obj_id].obj.title = SFNamespace[obj_id].obj.title + ' ' + index
        SFNamespace[obj_id].obj.install();
        if(action=='view'){
            $('.div1 :input').each(function(){
                disableField($(this))
            })
        }
        parent.cancelLoading()
        parent.resetTabLabels()
    })
    function reset_label(title){
        SFNamespace[obj_id].obj.title = title;
    }
    function submit_form(){
        $('#subForm').submit()
    }
    function validate_form(){
        return SFNamespace[obj_id].obj.validation();
    }
</script>
</head>
<body>
    <form action="/prepress/saveSubForm" method="POST" enctype="multipart/form-data" id="subForm">

        %if action=='view':
        <%include file="tribal.templates.prepress.sub_form_status_fun" args="cf=cf,has_permission=has_permission,isSameTeam=checkPSSameTeam(request.identity['user'],cf.main),isPSTeam=has_permission('PREPRESS_EDIT')"/>
        %endif
      
        <div class="div_subform">
            <input type="hidden" name="tab_id" id="tab_id" value="${tab_id}" />
            <input type='hidden' name='action' value='${action}' />
            <input type='hidden' name='token' value='${token}' />
            %if action == 'new' or action == 'copy':
            <input type="hidden" name="main_id"/>
            <input type="hidden" name="id"/>
            %elif main_id:
            <input type="hidden" name="main_id" value="${main_id}"/>
            <input type="hidden" name="id" value="${sub_id}"/>
            %endif
            ${html|n}
        </div>
        
        
        %if action=='view':
        <div class="jobs-div">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" id="jobs-table">
                <tr>
                    <td>Job Report</td>
                </tr>
                %for job in cf.jobs:
                <tr class="job_spands">
                    <td style="padding-top: 15px;">
                        <hr>
                        <table width="100%" border="0" cellspacing="5" cellpadding="0">
                            <tbody>
                                <tr>
                                    <td align="right" class="title-JL">Mins : </td>
                                    <td class="sample-content">${job.time_count}</td>
                                    <td align="right" class="title-JL">Items : </td>
                                    <td class="sample-content">${job.item}</td>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="right" class="title-JL">Remark : </td>
                                    <td class="sample-content" style="height:40px;">${job.remark}</td>
                                </tr>
                                <tr>
                                    <td align="right" class="title-JL">Updated By :</td>
                                    <td class="sample-content">${job.create_by}</td>
                                    <td align="right" class="title-JL">Updated Time :</td>
                                    <td class="sample-content">${job.update_time.strftime("%Y-%m-%d %H:%M")}</td>
                                    <td>&nbsp;</td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                %endfor
            </table>
        </div>
        <div id="job-div-pending" style="display:none">
            <p><label class="job_label">Reason</label><textarea id="job_reason"></textarea></p>
        </div>
        %endif
    </form>
    
    %if action=='view':
        <div id="job-div-complete" style="display:none">
            <form id="completeForm" action="/prepress/ajaxAction" method="POST"  enctype="multipart/form-data">
                <input type="hidden" name="sf_type" value="${cf.__class__.__name__}"/>
                <input type="hidden" name="sf_id" value="${cf.id}"/>
                <input type="hidden" name="action" value="COMPLETE"/>
                <input type="hidden" name="job_type" id="job_type" value=""/>
                
                <!-- <p><label class="job_label">Mins</label><input type="text" id="job_time_spand" name="job_time_spand" value="" class="input-100px numeric"/></p> -->
                <p><label class="job_label">Items</label><input type="text" id="job_item" name="job_item" value="" class="input-100px numeric"/></p>
                <p><label class="job_label">Remark</label><textarea id="job_remark" name="job_remark"></textarea></p>
                <p><input type="file" name="jobfile01"/></p>
                <p><input type="file" name="jobfile02"/></p>
                <p><input type="file" name="jobfile03"/></p>
                <p><input type="file" name="jobfile04"/></p>
                <p><input type="file" name="jobfile05"/></p>
            </form>
        </div>
    %endif
</body>