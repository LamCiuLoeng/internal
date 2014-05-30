<%inherit file="tribal.templates.master"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extJavaScript()">
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
		function convArray(off,obj){
			var currObj = $("select[name='"+off+"']");
			var iconObj = currObj.next("a")
			if(obj.search("{")>-1){
				var arr = obj.replace("{","").replace("}","").split(",")
				for(i in arr){
					if(i>0) workInput(iconObj,'add')
					var getIndex = $("select[name='"+off+"']").eq(i).children("option[value='"+arr[i]+"']").attr("index")
					$("select[name='"+off+"']").eq(i)[0].selectedIndex = getIndex
				}
			}else{
				var getIndex = $("select[name='"+off+"']").eq(0).children("option[value='"+obj+"']").attr("index")
				currObj.eq(0)[0].selectedIndex = getIndex
			}
		
		}
		function toSave() {
			$("form").submit();
		}
		function toDelete(){
			window.location='${deleteURL}'
		}
		function addInput(obj){
			workInput(obj,'add');
		}
		function delInput(obj){
			workInput(obj,'del');
			$(obj).remove();
		}
		function workInput(obj,type){
			var objInput = $(obj)
			if(type=="add"){
				var html = $('<div>').append(objInput.prev("select").clone()).remove().html();
				var texts = html+"<a  onclick='delInput(this)' class='"+length+"'><img src='/images/icon_deletelink.gif'/></a>"
				objInput.parent("li").append(texts).css("width","270px")
			}
			else{
				objInput.prev("select").remove();
				objInput.remove();
			}
		}
		$(document).ready(function(){
			$("select").each(function(){
				if($(this).attr("name") != "head_id"){
					$(this).parent("li").append("<a onclick='addInput(this)' ><img src='/images/icon_addlink.gif' /></a>")	
				}
			})
			var insertHtml = "<td width='64' valign='top' align='left'><a onclick='toDelete()' href='#'><img src='/images/images/menu_delete_g.jpg'></a></td>"
			$("#function-menu").find("td").eq(2).after(insertHtml);
			% if obj_detail:
				convArray('head_id','${obj_detail.head_id}');
				convArray('spec','${obj_detail.spec}');
				convArray('back_color','${obj_detail.back_color}');
				convArray('material','${obj_detail.material}');
				convArray('front_color','${obj_detail.front_color}');
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
<form class="bbymaterialspecupdateform required" method="post" action="${saveURL}">
  <div class="case-list-one">
    <ul>
      <li class="label">
        <label id="head_id.label" for="head_id" class="fieldlabel">name</label>
      </li>
      <li>
        <select name="head_id" class="width-250" id="head_id">
        <option value=""></option>
        %for i in nameOptions:
          <option value="${i.id}">${i.name}</option>
        %endfor 
        </select>
      </li>
    </ul>
    <ul>
      <li class="label">
        <label id="spec.label" for="spec" class="fieldlabel">spec</label>
      </li>
      <li>
        <select name="spec" class="width-250" id="spec">
        <option value=""></option>
        %for i in specOptions:
          <option value="${i.id}">${i.name}</option>
        %endfor 
        </select>
      </li>
    </ul>
    <ul>
      <li class="label">
        <label id="back_color.label" for="back_color" class="fieldlabel">back color</label>
      </li>
      <li style="width: 270px;">
        <select name="back_color" class="width-250" id="back_color">
        <option value=""></option>
        %for i in colorOptions:
          <option value="${i.id}">${i.name}</option>
        %endfor 
        </select>
      </li>
    </ul>
  </div>
  <div class="case-list-one">
    <ul>
      <li class="label">
        <label id="material.label" for="material" class="fieldlabel">material</label>
      </li>
      <li>
        <select name="material" class="width-250" id="material">
        <option value=""></option>
        %for i in materialOptions:
          <option value="${i.id}">${i.name}</option>
        %endfor 
        </select>
      </li>
    </ul>
    <ul>
      <li class="label">
        <label id="front_color.label" for="front_color" class="fieldlabel">front color</label>
      </li>
      <li>
        <select name="front_color" class="width-250" id="front_color">
         <option value=""></option>
        %for i in colorOptions:
          <option value="${i.id}">${i.name}</option>
        %endfor 
        </select>
      </li>
    </ul>
</div>





