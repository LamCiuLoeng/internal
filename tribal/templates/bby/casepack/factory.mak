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
		            <td width="64" valign="top" align="left"><a href="/bbycasepack/email?id=${header.id}"><img src="/images/images/menu_email_g.jpg"/></a></td>
		            <td width="64" valign="top" align="left"><a href="/bbycasepack/factory_update?id=${header.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
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
		<li id="current"><a href="factory?id=${header.id}"><span>Factory</span></a></li>
		<li><a href="customer?id=${header.id}"><span>Customer</span></a></li>
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
                    <th>Content</th>
                </tr>
            </thead>
            <tbody>
            	%for round,round_data in result.items():
            	<tr>
            		<td style="border-left:1px solid #ccc;">&nbsp;${round}</td>
            		<td>
            			%for cid,c in  round_data.items():
	            			<fieldset class="fieset-css">
	            				<legend><b>${c['component']}</b></legend>
	            				<table cellspacing="0" cellpadding="0" border="0" class="gridTable gridTable2">
	            					<thead>
	            						<tr>
						                    <th style="width:100px">Sender</th>
						                    <th style="width:180px">E-mail Date</th>
						                    <th style="width:150px">Factory</th>
						                    <th style="width:150px">Required Date</th>
						                    <th style="width:80px">Qty</th>
						                    <th style="width:150px">Ship To</th>
						                    <th style="width:150px">Sent Out Date</th>
						                    <th style="width:150px">Couier</th>
						                    <th style="width:100px">AWB#</th>
						                    <th style="width:250px">Casepack Received Date</th>
						                    <th style="width:150px">Remark</th>
						                    <th style="width:70px">Cancel</th>
						                    <th style="width:70px">Approval</th>
					                    </tr>
	            					</thead>
	            					<tbody>
	            						%for r in c['data']:
		            						<tr>
						            			<td style="border-left:1px solid #ccc;">&nbsp;${r.create_by}</td>
						            			<td>&nbsp;${f(r.create_time,'%Y-%m-%d %H:%M:%S')}</td>
						            			<td>&nbsp;${r.factory}</td>
						            			<td>&nbsp;${f(r.required_date)}</td>
						            			<td>&nbsp;${r.qty}</td>
						            			<td>&nbsp;${r.ship_to}</td>
						            			<td>&nbsp;${f(r.send_date)}</td>
						            			<td>&nbsp;${r.courier}</td>
						            			<td>&nbsp;${r.awb}</td>
						            			<td>&nbsp;${f(r.received_date)}</td>
						            			<td>&nbsp;${r.remark}</td>
						            			<td>&nbsp;${r.cancel}</td>
						            			<td>&nbsp;${r.approve}</td>
		            						</tr>
	            						%endfor
	            					</tbody>
	            				</table>
	            			</fieldset>
            			%endfor
            		</td>
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