<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>

<script type="text/javascript" src="/js/jquery.bgiframe.pack.js" language="javascript"></script>
<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/material.js?v=2"></script>

<script type="text/javascript">
	$(document).ready(function(){
		%if not action == 'view' :
			timepicker('#SFSampling-expected_time');
		%endif
		$('.material_widget').material_popup();
		resetDeliveryNote()
        $("input[name='SFSampling-delivery']").click(function(){
            resetDeliveryNote()
       	})
	})
	function resetDeliveryNote(){
        var id = $("input[name='SFSampling-delivery']:checked").val()
        if(id == "D"){
            $("#SFSampling-expected_time").attr("disabled",false);
            $("#SFSampling-expected_date").attr("disabled",true);
            $('#SFSampling-expected_date').val('');
            $("#warning").show();
        }
        else{
            $("#SFSampling-expected_date").attr("disabled",false);
            $("#SFSampling-expected_time").attr("disabled",true);
            $('#SFSampling-expected_time').val('');
            $("#warning").hide();
       }
    }
</script>
<div class='div1'>
	<fieldset>
  		<legend><span class="form-page-1"><sup class="red">*</sup>Files From&nbsp;:</span></legend>
	  	<table cellspacing="0" cellpadding="0" border="0" class="table2">
			<tbody>
				<tr>
					<td><input id="${prefix}file_from_ftp" ${_c('ftp','file_from')}/></td>
					<td>FTP, (Location:<input class="input-600px" ${_i('file_from_ftp_location')}/>)</td>
				</tr>
				<tr>
					<td><input id="${prefix}file_from_cd"${_c('cd','file_from')}/></td>
					<td>CD</td>
				</tr>
				<tr>
					<td><input id="${prefix}file_from_files" ${_c('files','file_from')}/></td>
					<td>Files, (Location:<input class="input-600px" ${_i('file_from_files_location')}/>)</td>
				</tr> 
				<tr>
					<td><input id="${prefix}file_from_see_per_attachment" ${_c('see_per_attachment','file_from')}/></td>
					<td>As Per Attachment</td>
				</tr>
				<tr>
					<td valign="top"><input id="${prefix}New_design_with_this_request" ${_c('New_design_with_this_request','file_from')}/></td>
					<td>
						New Design With This Request<br/>
						Please advise the task name: <input class="input-150px" ${_i('file_from_task_name')}/> (i.e.: Box01)
					</td>
				</tr>
			</tbody>
		</table>
	</fieldset>
	<fieldset>
		<legend><span class="form-page-1"><sup class="red">*</sup>Output&nbsp;:</span></legend>
		<table cellspacing="0" cellpadding="0" border="0" class="table2">
			<tbody>
				<tr>
					<td><input id="${prefix}output_white" ${_c('white','output')}/></td>
					<td>White Mock Up(<input class="input-50px numeric" ${_i('output_white_pcs')} class="numeric"/>pcs)</td>
				</tr>
				<tr>
					<td><input id="${prefix}output_woodfree" ${_c('woodfree','output')}/></td>
					<td>Color Mock Up In Woodfree Paper(<input class="input-50px numeric" ${_i('output_woodfree_pcs')}/>pcs)</td>
				</tr>
				<tr>
					<td><input id="${prefix}output_semi" ${_c('semi','output')}/></td>
					<td>Color Mock Up In Semi Gloss Paper(<input class="input-50px numeric" ${_i('output_semi_pcs')}/>pcs)</td>
				</tr>
				<tr>
					<td><input id="${prefix}output_label" ${_c('label','output')}/></td>
					<td>Color Mock Up In Label(<input class="input-50px numeric" ${_i('output_label_pcs')}/>pcs) <b class="red">#Recommended For Color Mock Up</b></td>
				</tr>
			</tbody>
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
				<td width="350">
					<input type="text" class="material_widget input-300px" value="${widget['SHOW_TEXT']|ue, h}" ref='${widget|jd,n}' ${ tw.attrs([('disabled',disable)]) }/>
				</td>
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
    	<p>
    		<input id="${prefix}same_day_delivery_D" ${_r('D','delivery')}/>Same Day Delivery
      		<input class="input-150px " ${_i('expected_time')}  class="datePickerTime" >
      		<span id='warning' style="display:none;color:red;">(It may NOT possible to arrange by the same day, please contact to PD team directly)</span>
  		</p>
      	<p>
      		<input id="${prefix}same_day_delivery_Y" ${_r('Y','delivery')}/>Expected Date
      		<input class="input-150px datePicker" ${_i('expected_date',_f)}>
      	</p>    	
		%if action == 'new' or isinstance(dbObject,type) :
			<p>Collection Point:  
				<input ${_r('HKO','collection_point')} id="${prefix}collection_point_hko" ${tw.attrs([('checked','Hong Kong' in regions)])}/> Hong Kong Office 
				<input ${_r('SZO','collection_point')} id="${prefix}collection_point_szo" ${tw.attrs([('checked','Shen Zhen' in regions)])}/> Shen Zhen Office
			</p>
		%else:
			<p>Collection Point : 
				<input ${_r('HKO','collection_point')} id="${prefix}collection_point_hko"/> Hong Kong Office 
				<input ${_r('SZO','collection_point')} id="${prefix}collection_point_szo"/> Shen Zhen Office
			</p>
		%endif
	</fieldset> 
</div>