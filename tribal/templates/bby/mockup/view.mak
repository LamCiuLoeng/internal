<%inherit file="tribal.templates.master"/>

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
            <td width="64" valign="top" align="left"><a href="/bbymockup/index"><img src="/images/images/menu_return_g.jpg"/></a></td>
	        %if has_permission("BBY_EDIT"):
	            %if not obj.is_complete():
		            <td width="64" valign="top" align="left"><a href="/bbymockup/update?id=${header.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
		            <td width="64" valign="top" align="left"><a href="/bbymockup/submit_pass?id=${header.id}" onclick="return toSubmit();"><img src="/images/images/menu_submit_g.jpg"/></a></td>
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
	
    <div style="width:1200px;float:left">
    	<div class="case-960-one">
	      <div class="log-one">Basic Info</div>${widget(value=values)|n}</div>
	  </div>
    </div>


</div>
<!-- Main Content end -->