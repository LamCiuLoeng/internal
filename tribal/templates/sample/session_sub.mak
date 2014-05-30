<%
	from repoze.what.predicates import in_any_group,in_group,has_permission
	from tribal.util.sample_helper import getManagerByTeam,checkSameTeam
%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-Equiv="Cache-Control" Content="no-cache">
<meta http-Equiv="Pragma" Content="no-cache">
<meta http-Equiv="Expires" Content="0">

<title>r-pac - Sample Development</title>
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
<script type="text/javascript" src="/js/custom/sample/util.js?6" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-ui-timepicker-addon.js" language="javascript"></script>
%if action=='view':
<script type="text/javascript" src="/js/jquery.progressbar.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/sample/sample_view_request_sub.js?6" language="javascript"></script>
%endif
<script type="text/javascript" src="${js_url}?6" language="javascript"></script>
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
    <form action="/sample/saveSubForm" method="POST" enctype="multipart/form-data" id="subForm">
        
        %if action=='view':
        <%include file="tribal.templates.sample.sub_form_status_fun" args="cf=cf,has_permission=has_permission,getManagerByTeam=getManagerByTeam,isSameTeam=checkSameTeam(request.identity['user'],cf.main),isPDTeam=has_permission('SAMPLE_PD_EDIT')"/>
        %endif
        <div class="div_subform">
            <input type="hidden" name="tab_id" id="tab_id" value="${tab_id}" />
            <input type='hidden' name='tab_index' value='${tab_id.split('-')[3]}' />
            <input type='hidden' name='action' value='${action}' />
            <input type='hidden' name='token' value='${token}' />
            %if action == 'new' or action == 'copy':
            <input type="hidden" name="main_id"/>
            <input type="hidden" name="id"/>
            %elif main_id:
            <input type="hidden" name="main_id" value="${main_id}"/>
            <input type="hidden" name="id" value="${sub_id}"/>
            %endif
            <input type="hidden" name="${prefix}group_no" value="${group_no}"/>
            ${html|n}
        </div>
        
        
        %if action=='view' and has_permission('SAMPLE_PD_EDIT'):
        <div class="jobs-div">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" id="jobs-table">
                <tr>
                    <td>Job Report
                    %if in_any_group("SAMPLE_PD_HK","SAMPLE_PD_SZ"):
                        <input type="button" value="Add" class="kk btn" onclick="addHidden('${cf.__class__.__name__}','${cf.id}');" style="margin-left:500px"/>
                    %endif
                    </td>
                </tr>
                %for job in cf.jobs:
                <tr>
                    <td style="padding-top: 15px;">
                        <hr>
                        <div class="job_spands">
                        %for (n,v,c) in job.populateOtherSpend():
                            <div class="job_spand"><label class="label">${c['label'] if c else ''} :</label><div class="field">${v}</div></div>
                        %endfor
                        </div>
                        <table width="100%" border="0" cellspacing="5" cellpadding="0">
                            <tbody>

                                %for material in job.suform_job_materials:
                                <tr>
                                    <td width="15%" align="right" class="title-JL">Material :</td>
                                    <td width="30%" class="sample-content">${material.stock}</td>
                                    <td width="15%" align="right" class="title-JL">Qty :</td>
                                    <td width="30%" class="sample-content">${material.qty}</td>
                                    <td width="10%">&nbsp;</td>
                                </tr>
                                %endfor
                                <tr>
                                    <td align="right" class="title-JL">Mins : </td>
                                    <td class="sample-content">${job.time_spand}</td>
                                    <td align="right" class="title-JL">&nbsp;</td>
                                    <td>&nbsp;</td>
                                    <td>&nbsp;</td>
                                </tr>
                                <tr>
                                    <td align="right" class="title-JL">Remark : </td>
                                    <td class="sample-content" colspan="3">${job.remark}</td>
                                </tr>
                                <tr>
                                    <td align="right" class="title-JL">Created By :</td>
                                    <td class="sample-content">${job.create_by}</td>
                                    <td align="right" class="title-JL">Creat Time :</td>
                                    <td class="sample-content">${job.create_time.strftime("%Y-%m-%d %H:%M")}</td>
                                    <td>&nbsp;</td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
                %endfor
            </table>
        </div>
        <div id="job-div" style="display:none">
            <div class="other_spand"></div>
            <p class="one-row">
                <label class="job_label">Stock</label>
                <select name="stock_10" class="input-150px">
                    <option value=""></option>
                    %for s in stocks:
                    <option value="${s.id}">${str(s)}</option>
                    %endfor
                </select>
                <label>Qty</label><input type="text" name="qty_10" class="input-100px numeric"/>
                <span>
                    <a href="#job-div" onclick="addRow(this);"><img src="/images/plus.gif"/></a>&nbsp;
                    <a href="#job-div" onclick="removeRow(this)";><img src="/images/minus.gif"/></a>
                </span>
            </p>

            <p class="row-template" style="display:none">
                <label class="job_label">Stock</label>
                <select name="stock_X" class="input-150px">
                    <option value=""></option>
                    %for s in stocks:
                    <option value="${s.id}">${str(s)}</option>
                    %endfor
                </select>
                <label>Qty</label><input type="text" name="qty_X" class="input-100px numeric"/>
                <span>
                    <a href="#" onclick="addRow(this);"><img src="/images/plus.gif"/></a>&nbsp;
                    <a href="#" onclick="removeRow(this)";><img src="/images/minus.gif"/></a>
                </span>
            </p>

            <p><label class="job_label">Mins</label><input type="text" name="time_spand" value="" class="input-100px numeric"/></p>
            <p><label class="job_label">Remark</label><textarea name="remark" id="remark"></textarea></p>
            %if in_group("SAMPLE_PD_HK"):
            <input type="hidden" name="designers" id="designers" value="HK"/>
            %elif in_group("SAMPLE_PD_SZ"):
            <input type="hidden" name="designers" id="designers" value="SZ"/>
            %endif
        </div>
        %endif
    </form>
</body>