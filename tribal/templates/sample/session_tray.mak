<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>

<%
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>

<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/material.js?v=2"></script>

<script type="text/javascript">
var changeStyleImg=function(){
	var obj = $("input[name='SFTray-style']:checked").val()
	if(!obj)
		$("#changeImg").html("");
	else
		$("#changeImg").html("<img src="+ (obj=='Flat' ? "/images/sample/Flat_Tray.jpg" : "/images/sample/PDQ.jpg") +" height='110'>");
}
	$(document).ready(function(){
	    $('.material_widget').material_popup();
	    
		linkScroll([$("#SFTray-product_dimension_w"),
			$("#SFTray-product_dimension_d"),
			$("#SFTray-product_dimension_h"),
			$("#SFTray-product_dimension_unit_mm"),
			$("#SFTray-product_dimension_inch")],
			$("input[name='SFTray-product_dimension_as_sample'][value='Y']")
			)
		linkScroll([$("#SFTray-weight"),
			$("#SFTray-product_weight_unit")],
			$("input[name='SFTray-product_weight_as_sample'][value='Y']")
			)
		changeStyleImg()
		$("input[name='SFTray-style']").click(function(){
			changeStyleImg();
		})
		var list = 	[
					 "#SFTray-product_dimension_w",
					 "#SFTray-product_dimension_d",
					 "#SFTray-product_dimension_h",
					 "#SFTray-product_dimension_unit_mm",
					 "#SFTray-product_dimension_unit_inch",
					 "#SFTray-product_weight_unit",
					 "#SFTray-tray_pack_left",
					 "#SFTray-tray_pack_front",
					 "#SFTray-tray_pack_top",
					 "#SFTray-tray_dimension_w",
					 "#SFTray-tray_dimension_d",
					 "#SFTray-tray_dimension_bh",
					 "#SFTray-product_specified_tray_mm",
					 "#SFTray-product_specified_tray_inch",
					 "#SFTray-material_other",
					 "#SFTray-paper_thickness",
					 "#SFTray-flute",
					 "#SFTray-weight",
					 "#SFTray-flute_type_gsm",
					 "#SFTray-bursting",
					 "#SFTray-ect",
					 "#SFTray-gramage",
					 "#SFTray-paper_thicknesss_type_cards",
					 "#SFTray-paper_thicknesss",
					 "#SFTray-paper_gramage",
					 "#SFTray-flute_type_corrugated",
					 "#SFTray-material_ccnb",
					 "#SFTray-material_c1s",
					 "#SFTray-material_c2s",
					 "#SFTray-material_others",
					 "#SFTray-paper_thickness",
					 "#SFTray-paper_thickness_unit_pt",
					 "#SFTray-paper_thickness_unit_mm",
					 "#SFTray-gramage",
					 "#SFTray-flute",
					 "#SFTray-bursting",
					 "#SFTray-ect",
					 "#SFTray-gramage_input",
					 "#SFTray-flute_type1_kraft_top",
					 "#SFTray-flute_type1_mottle_white_top",
					 "#SFTray-flute_type_ccnb",
					 "#SFTray-specification_burst_bursting",
					 "#SFTray-specification_burst_ect",
					 "#SFTray-product_dimension_inch",
					 "input[name='SFTray-product_dimension_as_sample']",
					 "input[name='SFTray-product_weight_as_sample']",
					 "input[name='SFTray-box_size']",
					 "#SFTray-gramages",
					 "#SFTray-tray_detail_pcs",
					 "#SFTray-tray_detail_thickness",
					 "#SFTray-shipper_other_content"
					 ]
		
		//lessCheckBox(list)
		var product_dimension_list1 = [
										"#SFTray-product_dimension_w",
										"#SFTray-product_dimension_d",
										"#SFTray-product_dimension_h",
										"#SFTray-product_dimension_unit_mm",
										"#SFTray-product_dimension_inch",
										"#SFTray-product_dimension_unit_inch",
										"#SFTray-weight",
										"#SFTray-product_weight_unit",
										"input[name='SFTray-product_dimension_as_sample']",
										"input[name='SFTray-product_weight_as_sample']"
										]
		var product_dimension_list2 = 	[
										"#SFTray-tray_pack_left",
										"#SFTray-tray_pack_front",
										"#SFTray-tray_pack_top"
										]
		var product_dimension_list3 =   [
										"#SFTray-tray_dimension_w",
										"#SFTray-tray_dimension_d",
										"#SFTray-tray_dimension_bh",
										"#SFTray-product_specified_tray_mm",
										"#SFTray-product_specified_tray_inch",
										"#SFTray-tray_dimension_fh",
										"input[name='SFTray-box_size']"
										]
		var product_dimension_list = product_dimension_list1.concat(product_dimension_list2,product_dimension_list3)
		
		$("#SFTray-product_dimension_type_according").click(function(){
					lessCheckBox(product_dimension_list1)
		})
		$("#SFTray-product_dimension_type_product_size").click(function(){
					lessCheckBox(product_dimension_list1)
		})
		
		
		$("#SFTray-product_dimension_type_option").click(function(){
					lessCheckBox(product_dimension_list1)
					workCheckBox($(this),["#SFTray-product_dimension_option_text"])
		})
		$("#SFTray-product_dimension_type_detail").click(function(){
					//lessCheckBox(product_dimension_list1)
					lessCheckBox(["#SFTray-product_dimension_option_text"])
					workCheckBox($(this),product_dimension_list1)
		})
		
		
		$("#SFTray-product_dimension_type_pack").click(function(){
					lessCheckBox(product_dimension_list3)
					workCheckBox($(this),product_dimension_list2)
		})
		$("#SFTray-product_dimension_type_specified").click(function(){
					lessCheckBox(product_dimension_list2)
					workCheckBox($(this),product_dimension_list3)
		})

		
		$("#SFTray-detail_Dividers").click(function(){
					workCheckBox($(this),[
										"#SFTray-tray_detail_pcs"
										])
		})
		$("#SFTray-detail_Thick").click(function(){
					workCheckBox($(this),[
										"#SFTray-tray_detail_thickness"
										])
		})

		$("input[name='SFTray-shipper']").click(function(){
					if($(this).val()=='Other'){
						workCheckBox($(this),[
										"#SFTray-shipper_other_content"
										])
					}
					else{
						lessCheckBox([
										"#SFTray-shipper_other_content"
										])
						}
		})

		$("input[name='SFTray-job_purpose'],input[name='SFTray-presentation']").click(function(){
				var name = $(this).attr("name");
				if(name=='SFTray-presentation'){
					lessCheckBox3(["input[name='SFTray-job_purpose']"]);		
				 }
				 else{
				 	lessCheckBox3(["input[name='SFTray-presentation']"]);	
				 }
				})
		
	})
</script>
<div class=div1>
	<fieldset>
		<legend><span class="form-page-1"><sup class="red">*</sup>Job Purpose&nbsp;:</span></legend>
		<input id="${prefix}job_purpose_q" ${_r('Quotation','job_purpose')}/>Quotation(Without Size Fitting)&nbsp;&nbsp;&nbsp;&nbsp;
		<input id="${prefix}job_purpose_p" ${_r('Production','job_purpose')}/>Production(With Size Fitting)&nbsp;&nbsp;&nbsp;&nbsp;
		<input id="${prefix}presentation" ${_c('Y','presentation')}/>Presentation
	</fieldset>
	<fieldset style='line-height:22px;'>
		<legend><span class="form-page-1"><sup class="red">*</sup>Product Details&nbsp;:</span></legend>
		<input ${_r('option','product_dimension_type')} id="${prefix}product_dimension_type_option"/>Refer to Packaging Option&nbsp;<input ${_i('product_dimension_option_text')} class="input-100px"/><br />
		<input ${_r('detail','product_dimension_type')} id="${prefix}product_dimension_type_detail"/>Product Dimension
		<input ${_i('product_dimension_w')} class="numeric input-50px"/>W &nbsp;
		<input ${_i('product_dimension_d')} class="numeric input-50px"/>D &nbsp;
		<input ${_i('product_dimension_h')} class="numeric input-50px"/>H
		<input ${_r('mm','product_dimension_unit')} id="${prefix}product_dimension_unit_mm"/>mm&nbsp;
		<input ${_r('inch','product_dimension_unit')} id="${prefix}product_dimension_inch"/>inch 
		<input ${_c('Y','product_dimension_as_sample')} /> As Sample<br />
		<ul class=ul2>
      		<li>
      			Product Weight
      			<input ${_i('weight')} class="numeric input-100px"/>&nbsp;&nbsp;
        		<select name="${prefix}weight_unit" id="${prefix}weight_unit" ${_d()} class="input-50px">
            		%for o in ["","gram","kg","lbs","oz"]:
            		<option value="${o}" ${tw.attrs([('selected',o == _('weight_unit'))])}>${o}</option>
            		%endfor
        		</select>&nbsp;&nbsp;
        		<input ${_c('Y','product_weight_as_sample')} /> As Sample
      		</li>
      	</ul>
      	<!-- <input ${_r('according','product_dimension_type')} id="${prefix}product_dimension_type_according"/>Size According To The New Design With This Request<br/> -->
      	<input ${_r('product_size','product_dimension_type')} id="${prefix}product_dimension_type_product_size"/>No Product Size Reference, Just According To The Tray Size
    </fieldset>
	<fieldset style='line-height:22px;'>
		<legend><span class="form-page-1"><sup class="red">*</sup>Tray Size&nbsp;:</span></legend>
		<input ${_r('dimension','product_tray_size')} id="${prefix}product_dimension_type_specified" />Specified Tray Size: 
		<ul class="ul3">
			<li>
				Dimension
				<input ${_i('tray_dimension_w')} class="numeric input-50px"/>W &nbsp;
				<input ${_i('tray_dimension_d')} class="numeric input-50px"/>D &nbsp;
				<input ${_i('tray_dimension_fh')} class="numeric input-50px"/>FH&nbsp;
				<input ${_i('tray_dimension_bh')} class="numeric input-50px"/>BH
				<input ${_r('mm','tray_size_unit')} id="${prefix}product_specified_tray_mm" />mm&nbsp;
				<input ${_r('inch','tray_size_unit')} id="${prefix}product_specified_tray_inch" />inch
				<br/>
				<input ${_r('Inside','box_size')}/> Inside Dimension
				<input ${_r('Die-line','box_size')}/> Die-line Dimension
				<input ${_r('Outside','box_size')}/> Outside Dimension
			</li>
		</ul>
		<input ${_r('according','product_tray_size')} id="${prefix}product_dimension_type_pack" />Tray Size According To Pack Count:
		<ul class=ul3>
			<li><input ${_i('tray_pack_left')} class="numeric input-100px"/>pcs Left To Right</li>
			<li><input ${_i('tray_pack_front')} class="numeric input-100px"/>pcs Front To Back</li>
			<li><input ${_i('tray_pack_top')} class="numeric input-100px"/>pcs Top To Bottom</li>
		</ul>
	</fieldset>
	
	
  <fieldset>
      <legend><span class="form-page-1"><sup class="red">*</sup>Material </span></legend>
      
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
                  <td width="350"><input type="text" class="material_widget input-300px" value="" ref=''/></td>
              </tr>
          </table>
          <input ${_h('material_widgets')} value='${_("material_widgets")|jd,n}'/>
      %endif
    </fieldset>
    
    
  <fieldset>
	<legend><span class="form-page-1">Tray Style&nbsp;:</span></legend>
		<table cellspacing="0" cellpadding="0" border="0" class="table2">
			<tr>
				<td class=title-page-1><sup class="red">*</sup>Stackable</td>
				<td>
					<input ${_r('Y','stackable')}/>Yes&nbsp;&nbsp;
					<input ${_r('N','stackable')}/>No
				</td>
				<td rowspan="4" id='changeImg' style='padding-left:20px;'></td>
			</tr>
			<tr>
				<td class=title-page-1><sup class="red">*</sup>Style</td>
				<td>
					<input ${_r('Flat','style')}/>Flat Tray
					<input ${_r('PDQ','style')}/>PDQ
				</td>
			</tr>
			<tr>
				<td valign=top class=title-page-1>Details</td>
				<td>
					<input ${_c('Inserts','tray_detail')}/>Inserts&nbsp;&nbsp;
					<input ${_c('Dividers','tray_detail')} id='${prefix}detail_Dividers'/>Dividers,
					<input ${_i('tray_detail_pcs')} class="numeric input-100px"/>pcs ,
					<input ${_c('slope_side_panel','tray_detail')} id='${prefix}detail_Slope_Side_Panel'/>Filler, 
					<input ${_c('platform','tray_detail')} id='${prefix}detail_platform'/>Platform, 
					<input ${_c('hook','tray_detail')} id='${prefix}detail_hook'/>Hook(s)/Peg(s)&nbsp;
					<input ${_i('tray_detail_hook_qty')} class="input-50px numeric"/>&nbsp;pcs
					<br/>
					<input ${_c('Handles','tray_detail')}/>Handles&nbsp;&nbsp;
					<input ${_c('Thick','tray_detail')} id='${prefix}detail_Thick'/>Thick Side Wall, Thickness:
					<input ${_i('tray_detail_thickness')} class="input-50px"/><input ${_r('mm','tray_detail_thickness_unit')} id="${prefix}detail_thickness_unit_mm"/> mm&nbsp;
					<input ${_r('inch','tray_detail_thickness_unit')} id="${prefix}detail_thickness_unit_inch"/>inch
				</td>
			</tr>
			<tr>
				<td class=title-page-1><sup class="red">*</sup>Shipper</td>
				<td>
					<input ${_r('HSC','shipper')}/>HSC
					<input ${_r('RSC','shipper')}/>RSC
					<input ${_r('FOL','shipper')}/>FOL
					<input ${_r('No','shipper')}/>No Shipper
					<input ${_r('Other','shipper')} id='${prefix}shipper_other'/>Other
					<input ${_i('shipper_other_content')} class="input-50px"/>
				</td>
			</tr>
			<tr>
			    <td class=title-page-1>Shipper Loading</td>
			    <td>
			        <input ${_r('Top','shipper_loading')}/>Top Loading
			        <input ${_r('Side','shipper_loading')}/>Side Loading
			        <input ${_r('Any','shipper_loading')}/>Any
			    </td>
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
    <fieldset><legend><span class="form-page-1"><sup class="red">*</sup>Expected Date&nbsp;:</span></legend>
  <ul class="form-ul">
    <li><input ${_i('expected_date',_f)} class="datePicker input-150px"/></li>
  </ul>
  </fieldset>
</div>