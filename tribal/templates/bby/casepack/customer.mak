<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - (BBY)Casepack</%def>

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
.gridTable2 thead th{
	background-color : gray;
}


</style>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    function toSubmit(){
        return confirm("Are you sure to submit the record?");
    }
    
    function toComplete(){
        return confirm("Are you sure to mark the record to be 'Completed'?");
    }
    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody>
        <tr>
            <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
            <td width="175" valign="top" align="left"><a href="/bbycasepack/index"><img src="/images/mainmenu_g.jpg"/></a></td>
	        %if has_permission("BBY_EDIT"):
	            %if not header.is_complete():
	            	<td width="64" valign="top" align="left"><a href="/bbycasepack/customer_update?id=${header.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
	            	<td width="64" valign="top" align="left"><a href="/bbycasepack/complete?id=${header.id}" onclick="return toComplete()"><img src="/images/images/menu_complete_g.jpg"/></a></td>
	            %endif
	        %endif
            <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
            <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
        </tr>
        </tbody>
    </table>
</div>

            
<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Casepack</div>



<!-- Main content begin -->
<div style="width:1500px;">
    <div id="tabsJ">
	<ul>
		<li><a href="view?id=${header.id}"><span>Item Information</span></a></li>
		<li><a href="factory?id=${header.id}"><span>Factory</span></a></li>
		<li id="current"><a href="customer?id=${header.id}"><span>Customer</span></a></li>
		<li><a href="history?id=${header.id}"><span>History</span></a></li>
	</ul>
    </div>

    <div><br class="clear"/><br /></div>
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
      ${widget(action="",value=values)|n}
    </div>
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
	    <table cellspacing="0" cellpadding="0" border="0" class="gridTable">
	    	<thead>
                <tr>
                    <th style="width:50px">Round</th>
                    <th style="width:100px">Received Date</th>
                    <th style="width:100px">Send Out Date</th>
                    <th style="width:150px">Customer Received Date</th>
                    <th style="width:100px">Test By</th>
                    <th style="width:50px">Qty</th>
                    <th style="width:70px">Pass/Fail</th>
                    <th style="width:100px">Reported Date</th>
                    <th style="width:150px">Reason for failure</th>
                    <th style="width:150px">Attachment</th>
                    <th style="width:150px">Remark</th>
                </tr>
            </thead>
            <tbody>
            	%for index,r in enumerate(header.results):
            		<tr class="${['odd','even'][index%2]}">
            			<td style="border-left:1px solid #ccc;">&nbsp;${index+1}</td>
            			<td>&nbsp;${f(r.received_date)}</td>
            			<td>&nbsp;${f(r.send_out_date)}</td>
            			<td>&nbsp;${f(r.customer_received_date)}</td>
            			<td>&nbsp;${r.test_by}</td>
            			<td>&nbsp;${r.qty}</td>
            			<td>&nbsp;${r.result}</td>
            			<td>&nbsp;${f(r.reported_date)}</td>
            			<td>&nbsp;${r.reason}</td>
            			<td>&nbsp;
            				%if r.getAttachments():
	            				%for a in r.getAttachments():
	            					<a href="/bbycasepack/download?id=${a.id}">${a.file_name}</a>&nbsp;&nbsp;&nbsp;
	            				%endfor
	            			%endif
            			</td>
            			<td>&nbsp;${r.remark}</td>
            		</tr>
            	%endfor
            </tbody>
	    </table>
	    
	    
    </div>
	
</div>
<!-- Main Content end -->

<%def name="f(date_value,date_format='%Y-%m-%d')" filter="trim">
	%if date_value:
		${date_value.strftime(date_format)}
	%endif
</%def>