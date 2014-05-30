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
        $("#material_tmp").material_popup({'afterSave' : function(){
           $("#SFBestBuy-material").val($("#material_tmp").attr("ref"));
        }});

		linkScroll([$('#SFBestBuy-size_w'), $('#SFBestBuy-size_d'), $('#SFBestBuy-size_h'), $("input[name='SFBestBuy-size_unit']"), $("input[name='SFBestBuy-size_type']")],$("input[name='SFBestBuy-size_as_sample']"))
		linkScroll([$('#SFBestBuy-weight'), $("#SFBestBuy-weight_unit")],$("input[name='SFBestBuy-weight_as_sample']"))
		linkScroll([$('#SFBestBuy-material')],$("input[name='SFBestBuy-material_as_sample']"))	
			})
</script>
<div class="div1">
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Job Purpose&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2" width="100%">
            <tr>
                <td width='33%'><input ${_r('quotation','job_purpose')}/>Quotation(Without Size Fitting)</td>
                <td width='34%'><input ${_r('production','job_purpose')}/>Production(With Size Fitting)</td>
                <td width='33%'><input ${_c('presentation','job_presentation')}/>Presentation</td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Submitted Items&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td><input ${_c('Product','submit_items')}/>Product / Prototype</td>
                <td width="30">&nbsp;</td>
                <td><input ${_c('Photos','submit_items')}/>Photos</td>
            </tr>
            <tr>
                <td><input ${_c('Previous','submit_items')}/>Previous Packaging</td>
                <td width="30">&nbsp;</td>
                <td><input ${_c('Artworks','submit_items')}/>Artworks</td>
            </tr>
            <tr>
                <td><input ${_c('Mock','submit_items')}/>Mock Up</td>
                <td width="30">&nbsp;</td>
                <td><input ${_c('Die','submit_items')}/>Die-Line</td>
            </tr>
            <tr>
                <td><input id="${prefix}submit_items_other_type" ${_c('Others','submit_items')} />Others <input class="input-150px" ${_i('submit_items_other')}/></td>
                <td width="30">&nbsp;</td>
                <td></td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Product & Packaging Details&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td>
                	Size&nbsp;<input ${_i('size_w')} class="input-100px numeric"/>&nbsp;
                    W&nbsp;<input ${_i('size_d')} class="input-100px numeric"/>&nbsp;
                    D&nbsp;<input ${_i('size_h')} class="input-100px numeric"/>&nbsp;
                    H&nbsp;
                    <input ${_r('mm','size_unit')}/>&nbsp;mm&nbsp;
                    <input ${_r('inch','size_unit')}/>&nbsp;inch&nbsp;<br />
                    <input ${_r('Product','size_type')}/>&nbsp;Product Size&nbsp;
                        <input ${_r('Packaging','size_type')}/>&nbsp;Packaging Size&nbsp;
                        <input ${_c('Y','size_as_sample')}/>&nbsp;As Sample
                </td>
            </tr>
            <tr>
                <td>Packaging Weight <input ${_i('weight')} class="input-150px"/>&nbsp;&nbsp;
                        <select name="${prefix}weight_unit" id="${prefix}weight_unit" ${_d()} class="input-50px">
                            %for o in ["","gram","kg","lbs","oz"]:
                            <option value="${o}" ${tw.attrs([('selected',o == _('weight_unit'))])}>${o}</option>
                            %endfor
                        </select>
                        <input ${_c('Y','weight_as_sample')}/>&nbsp;As Sample
                </td>
            </tr>
            <tr>
                <td>Packaging Material 
                    <%
                        material_val = _('material')
                    %>
                    %if material_val :
                        <input type="text" id="material_tmp" class="input-150px" value="${material_val['SHOW_TEXT']}"  ref='${material_val|jd,n}'/>&nbsp;&nbsp;
                        <input ${_h('material')} value='${material_val|jd,n}'/>
                    %else:
                        <input type="text" id="material_tmp" class="input-150px" value='' ref=''/>&nbsp;&nbsp;
                        <input ${_h('material')} value=''/>
                    %endif
                    <input ${_c('Y','material_as_sample')}/>&nbsp;As Sample
                </td>
            </tr>
        </table>
    </fieldset>
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Packaging Style&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr>
                <td><input ${_c('Paper','material_type')}/>Paper Box</td>
                <td width="30">&nbsp;</td>
                <td><input ${_c('Wrap','material_type')}/>Header Wrap</td>
            </tr>
            <tr>
                <td>
                    <input id="${prefix}material_type_window_type" ${_c('Window','material_type')}/>Window Box<br />(Window Size
                    <input ${_i('window_size_w')} class="numeric input-50px"/> W
                        <input ${_i('window_size_d')} class="numeric input-50px"/> D
                        <input ${_r('mm','window_size_unit')}/> mm
                        <input ${_r('inch','window_size_unit')}/> inch)
                </td>
                <td width="10">&nbsp;</td>
                <td><input ${_c('Card','material_type')}/>Header Card</td>
            </tr>
            <tr>
                <td><input ${_c('Plastic','material_type')}/>Plastic Box</td>
                <td width="10">&nbsp;</td>
                <td><input ${_c('Blister','material_type')}/>#Blister</td>
            </tr>
            <tr>
                <td><input ${_c('Insert','material_type')}/>Insert</td>
                <td width="10">&nbsp;</td>
                <td><input ${_c('Clamshell','material_type')}/>#Clamshell</td>
            </tr>
            <tr>
                <td><input ${_c('Backer','material_type')}/>Backer Card</td>
                <td width="10">&nbsp;</td>
                <td><input ${_c('Injection','material_type')}/>#Injection Mold</td>
            </tr>
            <tr>
                <td><input ${_c('Belly','material_type')}/>Belly Band</td>
                <td width="10">&nbsp;</td>
                <td><input ${_c('Poly','material_type')}/>#Poly Bag</td>
            </tr>
            <tr>
                <td><input ${_c('Hang','material_type')}/>Hang Tag</td>
                <td width="10">&nbsp;</td>
                <td><input id="${prefix}material_type_other_type" ${_c('Other','material_type')}/>Other&nbsp;&nbsp;<input ${_i('material_other')} class="input-150px"/></td>
            </tr>
        </table>
        # This design is for visual confirmation only.
    </fieldset>
    
    <fieldset>
        <legend><span class="form-page-1"><sup class="red">*</sup>Requirements&nbsp;:</span></legend>
        <table cellspacing="0" cellpadding="0" border="0" class="table2">
            <tr><td><input ${_c('die_line','requirement')}/></td><td>Die-line</td></tr>
            <tr><td><input ${_c('expose_view','requirement')}/></td><td>Expose View</td></tr>
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