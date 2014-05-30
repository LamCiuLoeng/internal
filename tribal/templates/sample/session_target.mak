<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_cid,_incd"/>
<%
from tribal.util.sample_helper import getSampleMaster
from tribal.model import Customer
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>
<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/material.js?v=2"></script>
<script type="text/javascript" src="/js/jquery.maskedinput-1.3.min.js"></script>
<script type="text/javascript">
	$(document).ready(function(){
        $("#material_other_tmp").material_popup({'afterSave' : function(){
           $("#SFTarget-material_other").val($("#material_other_tmp").attr("ref"));
        }});
		$("#SFTarget-dpci").mask("999-99-9999",{placeholder:" "});
        getText();
		var list = 	[
					 "#SFTarget-file_format",
					 "#SFTarget-file_format_eps",
					 "#SFTarget-file_format_jpeg",
					 "#SFTarget-file_format2",
					 "#SFTarget-file_format_eps2",
					 "#SFTarget-file_format_jpeg2",
					 //"#SFTarget-sample_qty",
					 //"#SFTarget-requirement_other",
					 //"#SFTarget-sample_white",
					 //"#SFTarget-sample_mock",
					 "#SFTarget-file_format_ard",
					 "#SFTarget-file_format_ard2"
					 ]
		
		lessCheckBox(list.concat("#SFTarget-submitted_item_other"))
		
		
		$("#SFTarget-requirement_quote").click(function(){
					lessCheckBox(list)
					workCheckBox($(this),
						[
						"#SFTarget-file_format",
						"#SFTarget-file_format_eps",
						"#SFTarget-file_format_jpeg",
						"#SFTarget-file_format_ard"
						]
					)
					//checkRadio(["#SFTarget-target_format_y","#SFTarget-file_protection_y"])
					
		})
		$("#SFTarget-requirement_production").click(function(){
					lessCheckBox(list)
					workCheckBox($(this),
						[
						"#SFTarget-file_format2",
						"#SFTarget-file_format_eps2",
						"#SFTarget-file_format_jpeg2",
						"#SFTarget-file_format_ard2"
						]
					)
					//checkRadio(["#SFTarget-target_format_y","#SFTarget-file_protection_y"])
					
		})
		$("#SFTarget-color_spot").click(function(){
					workCheckBox($(this),
						[
						"input[name=SFTarget-color_spot_content]"
						]
					)
		})
		$("#SFTarget-material_others").click(function(){
					workCheckBox($(this),
						[
						"#SFTarget-material_other"
						]
					)
		})
		
		$("#SFTarget-submitted_item_others").click(function(){
					workCheckBox($(this),
						[
						"#SFTarget-submitted_item_other"
						]
					)
		})
		
		/*
		$("#SFTarget-requirement_Sampling").click(function(){
					workCheckBox($(this),
						[
						"#SFTarget-sample_qty",
						"#SFTarget-sample_white",
						"#SFTarget-sample_mock"
						]
					)
		})
		$("#SFTarget-requirement_Others").click(function(){
					workCheckBox($(this),
						[
						"#SFTarget-requirement_other"
						]
					)
		})
		*/
		
		$("#SFTarget-material_e").click(function(){
					lessCheckBox(["#SFTarget-material_other"])
		})
		$("#SFTarget-material_b").click(function(){
					lessCheckBox(["#SFTarget-material_other"])
		})
		
	})
</script>
<div class='div1'>
	<fieldset> 
		<table class='table2' cellspacing="0" cellpadding="0" border="0">
              <tr>
                <td><label for="${prefix}dept_id">Dept#</label></td>
                <td><input ${_i('dept_id')} class="input-150px" /></td>
              </tr>
              <tr>
                <td><label for="${prefix}promo_id">Promo ID</label></td>
                <td><input ${_i('promo_id')} class="input-150px" /></td>
              </tr>
              <tr>
                <td><label for="${prefix}dpci">Target DPCI#</label></td>
                <td><input ${_i('dpci')} class="input-150px"/></td>
              </tr>
              <tr>
                <td><label for="${prefix}packaging_style">Packaging Style</label></td>
                <td><input ${_i('packaging_style')} class="input-150px" /></td>
              </tr>
              <tr>
                <td><label for="${prefix}vendor_style">Vendor Style#</label></td>
                <td><input ${_i('vendor_style')} class="input-150px"/></td>
              </tr>
              <tr>
                <td><label for="${prefix}spg">SPG#</label></td>
                <td><input ${_i('spg')} class="input-150px"/></td>
              </tr>
              <tr>
                <td><label for="${prefix}dimension">Dimension/Size</label></td>
                <td><input ${_i('dimension')} class="input-150px"/></td>
              </tr>
              <tr>
                <td><label for="${prefix}insert"><sup class="red">*</sup>Insert</label></td>
                <td>
                  <input id="${prefix}insert_yes" ${_r('Y','insert')}/>
                  <label for="${prefix}insert_yes">Yes</label>
                  <input id="${prefix}insert_no" ${_r('N','insert')}/>
                  <label for="${prefix}insert_yes">No</label>
                </td>
              </tr>
              <tr>
                <td valign="top"><label for="${prefix}material"><sup class="red">*</sup>Material</label></td>
                <td>
                  <input id="${prefix}material_e" ${_r('E','material')}/>
                  <label for="${prefix}material_e">350gsm CCNB+E Flute</label></p>
                  <p><input id="${prefix}material_b" ${_r('B','material')}/>
                  <label for="${prefix}material_b">350gsm CCNB + B Flute</label></p>
                  <p><input id="${prefix}material_others" ${_r('others','material')}/>
                  <label for="${prefix}material_other">Other&nbsp;</label>
                  
                   <%
                       material_other_val = _('material_other')
                   %>
                   %if material_other_val :
                       <input type="text" id="material_other_tmp" class="input-300px" value="${material_other_val['SHOW_TEXT']}"  ref='${material_other_val|jd,n}'/>&nbsp;&nbsp;
                       <input ${_h('material_other')} value='${material_other_val|jd,n}'/>
                   %else:
                       <input type="text" id="material_other_tmp" class="input-300px" value='' ref=''/>&nbsp;&nbsp;
                       <input ${_h('material_other')} value=''/>
                   %endif
                  
                </td>
              </tr>
          </table>
  </fieldset>
   <fieldset> 
   		<legend><span class="form-page-1"><sup class="red">*</sup>Submitted Items&nbsp;:</span></legend>
     	<table class='table2' cellspacing="0" cellpadding="0" border="0">
          <tr>
            <td><input id="${prefix}submitted_item_product" ${_c('Product','submitted_item')} class="SFTarget-submitted_item" /></td>
            <td><label for="${prefix}submitted_item_product">Product/Hand Made Sample</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}submitted_item_previous" ${_c('Previous','submitted_item')} class="SFTarget-submitted_item"/></td>
            <td><label for="${prefix}submitted_item_previous">Previous Packaging</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}submitted_item_photos" ${_c('Photos','submitted_item')} class="SFTarget-submitted_item"/></td>
            <td><label for="${prefix}submitted_item_photos">Photos</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}submitted_item_artwork" ${_c('Artwork','submitted_item')} class="SFTarget-submitted_item"/></td>
            <td><label for="${prefix}submitted_item_artwork">Artwork Files</label></td>
          </tr>
          <tr>
            <td><input id="${prefix}submitted_item_others" ${_c('Others','submitted_item')} class="SFTarget-submitted_item"/></td>
            <td><label for="${prefix}submitted_item_other">Others&nbsp;</label>
              <input ${_i('submitted_item_other')} class="input-150px" />
            </td>
          </tr>
      </table>
	</fieldset>	  
    <fieldset>
        <legend><span class="form-page-1">Artwork&nbsp;:</span></legend>
        <table class='table2' cellspacing="0" cellpadding="0" border="0">
        <tr><td><input ${_cid('ftp','file_from')}/>ftp (Location : <input ${_i('file_from_ftp_location')} class="input-150px" />)</td></tr>
        <tr><td><input ${_c('cd','file_from')}/>CD</td></tr>
        <tr><td><input ${_cid('files','file_from')}/>Files (Location : <input ${_i('file_from_files_location')} class="input-150px" />)</td></tr>
        <tr><td><input ${_cid('attachment','file_from')}/>As Per Attachment</td></tr>
        </table>
        <ul class="ul3">
        	<li>
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
	            	<ul class=ul2>
	            		<li>
			                <input ${_c('4color','color')}/>4 Color Processing<br/>
			                <input ${_cid('spot','color')}/>Spot Color
							<ul class=ul2>
			            		<li>
			            			PMS<input ${_i('color_spot_content')} class="input-50px numeric" />
			            		</li>
			               </ul>
			               <input ${_cid('other','color')}/>Other <input ${_i('color_other_content')} class="input-150px" />
	                	</li>
	                </ul>
            </li>
        </ul>
    </fieldset>
	<fieldset> <legend><span class="form-page-1">Requirements&nbsp;:</span></legend>
		<sup class="red">*</sup>Output Die-line/Artwork Format:
    	<ul class="ul2">
    		<li>
    			<table class='table2' cellspacing="0" cellpadding="0" border="0">
    			    <tr>
    			        <td><input id="${prefix}requirement_quote_only" ${_r('quote_only','die')}/>Estimate Flat Size For Quote Only.</td>
    			        <td>&nbsp;</td>
    			    </tr>
    				<tr>
    					<td><input id="${prefix}requirement_quote" ${_r('quote','die')}/>Die-line/Artwork For Quote(Without Fitting)</td>
    					<td>
    						<input id="${prefix}file_format" ${_c('PDF','file_format')}/>
							<label for="${prefix}file_format_pdf">PDF</label>
							<input id="${prefix}file_format_eps" ${_c('EPS','file_format')}/>
							<label for="${prefix}file_format_eps">EPS/AI</label>
							<input id="${prefix}file_format_jpeg" ${_c('JPEG','file_format')}/>
							<label for="${prefix}file_format_jpeg">JPEG</label>
							<input id="${prefix}file_format_ard" ${_c('ARD','file_format')}/>
							<label for="${prefix}file_format_ard">ARD</label>
    					</td>
    				</tr>
    				<tr valign=top>
    					<td><input id="${prefix}requirement_production" ${_r('production','die')}/>Die-line/Artwork For Production</td>
    					<td>
    						<input id="${prefix}file_format2" ${_c('PDF','file_format')}/>
							<label for="${prefix}file_format_pdf">PDF</label>
							<input id="${prefix}file_format_eps2" ${_c('EPS','file_format')}/>
							<label for="${prefix}file_format_eps2">EPS/AI</label>
							<input id="${prefix}file_format_jpeg2" ${_c('JPEG','file_format')}/>
							<label for="${prefix}file_format_jpeg2">JPEG</label>
							<input id="${prefix}file_format_ard2" ${_c('ARD','file_format')}/>
							<label for="${prefix}file_format_ard2">ARD</label>
    					</td>
    				</tr>
    				<tr>
    					<td colspan=2>
    						<ul class=ul3>
								<li>
									With Target Format:
									<input id="${prefix}target_format_y" ${_r('Y','target_format')}/>
									<label for="${prefix}target_format_y">Yes</label>
									<input id="${prefix}target_format_n" ${_r('N','target_format')}/>
									<label for="${prefix}target_format_n">No</label>
									<br/>
									Security File Protection:
									<input id="${prefix}file_protection_y" ${_r('Y','file_protection')}/>
									<label for="${prefix}file_protection_y">Yes</label>
									<input id="${prefix}file_protection_n" ${_r('N','file_protection')}/>
									<label for="${prefix}file_protection_n">No</label>
								</li>
							</ul>
    					</td>
    				</tr>
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