<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_cid,_r,_incd"/>

<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Files From&nbsp;:</span></legend>
        <input ${_cid('ftp','file_from')}/> FTP (Location : <input ${_i('file_from_ftp_location')} class="input-600px" />)<br/>
        <input ${_c('cd','file_from')}/> CD<br/>
        <input ${_cid('files','file_from')}/> Files (Location : <input ${_i('file_from_files_location')} class="input-600px" />)<br/>
        <input ${_cid('attachment','file_from')}/> As Per Attachment
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1">Artwork Info&nbsp;:</span></legend>
        <ul class="ul2">
            Factory Code(Artwork)
            <select name="${prefix}factory_code" ${_d()} class="input-150px">
                %for o in ["","Advance Label - 0013","AG GIGI - 0152","Morning Sun - 0019","Great Shengda (GSD) - 0195","Hangzhou Zezhong - 0168","Kunshan Printec - 0018","Parksons Printing - 0069","Precision Print - 0012","Safe Power - 0120","Sedele (SDL) - 0071","Tophand - 0121","Suteng - 0142","Sun Hing - 0009","DMS - 0126"]:
                <option value="${o}" ${tw.attrs([('selected',o == _('factory_code'))])}>${o}</option>
                %endfor
            </select><br/>
            Size&nbsp;:
            <input ${_i('size_w')} class="input-100px numeric" />&nbsp;W 
            <input ${_i('size_h')} class="input-100px numeric" />&nbsp;H
            <input ${_r('mm','size_unit')}/>mm
            <input ${_r('inch','size_unit')}/>inch<br/>
            Color:
            <li>
                <input ${_c('4color','color')}/> 4 Color Processing<br/>
                <input ${_cid('spot','color')}/> Spot Color:
            	<ul>
            		<li>
            			PMS<input ${_i('color_spot_content')} class="input-50px numeric" />
            		</li>
            	</ul>
                <input ${_cid('other','color')}/> Other <input ${_i('color_other_content')} class="input-150px" />
            </li>
          </tr>
        </ul>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Output&nbsp;:</span></legend>
        <input ${_c('pdf','output')} id="${prefix}output_pdf"/> PDF &nbsp;&nbsp; Security File Protction <input ${_r('YES','protection')}/> Yes <input ${_r('NO','protection')}/> No <br/>
        <input ${_c('ai','output')}/> AI<br/>
        <input ${_c('eps','output')}/> EPS<br/>
        <input ${_c('jpg','output')}/> JPG<br/>
        <input ${_cid('other','output')}> Other <input ${_i('output_other_content')} class="input-150px" />
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