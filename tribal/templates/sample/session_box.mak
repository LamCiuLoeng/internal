<%namespace name="tw" module="tw.core.mako_util"/>
<%page args="prefix,disable,_,_d,_f,_i,_c,_r,_incd"/>

<%
from tribal.util.mako_filter import jd,ue
_h = lambda n, f=lambda t:t : tw.attrs([('type','hidden'),('name',prefix+n),('id',prefix+n)])
%>

<script type="text/javascript" src="/js/json2.js"></script>
<script type="text/javascript" src="/js/custom/sample/material.js?v=2"></script>

<script type="text/javascript">
	$(document).ready(function(){
	       $('.material_widget').material_popup();
	       $('#insert_material_tmp').material_popup({'afterSave' : function(){
	           $("#SFBox-insert_material").val($("#insert_material_tmp").attr("ref"));
	       }});
	
			linkScroll([$("input[name='SFBox-top_locking']"), $("#SFBox-top_locking_other")],
            	                   $("input[name='SFBox-top_closure'][value='RSC'],input[name='SFBox-top_closure'][value='FOL']")
			)
			linkScroll([$("input[name='SFBox-bottom_locking']"), $("#SFBox-bottom_locking_other")],
            	                   $("input[name='SFBox-bottom_closure'][value='SLB'],input[name='SFBox-bottom_closure'][value='Auto'],input[name='SFBox-bottom_closure'][value='RSC'],input[name='SFBox-bottom_closure'][value='FOL'],input[name='SFBox-bottom_closure'][value='Open_Bottom']")
			)
			
			/*
			linkScroll([$('#SFBox-product_w'),$('#SFBox-product_d'),$('#SFBox-product_h'),$("input[name='SFBox-product_unit']"),$("#SFBox-product_weight"),$("#SFBox-product_weight_unit")],
			$("input[name='SFBox-product_weight_as_sample'][value='Y']")
			)
			*/
			
			linkScroll([$('#SFBox-window_size_w'),$('#SFBox-window_size_h'),$("input[name='SFBox-window_size_unit']")],
			$("input[name='SFBox-suggested_by_pd_team']")
			)
				var list = 	[
					 "#SFBox-window_size_w",
					 "#SFBox-window_size_h",
					 "input[name='SFBox-window_size_unit']",
					 "input[name='SFBox-window_with']",
					 "#SFBox-window_with_other_content",
					 "#SFBox-window_with_other_unit",
					 "#SFBox-pvc_thickness",
					 "#SFBox-pet_thickness",
					 "#SFBox-pp_thickness"
					 ]
		
		//lessCheckBox(list)
		
		$("input[name='SFBox-window_type']").click(function(){
					lessCheckBox(list);
					if($(this).val()=='With'){
						workCheckBox($(this),["#SFBox-window_size_w",
											  "#SFBox-window_size_h",
										      "input[name='SFBox-window_size_unit']",
										      "input[name='SFBox-window_with']"]
					 				)
					 }
					 else if($(this).val()=='Open'){
					 	workCheckBox($(this),["#SFBox-window_size_w",
											  "#SFBox-window_size_h",
										      "input[name='SFBox-window_size_unit']"]
					 				)
					 }
					 
					})
		var sc_list = [
					 "#SFBox-pvc_thickness",
					 "#SFBox-pet_thickness",
					 "#SFBox-pp_thickness",
					 "#SFBox-window_with_other_content",
					 "#SFBox-window_with_other_unit"
					 ]		
		$("input[name='SFBox-window_with']").click(function(){
					lessCheckBox(sc_list);
					if($(this).val()=='PVC'){
						workCheckBox($(this),["#SFBox-pvc_thickness"]
					 				)
					 }
					 if($(this).val()=='PET'){
					 	workCheckBox($(this),["#SFBox-pet_thickness"]
					 				)
					 }
					 if($(this).val()=='PP'){
						workCheckBox($(this),["#SFBox-pp_thickness"]
					 				)
					 }
					 if($(this).val()=='Other'){
					 	workCheckBox($(this),["#SFBox-window_with_other_content",
											  "#SFBox-window_with_other_unit"]
					 				)
					 }
					 
					})	
			$("input[name='SFBox-top_closure']").click(function(){
					if($(this).val()=='RSC' || $(this).val()=='FOL'){
						lessCheckBox(["input[name='SFBox-top_locking']","#SFBox-top_locking_other"]);		
					 }
					 else{
					 	workCheckBox($(this),["input[name='SFBox-top_locking']","#SFBox-top_locking_other"])
					 }
					})
			
			$("input[name='SFBox-suggested_by_pd_team']").click(function(){
		 				lessCheckBox2(["#SFBox-window_size_w",
								  "#SFBox-window_size_h",
							      "input[name='SFBox-window_size_unit']"]
		 				)
					})
			
			$("input[name='SFBox-job_perpose'],input[name='SFBox-presentation']").click(function(){
				var name = $(this).attr("name");
				if(name=='SFBox-presentation'){
					lessCheckBox3(["input[name='SFBox-job_perpose']"]);		
				 }
				 else{
				 	lessCheckBox3(["input[name='SFBox-presentation']"]);	
				 }
				})
		})
</script>
<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Job Purpose&nbsp;:</span></legend>
        <input ${_r('Quotation','job_perpose')}/>
            Quotation (Without Size Fitting)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input ${_r('Production','job_perpose')}/>
            Production (With Size Fitting)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input ${_c('Y','presentation')}>
            Presentation
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Product Details&nbsp;:</span></legend>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td>
                    <ul class="ul3">
                        <input ${_r('sample','product_or_box')}>As Sample<br/>
                        <input ${_r('product','product_or_box')}>Product
                            <li>
                            Dimension
                            <input ${_i('product_w')} class="input-50px numeric"/> W &nbsp;
                                <input ${_i('product_d')} class="input-50px numeric"/>D &nbsp;
                                <input ${_i('product_h')} class="input-50px numeric"/>H
                                <input ${_r('mm','product_unit')}/> mm
                                <input ${_r('inch','product_unit')}/> inch<br/>
                            Weight
                            <input ${_i('product_weight')} class="input-100px numeric"/>
                            <select name="${prefix}product_weight_unit" id="${prefix}product_weight_unit" ${_d()} class="input-50px">
                                %for o in ["","gram","kg","lbs","oz"]:
                                <option value="${o}" ${tw.attrs([('selected',o == _('product_weight_unit'))])}>${o}</option>
                                %endfor
                            </select>
                               
                        </li>
                        <input ${_r('box','product_or_box')}/>Box
                            <li>
                            Dimension
                            <input ${_i('box_w')} class="input-50px numeric"/>W &nbsp;
                                <input ${_i('box_d')} class="input-50px numeric"/>D &nbsp;
                                <input ${_i('box_h')} class="input-50px numeric"/>H
                                <input ${_r('mm','box_unit')}/> mm
                                <input ${_r('inch','box_unit')}/> inch<br/>
                            <input ${_r('Inside','box_size')}/> Inside Dimension
                            <input ${_r('Die-line','box_size')}/> Die-line Dimension
                            <input ${_r('Outside','box_size')}/> Outside Dimension
                        </li>
                    </ul>
                </td>
                <td><img width="138" height="165" src="/images/sample/pd-img1.jpg"></td>
                <td><img width="208" height="164" src="/images/sample/pd-img2.jpg"></td>
            </tr>
        </table>
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
        <legend><span class="form-page-1"><sup class="red">*</sup>Box Style&nbsp;:</span></legend>
        <span class="font-content">(as per the attached sketch)</span>
        <table class="table2" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td width="280" height="126">
                    <ul class="ul2">
                        Top Closure :
                        <li>
                            <input ${_r('Standard','top_closure')}/> Standard Slit Lock<br/>
                            <input ${_r('Friction','top_closure')}/> Friction Tuck<br/>
                            <input ${_r('RSC','top_closure')}/> RSC / HSC<br/>
                            <input ${_r('FOL','top_closure')}/> FOL<br/>
                            <input ${_r('Other','top_closure')}/> Other : <input ${_i('top_closure_other')} class="input-100px"/>
                        </li>
                    </ul>
                </td>
                <td width="280">
                    <ul class="ul2">
                        Top Locking :
                        <li>
                            <input ${_r('No','top_locking')}/> No<br/>
                            <input ${_r('Yes','top_locking')}/> Yes, Tongue Lock<br/>
                            <input ${_r('Other','top_locking')}/> Other : <input ${_i('top_locking_other')} class="input-100px"/>
                        </li>
                    </ul>
                </td>
                <td><img width="144" height="126" id="top_closure" src="/images/blank.png"></td>
            </tr>
            <tr><td height="30">&nbsp;</td><td>&nbsp;</td></tr>
            <tr>
                <td>
                    <ul class="ul2">
                        Bottom Closure :
                        <li>
                            <input ${_r('Standard','bottom_closure')}/> Standard Slit Lock<br/>
                            <input ${_r('Friction','bottom_closure')}/> Friction Tuck<br/>
                            <input ${_r('SLB','bottom_closure')}/> SLB (1-2-3 Snap Lock Bottom)<br/>
                            <input ${_r('Auto','bottom_closure')}/> Auto lock (Need To Glue In Production)<br/>
                            <input ${_r('RSC','bottom_closure')}/> RSC<br/>
                            <input ${_r('FOL','bottom_closure')}/> FOL<br/>
                            <input ${_r('Open_Bottom','bottom_closure')}/> Open Bottom<br/>
                            <input ${_r('Other','bottom_closure')}/> Other : <input ${_i('bottom_closure_other')} class="input-100px"/>
                        </li>
                    </ul>
                </td>
                <td>
                    <ul class="ul2">
                        Bottom Locking :
                        <li>
                            <input ${_r('No','bottom_locking')}/>No<br/>
                            <input ${_r('Yes','bottom_locking')}/>Yes, Tongue Lock<br/>
                            <input ${_r('Other','bottom_locking')}/> Other : <input ${_i('bottom_locking_other')} class="input-100px"/>
                        </li>
                    </ul>
                </td>
                <td>
                    <img width="144" height="126" id="bottom_closure" src="/images/blank.png">
                </td>
            </tr>
        </table>
        Insert :&nbsp;&nbsp;&nbsp;&nbsp;
        <input ${_r('No','insert')}/> No&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input ${_r('Yes','insert')}/> Yes, (Material:
            
            <%
                insert_material_val = _('insert_material')
            %>
            
            %if insert_material_val :
                <input type="text" id="insert_material_tmp" class="input-300px" value="${insert_material_val['SHOW_TEXT']}"  ref='${insert_material_val|jd,n}'/>)
                <input ${_h('insert_material')} value='${insert_material_val|jd,n}'/>
            %else:
                <input type="text" id="insert_material_tmp" class="input-300px" value=""  ref=''/>)
                <input ${_h('insert_material')} value=''/>
            %endif
            
            <table class="table2" cellspacing="0" cellpadding="0" border="0">
            <tr>
                <td><input ${_r('Top','loading')}/> Top Loading&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                <td><input ${_r('Side','loading')}/> Side Loading</td>
                <td><input ${_r('Any','loading')}/> Any</td>
            </tr>
            <tr>
                <td><input ${_r('No','window_type')}/> No Window</td>
                <td><input ${_r('Open','window_type')}/> Open Window&nbsp;&nbsp;&nbsp;&nbsp;</td>
                <td><input ${_r('With','window_type')}/> Window With</td>
            </tr>
            <tr>
                <td>&nbsp;</td>
                <td>&nbsp;</td>
                <td>
                    <ul class="ul2">
                        <li>
                            <input ${_r('PVC','window_with')}/> PVC&nbsp;&nbsp;&nbsp;&nbsp;(Thickness:<input ${_i('pvc_thickness')} class="input-100px"/> mm)<br/>
                            <input ${_r('PET','window_with')}/> PET&nbsp;&nbsp;&nbsp;&nbsp;(Thickness:<input ${_i('pet_thickness')} class="input-100px"/> mm)<br/>
                            <input ${_r('PP','window_with')}/> PP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Thickness:<input ${_i('pp_thickness')} class="input-100px"/> mm)<br />
                            <input ${_r('Other','window_with')}/> Other <input ${_i('window_with_other_content')} class="input-100px"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Thickness:<input ${_i('window_with_other_unit')} class="input-100px"/> mm)
                        </li>
                    </ul>
                </td>
            </tr>
        </table>
        Window Size:
        <input ${_i('window_size_w')} class="input-100px numeric"/> W 
            <input ${_i('window_size_h')} class="input-100px numeric"/> H
            <input ${_r('mm','window_size_unit')}/>mm
            <input ${_r('inch','window_size_unit')}/>inch &nbsp;
            <input ${_r('Suggested','suggested_by_pd_team')}/>Suggested By PD Team 
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
        <input ${_i('expected_date',_f)} class="datePicker input-150px"/>
    </fieldset>
</div>