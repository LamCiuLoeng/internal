<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_cid,_incd"/>

<%
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>

<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/material.js?v=2"></script>

<script type="text/javascript">
$(document).ready(function(){
        $('.material_widget').material_popup();
        
		linkScroll([$("#SFGeneral-size_w"), $("#SFGeneral-size_d"),$("#SFGeneral-size_h"),$("input[name='SFGeneral-size_unit']"),$("input[name='SFGeneral-size_type']")],
            	                   $("input[name='SFGeneral-size_as_sample']")
			)
		linkScroll([$('#SFGeneral-weight'), $("#SFGeneral-weight_unit")],$("input[name='SFGeneral-weight_as_sample']"))
		$("input[name='SFGeneral-job_purpose'],input[name='SFGeneral-job_presentation']").click(function(){
				var name = $(this).attr("name");
				if(name=='SFGeneral-job_presentation'){
					lessCheckBox3(["input[name='SFGeneral-job_purpose']"]);		
				 }
				 else{
				 	lessCheckBox3(["input[name='SFGeneral-job_presentation']"]);	
				 }
				})
})
</script>
<div class="div1">
	<fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Job Purpose&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2" width="100%">
            <tr>
                <td width='33%'><input ${_r('quotation','job_purpose')}/>Quotation(Without Size Fitting)</td>
                <td width='34%'><input ${_r('production','job_purpose')}/>Production(With Size Fitting)</td>
                <td width='33%'><input ${_c('presentation','job_presentation')}/>Presentation</td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Product Details&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td>
                   Size <input ${_i('size_w')} class="input-50px numeric"/> W 
                        <input ${_i('size_d')} class="input-50px numeric"/> D 
                        <input ${_i('size_h')} class="input-50px numeric"/> H
                        <input ${_r('nn','size_unit')}/> mm
                        <input ${_r('inch','size_unit')}/> inch
                </td>
            </tr>
            <tr>
                <td>
                    <input ${_r('product','size_type')}/>Product Size
                        <input ${_r('packing','size_type')}/>Packing Size
                        <input ${_c('Y','size_as_sample')}/>As Sample
                </td>
            </tr>
            <tr>
                <td>Product Weight :
                    <input ${_i('weight')} class="input-100px"/>&nbsp;&nbsp;
                    <select name="${prefix}weight_unit" id="${prefix}weight_unit" ${_d()} class="input-50px">
                        %for o in ["","lbs","kgs"]:
                        <option value="${o}" ${tw.attrs([('selected',o == _('weight_unit'))])}>${o}</option>
                        %endfor
                    </select>&nbsp;&nbsp;
                        <input ${_c('Y','weight_as_sample')}/>As Sample</td>
            </tr>
        </table>
    </fieldset>
    
    
    
    <fieldset>
      <legend><span class="form-page-1"><sup class="red">*</sup>Material </span></legend>
      
      %if disable:
          <table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="margin: 10px 0px;" id="material_ul">
              %for widget in _('material_widgets'):
                  <tr>
                    <td><input type="text" class="material_widget input-300px" value="${widget['SHOW_TEXT']|ue, h}" disabled="disabled"/></td>
                  </tr>
              %endfor
          </table>
      %else:
          <table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="margin: 10px 0px;" id="material_ul">
              %for index,widget in enumerate(_('material_widgets')):
                  <tr>
                      <td width="35">
                          <img title="Add" src="/images/plus.gif" onclick="add_material('material_ul')"/>
                          %if index !=0:
                            <img title="Delete" src="/images/minus.gif" onclick="remove_material(this)"/>
                          %endif
                      </td>
                      <td width="350"><input type="text" class="material_widget input-300px" value="${widget['SHOW_TEXT']|ue, h}" ref='${widget|jd,n}' ${ tw.attrs([('disabled',disable)]) }/></td>
                  </tr>
              %endfor
              <tr>
                  <td width="35">
                      <img title="Add" src="/images/plus.gif" onclick="add_material('material_ul')"/>
                      %if len(_('material_widgets')) >0:
                          <img title="Delete" src="/images/minus.gif" onclick="remove_material(this)"/></td>
                      %endif
                  <td width="350"><input type="text" class="material_widget input-300px" value="" ref=''/></td>
              </tr>
          </table>
          <input ${_h('material_widgets')} value='${_("material_widgets")|jd,n}'/>
      %endif
    </fieldset>
    
    
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Submitted Items&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="25"><input ${_c('product','submit_item')}/></td>
                <td>Product / Prototype</td>
                <td width="10">&nbsp;</td>
                <td width="25"><input ${_c('photos','submit_item')}/></td>
                <td>Photos</td>
            </tr>
            <tr>
                <td><input ${_c('packaging','submit_item')}/></td>
                <td>Previous Packaging</td>
                <td></td>
                <td><input ${_c('artworks','submit_item')}/></td>
                <td>Artworks</td>
            </tr>
            <tr>
                <td><input ${_c('mock','submit_item')}/></td>
                <td>Mock Up</td>
                <td></td>
                <td><input id="${prefix}submit_item_other_type" ${_c('other','submit_item')}/></td>
                <td>Others <input ${_i('submit_item_other')} class="input-100px"/></td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Packaging Style&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr><td><input ${_c('hangtag','item_type')}/>Hang Tag</td><td width="10">&nbsp;</td><td><input ${_c('belly','item_type')}/>Belly Band</td></tr>
            <tr><td><input ${_c('vinyl','item_type')}/>#Vinyl Bag</td><td>&nbsp;</td><td><input ${_c('clamshell','item_type')}/>#Clamshell</td></tr>
            <tr><td><input ${_c('blister','item_type')}/>#Blister</td><td>&nbsp;</td><td><input ${_cid('other_cb','item_type')}/>Others <input ${_i('item_type_other')} class="input-300px"/></td></tr>
            <tr><td colspan="5">#This design is for visual confirmation only</td></tr>
        </table>
        </td>
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
        <input ${_i('expected_date',_f)} class="input-150px datePicker" />
    </fieldset>    
</div>
