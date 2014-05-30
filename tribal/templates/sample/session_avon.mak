<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_cid,_r,_incd"/>
<%
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>
<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/material.js?v=2"></script>
<script type="text/javascript">
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
$(document).ready(function(){
	$('.material_widget').material_popup();
})
</script>
<div class="div1">
    PP#<input ${_i('pp_no')} class="input-150px" />
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Design Category&nbsp;:</span></legend>
        <input ${_c('Insert','category')}/>Insert&nbsp;
        <input ${_c('Bubble','category')}/>Bubble Bag&nbsp;
        <input ${_c('Polybag','category')}/>Polybag&nbsp;
        <input ${_cid('GB','category')}/>Gift Box&nbsp;
        <input ${_cid('MP','category')}/>Master Packer&nbsp;
        <input ${_cid('Artwork','category')}/>Artwork&nbsp;
        <input ${_cid('Barcode','category')}/>Barcode Label
    </fieldset>

    <fieldset class='fset_dc4'>
      <legend><span class="form-page-1">Material </span></legend>
      
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
                      <td width="350"><input type="text" class="material_widget input-300px" value="${widget['SHOW_TEXT']|ue, h}" ref='${widget|jd,n}' ${ tw.attrs([('disabled',disable)]) }/></td>
                  </tr>
              %endfor
              <tr>
                  <td width="35">
                      <img title="Add" src="/images/plus.gif" onclick="add_material('material_ul')"/>
                      %if len(_('material_widgets')) >0:
                          <img title="Delete" src="/images/minus.gif" onclick="remove_material(this)"/></td>
                      %endif
                  </td>
                  <td width="350"><input type="text" class="material_widget input-300px" value="" ref=''/></td>
              </tr>
          </table>
          <input ${_h('material_widgets')} value='${_("material_widgets")|jd,n}'/>
      %endif
    </fieldset>
    
    
    <fieldset class='fset_dc4'>
        <legend><span class="form-page-1">Submitted Items&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td>Sample Reference:</td>
                <td><input ${_r('Y','sample')}/> Yes
                    <input ${_r('N','sample')}/> No
                </td>
            </tr>
            <tr>
                <td>Artworks:</td>
                <td><input ${_r('Y','artwork')}/> Yes
                    <input ${_r('N','artwork')}/> No
                </td>
            </tr>
        </table>
    </fieldset>
    <fieldset class='fset_dc4'>
        <legend><span class="form-page-1">Dimension&nbsp;:</span></legend>
        <table>
        	<tr>
        		<td><input ${_r('product','dimension_type')}/>&nbsp;Product Dimension:</td>
        		<td>
        			<input ${_i('product_width')} class="input-100px numeric" />&nbsp;Width&nbsp;
		            <input ${_i('product_depth')} class="input-100px numeric" />&nbsp;Depth&nbsp;
		            <input ${_i('product_height')} class="input-100px numeric" />&nbsp;Height&nbsp;
		            <input ${_r('mm','product_unit')}/>&nbsp;mm
		            <input ${_r('inch','product_unit')}/>&nbsp;inch
		            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input ${_c('Y','product_as_sample')}/>&nbsp;As Sample<br/>
        		</td>
        	</tr>
        	<tr>
        		<td><input ${_r('styrofoam','dimension_type')}/>&nbsp;Styrofoam Dimension:</td>
        		<td>
        			<input ${_i('dimension_width')} class="input-100px numeric" />&nbsp;Width&nbsp;
		            <input ${_i('dimension_depth')} class="input-100px numeric" />&nbsp;Depth&nbsp;
		            <input ${_i('dimension_height')} class="input-100px numeric"/>&nbsp;Height&nbsp;
		            <input ${_r('mm','dimension_unit')}/>&nbsp;mm
		            <input ${_r('inch','dimension_unit')}/>&nbsp;inch
		            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input ${_c('Y','dimension_as_sample')}/>&nbsp;As Sample<br/>
        		</td>
        	</tr>
        	<tr valign=top>
        		<td><input ${_r('box','dimension_type')}/>&nbsp;Box Dimension:</td>
        		<td>
        			<table class="table2" cellspacing="0" cellpadding="0" border="0">
			            <tr>
			                <td>
			                    <input ${_i('box_width')} class="input-100px numeric" />&nbsp;Width&nbsp;
			                        <input ${_i('box_depth')} class="input-100px numeric" />&nbsp;Depth&nbsp;
			                        <input ${_i('box_height')} class="input-100px numeric"/>&nbsp;Height&nbsp;
			                        <input ${_r('mm','box_unit')}/>&nbsp;mm
			                        <input ${_r('inch','box_unit')}/>&nbsp;inch
			                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input ${_c('Y','box_as_sample')}/>&nbsp;As Sample
			                </td>
			            </tr>
			            <tr>
			                <td>
			                    <input ${_r('Inside','box_size')}/> Inside Dimension
			                        <input ${_r('Die-line','box_size')}/> Die-line Dimension
			                        <input ${_r('Outside','box_size')}/> Outside Dimension
			                </td>
			            </tr>
			        </table>
			    </td>
        	</tr>
        </table>
    </fieldset>
    <fieldset class='fset_dc4'>
        <legend><span class="form-page-1">Product Weight&nbsp;:</span></legend>
            <input ${_i('product_weight')} class="input-100px numeric" />
            &nbsp;&nbsp;<select name="${prefix}product_weight_unit" id="${prefix}product_weight_unit" ${_d()} class="input-50px">
                %for o in ["","gram","kg","lbs","oz"]:
                <option value="${o}" ${tw.attrs([('selected',o == _('product_weight_unit'))])}>${o}</option>
                %endfor
            </select>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input ${_c('Y','product_weight_as_sample')}/>&nbsp;As Sample
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1">Top &amp; Bottom Closure&nbsp;:</span></legend>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td><input ${_r('Bottom','top')}/></td>
                <td>French Tuck Top &amp; Bottom</td>
                <td><input ${_r('123Bottom','top')}/></td>
                <td>French Tuck Top &amp; 123 Bottom</td>
            </tr>
            <tr>
                <td><input ${_r('No','top')}/></td>
                <td>No Top &amp; Bottom</td>
                <td><input ${_r('Other','top')}/></td>
                <td>Other&nbsp;<input ${_i('top_other')} class="input-150px" /></td>
            </tr>
        </table>
    </fieldset>
    <fieldset id='fset_mp'>
        <legend><span class="form-page-1">Master Packer&nbsp;:</span></legend>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td valign="top" width="160">Specified Master Packer Size:</td>
                <td>
                    <input ${_i('mp_width')} class="input-100px numeric" /> Width
                    <input ${_i('mp_depth')} class="input-100px numeric" /> Depth
                    <input ${_i('mp_height')} class="input-100px numeric" /> Height
                    <input ${_r('mm','mp_unit')}/>&nbsp;mm
                    <input ${_r('inch','mp_unit')}/>&nbsp;inch<br/>
                    <input ${_r('Inside','mp_size')}/> Inside Dimension
                    <input ${_r('Die-line','mp_size')}/> Die-line Dimension
                    <input ${_r('Outside','mp_size')}/> Outside Dimension
                </td>
            </tr>
            <tr valign="top">
                <td>Quantity:</td>
                <td>
                	<table class="table2" cellspacing="0" cellpadding="0" border="0">
                		<tr valign="top">
                			<td><input ${_c('Max','quantity')}/> Max</td>
                			<td><input ${_cid('Fixed','quantity')}/> Fixed Quantity</td>
                			<td>
                				<ul class='ul1'>
                					<li>
                						<input ${_i('quantity_pcs')} class="input-100px"/>
            						</li>
                				</ul>
            				</td>
                		</tr>
                	</table>
                </td>
            </tr>
            <tr>
                <td>Country:</td>
                <td>
                    <input ${_r('USA','country')}/> USA
                    <input ${_r('CAN','country')}/> CAN
                    <input ${_r('Both','country')}/> USA &amp; CAN
                    <input ${_r('Other','country')}/> Other <input ${_i('country_other')} class="input-150px" />
                </td>
            </tr>
            <tr>
                <td>Product Orientation:</td>
                <td>
                    <table class="table2" cellspacing="0" cellpadding="0" border="0">
                        <tr>
                            <td><input ${_r('Top','product')}/></td>
                            <td>Top &amp; Bottom Side Up</td>
                            <td width="10">&nbsp;</td>
                            <td><input ${_r('Left','product')}/></td>
                            <td>Left &amp; Right Side Up</td>
                        </tr>
                        <tr>
                            <td><input ${_r('Front','product')}/></td>
                            <td>Front &amp; Back Side Up</td>
                            <td>&nbsp;</td>
                            <td><input ${_r('Any','product')}/></td>
                            <td>Any</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </fieldset>

    <fieldset>
        <legend><span class="form-page-1">Design Criteria&nbsp;:</span></legend>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td><input ${_c('Low','design_criteria')}/></td>
                <td>Basic Design</td>
                <td width="10">&nbsp;</td>
                <td><input ${_c('High','design_criteria')}/></td>
                <td>Fancy Design</td>
            </tr>
            <tr>
                <td><input ${_c('Specified','design_criteria')}/></td>
                <td>Specified As Sample Provided</td>
                <td>&nbsp;</td>
                <td><input ${_c('Pass','design_criteria')}/></td>
                <td>Pass Drop Test</td>
            </tr>
        </table>
    </fieldset>

    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Artwork & Barcode Label&nbsp;:</span></legend>
        <span class='title-page-1'>Files From:</span>
        <ul class='ul2 fset_artwork_barcode'>
        	<li>
        		<input ${_cid('ftp','artwork_file_from')}/> FTP (Location : <input ${_i('artwork_file_from_ftp_location')} class="input-600px" />)<br/>
		        <input ${_c('cd','artwork_file_from')}/> CD<br/>
		        <input ${_cid('files','artwork_file_from')}/> Files (Location : <input ${_i('artwork_file_from_files_location')} class="input-600px" />)<br/>
		        <input ${_cid('attachment','artwork_file_from')}/> As Per Attachment
        	</li>
        </ul>
        <span class='title-page-1'>Artwork Info:</span>
        <ul class='ul2 fset_artwork'>
        	<li>
	        	Factory Code(Artwork)
	            <select name="${prefix}artwork_factory_code" id="${prefix}artwork_factory_code" ${_d()} class="input-150px">
	                %for o in ["","Advance Label - 0013","AG GIGI - 0152","Morning Sun - 0019","Great Shengda (GSD) - 0195","Hangzhou Zezhong - 0168","Kunshan Printec - 0018","Parksons Printing - 0069","Precision Print - 0012","Safe Power - 0120","Sedele (SDL) - 0071","Tophand - 0121","Suteng - 0142","Sun Hing - 0009","DMS - 0126"]:
	                <option value="${o}" ${tw.attrs([('selected',o == _('artwork_factory_code'))])}>${o}</option>
	                %endfor
	            </select><br/>
	            Size&nbsp;:
	            <input ${_i('artwork_size_w')} class="input-100px numeric" />&nbsp;W 
	            <input ${_i('artwork_size_h')} class="input-100px numeric" />&nbsp;H
	            <input ${_r('mm','artwork_size_unit')}/>mm
	            <input ${_r('inch','artwork_size_unit')}/>inch<br/>
	            Color:
	            <ul class='ul2'>
		            <li>
		                <input ${_c('4color','artwork_color')}/> 4 Color Processing<br/>
		                <input ${_cid('spot','artwork_color')}/> Spot Color:
		            	<ul>
		            		<li>
		            			PMS<input ${_i('artwork_color_spot_content')} class="input-50px numeric" />
		            		</li>
		            	</ul>
		                <input ${_cid('other','artwork_color')}/> Other <input ${_i('artwork_color_other_content')} class="input-150px" />
		            </li>
	            </ul>
            </li>
        </ul>
        <span class='title-page-1'>Barcode Label Info:</span>
        <ul class='ul2 fset_barcode'>
        	<li>
				<table class="table2" cellspacing="0" cellpadding="0" border="0">
				    <tr>
				        <td>Size</td>
				        <td>
				            <input ${_i('label_size_w')} class="input-100px numeric"/>&nbsp;W 
				            <input ${_i('label_size_h')} class="input-100px numeric" />&nbsp;H
				            <input ${_r('mm','label_size_unit')}/>mm
				            <input ${_r('inch','label_size_unit')}/>inch
				        </td>
				        <td rowspan="9" id='dis_barcode'></td>
				    </tr>
				    <tr>
				        <td>Material</td>
				        <td><input ${_i('label_material')} class="input-150px" /></td>
				    </tr>
				    <tr>
				        <td>Country</td>
				        <td><input ${_i('label_country')} class="input-150px" /></td>
				    </tr>
				    <tr>
				        <td>Item Code&nbsp;</td>
				        <td><input ${_i('label_item_code')} class="input-150px" /></td>
				    </tr>
				    <tr>
				        <td>Item Name&nbsp;</td>
				        <td><input ${_i('label_item_name')} class="input-150px" /></td>
				    </tr>
				    <tr>
				        <td><sup class="red">*</sup>Bar Code No. &amp Type&nbsp;</td>
				        <td>
				        	<select name="${prefix}label_barcode" id="${prefix}label_barcode" ${_d()} class="input-150px" onchange='changeBarcode(this)'>
				                %for o in ["","Code 128 (General)","Code 128 (Code A)","Code 128 (Code B)","Code 128 (Code C)",'Code 39','Code 93','EAN-13','EAN-8','UCC/EAN-128','UPC(A)','UPC(E) (11-Digit Input)','UPC(E) (6-Digit Input)']:
				                <option value="${o}" ${tw.attrs([('selected',o == _('label_barcode'))])}>${o}</option>
				                %endfor
				            </select>
				    </tr>
				    <tr>
				        <td>Font Request&nbsp;</td>
				        <td><input ${_i('label_font')} class="input-150px" /></td>
				    </tr>
				    <tr>
				        <td>Others&nbsp;</td>
				        <td><input ${_i('label_content_other')} class="input-150px" /></td>
				    </tr>
				    <tr>
				        <td><sup class="red">*</sup>Print&nbsp;</td>
				        <td>
				            <input ${_r('color','label_color')}/>Color
				            <input ${_r('Black','label_color')}/>Black
				            <input ${_r('Others','label_color')}/>Other&nbsp;<input ${_i('label_color_other')} class="input-150px" />
				        </td>
				    </tr>
				</table>
        	</li>
        </ul>
        <span class='title-page-1'>Output:</span>
        <ul class='ul2 fset_artwork_barcode'>
        	<li>
        		<input ${_cid('pdf','artwork_output')}/> PDF &nbsp;&nbsp; Security File Protction <input ${_r('YES','artwork_protection')}/> Yes <input ${_r('NO','artwork_protection')}/> No <br/>
		        <input ${_c('ai','artwork_output')}/> AI<br/>
		        <input ${_c('eps','artwork_output')}/> EPS<br/>
		        <input ${_c('jpg','artwork_output')}/> JPG<br/>
		        <input ${_cid('other','artwork_output')}> Other <input ${_i('artwork_output_other_content')} class="input-150px" />
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
        <input ${_i('expected_date',_f)} class="input-150px datePicker"/>
    </fieldset>
</div>