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
.input-277px{border:#aaa solid 1px; width:277px; background-color:#FFe;}
.casepack_input_table td{ padding:6px;}
.casepack_input_table td label{ font-weight: bold;}
.casepack_input_table ul li{ list-style: none; padding:0 2px 2px 2px;}

.gridTable2 thead th{
	background-color : gray;
}

</style>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    function toComplete(){
        return confirm("Are you sure to mark the record to be 'Completed'?");
    }

    function toEOL(){
        return confirm("Are you sure to mark the record to be 'EOL'?");
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
	       
	        %if header.is_eol():
	           %if has_permission("BBY_EDIT_COMPLETE"):
	               <td width="64" valign="top" align="left"><a href="/bbycasepack/update?id=${header.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
	           %endif
	        %elif header.is_complete():
	           %if has_permission("BBY_EDIT"):
                   <td width="64" valign="top" align="left"><a href="/bbycasepack/eol?id=${header.id}" onclick="return toEOL()"><img src="/images/images/eol_g.jpg"/></a></td>
               %endif
	        %else:
	           %if has_permission("BBY_EDIT"):
                   <td width="64" valign="top" align="left"><a href="/bbycasepack/update?id=${header.id}"><img src="/images/images/menu_revise_g.jpg"/></a></td>
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
		<li id="current"><a href="view?id=${header.id}"><span>Item Information</span></a></li>
		<li><a href="factory?id=${header.id}"><span>Factory</span></a></li>
		<li><a href="customer?id=${header.id}"><span>Customer</span></a></li>
		<li><a href="history?id=${header.id}"><span>History</span></a></li>
	</ul>
    </div>

    <div><br class="clear"/><br /></div>
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
      ${widget(action="",value=values)|n}
    </div>
    
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
    	
	    	<p><b>Final Package Details</b></p>
	    	%for c in option.components:
	    		<div style="border:1px solid #ccc;width:1050px">
		    		<table cellspacing="0" cellpadding="0" border="0" class="gridTable">
		    			<thead>
			                <tr>
			                    <th style="width:150px">Component</th>
			                    <th style="width:100px">Material Name</th>
			                    <th style="width:100px">Spec</th>
			                    <th style="width:100px">Front Color</th>
			                    <th style="width:100px">Back Color</th>
			                    <th style="width:150px">Finished Size</th>
			                    <th style="width:150px">Closure</th>
			                    <th style="width:100px">Display Mode</th>
			                </tr>
		                </thead>
		                <tbody>
		                	<tr>
			                    <td style="border-left:1px solid #CCCCCC">${c.format}</td>
			                    <td>${c.material.name if c.material else ''}&nbsp;</td>
			                    <td>${c.coating.name if c.coating else ''}&nbsp;</td>
			                    <td>${c.front_color.name if c.front_color else ''}&nbsp;</td>
			                    <td>${c.back_color.name if c.back_color else ''}&nbsp;</td>
			                    <td>${c.finished_size}&nbsp;</td>
			                    <td>${c.closure.name if c.closure else ''}&nbsp;</td>
			                    <td>${c.display_mode.name if c.display_mode else ''}&nbsp;</td>
			                </tr>
		                </body>
		    		</table>
		    		
					<p>Factory : ${c.factory}</p>
	           		<table cellspacing="0" cellpadding="0" border="0" class="gridTable gridTable2">
					 	<thead>
			                <tr>
			                    <th style="width:50px">Round</th>
			                    <th style="width:80px">Qty</th>
			                    <th style="width:150px">Required Ready Date</th>
			                    <th style="width:150px">Ship To</th>
			                    <th style="width:120px">Attention To</th>
			                    <th style="width:250px">Remarks</th>
			                </tr>  
		                </thead>
		    			<tbody>
			    			%for index,cd in enumerate(c.casepack_details):
								<tr>
									<td style="border-left:1px solid #CCCCCC">${index+1}</td>
									<td>&nbsp;${cd.qty}</td>
									<td>&nbsp;${f(cd.required_date)}</td>
									<td>&nbsp;${cd.ship_to}</td>
									<td>&nbsp;${cd.attention}</td>
									<td>&nbsp;${cd.remark}</td>
								</tr>		    				
			    			%endfor
		    			</tbody>
					</table>
	    		</div>
	    		<br />
	    	%endfor
    </div>
	
</div>
<!-- Main Content end -->

<%def name="f(date_value,date_format='%Y-%m-%d')">
	%if date_value:
		${date_value.strftime(date_format)}
	%endif
</%def>