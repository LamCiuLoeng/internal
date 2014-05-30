<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
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
input.btn {
background-color:#FFEEDD;
border-color:#669966 #336633 #336633 #669966;
border-style:solid;
border-width:1px;
color:#005500;
font:bold 90% 'trebuchet ms',helvetica,sans-serif;
}
.input-277px{border:#aaa solid 1px; width:277px; background-color:#FFe;}
.casepack_input_table td{ padding:6px;}
.casepack_input_table td label{ font-weight: bold;}
.casepack_input_table ul li{ list-style: none; padding:0 2px 2px 2px;}
.casepack_input_div{ width:700px; overflow:hidden; margin:8px 0px 10px 60px; border: 2px #F70A0D solid; padding:10px 0 12px 6px;}



.final{
	background-color : yellow;
}






</style>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    function toSubmit(){
        return confirm("Are you sure to submit the record?");
    }
    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
        <tr>
            <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
            <td width="175" valign="top" align="left"><a href="/bbymockup/index"><img src="/images/mainmenu_g.jpg"/></a></td>
	        %if has_permission("BBY_EDIT"):
	            %if not header.is_complete() and not header.is_eol():
		            <td width="64" valign="top" align="left"><a href="/bbymockup/item_edit?id=${header.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
		            %if header.status == 20:
		            	<td width="64" valign="top" align="left"><a href="/bbymockup/send?id=${header.id}" onclick="return toSubmit();"><img src="/images/images/menu_send_g.jpg"/></a></td>
		            %endif
	            %endif
			%endif		            
            <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
            <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
        </tr>
        </tbody>
    </table>
</div>
            

<div class="nav-tree">BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Mockup</div>



<!-- Main content begin -->
<div style="width:1500px;">
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
    
 
    
    
    
    <div>
    	<table cellspacing="0" cellpadding="3" border="0" id="dataTable" class="gridTable">
    		<thead>
    		<tr>
    			<th width="150">Options</th>
    			<th width="150">Components</th>
    			<th width="150">Material Name</th>
    			<th width="100">Spec</th>
    			<th width="100">Front Color</th>
    			<th width="100">Back Color</th>
    			<th width="150">Size(L x W x H inch)</th>
    			<th width="200">Closure</th>
    			<th width="150">Display Mode</th>
    			<th width="250">Remarks</th>
    			<th width="80">Final</th>
    		</tr>
    		</thead>
    		<tbody>
    			%for o in options:
    				%if not o.components:
		    			${is_confirm(o)}
		    				<td>&nbsp;${o.name}</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;</td>
		    				<td>&nbsp;${o.final}</td>
		    			</tr>
	    			%else:
		    			${is_confirm(o)}
		    				<td rowspan="${len(o.components)}">&nbsp;${o.name}</td>
		    				<td>&nbsp;${o.components[0].format}</td>
		    				<td>&nbsp;${o.components[0].material}</td>
		    				<td>&nbsp;${o.components[0].coating}</td>
		    				<td>&nbsp;${o.components[0].front_color}</td>
		    				<td>&nbsp;${o.components[0].back_color}</td>
		    				<td>&nbsp;${o.components[0].finished_size}</td>
		    				<td>&nbsp;${o.components[0].closure}</td>
		    				<td>&nbsp;${o.components[0].display_mode}</td>
		    				<td>&nbsp;${o.components[0].remark}</td>
			    			<td rowspan="${len(o.components)}">&nbsp;${o.final}</td>
		    			</tr>
		    			%for c in o.components[1:]:
		    				${is_confirm(o)}
			    				<td>&nbsp;${c.format}</td>
			    				<td>&nbsp;${c.material}</td>
				    			<td>&nbsp;${c.coating}</td>
				    			<td>&nbsp;${c.front_color}</td>
				    			<td>&nbsp;${c.back_color}</td>
				    			<td>&nbsp;${c.finished_size}</td>
				    			<td>&nbsp;${c.closure}</td>
				    			<td>&nbsp;${c.display_mode}</td>
				    			<td>&nbsp;${c.remark}</td>
			    			</tr>
		    			%endfor
	    			%endif
    			%endfor
    		</tbody>
    	</table>
    </div>
    
</div>
<!-- Main Content end -->


<%def name="is_confirm(o)">
	%if o.final == "YES":
		<tr class="confirm">
	%else:
		<tr>
	%endif
</%def>