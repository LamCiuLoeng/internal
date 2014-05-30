<%inherit file="tribal.templates.master"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - (BBY)Case pack</%def>

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


<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    $(document).ready(function(){
			var dateFormat = 'yy-mm-dd';
			$('.datePicker').datepicker({
		        changeMonth : true,
		        changeYear : true,
		        dateFormat : dateFormat
		      });
		});
		
    function toSearch(){
        $("form").submit();
    }
    
    function toComplete(){
        return confirm("Are you sure to mark the record to be 'Completed'?");
    }
    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody><tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="175" valign="top" align="left"><a href="/bbycasepack/index"><img src="/images/mainmenu_g.jpg"/></a></td>
                %if has_permission("BBY_EDIT"):
		            %if not header.is_complete():
			        	<td width="64" valign="top" align="left"><a href="/bbycasepack/complete?id=${header.id}" onclick="return toComplete()"><img src="/images/images/menu_complete_g.jpg"/></a></td>
		            %endif
		        %endif
                <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
                <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
            </tr>
        </tbody></table>
</div>


<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Casepack</div>

<!-- Main content begin -->
<div style="width:1500px;">
    <div id="tabsJ">
		<ul>
            <li><a href="view?id=${header.id}"><span>Item Information</span></a></li>
			<li><a href="factory?id=${header.id}"><span>Factory</span></a></li>
			<li><a href="customer?id=${header.id}"><span>Customer</span></a></li>
			<li id="current"><a href="history?id=${header.id}"><span>History</span></a></li>
		</ul>
    </div>
    <div style="padding-left:20px;">
		<%include file="tribal.templates.bby.history_session" args="header=header,history=history"/>
	</div>	
</div>
<!-- Main Content end -->