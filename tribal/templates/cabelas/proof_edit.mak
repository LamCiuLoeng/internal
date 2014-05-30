<%inherit file="tribal.templates.master"/>
<%def name="extTitle()">r-pac - Cabelas</%def>
<%def name="extCSS()">
<link rel="stylesheet" type="text/css" media="screen" href="/css/custom/cabelas.css"/>
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/inlines.min.js"></script>
<script>
$(document).ready(function($) {

})
var addLogo = function(obj){
	var count=0;
	$(obj).parent().find('input[name="logo_id"]').each(function(){
		count++;
	})
	$(obj).parent().find('input[name="logo"]').each(function(){
		count++;
	})
	if(count>=4)
		alert('oops! you can only add 4 logos at most.')
	else
		$(obj).parent().append($('#hide_logo_file').html())
}
var addProof = function(obj){
	$(obj).parent().append($('#hide_proof_file').html())
}
var toSubmit = function(){
	var msg = []
	var flag = false;
	$('.required').each(function(){
		if(!flag && $(this).val()==''){
			flag = true;
		}
	})
	if(flag) msg.push('Please input value for the <span class=red>*</span> fields.')
	if(msg.length==0) return true;
	else{
		showError(msg.join('</br>'))
		return false;
	}
}
var removeAttachment = function(obj){$(obj).parent().remove()}
var removeLogo = function(obj){$(obj).parent().remove()}
</script>
</%def>
<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/cabelas/development"><img src="/images/images/menu_return_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Development&nbsp;&nbsp;&gt;&nbsp;&nbsp;Edit</div>
<div class='main'>
	<form action='/cabelas/development/save' method=post enctype="multipart/form-data" id='_form' onsubmit="return toSubmit()">
		<input type='hidden' name='id' value='${label.id}'/>
		<ul id="step_menu">
			<li class="
			%if label.status==1:
			first
			%else:
			fdone
			%endif
			">Package request</li>
		    <li class="
		    %if label.status==2:
			inprogress
			%elif label.status>2:
			done
			%endif
		    ">First proof<span></span></li>
		    <li class="
		    %if label.status==3:
			inprogress
			%elif label.status>3:
			done
			%endif
		    ">Final proof<span></span></li>
		    <li class="
		    %if label.status==4:
			lastinprogress
			%else:
			last
			%endif
		    ">Released to printer<span></span></li>
		</ul>
		<div class='clear'>&nbsp;</div>
		<div class="ca_box1">
            <fieldset class="module aligned">
                <legend>Vendor</legend>
                <div class="form-row">
                    <label>Name:</label>
                    <select name='vendor_ids'>
                    	%for i in vendors:
                    	<option value='${i.id}' ${'selected' if label.vendor_ids==str(i.id) else ''}>${i.name}</option>
                    	%endfor
                    </select>
                </div>
            </fieldset>
        </div>
        <div class="ca_box1">
            <fieldset class="module aligned">
            	<legend>Proof Information</legend>
                <div class="form-row">
                    <label><span class="red">*</span>Dept#:</label>
                    <input type="text" name="dept" class="required" value='${label.dept}'/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Sub Dept#:</label>
                    <input type="text" name="sub_dept" class="required" value='${label.sub_dept}'/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Set No#:</label>
                    <input type="text" name="set_no" class="required" value='${label.set_no}'/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Color:</label>
                    <input type="text" name="color" class="required" value='${label.color}'/>
                </div>
            </fieldset>
        </div>
		<div class="ca_box2">
            <fieldset class="module aligned">
            	<legend>Label Development</legend>
                <div class="form-row">
                    <label><span class="red">*</span>Product Name:</label>
                    <input type="text" name="product_desc" class="required" value='${label.product_desc}'/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Bullet Information:</label>
                    <textarea name='bullet_info'>${label.bullet_info}</textarea>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Shoe Box Size:</label>
                    <select name='box_size_id' class="required">
                    	%for i in box_sizes:
                    	<option value='${i.id}' ${'selected' if label.box_size_id==i.id else ''}>${i.name}</option>
                    	%endfor
                    </select>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Gender:</label>
                    <select name='gender_id' class="required">
                    	%for i in genders:
                    	<option value='${i.id}' ${'selected' if label.gender_id==i.id else ''}>${i.name}</option>
                    	%endfor
                    </select>
                </div>
                <div class="form-row">
                    <label>Logo:</label>
                    <div class='content'>
	                    %for i in label_logos:
	                    <div>
	                    	<input type='hidden' name='logo_id' value='${i.id}'/>
	                    	<img src='/upload/${i._file_path}'>
	                    	&nbsp;&nbsp;&nbsp;&nbsp;<a class="deletelink" href="javascript:void(0)" onclick='removeAttachment(this)'></a>
	                    </div>
	                    %endfor
	                    <a href='javascript:void(0)' onclick='addLogo(this)' class='addlink'>Add Logo</a><br/>
                    </div>
                </div>
                <div class="form-row last">
                    <label>Proof:</label>
                    <div class='content'>
	                    %for i in label_proofs:
	                    <div>
	                    	<input type='hidden' name='proof_id' value='${i.id}'/>
	                    	<a href='/download?id=${i.id}'>${i.file_name}</a>
	                    	&nbsp;&nbsp;&nbsp;&nbsp;<a class="deletelink" href="javascript:void(0)" onclick='removeAttachment(this)'></a>
	                    </div>
	                    %endfor
	                    <a href='javascript:void(0)' onclick='addProof(this)' class='addlink'>Add Proof</a><br/>
                    </div>
                </div>
            </fieldset>
        </div>
        <div class="submit-row" >
        	%if label.status == 1:
        	<input type="submit" value="Save" class="default" name="_save" />
            <input type="submit" value="Save as first proof" class="default" name="_approve_first" />
        	%elif label.status == 2:
        	<input type="submit" value="Save" class="default" name="_save" />
        	<input type="submit" value="Save as final proof" class="default" name="_approve_final" />
        	%elif label.status == 3:
        	<input type="submit" value="Save" class="default" name="_save" />
        	<input type="submit" value="Released to printer" class="default" name="_release" />
        	%endif
        </div>
	</form>
</div>
<div class='none' id='hide_logo_file'>
	<div><input type='file' name='logo' />&nbsp;&nbsp;&nbsp;&nbsp;<a class="deletelink" href="javascript:void(0)" onclick='removeLogo(this)'></a></div>
</div>
<div class='none' id='hide_proof_file'>
	<div><input type='file' name='proof' />&nbsp;&nbsp;&nbsp;&nbsp;<a class="deletelink" href="javascript:void(0)" onclick='removeAttachment(this)'></a></div>
</div>