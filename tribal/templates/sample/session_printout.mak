<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
_si = lambda n, f=lambda t:t : tw.attrs([('type','text'),('name',prefix+n),('id',prefix+n),('value',f(_(n)))])
_sr = lambda v,n : tw.attrs([('name',prefix+n),('type','radio'),('value',v),('disabled',disable),('onclick', 'check(this)')])
%>

<script type="text/javascript">
	$(document).ready(function(){
		%if not action == 'view' :
			timepicker('#SFPrintout-expected_time');
		%endif
        resetDeliveryNote()
        $("input[name='SFPrintout-delivery']").click(function(){
            resetDeliveryNote()
       })
	})
    function resetDeliveryNote(){
        var id = $("input[name='SFPrintout-delivery']:checked").val()
        if(id == "D"){
            $("#SFPrintout-expected_time").attr("disabled",false);
            $("#SFPrintout-expected_date").attr("disabled",true);
            $('#SFPrintout-expected_date').val('');
            $("#warning").show();
        }
        else{
            $("#SFPrintout-expected_date").attr("disabled",false);
            $("#SFPrintout-expected_time").attr("disabled",true);
            $('#SFPrintout-expected_time').val('');
            $("#warning").hide();
       }
    }
</script>
<div class="div1">
	<fieldset>
		<legend><span class="form-page-1"><sup class="red">*</sup>Files From&nbsp;:</span></legend>
		<table cellspacing="0" cellpadding="0" border="0" class='table2'>
			<tbody>
				<tr>
					<td><input id="${prefix}file_from_ftp" ${_c('ftp','file_from')}/></td>
					<td>FTP, (Location:<input ${_i('file_from_ftp_location')} class="input-600px"/>)</td>
				</tr>
				<tr>
					<td><input id="${prefix}file_from_cd" ${_c('cd','file_from')}/></td>
					<td>CD</td>
				</tr>
				<tr>
					<td><input id="${prefix}file_from_files" ${_c('files','file_from')}/></td>
					<td>Files, (Location:<input ${_i('file_from_files_location')} class="input-600px"/>)</td>
				</tr>
				<tr>
					<td valign="top"><input id="${prefix}file_from_new" ${_c('new','file_from')}/></td>
					<td>
						New Artwork With This Request<br/>
						Please advise the task name: <input class="input-150px" ${_i('file_from_task_name')}/> (i.e.: Box01)
					</td>
				</tr>
				<tr>
					<td><input id="${prefix}file_from_see_per_attachment" ${_c('see_per_attachment','file_from')}/></td>
					<td>As Per Attachment</td>
				</tr>
			</tbody>
		</table>
	</fieldset>
	<fieldset>
		<legend><span class="form-page-1"><sup class="red">*</sup>Output&nbsp;:</span></legend>
		<table cellspacing="0" cellpadding="0" border="0" class='table2'>
			<tbody>
				<tr>
					<td><input id="${prefix}output_woodfree" ${_c('woodfree','output')}/></td>
					<td>Epson - Woodfree Paper(<input ${_i('output_woodfree_pcs')} class="input-50px numeric"/>pcs)</td>
				</tr>
				<tr>
					<td><input id="${prefix}output_semi" ${_c('semi','output')}/></td>
					<td>Epson - Semi Gloss Paper(<input ${_i('output_semi_pcs')} class="input-50px numeric"/>pcs)</td>
				</tr>
				<tr>
					<td><input id="${prefix}output_label" ${_c('label','output')}/></td>
					<td>Epson - Label(<input ${_i('output_label_pcs')} class="input-50px numeric"/>pcs)</td>
				</tr>
				<tr>
					<td><input id="${prefix}output_normal" ${_c('normal','output')}/></td>
					<td>Laser Proof(<input ${_i('output_normal_pcs')} class="input-50px numeric"/>pcs)</td>
				</tr>
			</tbody>
		</table>
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
    	<p><input id="${prefix}same_day_delivery_D" ${_r('D','delivery')}/>Same Day Delivery
    		%if not disable and 'D' == _('delivery'):
      			<input class="input-150px " ${_si('expected_time')}  class="datePickerTime" >
      		%else:
      			<input class="input-150px " ${_si('expected_time')}  class="datePickerTime" disabled="disabled"> 
      		%endif
    	 	<span id='warning' style="display:none;color:red;">(It may NOT possible to arrange by the same day, please contact to PD team directly)</span></p>
    	<p><input id="${prefix}same_day_delivery_Y" ${_r('Y','delivery')}/>Expected Date
		 	%if not disable and 'Y' == _('delivery'):
      			<input class="input-150px datePicker" ${_si('expected_date',_f)}>
      		%else:
      			<input class="input-150px datePicker" ${_si('expected_date',_f)} disabled="disabled">
      		%endif
		</p>
    	%if action == 'new' :
			<p>Collection Point : 
				<input ${_sr('HKO','collection_point')} id="${prefix}collection_point_hko" ${tw.attrs([('checked','Hong Kong' in regions)])}/> Hong Kong Office 
				<input ${_sr('SZO','collection_point')} id="${prefix}collection_point_szo" ${tw.attrs([('checked','Shen Zhen' in regions)])}/> Shen Zhen Office
			</p>
		%else:
			<p>Collection Point : 
				<input ${_r('HKO','collection_point')} id="${prefix}collection_point_hko"/> Hong Kong Office 
				<input ${_r('SZO','collection_point')} id="${prefix}collection_point_szo"/> Shen Zhen Office
			</p>
		%endif
 	</fieldset>
</div>