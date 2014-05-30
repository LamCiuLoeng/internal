<%page args="prefix,disable,_,_d,_f,_i,_c,_cid,_r,_incd"/>

<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Files From&nbsp;:</span></legend>
        <input ${_cid('ftp','file_from')}/> FTP, ( Location: <input ${_i('file_from_ftp_location')} class="input-600px"/> )<br/>
        <input ${_c('cd','file_from')}/> CD<br/>
        <input ${_cid('files','file_from')}/> Files, ( Location: <input ${_i('file_from_files_location')} class="input-600px"/> )<br/>
        <input ${_c('new','file_from')}/> New Design With This Request<br/>
        <input ${_cid('attachment','file_from')}/> As Per Attachment
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Output&nbsp;:</span></legend>
        <input ${_r('plain','output')}/> Basic assembly sheet in plain<br/>
        <input ${_r('graphics','output')}/> Basic assembly sheet with graphics(Please make sure the artworks were provided)<br/>
        <input ${_r('products','output')}/> Plain assembly with products(Please make sure the products or product photos were provided)<br/>
        <input ${_r('assembly','output')}/> Assembly sheet with products and graphics(Please make sure the artworks,products or product photos were provided)
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