<%inherit file="tribal.templates.master"/>

<%
	from repoze.what.predicates import not_anonymous, in_group, has_permission
	from tribal.util.mako_filter import b,tp,cd
	from tribal.util.common import Date2Text
%>

<%def name="extTitle()">r-pac - (BBY)Case pack</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/sample.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/bby.css" type="text/css" media="screen"/>
<style type="text/css">
.more {display : none}
.more_div {padding-left:100px;}
</style>
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
    
    function showAndHide(obj){
			var t = $(obj);
			var td = $(t.parents("td")[0]);
			$(".more",td).toggle();
			$(".fn",td).toggle();
		}
    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody><tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="175" valign="top" align="left"><a href="/bbycasepack/index"><img src="/images/mainmenu_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="#" onclick="toSearch()"><img src="/images/images/menu_search_g.jpg"/></a></td>
                <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
                <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
            </tr>
        </tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;Casepack</div>



<!-- Main content begin -->
<div style="width:1500px;">


<div class="div-todolist">
  <table width="180" cellspacing="0" cellpadding="0" border="0">
    <tbody><tr>
      <td height="25" bgcolor="#ffffcc" align="center" class="title-page" style="border-bottom:1px solid #ccc;">TO DO LIST</td>
    </tr>
    <tr>
      <td height="30" align="center" class="todoliset-menu" background="/images/TDLBG.jpg">Outstanding List(<span id="todo-new-count">${todolist["new_count"]}</span>)</td>
    </tr>
    <tr>
      <td>
	  	<ul id="todo-new">
	  		%for i,n in enumerate(todolist["new"]):
	  			%if i < 5 :
		  			<li><a href="/bbycasepack/view?id=${n.id}">${n}</a>[${cd(n.update_time)}]</li>
		  		%else:
		  			<li class="more"><a href="/bbycasepack/view?id=${n.id}">${n}</a>[${cd(n.update_time)}]</li>
		  		%endif
	  		%endfor
	  	</ul>
	  	%if todolist["new_count"] >5:
	  		<div class="more_div"><a href="#" onclick="showAndHide(this)"><span class="fn">More</span><span class="fn" style="display:none">Less</span></a></div>
	  	%endif
	  </td>
    </tr>
    <tr>
      <td height="30" align="center" class="todoliset-menu" background="/images/TDLBG.jpg">Sent(<span id="todo-sent-count">${todolist["send_count"]}</span>)</td>
    </tr>
    <tr>
      <td>
	  	<ul id="todo-sent">
	  		%for i,s in enumerate(todolist["send"]):
	  			%if i < 5 :
		  			<li><a href="/bbycasepack/view?id=${s.id}">${s}</a>[${cd(s.update_time)}]</li>
		  		%else:
		  			<li class="more"><a href="/bbycasepack/view?id=${s.id}">${s}</a>[${cd(s.update_time)}]</li>
		  		%endif
	  		%endfor
	  	</ul>
	  	%if todolist["send_count"] >5:
	  		<div class="more_div"><a href="#" onclick="showAndHide(this)"><span class="fn">More</span><span class="fn" style="display:none">Less</span></a></div>
	  	%endif
	  </td>
    </tr>
  </tbody></table>
</div>



<div style="width:1200px;float:left">
	<div style="overflow:hidden;margin:5px 0px 10px 10px">
            ${widget(action="/bbycasepack/index",value=values)|n}
	</div>


	<div class="clear"><br /></div>
	<div id="recordsArea" style="margin:5px 0px 10px 10px">
	  <%
		my_page = tmpl_context.paginators.result
		pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
	  %>
      <table cellspacing="0" cellpadding="0" border="0" id="dataTable" class="gridTable">
		<thead>
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="100">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
            <tr> 
				  <th width="180">SKU#</th>
		    	  <th width="200">Product Description</th>
		    	  <th width="150">Brand</th>
		    	  <th width="120">Package Format</th>
				  <th width="170">Vendor</th>
				  <th width="150">PD</th>
				  <th width="150">AE</th>
				  <th width="180">Status</th>
	    	</tr>
		</thead>
		<tbody>
			% for index,h in enumerate(result):
    	    	%if h.status == 50:
                    <tr class="eol">
                %elif index %2 == 0 :
                    <tr class="even">
                %else:
                    <tr class="odd">
                %endif
				<td style="border-left:1px solid #ccc"><a href="/bbycasepack/view?id=${h.id}">${h.sku}</a></td>
				<td>&nbsp;${h.product_description}</td>
				<td>&nbsp;${h.brand}</td>
			    <td>&nbsp;${h.packaging_format}</td>
				<td>&nbsp;${h.vendor}</td>
				<td>&nbsp;${h.pd|b}</td>
				<td>&nbsp;${h.ae|b}</td>
				<td>
				    %if  h.status >= 50 :
                        EOL
					%elif h.status >= 40:
						Completed
					%elif h.status == 30:
						New
					%elif h.status == 31:
						Sent
					%endif
					&nbsp;
					%if h.is_cancel():
			    		<span class="red">(CANCEL)</span>
			    	%elif h.is_on_hold():
			    		<span class="red">(ON HOLD)</span>
			    	%endif
				</td>
			%endfor
			%if my_page.item_count > 0 :
			<tr>
				<td style="text-align:right;border-right:0px;border-bottom:0px" colspan="100">
					${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
				</td>
			</tr>
			%endif
		</tbody>
	</table>
  </div>
</div>	


</div>
<!-- Main Content end -->