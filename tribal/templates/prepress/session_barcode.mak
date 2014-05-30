<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>
<script type="text/javascript">
	$(document).ready(function(){
				var list = 	[
					 "#PSSFBarcode-from_ftp_location",
					 "#PSSFBarcode-from_public_location",
					 "#PSSFBarcode-to_ftp_location",
					 "#PSSFBarcode-to_public_location"
					 ]
		
		$("#PSSFBarcode-file_from_ftp").click(function(){
					lessCheckBox(["#PSSFBarcode-from_ftp_location","#PSSFBarcode-from_public_location"])
					workCheckBox($(this),
						[
						"#PSSFBarcode-from_ftp_location",
						]
					)
					
		})
		$("#PSSFBarcode-file_from_public").click(function(){
					lessCheckBox(["#PSSFBarcode-from_ftp_location","#PSSFBarcode-from_public_location"])
					workCheckBox($(this),
						[
						"#PSSFBarcode-from_public_location",
						]
					)
		})
		$("#PSSFBarcode-file_from_cd,#PSSFBarcode-New_design_with_this_request").click(function(){
			lessCheckBox(["#PSSFBarcode-from_ftp_location","#PSSFBarcode-from_public_location"])		
		})
		
		$("#PSSFBarcode-file_to_ftp").click(function(){
					lessCheckBox(["#PSSFBarcode-to_ftp_location","#PSSFBarcode-to_public_location"])
					workCheckBox($(this),
						[
						"#PSSFBarcode-to_ftp_location",
						]
					)
					
		})

		$("#PSSFBarcode-file_to_public").click(function(){
					lessCheckBox(["#PSSFBarcode-to_ftp_location","#PSSFBarcode-to_public_location"])
					workCheckBox($(this),
						[
						"#PSSFBarcode-to_public_location",
						]
					)				
		})
		$("#PSSFBarcode-file_to_cd").click(function(){
			lessCheckBox(["#PSSFBarcode-to_ftp_location","#PSSFBarcode-to_public_location"])				
		})
		
		$("#PSSFBarcode-output_other").click(function(){
			workCheckBox($(this),
				[
				"#PSSFBarcode-output_other_content2"
				]
			)		
		})	
	
	})
	
	
	var changeBarcode=function(obj){
		var barcodeImages = {
			'Code 128 (General)':'/images/sample/barcode/Code 128 General.jpg',
			'Code 128 (Code A)':'/images/sample/barcode/Code 128 A.jpg',
			'Code 128 (Code B)':'/images/sample/barcode/Code 128 B.jpg',
			'Code 128 (Code C)':'/images/sample/barcode/Code 128 C.jpg',
			'Code 39':'/images/sample/barcode/Code 39.jpg',
			'Code 93':'/images/sample/barcode/Code 93.jpg',
			'EAN-13':'/images/sample/barcode/EAN-13.jpg',
			'EAN-8':'/images/sample/barcode/EAN-8.jpg',
			'UCC/EAN-128':'/images/sample/barcode/UCCEAN-128.jpg',
			'UPC(A)':'/images/sample/barcode/UPC(A).jpg',
			'UPC(E) (11-Digit Input)':'/images/sample/barcode/UPC (E) (11-Digit Input).jpg',
			'UPC(E) (6-Digit Input)':'/images/sample/barcode/UPC (E) (6-Digit Input).jpg'
		}
		$('#dis_barcode').html('<img src="'+barcodeImages[$(obj).val()]+'" width=300px>')
	}
</script>
<div>  
    <!-- label begin -->
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Label Files From&nbsp;:</span></legend>
        <input id="${prefix}file_from_ftp" ${_c('ftp','file_from')}/> FTP (Location : <input ${_i('file_from_ftp_location')} class="input-600px" />)<br/>
        <input id="${prefix}file_from_cd" ${_c('cd','file_from')}/> CD<br/>
        <input id="${prefix}file_from_files" ${_c('files','file_from')}/> Files (Location : <input ${_i('file_from_files_location')} class="input-600px" />)<br />
        <input id="${prefix}file_from_see_per_attachment" ${_c('see_per_attachment','file_from')}/>As Per Attachment
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1">Label Info&nbsp;:</span></legend>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td>Size</td>
                <td>
                    <input ${_i('size_w')} class="input-100px numeric"/>&nbsp;W 
                    <input ${_i('size_h')} class="input-100px numeric" />&nbsp;H
                    <input ${_r('mm','size_unit')}/>mm
                    <input ${_r('inch','size_unit')}/>inch
                </td>
                <td rowspan="9" id='dis_barcode'></td>
            </tr>
            <tr>
                <td>Material</td>
                <td><input ${_i('material')} class="input-150px" /></td>
            </tr>
            <tr>
                <td>Country</td>
                <td><input ${_i('country')} class="input-150px" /></td>
            </tr>
            <tr>
                <td>Item Code&nbsp;</td>
                <td><input ${_i('item_code')} class="input-150px" /></td>
            </tr>
            <tr>
                <td>Item Name&nbsp;</td>
                <td><input ${_i('item_name')} class="input-150px" /></td>
            </tr>
            <tr>
                <td><sup class="red">*</sup>Bar Code No. &amp Type&nbsp;</td>
                <td>
                	<select name="${prefix}barcode" id="${prefix}barcode" ${_d()} class="input-150px" onchange='changeBarcode(this)'>
		                %for o in ["","Code 128 (General)","Code 128 (Code A)","Code 128 (Code B)","Code 128 (Code C)",'Code 39','Code 93','EAN-13','EAN-8','UCC/EAN-128','UPC(A)','UPC(E) (11-Digit Input)','UPC(E) (6-Digit Input)']:
		                <option value="${o}" ${tw.attrs([('selected',o == _('barcode'))])}>${o}</option>
		                %endfor
		            </select>
            </tr>
            <tr>
                <td>Font Request&nbsp;</td>
                <td><input ${_i('font')} class="input-150px" /></td>
            </tr>
            <tr>
                <td>Others&nbsp;</td>
                <td><input ${_i('content_color')} class="input-150px" /></td>
            </tr>
            <tr>
                <td><sup class="red">*</sup>Print&nbsp;</td>
                <td>
                    <input ${_r('color','color')}/>Color
                    <input ${_r('Black','color')}/>Black
                    <input ${_r('Others','color')}/>Other&nbsp;<input ${_i('color_other_content')} class="input-150px" />
                </td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Label Output&nbsp;:</span></legend>
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
    
    <!-- label end -->
    
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