<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>

<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Submitted Items&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="30"><input id="${prefix}submit_items_dieline" ${_c('dieline','submit_items')}/></td>
                <td><label for="${prefix}submit_items_dieline">Die-line Files</label>
                    , (Location:
                    <input ${_i('submit_items_location')} class="input-600px"/>
                        )</td>
            </tr>
            <tr>
                <td><input id="${prefix}submit_items_actual_packaging" ${_c('actual','submit_items')}/></td>
                <td><label for="${prefix}submit_items_actual_packaging">Actual Packaging</label></td>
            </tr>
            <tr>
                <td><input id="${prefix}submit_items_new_design" ${_c('new','submit_items')}/></td>
                <td><label for="${prefix}submit_items_new_design">New Design With This Request</label></td>
            </tr>
            <tr>
                <td><input id="${prefix}submit_items_fake_product" ${_c('fake','submit_items')}/></td>
                <td><label for="${prefix}submit_items_fake_product">Fake Product For Drop Test</label></td>
            </tr>
            <tr>
                <td><input id="${prefix}submit_items_attachment" ${_c('attachment','submit_items')}/></td>
                <td><label for="${prefix}submit_items_attachment">As Per Attachment</label></td>
            </tr>
            <tr>
                <td><input id="${prefix}submit_items_guideline" ${_c('guideline','submit_items')}/></td>
                <td><label for="${prefix}submit_items_guideline">Guideline</label></td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Test Info&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="30"><input id="${prefix}test_info_1a" ${_r('ISTA_1A','test_info')}/></td>
                <td><label for="${prefix}test_info_1a">ISTA 1A</label></td>
            </tr>
            <tr>
                <td><input id="${prefix}test_info_2a" ${_r('ISTA_2A','test_info')}/></td>
                <td><label for="${prefix}test_info_2a">ISTA 2A</label></td>
            </tr>
            <tr>
                <td colspan="2" style="font-weight:bold;">**Please contact QE Team in case you need others ISTA test</td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Conditions&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td width="30"><input id="${prefix}condition_product" ${_r('product','condition')}/></td>
                <td><label for="${prefix}condition_product">Drop test PASS when only product without damage</label></td>
            </tr>
            <tr>
                <td><input id="${prefix}condition_packaging" ${_r('packaging','condition')}/></td>
                <td><label for="${prefix}condition_packaging">Drop test PASS when product and packaging without damage(drop test with Master Packer)</label></td>
            </tr>
            <tr>
                <td><input id="${prefix}condition_other" ${_r('other','condition')}/></td>
                <td><label for="${prefix}condition_other">Others : </label><input ${_i('condition_other_content')} class="input-150px"/></td>
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