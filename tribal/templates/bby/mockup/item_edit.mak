<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
	from tribal.util.bby_helper import getMaster,getComponent
%>

<%def name="extTitle()">r-pac - (BBY)Mockup</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/bby.css" type="text/css" media="screen"/>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>

<style>
body,td,th {
	font-family: Tahoma, Geneva, sans-serif;
	font-size: 12px;
	line-height: normal;
	color: #000;
	text-decoration: none;
}
.bline,.sline { display : none; }
.final{	background-color : yellow;}
.fsize{width: 50px}
</style>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
	var count = ${ max([o.id for o in header.options] or [10,]) +10 };   
    //]]>
</script>
<script type="text/javascript" src="/js/custom/bby/mockup_item.js" language="javascript"></script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
        <tr>
            <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
            <td width="175" valign="top" align="left"><a href="/bbymockup/index"><img src="/images/mainmenu_g.jpg"/></a></td>
            <td width="64" valign="top" align="left"><a href="#" onclick="toSave();"><img src="/images/images/menu_save_g.jpg"/></a></td>
            <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
            <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
        </tr>
        </tbody>
    </table>
</div>
            

<div class="nav-tree">BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Mockup</div>



<!-- Main content begin -->
<div style="width:2500px;">
	<div id="tabsJ">
    	<ul>
			<li id="current"><a href="item_view?id=${header.id}"><span>Item Information</span></a></li>
			<li><a href="detail_view?id=${header.id}"><span>Mockup Details</span></a></li>
			<li><a href="vendor_fitting?id=${header.id}"><span>Vendor Fitting</span></a></li>
			<li><a href="history?id=${header.id}"><span>History</span></a></li>
		</ul>
	</div>
    <div><br class="clear"/></div>

    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
    	${widget(value=values)|n}
    </div>
    
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
    <p><input type="button" value="Add Option" onclick="addbline()" class="btn"/></p>
    
    <p class="red"><sup>*</sup> The 'Option' field for each option line is required, otherwise the related component information won't be saved for the system !</p>
    <p class="red"><sup>*</sup> The 'Component' field for each component line is required, otherwise the related information won't be saved for the system !</p>
    
    	<form action="/bbymockup/save_item_edit" method="post">
    	<input type="hidden" name="header_id" value="${header.id}"/>
    	<table cellspacing="0" cellpadding="0" border="0" class="gridTable" id="c_table">
    		<thead>
    		<tr>
    			<th>Option</th>
    			<th>Component</th>
    			<th>Material</th>
    			<th>Spec</th>
    			<th>Front Color</th>
    			<th>Back Color</th>
    			<th>Size(L x W x H inch)</th>
    			<th>Closure</th>
    			<th>Display Mode</th>
    			<th>Remarks</th>
    			<th>Final</th>
    			<th colspan="2">Action</th>
      		</tr>
      		</thead>
      		 
    		%for o in header.options : 
    			${populate(o)}
    		%endfor
    	 
    		
    		<tr class="bline">
			    <td rowspan="1" style="border-left:1px solid #CCCCCC"><input type="text" name="o_name_x" value=""/></td>
			    <td>${component_select("c_format_id_x_10",None)}</td>
			    <td>${master_select("c_material_id_x_10","BBYMaterial",None)}</td>
			    <td>${master_select("c_coating_id_x_10","BBYSpec",None)}</td>
			    <td>${master_select("c_front_color_id_x_10","BBYColor",None)}</td>
			    <td>${master_select("c_back_color_id_x_10","BBYColor",None)}</td>
			    <td><input type="text" name="c_finished_size_l_x_10" value="" class="fsize"/> x <input type="text" name="c_finished_size_w_x_10" value="" class="fsize"/> x <input type="text" name="c_finished_size_h_x_10" value="" class="fsize"/></td>
			    <td>${master_select("c_closure_id_x_10","BBYClosure",None)}</td>
			    <td>${master_select("c_display_mode_id_x_10","BBYDisplayMode",None)}</td>
			    <td><textarea name="c_remark_x_10"></textarea></td>
			    <td><input type="checkbox" name="o_final_x" value="YES" onclick="final(this)"/>YES</td>
			    <td>&nbsp;</td>
			    <td rowspan="1">
			    	<input type="button" class="btn" value="Del Option" onclick="delbline(this)"/>&nbsp;&nbsp;
			    	<input type="button" class="btn addDetail" value="Add Component" brow_index="" srow_index="10" onclick="addsline(this)"/>
			    	<input type="button" class="btn" value="Copy Option" onclick="copybline(this)"/>
			    </td>
			</tr>		
			
			<tr class="sline">
			    <td>${component_select("c_format_id_x_y",None)}</td>
			    <td>${master_select("c_material_id_x_y","BBYMaterial",None)}</td>
			    <td>${master_select("c_coating_id_x_y","BBYSpec",None)}</td>
			    <td>${master_select("c_front_color_id_x_y","BBYColor",None)}</td>
			    <td>${master_select("c_back_color_id_x_y","BBYColor",None)}</td>
			    <td><input type="text" name="c_finished_size_l_x_y" value="" class="fsize"/> x <input type="text" name="c_finished_size_w_x_y" value="" class="fsize"/> x <input type="text" name="c_finished_size_h_x_y" value="" class="fsize"/></td>
			    <td>${master_select("c_closure_id_x_y","BBYClosure",None)}</td>
			    <td>${master_select("c_display_mode_id_x_y","BBYDisplayMode",None)}</td>
			    <td><textarea name="c_remark_x_y"></textarea></td>
			    <td><input type="button" class="btn" value="Del Component" onclick="delsline(this)"/></td>
			</tr>
    		
    	</table>
    	</form>
    </div>
    
</div>
<!-- Main Content end -->






<%def name="master_select(name,master,value)">
	<select name="${name}">
		<option></option>
		%for a in getMaster(master):
			<option value="${a.id}" ${tw.attrs([('selected',a.id==value),])}>${a}</option>
		%endfor
	</select>
</%def>


<%def name="component_select(name,value)">
	<select name="${name}">
		<option></option>
		%for a in getComponent():
			<option value="${a.id}" ${tw.attrs([('selected',a.id==value),])}>${a}</option>
		%endfor
	</select>
</%def>


<%def name="populate(o)">
	%if not o.components:
		${is_confirm(o)}
			<td rowspan="1" style="border-left:1px solid #CCCCCC"><input type="text" name="o_name_${o.id}" value="${o.name}"/></td>
			<td>${master_select("c_format_id_%d_y" %o.id,"BBYPackagingFormat",None)}</td>
			<td>${master_select("c_material_id_%d_y" %o.id,"BBYMaterial",None)}</td>
			<td>${master_select("c_coating_id_%d_y" %o.id,"BBYSpec",None)}</td>
			<td>${master_select("c_front_color_id_%d_y" %o.id,"BBYColor",None)}</td>
			<td>${master_select("c_back_color_id_%d_y" %o.id,"BBYColor",None)}</td>
			<td><input type="text" name="c_finished_size_l_${o.id}_y" value="" class="fsize"/> x <input type="text" name="c_finished_size_w_${o.id}_y" value="" class="fsize"/> x <input type="text" name="c_finished_size_h_${o.id}_y" value="" class="fsize"/></td>
			<td>${master_select("c_closure_id_%d_y" %o.id,"BBYClosure",None)}</td>
    		<td>${master_select("c_display_mode_id_%d_y" %o.id,"BBYDisplayMode",None)}</td>
			<td><textarea name="c_remark_${o.id}_y"></textarea></td>
			<td><input type="checkbox" name="o_final_${o.id}" value="YES" ${tw.attrs([('checked','YES'==o.final),])} onclick="final(this)"/>YES</td>
			<td><input type="button" class="btn" value="Del Component"/></td>
			<td rowspan="1">
				<input type="button" class="btn" value="Del Option" onclick="delbline(this)"/>&nbsp;&nbsp;
				<input type="button" class="btn" value="Add Component" brow_index="${o.id}" srow_index="10" onclick="addsline(this)"/>
				<input type="button" class="btn" value="Copy Option" onclick="copybline(this)"/>
			</td>
		</tr>
	%else:
		<% c = o.components[0] %>
		${is_confirm(o)}
			<td rowspan="${len(o.components)}" style="border-left:1px solid #CCCCCC"><input type="text" name="o_name_${o.id}" value="${o.name}"/></td>
			
			<td>${master_select("c_format_id_%d_%d" %(o.id,c.id),"BBYPackagingFormat",c.format_id)}</td>
			<td>${master_select("c_material_id_%d_%d" %(o.id,c.id),"BBYMaterial",c.material_id)}</td>
			<td>${master_select("c_coating_id_%d_%d" %(o.id,c.id),"BBYSpec",c.coating_id)}</td>
			<td>${master_select("c_front_color_id_%d_%d" %(o.id,c.id),"BBYColor",c.front_color_id)}</td>
			<td>${master_select("c_back_color_id_%d_%d" %(o.id,c.id),"BBYColor",c.back_color_id)}</td>
			<td><input type="text" name="c_finished_size_l_${o.id}_${c.id}" value="${c.finished_size_l}" class="fsize"/> x <input type="text" name="c_finished_size_w_${o.id}_${c.id}" value="${c.finished_size_w}" class="fsize"/> x <input type="text" name="c_finished_size_h_${o.id}_${c.id}" value="${c.finished_size_h}" class="fsize"/></td>
			<td>${master_select("c_closure_id_%d_%d" %(o.id,c.id),"BBYClosure",c.closure_id)}</td>
			<td>${master_select("c_display_mode_id_%d_%d" %(o.id,c.id),"BBYDisplayMode",c.display_mode_id)}</td>
			<td><textarea name="c_remark_${o.id}_${c.id}">${c.remark}</textarea></td>
			<td rowspan="${len(o.components)}"><input type="checkbox" name="o_final_${o.id}" value="YES" ${tw.attrs([('checked','YES'==o.final),])} onclick="final(this)"/>YES</td>
			
			<td>&nbsp;</td>
			<td rowspan="${len(o.components)}">
				<input type="button" class="btn" value="Del Option" onclick="delbline(this)"/>
				<input type="button" class="btn" value="Add Component" brow_index="${o.id}" srow_index="${o.components[-1].id}" onclick="addsline(this)"/>
				<input type="button" class="btn" value="Copy Option" onclick="copybline(this)"/>
			</td>
		</tr>
		
		%for c in o.components[1:]:
			${is_confirm(o)}
				<td>${master_select("c_format_id_%d_%d" %(o.id,c.id),"BBYPackagingFormat",c.format_id)}</td>
				<td>${master_select("c_material_id_%d_%d" %(o.id,c.id),"BBYMaterial",c.material_id)}</td>
    			<td>${master_select("c_coating_id_%d_%d" %(o.id,c.id),"BBYSpec",c.coating_id)}</td>
    			<td>${master_select("c_front_color_id_%d_%d" %(o.id,c.id),"BBYColor",c.front_color_id)}</td>
    			<td>${master_select("c_back_color_id_%d_%d" %(o.id,c.id),"BBYColor",c.back_color_id)}</td>
    			<td><input type="text" name="c_finished_size_l_${o.id}_${c.id}" value="${c.finished_size_l}" class="fsize"/> X <input type="text" name="c_finished_size_w_${o.id}_${c.id}" value="${c.finished_size_w}" class="fsize"/> X <input type="text" name="c_finished_size_h_${o.id}_${c.id}" value="${c.finished_size_h}" class="fsize"/></td>
    			<td>${master_select("c_closure_id_%d_%d" %(o.id,c.id),"BBYClosure",c.closure_id)}</td>
    			<td>${master_select("c_display_mode_id_%d_%d" %(o.id,c.id),"BBYDisplayMode",c.display_mode_id)}</td>
    			<td><textarea name="c_remark_${o.id}_${c.id}">${c.remark}</textarea></td>
    			<td><input type="button" class="btn" value="Del Component" onclick="delsline(this)"/></td>
			</tr>
		%endfor
	%endif
</%def>



<%def name="is_confirm(o)">
	%if o.final == "YES":
		<tr class="final">
	%else:
		<tr>
	%endif
</%def>