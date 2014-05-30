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
	$(obj).parent().find('input:file').each(function(){
		count++;
	})
	if(count>=4)
		alert('oops! you can only add 4 logos at most.')
	else
		$(obj).parent().append($('#hide_logo_file').html())
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
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Cabelas&nbsp;&nbsp;&gt;&nbsp;&nbsp;Development&nbsp;&nbsp;&gt;&nbsp;&nbsp;New</div>
<div class='main'>
	<form action='/cabelas/development/save' method=post enctype="multipart/form-data" id='_form' onsubmit="return toSubmit()">
		<ul id="step_menu">
			<li class="first">Package request</li>
		    <li>First proof<span></span></li>
		    <li>Final proof<span></span></li>
		    <li class="last">Released to printer<span></span></li>
		</ul>
		<div class='clear'>&nbsp;</div>
		<div class="ca_box1">
            <fieldset class="module aligned">
                <legend>Vendor</legend>
                <div class="form-row">
                    <label>Name:</label>
                    <select name='vendor_ids'>
                    	%for i in vendors:
                    	<option value='${i.id}'>${i.name}</option>
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
                    <input type="text" name="dept" class="required"/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Sub Dept#:</label>
                    <input type="text" name="sub_dept" class="required"/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Set No#:</label>
                    <input type="text" name="set_no" class="required"/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Color:</label>
                    <input type="text" name="color" class="required"/>
                </div>
            </fieldset>
        </div>
		<div class="ca_box2">
            <fieldset class="module aligned">
            	<legend>Label Development</legend>
                <div class="form-row">
                    <label><span class="red">*</span>Product Name:</label>
                    <input type="text" name="product_desc" class="required"/>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Bullet Information:</label>
                    <textarea name='bullet_info'></textarea>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Shoe Box Size:</label>
                    <select name='box_size_id' class="required">
                    	%for i in box_sizes:
                    	<option value='${i.id}'>${i.name}</option>
                    	%endfor
                    </select>
                </div>
                <div class="form-row">
                    <label><span class="red">*</span>Gender:</label>
                    <select name='gender_id' class="required">
                    	%for i in genders:
                    	<option value='${i.id}'>${i.name}</option>
                    	%endfor
                    </select>
                </div>
                <div class="form-row last">
                    <label>Logo:</label>
                    <div class='content'><a href='javascript:void(0)' onclick='addLogo(this)' class='addlink'>Add Logo</a></div>
                </div>
            </fieldset>
        </div>
        <div class="submit-row" >
            <input type="submit" value="Create" class="default" name="_create" />
        </div>
	</form>
</div>
<div class='none' id='hide_logo_file'>
	<div><input type='file' name='logo' />&nbsp;&nbsp;&nbsp;&nbsp;<a class="deletelink" href="javascript:void(0)" onclick='removeLogo(this)'></a></div>
</div>
