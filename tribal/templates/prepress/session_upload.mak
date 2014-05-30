<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="cf,prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>


<script type="text/javascript">
	$(document).ready(function(){
				var list = 	[
					 "#PSSFUpload-from_ftp_location",
					 "#PSSFUpload-from_public_location",
					 "#PSSFUpload-to_ftp_location",
					 "#PSSFUpload-to_public_location"
					 ]
		
		$("#PSSFUpload-file_from_ftp").click(function(){
					lessCheckBox(["#PSSFUpload-from_ftp_location","#PSSFUpload-from_public_location"])
					workCheckBox($(this),
						[
						"#PSSFUpload-from_ftp_location",
						]
					)
					
		})
		$("#PSSFUpload-file_from_public").click(function(){
					lessCheckBox(["#PSSFUpload-from_ftp_location","#PSSFUpload-from_public_location"])
					workCheckBox($(this),
						[
						"#PSSFUpload-from_public_location",
						]
					)
		})
		$("#PSSFUpload-file_from_cd,#PSSFUpload-New_design_with_this_request").click(function(){
			lessCheckBox(["#PSSFUpload-from_ftp_location","#PSSFUpload-from_public_location"])		
		})
		
		$("#PSSFUpload-file_to_ftp").click(function(){
					lessCheckBox(["#PSSFUpload-to_ftp_location","#PSSFUpload-to_public_location"])
					workCheckBox($(this),
						[
						"#PSSFUpload-to_ftp_location",
						]
					)
					
		})

		$("#PSSFUpload-file_to_public").click(function(){
					lessCheckBox(["#PSSFUpload-to_ftp_location","#PSSFUpload-to_public_location"])
					workCheckBox($(this),
						[
						"#PSSFUpload-to_public_location",
						]
					)				
		})
		$("#PSSFUpload-file_to_cd").click(function(){
			lessCheckBox(["#PSSFUpload-to_ftp_location","#PSSFUpload-to_public_location"])				
		})
		
	
	})

</script>
<div>
  <fieldset>
  <legend><span class="form-page-1"><sup class="red">*</sup>Job Nature&nbsp;:</span></legend>
  <ul class="form-ul">
    <li>
      %if action == 'view' :
          <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 10px 0px;" class="table-line-height">
            <tbody>
              <tr>
                <td width="30"><input id="${prefix}upload_checking" ${_c('upload','checking')}/></td>
                <td><label for="${prefix}upload_checking">Upload</label></td>
                <td>
                    <%include file="status_fun.mak" args="val='upload',cbvalues=_('checking'),sftype=cf.__class__.__name__,cf=cf,jobdata=jobdata"/>
                </td>
              </tr>
              <tr>
                <td><input id="${prefix}download_checking" ${_c('download','checking')}/></td>
                <td><label for="${prefix}download_checking">Download</label></td>
                <td>
                    <%include file="status_fun.mak" args="val='download',cbvalues=_('checking'),sftype=cf.__class__.__name__,cf=cf,jobdata=jobdata"/>
                </td>
              </tr>
              <tr>
                <td><input id="${prefix}preflight_checking" ${_c('preflight','checking')}/></td>
                <td><label for="${prefix}preflight_checking">Artwork Pre-Flight</label></td>
                <td>
                    <%include file="status_fun.mak" args="val='preflight',cbvalues=_('checking'),sftype=cf.__class__.__name__,cf=cf,jobdata=jobdata"/>
                </td>
              </tr>
              <tr>
                <td><input id="${prefix}adaption_checking" ${_c('adaption','checking')}/></td>
                <td><label for="${prefix}adaption_checking">Artwork Adaption</label></td>
                <td>
                    <%include file="status_fun.mak" args="val='adaption',cbvalues=_('checking'),sftype=cf.__class__.__name__,cf=cf,jobdata=jobdata"/>
                </td>
              </tr>
              <tr>
                <td><input id="${prefix}design_checking" ${_c('design','checking')}/></td>
                <td><label for="${prefix}design_checking">Artwork Design</label></td>
                <td>
                    <%include file="status_fun.mak" args="val='design',cbvalues=_('checking'),sftype=cf.__class__.__name__,cf=cf,jobdata=jobdata"/>
                </td>
              </tr>
              <tr>
                <td><input id="${prefix}artwork_checking" ${_c('artwork','checking')}/></td>
                <td><label for="${prefix}artwork_checking">Artwork Checking</label></td>
                <td>
                    <%include file="status_fun.mak" args="val='artwork',cbvalues=_('checking'),sftype=cf.__class__.__name__,cf=cf,jobdata=jobdata"/>            
                </td>  
              </tr>
              <tr>
                  <td><input id="${prefix}full_set_layout" ${_c('layout','checking')}/></td>
                  <td><label for="${prefix}full_set_layout">Full-set Layout</label></td>
                  <td>
                    <%include file="status_fun.mak" args="val='layout',cbvalues=_('checking'),sftype=cf.__class__.__name__,cf=cf,jobdata=jobdata"/>           
                </td>  
              </tr>
            </tbody>
          </table>
      %else:
          <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 10px 0px;" class="table-line-height">
            <tbody>
              <tr>
                <td width="30"><input id="${prefix}upload_checking" ${_c('upload','checking')}/></td>
                <td><label for="${prefix}upload_checking">Upload</label></td>
              </tr>
              <tr>
                <td><input id="${prefix}download_checking" ${_c('download','checking')}/></td>
                <td><label for="${prefix}download_checking">Download</label></td>
              </tr>
              <tr>
                <td><input id="${prefix}preflight_checking" ${_c('preflight','checking')}/></td>
                <td><label for="${prefix}preflight_checking">Artwork Pre-Flight</label></td>
              </tr>
              <tr>
                <td><input id="${prefix}adaption_checking" ${_c('adaption','checking')}/></td>
                <td><label for="${prefix}adaption_checking">Artwork Adaption</label></td>
              </tr>
              <tr>
                <td><input id="${prefix}design_checking" ${_c('design','checking')}/></td>
                <td><label for="${prefix}design_checking">Artwork Design</label></td>
              </tr>
              <tr>
                <td><input id="${prefix}artwork_checking" ${_c('artwork','checking')}/></td>
                <td><label for="${prefix}artwork_checking">Artwork Checking</label></td>
              </tr>
              <tr>
                  <td><input id="${prefix}full_set_layout" ${_c('layout','checking')}/></td>
                  <td><label for="${prefix}full_set_layout">Full-set Layout</label></td>
              </tr>
            </tbody>
          </table>
      %endif
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
        <legend><span class="form-page-1"><sup class="red">*</sup>Output&nbsp;:</span></legend>
        <table class="table2">
            <tr>
                <td><input ${_c('pdf','output')} id="${prefix}output_pdf"></td>
                <td>PDF &nbsp;&nbsp; Security File Protction <input ${_r('YES','protection')}/> Yes <input ${_r('NO','protection')}/> No</td>
            </tr>
            <tr>
                <td><input ${_c('ai','output')}></td>
                <td>AI</td>
            </tr>
            <tr>
                <td><input ${_c('eps','output')}></td>
                <td>EPS</td>
            </tr>
            <tr>
                <td><input ${_c('jpg','output')}></td>
                <td>JPG</td>
            </tr>
            <tr>
                <td><input id="${prefix}output_other_type" ${_c('other','output')}></td>
                <td>Other <input ${_i('output_other_content')} class="input-150px" /></td>
            </tr>
        </table>
    </fieldset>    
    <fieldset>
        <legend><span class="form-page-1">Remark&nbsp;:</span></legend>
        %if disable: 
        	${_('remark').replace("\n","<br/>")}
        %else:
        	<textarea class="input-600px" rows="5"  name="${prefix}remark">
${_('remark')}</textarea>
        %endif
    </fieldset>
  <fieldset>
  <legend><span class="form-page-1"><sup class="red">*</sup>Expected Date&nbsp;:</span></legend>
  <ul class="form-ul">
    <li><input  ${_i('expected_date',_f)} class="input-150px datePicker"/></li>
  </ul>
  </fieldset>
</div> 