<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_cid,_r,_incd"/>
<%
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>

<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/shoot.js?v=1"></script>

<script type="text/javascript">
    $(document).ready(function(){
           $('.shoot_widget').shoot_popup();
    });
</script>

<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Job Purpose&nbsp;:</span></legend>
        <input ${_r('Internal','job_purpose')}/>
            Internal Reference&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input ${_r('Production','job_purpose')}/>
            Production&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input ${_r('Presentation','job_purpose')}>
            Presentation
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Submitted Items&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="25"><input ${_c('product','submit_items')}/></td>
                <td>Product Prototype</td>
            </tr>
            <tr>
                <td><input ${_c('packaging','submit_items')}/></td>
                <td>Previous Packaging</td>
            </tr>
            <tr>
                <td><input ${_c('new_design','submit_items')}/></td>
                <td>New Design With This Request</td>
            </tr>
            <tr>
                <td><input id="${prefix}submit_other" ${_c('other','submit_items')}/></td>
                <td>Others <input ${_i('submit_items_other')} class="input-300px"/></td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1">Job Nature&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="25"><input ${_c('photo','job_nature')}/></td>
                <td>Photo Retouch/Adjustment</td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1">View Of Shoots&nbsp;:</span></legend>
        
        %if disable:
          <table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="margin: 10px 0px;" id="shoot_ul">
              %for widget in _('shoot_widgets'):
                  <tr>
                    <td><input type="text" class="shoot_widget input-300px" value="${widget['SHOW_TEXT']|ue, h}" disabled="disabled"/></td>
                  </tr>
              %endfor
          </table>
      %else:
          <table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="margin: 10px 0px;" id="shoot_ul">
              %for index,widget in enumerate(_('shoot_widgets')):
                  <tr>
                      <td width="35">
                          <img title="Add" src="/images/plus.gif" onclick="add_shoot('shoot_ul')"/>
                          %if index !=0:
                              <img title="Delete" src="/images/minus.gif" onclick="remove_shoot(this)"/>
                          %endif
                      </td>
                      <td width="350"><input type="text" class="shoot_widget input-300px" value="${widget['SHOW_TEXT']|ue, h}" ref='${widget|jd,n}' ${ tw.attrs([('disabled',disable)]) }/></td>
                  </tr>
              %endfor
              <tr>
                  <td width="35">
                      <img title="Add" src="/images/plus.gif" onclick="add_shoot('shoot_ul')"/>
                      %if len(_('shoot_widgets')) >0:
                          <img title="Delete" src="/images/minus.gif" onclick="remove_shoot(this)"/>
                      %endif
                  </td>
                  <td width="350"><input type="text" class="shoot_widget input-300px" value="" ref=''/></td>
              </tr>
          </table>
          <input ${_h('shoot_widgets')} value='${_("shoot_widgets")|jd,n}'/>
      %endif
      
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Output&nbsp;:</span></legend>
        <input ${_r('TIF','output')}/> Tif<br/>
        <input ${_r('JPG','output')}/> JPG<br/>
        <input ${_r('other','output')} id="${prefix}output_other"/> Others <input ${_i('output_other_content')} class="input-300px"/>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1">Remark&nbsp;:</span></legend>
        %if action == 'copy':
            <textarea class="input-600px" rows="5"  name="${prefix}remark">${_('remark')}</textarea>
        %else:     
            <p>${_('remark').replace("\n","<br/>")}</p>
            %if not disable: 
                <textarea class="input-600px" rows="5"  name="${prefix}remark"></textarea>
            %endif
        %endif
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Expected Date&nbsp;:</span></legend>
        <input  ${_i('expected_date',_f)} class="input-150px datePicker"/>
    </fieldset>
</div>