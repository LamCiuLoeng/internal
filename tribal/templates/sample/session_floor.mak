<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_cid,_r,_incd"/>

<%
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>

<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/material.js?v=2"></script>

<script type="text/javascript">
$(document).ready(function(){
        $('.material_widget').material_popup();
        
		linkScroll([$('#SFFloor-dimension_w'),$('#SFFloor-dimension_d'),$('#SFFloor-dimension_h'),$("input[name='SFFloor-dimension_unit']")],
                                   $("input[name='SFFloor-dimension_as_sample'][value='Y']"));
        
        //linkScroll( [$('#SFFloor-dimension_type_option_text')],$("input[name='SFFloor-dimension_as_sample'][value='Y']") );
		
		linkScroll([$('#SFFloor-weight'),$("#SFFloor-weight_unit")],
            	                   $("input[name='SFFloor-weight_as_sample'][value='Y']"));
			})
</script>
<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Job Purpose&nbsp;:</span></legend>
        <input ${_r('Quotation','job_purpose')}/>Quotation (Without Size Fitting)&nbsp;&nbsp;&nbsp;&nbsp;
            <input ${_r('Production','job_purpose')}/>Production (With Size Fitting)&nbsp;&nbsp;&nbsp;&nbsp;
            <input id="${prefix}presentation" ${_c('Y','presentation')}>Presentation&nbsp;&nbsp;&nbsp;&nbsp;
            <input id="${prefix}diagram_for_approval" ${_c('Y','diagram_for_approval')}>Diagram For Approval
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Product Details&nbsp;:</span></legend>
            <input ${_r('option','dimension_type')} id="${prefix}dimension_type_option"/>Refer to Packaging Option&nbsp;<input ${_i('dimension_type_option_text')} class="input-100px"/><br />
            <input ${_r('detail','dimension_type')}/> Product Dimension <input ${_i('dimension_w')} class="numeric input-50px"/> W &nbsp;
            <input ${_i('dimension_d')} class="numeric input-50px"/> D &nbsp; <input ${_i('dimension_h')} class="numeric input-50px"/> H&nbsp;
            <input ${_r('mm','dimension_unit')} />mm &nbsp;&nbsp;
            <input ${_r('inch','dimension_unit')}/>inch&nbsp;&nbsp;
            <input ${_c('Y','dimension_as_sample')} /> As Sample<br />
        <span class="span2">Weight</span>
        <input ${_i('weight')} class="numeric input-100px"/>
        <select name="${prefix}weight_unit" id="${prefix}weight_unit" ${_d()} class="input-50px">
            %for o in ["","gram","kg","lbs","oz"]:
            <option value="${o}" ${tw.attrs([('selected',o == _('weight_unit'))])}>${o}</option>
            %endfor
        </select>
        <input ${_c('Y','weight_as_sample')} /> As Sample<br/>
        <!-- <input ${_r('according','dimension_type')}/> Size According To The New Design With This Request<br/> -->
        <input ${_r('no','dimension_type')}/> No Product Size Reference, Just According To The Pallet Display Size.
    </fieldset>
    
    <fieldset>
      <legend><span class="form-page-1"><sup class="red">*</sup>Material </span></legend>
      
      %if disable:
          <table cellspacing="0" cellpadding="0" border="0" width="100%" class="table-line-height" style="margin: 10px 0px;" id="material_ul">
              %for widget in _('material_widgets'):
                  <tr>
                    <td><input type="text" class="material_widget input-300px" value="${widget['SHOW_TEXT']|ue,h}" disabled="disabled"/></td>
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
                      <td width="350"><input type="text" class="material_widget input-300px" value="${widget['SHOW_TEXT']|ue,h}" ref='${widget|jd,n}' ${ tw.attrs([('disabled',disable)]) }/></td>
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
        <legend><span class="form-page-1">Display Size&nbsp;:</span></legend>
        <table>
        	<tr>
        		<td valign=top><sup class="red">*</sup><span class='title-page-1'>Display Size:</span></td>
        		<td>
        			<ul class="ul3">
			            <li class="head"><input ${_r('full','pallet_size')}/>Full Pallet</li>
			            <li>
			                <input ${_r('1','full_pallet')}/>&nbsp;&nbsp;(48"W x 48"D)<br/>
			                <input ${_r('2','full_pallet')}/>&nbsp;&nbsp;(48"W x 40"D)<br/>
			                <input ${_i('full_pallet_height_limit')} class="numeric input-100px"/>&nbsp;Height&nbsp;&nbsp;<input ${_r('1','full_pallet_height_limit_unit')}/>&nbsp;mm&nbsp;&nbsp;<input ${_r('2','full_pallet_height_limit_unit')}/>&nbsp;inch (Without Wooden Pallet)<br/>
			            </li>
			            <li class="head"><input ${_r('half','pallet_size')}/>Half Pallet</li>
			            <li>
			                <input ${_r('1','half_pallet')}/>&nbsp;&nbsp;(48"W x 20"D)<br/>
			                <input ${_r('2','half_pallet')}/>&nbsp;&nbsp;(40"W x 24"D)<br/>
			                <input ${_i('half_pallet_height_limit')} class="numeric input-100px"/>&nbsp;Height&nbsp;&nbsp;<input ${_r('1','half_pallet_height_limit_unit')}/>&nbsp;mm&nbsp;&nbsp;<input ${_r('2','half_pallet_height_limit_unit')}/>&nbsp;inch (Without Wooden Pallet)<br/>
			            </li>
			            <li class="head"><input ${_r('pack','pallet_size')}/>Display Size According To Pack Count</li>
		                <li>
			                <input ${_i('display_pack_left')} class="numeric input-100px" disabled='true'/>&nbsp;pcs Left To Right<br/>
			                <input ${_i('display_pack_front')} class="numeric input-100px" disabled='true'/>&nbsp;pcs Front To Back<br/>
			                <input ${_i('display_pack_top')} class="numeric input-100px" disabled='true'/>&nbsp;pcs Top To Bottom
			            </li>
			            <li class="head"><input ${_r('other','pallet_size')}/>Other Specified Size</li>
			                <li>
			                <input ${_i('other_size_w')} class="numeric input-100px"/> Width &nbsp;
		                    <input ${_i('other_size_d')} class="numeric input-100px"/> Depth &nbsp;
		                    <input ${_i('other_size_h')} class="numeric input-100px"/> Height
		                    <input ${_r('mm','other_size_unit')}/> mm <input ${_r('inch','other_size_unit')}/> inch (Without Wooden Pallet)
			            </li>
			        </ul>
        		</td>
        	</tr>
        </table>
        <ul class="ul3">
            <li class="head">
                <br/>
                <span class='title-page-1'>Front Lip Height</span> <input ${_i('front_lip_height')} class="numeric input-100px"/> <input ${_r('mm','front_lip_unit')}/> mm <input ${_r('inch','front_lip_unit')}/> inch<br/>
                <sup class="red">*</sup><span class='title-page-1'>No. Of Shelves Per Facing</span> <input ${_i('shelves_left')} class="numeric input-100px"/> Left To Right &nbsp; <input ${_i('shelves_top')} class="numeric input-100px"/> Top To Bottom<br/>
                <span class='title-page-1'>Pack Count Per Shelf</span> <input ${_i('pack_left')} class="numeric input-100px"/> Left To Right &nbsp;<input ${_i('pack_front')} class="numeric input-100px"/> Front To Back
        	 <input ${_i('top_to_bottom')} class="input-100px"/> Top To Bottom
            </li>
        </ul>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Pallet Style&nbsp;:</span></legend>
        <ul class="ul1">
            <li><span class="title-page-1">Style</span> <input ${_r('floor','style')}/>Floor Display <input ${_r('stackable','style')}/>Stackable Tray display</li>
            <li><span class="title-page-1">Facing</span> <input ${_r('1','facing')}/>1 Facing &nbsp;&nbsp;<input ${_r('2','facing')}/>2 Facing &nbsp;&nbsp;<input ${_r('3','facing')}/>3 Facing &nbsp;&nbsp;<input ${_r('4','facing')}/>4 Facing &nbsp;&nbsp;<input ${_r('other','facing')}/>Others <input ${_i('facing_other')}/></li>
            <li><span class="title-page-1">Details</span> 
                <input ${_c('Fillers','detail_type')}/>Fillers &nbsp;&nbsp;
                <input ${_cid('Header','detail_type')}/>Header(Height <input ${_i('detail_height')} class="input-100px"/> <input ${_r('mm','detail_height_unit')}/>mm <input ${_r('inch','detail_height_unit')}/>inch) &nbsp;&nbsp;
                <input ${_c('Side','detail_type')}/>Side/Back Panel
                <br />
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <input ${_cid('Hook','detail_type')}/>Hook(s)/Peg(s) &nbsp;&nbsp;<input ${_i('detail_type_hook_qty')} class="input-100px"/>pcs &nbsp;&nbsp;
                <input ${_cid('Other','detail_type')}/>Other <input ${_i('detail_type_other_content')} class="input-100px"/></li>
            <li><span class="title-page-1">Shipper</span>
                <input ${_c('top','shipper_type1')}/>Top Cap&nbsp;&nbsp; <input ${_c('bottom','shipper_type1')}/>Bottom Cap&nbsp;&nbsp; <input ${_c('shroud','shipper_type1')}/>Shroud &nbsp;&nbsp;<input ${_c('corner','shipper_type1')}/>Corner Post
                    &nbsp;&nbsp;<input ${_r('hsc','shipper_type2')}/>HSC &nbsp;&nbsp;<input ${_r('rsc','shipper_type2')}/>RSC &nbsp;&nbsp;<input ${_r('no','shipper_type2')}/>No Shipper
            </li>
            <li><span class="title-page-1">Transit</span> <input ${_r('flat','transit')}/>Flat Pack Transit&nbsp;&nbsp; <input ${_r('assembled','transit')}/>Assembled With Products</li>

        </ul>
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
        <input ${_i('expected_date',_f)} class="datePicker input-150px"/>
    </fieldset> 
</div>