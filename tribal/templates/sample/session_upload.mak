<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>
<script type="text/javascript">
	$(document).ready(function(){
				var list = 	[
					 "#SFUpload-from_ftp_location",
					 "#SFUpload-from_public_location",
					 "#SFUpload-to_ftp_location",
					 "#SFUpload-to_public_location"
					 ]
		
		//lessCheckBox(list)
		
		$("#SFUpload-file_from_ftp").click(function(){
					lessCheckBox(["#SFUpload-from_ftp_location","#SFUpload-from_public_location"])
					workCheckBox($(this),
						[
						"#SFUpload-from_ftp_location",
						]
					)
					
		})
		$("#SFUpload-file_from_public").click(function(){
					lessCheckBox(["#SFUpload-from_ftp_location","#SFUpload-from_public_location"])
					workCheckBox($(this),
						[
						"#SFUpload-from_public_location",
						]
					)
		})
		$("#SFUpload-file_from_cd,#SFUpload-New_design_with_this_request").click(function(){
			lessCheckBox(["#SFUpload-from_ftp_location","#SFUpload-from_public_location"])		
		})
		
		$("#SFUpload-file_to_ftp").click(function(){
					lessCheckBox(["#SFUpload-to_ftp_location","#SFUpload-to_public_location"])
					workCheckBox($(this),
						[
						"#SFUpload-to_ftp_location",
						]
					)
					
		})

		$("#SFUpload-file_to_public").click(function(){
					lessCheckBox(["#SFUpload-to_ftp_location","#SFUpload-to_public_location"])
					workCheckBox($(this),
						[
						"#SFUpload-to_public_location",
						]
					)				
		})
		$("#SFUpload-file_to_cd").click(function(){
			lessCheckBox(["#SFUpload-to_ftp_location","#SFUpload-to_public_location"])				
		})
	
	})
</script>
<div>
  <fieldset>
  <legend><span class="form-page-1"><sup class="red">*</sup>Job Nature&nbsp;:</span></legend>
  <ul class="form-ul">
    <li>
      <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 10px 0px;" class="table-line-height">
        <tbody>
          <tr>
            <td width="30"><input id="${prefix}job_nature_u" ${_c('Upload','checking')}/></td>
            <td><label for="${prefix}job_nature_u">Upload</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}job_nature_d" ${_c('Download','checking')}/></td>
            <td><label for="${prefix}job_nature_d">Download</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}artwork_checking" ${_c('artwork','checking')}/></td>
            <td><label for="${prefix}artwork_checking">Artwork Pre-Flight</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}dieline_checking" ${_c('dieline','checking')}/></td>
            <td><label for="${prefix}dieline_checking">Die-line Pre-Flight</label></td>
          </tr>
        </tbody>
      </table>
    </li>
  </ul>
  </fieldset>
  <fieldset>
  <legend><span class="form-page-1"><sup class="red">*</sup>Files From&nbsp;:</span></legend>
  <ul class="form-ul">
    <li> 
      <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 10px 0px;" class="table-line-height">
        <tbody>
          <tr>
            <td width="30"><input id="${prefix}file_from_ftp" ${_r('ftp','file_from')}/></td>
            <td><label for="${prefix}file_from_ftp">FTP</label>
              , (Location:
              <input ${_i('from_ftp_location')} class="input-600px"/>
              )</td>
          </tr>
          <tr>
            <td><input id="${prefix}file_from_public" ${_r('public','file_from')}/></td>
            <td><label for="${prefix}file_from_public">Public</label>
              , (Location:
              <input ${_i('from_public_location')} class="input-600px"/>
              ) </td>
          </tr>
          <tr>
            <td><input id="${prefix}file_from_cd" ${_r('cd','file_from')}/></td>
            <td><label for="${prefix}file_from_cd">CD/DVD</label></td>
          </tr>
           <tr>
            <td><input ${_r('attachment','file_from')}/></td>
            <td><label>As Per Attachment</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}New_design_with_this_request" ${_r('New_design_with_this_request','file_from')}/></td>
            <td><label for="${prefix}New_design_with_this_request">New Design With This Request</label></td>
          </tr>
        </tbody>
      </table>
    </li>
  </ul>
  </fieldset>
  <fieldset>
  <legend><span class="form-page-1"><sup class="red">*</sup>File To&nbsp;:</span></legend>
  <ul class="form-ul">
    <li> 
      <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 10px 0px;" class="table-line-height">
        <tbody>
          <tr>
            <td width="30"><input id="${prefix}file_to_ftp" ${_r('ftp','file_to')}/></td>
            <td><label for="${prefix}file_to_ftp">FTP</label>
              (Location
              <input ${_i('to_ftp_location')} class="input-600px"/>
              ) </td>
          </tr>
          <tr>
            <td><input id="${prefix}file_to_public" ${_r('public','file_to')}/></td>
            <td><label for="${prefix}file_to_public">Public</label>
              (Location
              <input ${_i('to_public_location')}  class="input-600px"/>
              )</td>
          </tr>
          <tr>
            <td><input id="${prefix}file_to_cd" ${_r('cd','file_to')}/></td>
            <td><label for="${prefix}file_to_cd">CD/DVD</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}file_to_email" ${_r('email','file_to')}/></td>
            <td><label for="${prefix}file_to_email">By E-mail</label></td>
          </tr>
        </tbody>
      </table>
    </li>
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
  <ul class="form-ul">
    <li><input  ${_i('expected_date',_f)} class="input-150px datePicker"/></li>
  </ul>
  </fieldset>
</div> 