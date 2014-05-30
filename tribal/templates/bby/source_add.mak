<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extJavaScript()">
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
		function toSave(){
			formArray = $("form").serialize() 
			$.ajax({
				type:"POST",
				dataType:"json",
				data:formArray,
				url: "${saveURL}",
				success: function(data,textStatus){
					$.prompt(data.Msg,{opacity: 0.6,prefix:'cleanblue'});
				},
				error: function(){
					$.prompt("Error",{opacity: 0.6,prefix:'cleanblue'});
				}
			});
		}
		function toUpdate() {
			$("form").attr("action", "/itemcode/updateAttr");
			$("form").submit();
		}
		function checkName(obj){
			var name = $(obj).val();
			$.ajax({
				type:"GET",
				dataType:"json",
				data:{"name":name},
				url: "/bby_source/checkName",
				success: function(data,textStatus){
					if(data.Msg != null){
						$.prompt(data.Msg,{opacity: 0.6,prefix:'cleanblue'});
					}
				},
				error: function(){
					//alert(data.Msg)
				}
			});
		}
		var iconArray = ["#contact","#tel","#mobile","#email","#address"];
		function focusArr(obj){
			for (x in iconArray){
				var Input = iconArray[x]+$(obj).attr("length")
				$(Input).css("backgroundColor","#E8F3F7");
			}
		}
		function blurArr(obj){
			for (x in iconArray){
				var Input = iconArray[x]+$(obj).attr("length")
				$(Input).removeAttr("style");
			}
		}
		function addInput(obj){
			workInput(obj,'add');
		}
		function delInput(obj){
			workInput(obj,'del');
			$(obj).remove();
		}
		function workInput(obj,type){
			var length = $(obj).parent("li").children("input").length
			for (x in iconArray)
				{
					var objInput = $(iconArray[x]+$(obj).attr("class"))
					if(type=="add"){
						var inputText = "<input type='"+objInput.attr('type')+"' value='' name='"+objInput.attr('back_name')+length+"' class='"+objInput.attr('class')+"' id='"+objInput.attr('back_name')+length+"' length='"+length+"' onfocus='focusArr(this)' onblur='blurArr(this)' >"
						if(objInput.attr("back_name")=='contact'){
							objInput.parent("li").append(inputText+"<a  onclick='delInput(this)' class='"+length+"'><img src='/images/icon_deletelink.gif'/></a>").css("width","270px")
						}
						else if(objInput.attr("back_name")=='address'){
							objInput.parent("li").append("<textarea cols='50' rows='7' name='"+objInput.attr('back_name')+length+"' class='"+objInput.attr('class')+"' id='"+objInput.attr('back_name')+length+"' length='"+length+"' back_name='address' onfocus='focusArr(this)' onblur='blurArr(this)'></textarea>")
						}
						else{
							objInput.parent("li").append(inputText).css("width","270px")
						}
						$("#count").val(length);
					}
					else{
						le = length-1
						var delInput = iconArray[x]+$(obj).attr("class")
						$(delInput).remove()
						$("#count").val(le-1);
					}
				}
			% if obj_detail:
				if(type=="del"){
					var hid = $("#hid"+$(obj).attr("class")).val();
					if(hid){
						$.ajax({
							type:"GET",
							dataType:"json",
							url: "/bby_source/ajaxDelete?hid="+hid,
							success: function(data,textStatus){
								$.prompt("Delete successfully!",{opacity: 0.6,prefix:'cleanblue'});
							},
							error: function(){
								$.prompt("Delete fail,Please reload the page!",{opacity: 0.6,prefix:'cleanblue'});
							}
						});
					}
				}
			% endif
		}
		$(document).ready(function(){
			$("#contact").parent("li").append("<a  onclick='addInput(this)' ><img src='/images/icon_addlink.gif' /></a>")
			%if saveURL == '/bby_source/saveNew':
			$("#name").replaceWith("<input value='"+$("#name").val()+"' type='text' name='name' class='width-250 inputText' id='name' onblur='checkName(this)' >")
			%endif
			$(".bbysourceupdateform").append("<input type='hidden' value='0' name='count' id='count'>");
			for (x in iconArray){
				$(iconArray[x]).attr({"name":$(iconArray[x]).attr("name")+0,"back_name":$(iconArray[x]).attr("name"),"onblur":"blurArr(this)","onfocus":"focusArr(this)","length":"0"})
				$(iconArray[x]).parent("li").css("width","270px")
			}
			% if obj_detail:
				var contact = [];
				var mobile = [];
				var address = [];
				var tel = [];
				var email = [];
				<% k=0 %>
				% for i in obj_detail:
					%if k == 0:
						contact.push("<input type='text' value='${i.contact}' name='contact${k}' class='width-250 inputText' id='contact${k}' back_name='contact' onfocus='focusArr(this)' onblur='blurArr(this)' length='${k}' ><a  onclick='addInput(this)' class='${k}' length='${k}' ><img src='/images/icon_addlink.gif' /></a>");
					%else:
						contact.push("<input type='text' value='${i.contact}' name='contact${k}' class='width-250 inputText' id='contact${k}' back_name='contact' onfocus='focusArr(this)' onblur='blurArr(this)'  length='${k}' ><a  onclick='delInput(this)' class='${k}' length='${k}'><img src='/images/icon_deletelink.gif'/></a>");
					%endif
					mobile.push("<input type='text' value='${i.mobile}' name='mobile${k}' class='width-250 inputText' id='mobile${k}' back_name='mobile' onfocus='focusArr(this)' onblur='blurArr(this)' length='${k}' >")
					tel.push("<input type='text' value='${i.tel}' name='tel${k}' class='width-250 inputText' id='tel${k}' back_name='tel' onfocus='focusArr(this)' onblur='blurArr(this)' length='${k}'>")
					address.push("<textarea cols='50' rows='7' class='width-250 height-70' name='address${k}' id='address${k}' back_name='address' onfocus='focusArr(this)' onblur='blurArr(this)' length='${k}'>${'\\n'.join(i.address.split("\n"))}</textarea>")
					email.push("<input type='text' value='${i.email}' name='email${k}' class='width-250 inputText' id='email${k}' back_name='email' onfocus='focusArr(this)' onblur='blurArr(this)' length='${k}' ><input type='hidden' value='${i.id}' name='hid${k}' class='width-250 inputText' id='hid${k}' back_name='hid' >")
					<% k+=1 %>
				% endfor 
				var contact = contact.join("");
				var mobile = mobile.join("");
				var address = address.join("");
				var tel = tel.join("");
				var email = email.join("");
				$("#contact").parent("li").html(contact);
				$("#tel").parent("li").html(tel);
				$("#mobile").parent("li").html(mobile);
				$("#email").parent("li").html(email);
				$("#address").parent("li").html(address);
				$("#count").val(${k-1});
			% endif
		})
    //]]>
   </script>
</%def>
<div id="function-menu">
<table width="100%" cellspacing="0" cellpadding="0" border="0">
<tbody>
  <tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="176" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_${funcURL}_g.jpg"/></a></td>
    <td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    % if funcURL == 'itemcode':
    <td width="64" valign="top" align="left"><a href="#" onclick="toUpdate()"><img src="/images/images/menu_update_g.jpg"/></a></td>
    % endif
    <td width="64" valign="top" align="left"><a href="/${funcURL}/index"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody>
</table>
</div>
<div class="nav-tree">Master&nbsp;&nbsp;&gt;&nbsp;&nbsp;New or Update</div>
<div>
	${widget(values,action=saveURL)|n}
</div>





