<%namespace name="tw" module="tw.core.mako_util"/>
<%
import inspect
prefix = context.get("formPrefix","test-")
disable = context.get("isDisable",False)
dbObject = context.get("dbObject",None)
action = context.get("action",None)
jobdata = context.get("jobdata",{})
not_new_copy_draft = action not in ['new','copy','draft']
_ = lambda n : value_for(prefix+n) if (value_for(prefix+n) or value_for(prefix+n)==0) else ""

_d = lambda : tw.attrs([('disabled',disable)])
_f = lambda v: '' if not v else (v if isinstance(v,basestring) else v.strftime('%Y-%m-%d'))
_i = lambda n, f=lambda t:t : tw.attrs([('type','text'),('name',prefix+n),('id',prefix+n),('value',f(_(n))),('disabled',disable)])
_c = lambda v,n : tw.attrs([('name',prefix+n),('type','checkbox'),('value',v),('disabled',disable),('checked', v in _(n))])
_cid = lambda v,n : tw.attrs([('name',prefix+n),('id',prefix+n+'_'+v.lower()),('type','checkbox'),('value',v),('disabled',disable),('checked', v in _(n))])
_r = lambda v,n : tw.attrs([('name',prefix+n),('type','radio'),('value',v),('disabled',disable),('checked', v == _(n) or v in _(n)),('onclick', 'check(this)')])
_incd = lambda n, f=lambda t:t : tw.attrs([('type','text'),('name',prefix+n),('id',prefix+n),('value',f(_(n))),('disabled',not_new_copy_draft and _(n))])
%>

<script type="text/javascript" src="/js/custom/prepress/prepress_view_func.js?3"></script>

<%include file="${dbObject.getWidget().sub_template}" args="cf=dbObject,prefix=prefix,disable=disable,_=_,_d=_d,_f=_f,_i=_i,_c=_c,_cid=_cid,_r=_r,_incd=_incd,jobdata=jobdata"/>

<div class=div1>
    <fieldset>
        <legend><span class="form-page-1">Attachment&nbsp;:</span></legend>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            %if dbObject and not inspect.isclass(dbObject) and dbObject.getAttachment():
	            <tr>
	        		<td colspan="3"><a href='/prepress/downloadAllAttachment?form_id=${dbObject.__class__.__name__}&sub_id=${dbObject.id}' target="_blank">Download All</a></td>
	        	</tr>
	            %for a in dbObject.getAttachment(True):
		            %if a:
		            <tr>
		                <td width="60%">
                            %if action=='update' or action=='copy':
                            <a href="#" onclick="deleteDownload(this,{'form_id':'${dbObject.__class__.__name__}','id':'${dbObject.id}','a_id':'${a.id}','action':'${action}'})">
                                <img src="/images/error.gif" title="Delete this file."/>
                            </a>
                            %endif
                            %if action=='copy':
                            	<input type='hidden' name="${prefix}attachment_copy" value='${a.id}' />
                            %elif action=='update':
                            	<input type='hidden' name="${prefix}attachment_update" value='${a.id}' />
                            %endif
		                    <a href="/download?id=${a.id}" class="${prefix}attachment_link">${a.file_name}</a>
		                </td>
		                <td width="15%" style="text-align:center">${a.upload_by}</td>
		                <td width="25%" style="text-align:center">${a.create_time.strftime("%Y-%m-%d %H:%M:%S")}</td>
		            </tr>
		            %endif
	            %endfor
            %endif
        </table>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            %if not disable:
            <tr>
                <td align=left>
                    <a href="javascript:void(0)" onclick="addFile(this)"><img src="/images/plus.gif" title="Add file"/></a>
                    <a href="javascript:void(0)" onclick="deleteFile(this)" style="display:none"><img src="/images/minus.gif" title="Delete this file"/></a>
                </td>
                <td colspan="2">
                	<input class="input-150px" ${_i('attachment_name')}/>
					<input type="file" name="${prefix}attachment" class="input-150px" size="45" onchange="getFileName(this)" style="width:350px"/>
                </td>
            </tr>
            %endif
        </table>
    </fieldset>

    %if action=='view':
    <fieldset>
        <legend><span class="form-page-1">Job Attachment&nbsp;:</span></legend>
        <table class="table2" cellspacing="0" cellpadding="0" border="0" style="width:700px">
            %if dbObject and not inspect.isclass(dbObject) and dbObject.getAttachment(attach_type='complete_attachment'):
            <tr>
                <td colspan="3"><a href='/prepress/downloadAllAttachment?form_id=${dbObject.__class__.__name__}&sub_id=${dbObject.id}&attach_type=complete_attachment' target="_blank">Download All</a></td>
            </tr>
            %for a in dbObject.getAttachment(True, attach_type='complete_attachment'):
            %if a:
            <tr>
                <td style="width:400px">
                    <a href="/download?id=${a.id}" class="${prefix}attachment_link">${a.file_name}</a>
                </td>
                <td style="text-align:center;style=150px">${a.upload_by}</td>
                <td style="text-align:center;style=150px">${a.create_time.strftime("%Y-%m-%d %H:%M:%S")}</td>
            </tr>
            %endif
            %endfor
            %endif
        </table>
    </fieldset>
    %endif
</div>


%if et:
<div style="text-align:right">
    <p>Estimate Time : <span class="hlfont">${et}</span></p>
</div>
%endif

