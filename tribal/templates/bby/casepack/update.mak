<%inherit file="tribal.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
	from tribal.util.bby_helper import getMaster
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
<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>


<style>
.template{ display : none; }

.gridTable2 thead th{
	background-color : gray;
}
</style>

<script language="JavaScript" type="text/javascript">
    //<![CDATA[
    var dateFormat = 'yy-mm-dd';
    $(function(){
        $('.datePicker').datepicker({firstDay: 1 , dateFormat: dateFormat});
        $(".numeric").numeric();

    });
    function toSave(){
        $(".template").remove();
        $("form").submit();
    }

    function toCompleted(){
        
        if(confirm("Are you sure to complete the record?")){
            $('input[name=status]').val('completed');
            toSave();
        }else{
            return false;
        }
    }

    function getFileName(obj){
      var tmp = $(obj);
      var path = tmp.val();
      if( path && path.length > 0){
        var location = path.lastIndexOf("\\") > -1 ?path.lastIndexOf("\\") + 1 : 0;
        var fn = path.substr( location,path.length-location );
        //alert(tmp.parent().prev().prev().find('input').val())
        //tmp.siblings("input").val(fn);
        tmp.parent().prev().prev().find('input').val(fn)
      }
    }

    //row_index = 800;
    function addline(obj){
    	var btn = $(obj);
    
    	var tmp = $(".template").clone();
        $('.datePicker', tmp).attr("id","");
		tmp.removeClass("template");
		$("input,select,textarea",tmp).each(function(){
			var t = $(this);
			var n = t.attr("name")
			t.removeClass("hasDatepicker");
			t.attr("name",n.replace("_x","_"+btn.attr("bindex")).replace("_y","_"+btn.attr("sindex")));
		});
        
        $('.datePicker',tmp).datepicker({
		        changeMonth : true,
		        changeYear : true,
		        dateFormat : dateFormat
		});
		
		$(".numeric",tmp).numeric();

    	$("#detail_"+btn.attr("bindex")).append(tmp);
    	btn.attr("sindex",parseInt(btn.attr("sindex"))+1);
    }
    
    function delline(obj){
    	var tmp = $(obj);
    	$(tmp.parents("tr")[0]).remove();
    }

    function addFile(obj){
    	var td = $(obj).parents("td")[0];
    	var table = $(".popup-table",td);

    	var tmp = $(".template",table).clone();
    	tmp.removeClass("template");
    	var index = row_index++;
    	$("input",tmp).each(function(){
    		var t = $(this);
    		t.attr("name",t.attr("name")+"_"+index);
    	});
        
    	table.append(tmp);
    }

    function delFile(obj){
    	var tr = $(obj).parents("tr")[0];
    	$(tr).remove();
    }

    function ajaxDelFile(type,id,fid,obj){
    	$.getJSON("/bbycasepack/ajaxDeleteFile",
    	          {
    	          	type : type,
    	          	id : id,
    	          	fid : fid
    	          },
    	          function(r){
    	          	if(r.result == "0"){
    	          		alert("Delete the file successfully!");
    	          		$($(obj).parents("li")[0]).remove();
    	          	}else{
    	          		alert("Error when deleting the file!");
    	          	}
    	          });
    }

    function selectRadio(this_obj){
          var obj = $(this_obj);
          if(obj.val()!=''){
               obj.prev('input').attr('checked', 'checked')
          }

    }

    //]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
        <tbody><tr>
                <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
                <td width="175" valign="top" align="left"><a href="/bbycasepack/index"><img src="/images/mainmenu_g.jpg"/></a></td>
                <td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
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
			<li id="current"><a href="view?id=${header.id}"><span>Item Information</span></a></li>
			<li><a href="factory?id=${header.id}"><span>Factory</span></a></li>
			<li><a href="customer?id=${header.id}"><span>Customer</span></a></li>
			<li><a href="history?id=${header.id}"><span>History</span></a></li>
		</ul>
    </div>

    <div><br class="clear"/></div>
    <div style="overflow: hidden; margin: 5px 0px 10px 10px;">
      ${widget(action="",value=values)|n}
    </div>
    
    <form action="/bbycasepack/save_update" method="post" enctype="multipart/form-data">
    	<input type="hidden" name="id" value="${header.id}"/>
    	
    	<div style="overflow: hidden; margin: 5px 0px 10px 10px;">
	    	<p><b>Final Package Details</b></p>
	    	
	    	<p class="red"><sup>*</sup> Either one of the fields ('Qty','Required Ready Date','Ship To','Attention To','Remarks') must be filled, otherwise the related information won't be saved for the system !</p>
	    	
	    	%for c in option.components:
	    		<div style="border:1px solid #ccc;width:1050px;">
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
		    		
					<p>Factory : ${select_widget('factory_id_%d' %c.id,'BBYSource',c.factory_id)}</p>
					<p>Details : <input type="button" class="btn" value="Add Line" bindex="${c.id}" sindex="${c.casepack_details[-1].id+10 if c.casepack_details else 10}" onclick="addline(this)"/>
    				<table cellspacing="0" cellpadding="0" border="0" class="gridTable gridTable2" id="detail_${c.id}">
    				 	<thead>
			                <tr>
			                    <th>Round</th>
			                    <th>Qty</th>
			                    <th>Required Ready Date</th>
			                    <th>Ship To</th>
			                    <th>Attention To</th>
			                    <th>Remarks</th>
			                    <th>Action</th>
			                </tr>					                
		                </thead>
		    			<tbody>
			    			%for index,cd in enumerate(c.casepack_details):
								<tr>
									<td style="border-left:1px solid #CCCCCC">${index+1}</td>
									<td>&nbsp;<input type="text" class="numeric" name="qty_${c.id}_${cd.id}" value="${cd.qty}"/></td>
									<td>&nbsp;<input type="text" name="required_date_${c.id}_${cd.id}" value="${cd.required_date.strftime('%Y-%m-%d') if cd.required_date else ''}" class="datePicker"/></td>
									<td>&nbsp;${select_widget('ship_to_id_%d_%d' %(c.id,cd.id),'BBYVendor',cd.ship_to_id)}</td>
									<td>&nbsp;<input type="text" name="attention_${c.id}_${cd.id}" value="${cd.attention}"/></td>
									<td>&nbsp;<textarea name="remark_${c.id}_${cd.id}">${cd.remark}</textarea></td>
									<td><input type="button" class="btn" value="Del Line" onclick="delline(this)"/></td>
								</tr>		    				
			    			%endfor
		    			</tbody>
					 </table>
	    		</div>
	    		<br />
	    	%endfor
	    </div>
    

	    

</form>

</div>
<!-- Main Content end -->

<table>
	<tr class="template">
		<td style="border-left:1px solid #CCCCCC"></td>
		<td>&nbsp;<input type="text" class="numeric" name="qty_x_y" value=""/></td>
		<td>&nbsp;<input type="text" name="required_date_x_y" value="" class="datePicker"/></td>
		<td>&nbsp;${select_widget('ship_to_id_x_y','BBYVendor',None)}</td>
		<td>&nbsp;<input type="text" name="attention_x_y" value=""/></td>
		<td>&nbsp;<textarea name="remark_x_y"></textarea></td>
		<td><input type="button" class="btn" value="Del Line" onclick="delline(this)"/>
	</tr>
</table>


<%def name="select_widget(name,master,value)">
	<select name="${name}" style="width:150px">
		<option></option>
		%for m in getMaster(master):
			<option value="${m.id}" ${tw.attrs([('selected',m.id==value),])}>${m}</option>
		%endfor
	</select>
</%def>

<%def name="f(date_value,date_format='%Y-%m-%d')" filter="trim">
	%if date_value:
		${date_value.strftime(date_format)}
	%endif
</%def>
