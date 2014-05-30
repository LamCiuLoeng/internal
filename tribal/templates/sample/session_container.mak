<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>
<script type="text/javascript">
$(document).ready(function(){
		linkScroll([$("#SFContainer-outer_w"),
			$("#SFContainer-outer_d"),
			$("#SFContainer-outer_h"),
			$("input[name='SFContainer-outer_unit']")],
			$("input[name='SFContainer-outer_as_sample']")
			)
})
</script>
<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Loading Info&nbsp;:</span></legend>
        Weight
        <input ${_i('weight')} class="input-100px numeric"/>&nbsp;&nbsp;
            <select name="${prefix}weight_unit" id="${prefix}weight_unit" ${_d()} class="input-50px">
                %for o in ["","gram","kg","lbs","oz"]:
                <option value="${o}" ${tw.attrs([('selected',o == _('weight_unit'))])}>${o}</option>
                %endfor
            </select>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input ${_c('Y','weight_as_sample')}/>&nbsp;As Sample<br/>
        <table>
        	<tr>
        		<td><sup class="red">*</sup>Size:</td>
        		<td>
        			<input id="${prefix}size_according_out" ${_r('out','size_according')}/>Overall Outer Size:
	               	<input ${_i('outer_w')} class="input-50px numeric"/> W 
	               	<input ${_i('outer_d')} class="input-50px numeric"/> D 
	               	<input ${_i('outer_h')} class="input-50px numeric"/> H
	               	<input id="${prefix}outer_unit_mm" ${_r('mm','outer_unit')}/> mm
	               	<input id="${prefix}outer_unit_inch" ${_r('inch','outer_unit')}/> inch
	               	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input ${_c('Y','outer_as_sample')}/>&nbsp;As Sample<br/>
        		</td>
        	</tr>
        	<tr>
        		<td>&nbsp;</td>
        		<td><input ${_r('new','size_according')}/>Size According To The New Deisgn With This Request</td>
        	</tr>
        	<tr>
        		<td>&nbsp;</td>
        		<td><input ${_r('attachment','size_according')}/>As Per Attachment</td>
        	</tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Pallet&nbsp;:</span></legend>
        <input id="${prefix}pallet_without" ${_r('without','pallet')}/> Without Pallet<br/>
        <input id="${prefix}pallet_with" ${_r('with','pallet')}/> With Pallet
               <input ${_i('pallet_w')} class="input-50px numeric"/> W 
               <input ${_i('pallet_d')} class="input-50px numeric"/> D 
               <input ${_i('pallet_h')} class="input-50px numeric"/> H
               <input id="${prefix}pallet_unit_mm" ${_r('mm','pallet_unit')}/> mm
               <input id="${prefix}pallet_unit_inch" ${_r('inch','pallet_unit')}/> inch
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Product Orientation&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="30"><input id="${prefix}orientation_t" ${_r('top','orientation')}/></td>
                <td>Top &amp; Bottom Side Up</td>
                <td width="10">&nbsp;</td>
                <td width="30"><input id="${prefix}orientation_l" ${_r('left','orientation')}/></td>
                <td>Left &amp; Right Side Up</td>
            </tr>
            <tr>
                <td><input id="${prefix}orientation_f" ${_r('front','orientation')}/></td>
                <td>Front &amp; Back Side Up</td>
                <td>&nbsp;</td>
                <td width="30"><input id="${prefix}orientation_a" ${_r('any','orientation')}/></td>
                <td>Any</td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Container Info&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="30"><input ${_c('20fts','info')}/></td>
                <td>20ft Standard</td>
                <td width="10">&nbsp;</td>
                <td width="30"><input ${_c('40fts','info')}/></td>
                <td>40ft Standard</td>
            </tr>
            <tr>
                <td><input ${_c('40fth','info')}/></td>
                <td>40ft High Cube</td>
                <td>&nbsp;</td>
                <td width="30"><input id="${prefix}info_other_type" ${_c('other','info')}/></td>
                <td>Others
                    <input ${_i('info_other')} class="input-150px"/></td>
            </tr>
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
        <input  ${_i('expected_date',_f)} class="input-150px datePicker"/>
    </fieldset>
</div>