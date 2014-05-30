<%inherit file="tribal.templates.master"/>

<%
	from tribal.util.mako_filter import b,tp
	from tribal.util.common import Date2Text
	from tribal.util.bby_helper import getMaster,getPackagingFormat
%>

<%def name="extTitle()">r-pac</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/jquery-ui-1.7.3.custom.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/jquery.autocomplete.css" type="text/css" />
<link rel="stylesheet" href="/css/jquery.loadmask.css" type="text/css" media="screen"/>
<link rel="stylesheet" href="/css/custom/bby.css" type="text/css" media="screen"/>

	<style type="text/css">
	<!--
	body,td,th {
		font-family: Tahoma, Geneva, sans-serif;
		font-size: 12px;
		line-height: normal;
		color: #000;
		text-decoration: none;
	}

	
	.xxinput{
		background-color:#FFC;
		border:#069 solid 1px;
		width:150px;
		
		
	}
	.title-td{
		font-family: Tahoma, Geneva, sans-serif;
		font-size: 12px;
		line-height: normal;
		font-weight: bold;
		color: #069;
		text-decoration: none;
	}
	.right-td{
		text-align:right;
		padding-right:10px;
		
		font-family: Tahoma, Geneva, sans-serif;
		font-size: 12px;
		line-height: normal;
		font-weight: bold;
		color: #069;
		text-decoration: none;
	}
	.biaoge1 {
		border:#069 solid 1px;
	}
	
	.bline,.sline{
		display : none;
	}
	
	
	
	-->
	</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery-impromptu.1.5.js" language="javascript"></script>
<script type="text/javascript" src="/js/jquery.loadmask.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>

<script language="JavaScript" type="text/javascript">
	//<![CDATA[
		var dateFormat = 'yy-mm-dd';
		$(document).ready(function(){
		      $('.datePicker').datepicker({
		        changeMonth : true,
		        changeYear : true,
		        dateFormat : dateFormat
		      });
	      
	      	  $(".numeric").numeric();
		});
	      
		
	  function toSave(){
	  		var msg = Array();
	  	
	  		if(!$("#sku").val()){ msg.push("The SKU# could not be blank!"); }
			//if(!$("#pd_id").val()){ msg.push("Please select the option for PD."); }
			//if(!$("#ae_id").val()){ msg.push("Please select the option for AE."); }
	  
	  		if(msg.length<1){
		  		$(".template").remove();
				$("form").submit();
	  		}else{
	  			$.prompt(msg.join("<br />"),{opacity: 0.6,prefix:'cleanred'});
	  			return;
	  		}
		}
		
		
	  var count = 20
	  
	  function addbline(){
    	var t = $(".bline");
    	var n = t.clone();
    	n.removeClass("bline");
    	$('.datePicker',n).attr("id","");
    	
    	var index = count++;   	
    	$("input,textarea",n).each(function(){
    		var tmp = $(this);
    		var new_name = tmp.attr("name").replace("_x","_"+index);
    		tmp.removeClass("hasDatepicker");
    		tmp.attr("name",new_name);
    		});
    		
    	$(".addDetail",n).attr("brow_index",index);
    	$('.datePicker',n).datepicker({
		        changeMonth : true,
		        changeYear : true,
		        dateFormat : dateFormat
			});
    		
    	$(t.parents("table")[0]).append(n);
      }
      
      
      function addsline(obj){
      	var btn = $(obj);
      
      	var t = $(".sline");
    	var n = t.clone();
    	n.removeClass("sline");
    	$('.datePicker',n).attr("id","");
    	
    	var bindex = btn.attr("brow_index");
    	var sindex = parseInt(btn.attr("srow_index"))+1;

    	$("input,textarea",n).each(function(){
    		var tmp = $(this);
    		var new_name = tmp.attr("name").replace("_x","_"+bindex).replace("_y","_"+sindex);
    		tmp.removeClass("hasDatepicker");
    		tmp.attr("name",new_name);
    	});
    	
    	btn.attr("srow_index",sindex);
    	var tr = $(btn.parents("tr")[0]);
    	
    	var ftd = $("td:first-child",tr);
    	ftd.attr("rowspan",parseInt(ftd.attr("rowspan")) + 1);
    	
    	var ltd = $("td:last-child",tr);
    	ltd.attr("rowspan",parseInt(ltd.attr("rowspan")) + 1);
    	
    	$('.datePicker',n).datepicker({
		        changeMonth : true,
		        changeYear : true,
		        dateFormat : dateFormat
			});
    	
    	var nexttr = tr.nextAll("tr:has(input[name*='row_name_'])");
    	if(nexttr.length>0){
    		$(nexttr[0]).before(n);
    	}else{
    		$(tr.parents("table")[0]).append(n);
    	}
      }
      
      
    	
	  function delbline(obj){  	
	  	var tr = $($(obj).parents("tr")[0]);
	  	var rows = $("td:first-child",tr).attr("rowspan");
	  	var r = parseInt(rows)-1; 	  	
	  	tr.nextAll("tr").each(function(){
	  		if(r>0){ 
	  			$(this).remove(); 
	  			r--;
	  		}
	  	});
	  	tr.remove();
	  }
	  
	  function delsline(obj){
	  	var t = $(obj);
	  	var tr = $(t.parents("tr")[0]);
	  	
	  	if($("input[name*='row_name_']",tr).length <1 ){	
		  	var btr = tr.prevAll("tr:has(input[name*='row_name_'])")[0];
	  		var ftd = $("td:first-child",btr);
	    	ftd.attr("rowspan",parseInt(ftd.attr("rowspan")) - 1);
	    	var ltd = $("td:last-child",btr);
	    	ltd.attr("rowspan",parseInt(ltd.attr("rowspan")) - 1);
	  	}	  	
	  	tr.remove();
	  }
	  
		
		function getFileName(obj){
		    var tmp = $(obj);
			var path = tmp.val();
			if( path && path.length > 0){
				var location = path.lastIndexOf("\\") > -1 ?path.lastIndexOf("\\") + 1 : 0;
				var fn = path.substr( location,path.length-location );	
				var tr = tmp.parents("tr")[0];
				$("input[type='text'][name='"+ tmp.attr("name").replace('row_file_path','row_file_name') +"']",tr).val(fn);
			}
		}
		
				
		function confirmOption(obj){
	    	var t = $(obj);
	    	var td = $(t.parents("td")[0]);
	    	if(t.attr("checked")){
	    		td.prevAll(":lt(3)").addClass("confirm");
	    		td.addClass("confirm");
	    	}else{
	    		td.prevAll(":lt(3)").removeClass("confirm");
	    		td.removeClass("confirm");
	    	}
	    }
	    
	    
	    function changeAgent(obj){
	   		var t = $(obj);
	   		$.getJSON("/sku/getVendorByAgent",
	   			{"agent_id":t.val()},
	   			function(r){
	   				if(r.flag != 0){
	   					return;
	   				}else{
	   					var a = $("#vendor_id");
	   					a.html('<option></option>');
	   					for(var i=0;i<r.vendors.length;i++){
	   						var o = r.vendors[i];
	   						a.append('<option value="'+o[0]+'">'+o[1]+'</option>');
	   					}
	   				}
	   			}) 
	    }
	    
	//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="175" valign="top" align="left"><a href="/sku/index"><img src="/images/mainmenu_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;BBY&nbsp;&nbsp;&gt;&nbsp;&nbsp;New SKU</div>



<!-- Main content begin -->
<div style="overflow:hidden;margin:5px 0px 10px 10px">
   
<form action="/sku/save_new" method="post"  enctype="multipart/form-data">
    
	<table border="1" cellpadding="3" cellspacing="0">
			<tr>
				<td width="150" height="30" class="title-td">SKU#</td>
			  	<td width="250"><input name="sku" id="sku" type="text" class="xxinput" value=""/></td>
			  	<td width="150" height="30" class="title-td">Brand</td>
		   		<td width="250">
		   			<select name="brand_id" id="brand_id" class="xxinput">
		   				<option></option>
		   				%for b in getMaster("BBYBrand"):
		   					<option value="${b.id}">${b}</option>
		   				%endfor
		   			</select>
		   		</td>
		  	</tr>
			<tr>
				<td width="150" height="30" class="title-td">Agent</td>
		   		<td width="250">
		   			<select name="agent_id" id="agent_id" class="xxinput" onchange="changeAgent(this)">
		   				<option></option>
		   				%for b in getMaster("BBYAgent"):
		   					<option value="${b.id}">${b}</option>
		   				%endfor
		   			</select>
		   		</td>
				<td width="150" class="title-td">Vendor</td>
				<td width="250">
					<select name="vendor_id" class="xxinput" id="vendor_id">
						<option></option>
						%for vendor in getMaster("BBYVendor"):
							<option value="${vendor.id}">${vendor}</option>
						%endfor
					</select>
				</td>
		  </tr>
			<tr>
				<td width="150" height="30" class="title-td">Package Format</td>
				<td width="200">
					<select name="packaging_format_id" class="xxinput" id="packaging_format_id">
				  		<option></option>
						%for pf in getPackagingFormat():
							<option value="${pf.id}">${pf}</option>
						%endfor
					</select>
			  </td>
				<td width="150" class="title-td">UPC#</td>
				<td><input name="upc_no" id="upc_no" type="text" class="xxinput" value=""/></td>
		  </tr>
			<tr>
				<td width="150" height="30" class="title-td">Closure</td>
				<td width="200">
					<select name="closure_id" class="xxinput" id="closure_id">
				  		<option></option>
						%for c in getMaster("BBYClosure"):
							<option value="${c.id}">${c}</option>
						%endfor
					</select>
			  </td>
				<td width="150" class="title-td">Display Mode</td>
				<td>
					<select name="display_mode_id" id="display_mode_id" class="xxinput">
						<option></option>
						%for d in getMaster("BBYDisplayMode"):
							<option value="${d.id}">${d}</option>
						%endfor
					</select>
				</td>
		  </tr>
			<tr>
				<td width="150" height="30" class="title-td">IOQ</td>
		    	<td width="200"><input name="ioq" id="ioq" type="text" class="xxinput numeric" value=""/></td>
				<td width="150" class="title-td">AOQ</td>
				<td><input name="aoq" id="aoq" type="text" class="xxinput numeric" value=""/></td>
		  </tr>
			<tr>
				<td width="150" height="30" class="title-td">Product Descrption</td>
			  	<td colspan="3"><textarea name="product_description" id="product_description" class="xxinput"></textarea></td>
		  </tr>
			<tr>
				<td width="150" height="30" class="title-td">PD</td>
				<td>
					<select name="pd_id" class="xxinput" id="pd_id">
				  		<option></option>
						%for pd in getMaster("BBYTeammate"):
							<option value="${pd.id}">${pd}</option>
						%endfor
					</select>
			  </td>
				<td class="title-td">AE</td>
				<td>
					<select name="ae_id" id="ae_id" class="xxinput">
						<option></option>
						%for ae in getMaster("BBYTeammate"):
							<option value="${ae.id}">${ae}</option>
						%endfor
					</select>
				</td>
		  </tr>
		  <tr>
				<td width="150" height="30" class="title-td">Formed Size</td>
				<td colspan="3"><input type="text" name="formed_size_l" value="" class="xxinput numeric"/> x <input type="text" name="formed_size_w" value="" class="xxinput numeric"/> x <input type="text" name="formed_size_h" value="" class="xxinput numeric"/>&nbsp;&nbsp;(L * W * H  Unit:inch)</td>
			</tr>
			<tr>
				<td width="150" height="30" class="title-td">Asia Packaging Team Contact</td>
				<td>
					<select name="bby_asia_contact_id" class="xxinput" id="bby_asia_contact_id">
				  		<option></option>
						%for ct in getMaster("BBYContact"):
							<option value="${ct.id}">${ct}</option>
						%endfor
					</select>
			  </td>
				<td class="title-td">US Packaging Team Contact</td>
				<td>
					<select name="bby_us_contact_id" id="bby_us_contact_id" class="xxinput">
						<option></option>
						%for ct in getMaster("BBYContact"):
							<option value="${ct.id}">${ct}</option>
						%endfor
					</select>
				</td>
		  </tr>
		</table>
		
		<br />
		
		
		<p class="red"><sup>*</sup> The 'Date' field for each detail line is required, otherwise the related attachment and remark won't save for the system !</p>
	
	
		<table border="1" cellpadding="3" cellspacing="0">
			<thead>
				<tr>
					<td style="width:150px">Item</td>
					<td style="width:150px">Date</td>
					<td style="width:400px">Attachment</td>
					<td style="width:150px">Remark</td>
					<td style="width:50px">Confirm</td>
					<td colspan="2" style="width:200px"><input type="button" class="btn" value="Add Line" onclick="addbline()"></td>
				</tr>
			</thead>
			%for i,v in enumerate(["PIF","Product Sample Photo","3D Drawing","Die Line","Fit Waiver","Test Waiver",]):
				${show_row(i+10,v)}
			%endfor
			
			<tr class="bline">
				<td rowspan="1"><input type="text" name="row_name_x" value="" class="xxinput"/></td>
				<td><input type="text" name="row_date_x" value="" class="datePicker xxinput"/></td>
				<td><input type="text" name="row_file_name_x" value="" class="xxinput file_name"/>&nbsp;<input type="file" name="row_file_path_x" value="" onchange="getFileName(this)"/></td>
				<td><textarea name="row_remark_x" class="xxinput"></textarea></td>
				<td><input type="checkbox" name="row_confirm_x" value="Y" onclick="confirmOption(this);"/>&nbsp;YES</td>
				<td>&nbsp;</td>
				<td>
					<input type="button" class="btn addDetail" value="Add Detail"  brow_index="" srow_index="10"  onclick="addsline(this)"/>&nbsp;
					<input type="button" class="btn" value="Del Line" onclick="delbline(this);"/>
				</td>
			</tr>
			<tr class="sline">
				<td><input type="text" name="row_date_x_y" value="" class="datePicker xxinput"/></td>
				<td><input type="text" name="row_file_name_x_y" value="" class="xxinput file_name"/>&nbsp;<input type="file" name="row_file_path_x_y" value="" onchange="getFileName(this)"/></td>
				<td><textarea name="row_remark_x_y" class="xxinput"></textarea></td>
				<td><input type="checkbox" name="row_confirm_x_y" value="Y" onclick="confirmOption(this);"/>&nbsp;YES</td>
				<td><input type="button" class="btn" value="Del Detail" onclick="delsline(this);"/></td>
			</tr>
		</table>
	
</form>
	

	
</div>
<!-- Main Content end -->



<%def name="show_row(i,v)">
	<tr>
		<td rowspan="1"><input type="text" name="row_name_${i}" value="${v}" class="xxinput"/></td>
		<td><input type="text" name="row_date_${i}" value="" class="datePicker xxinput"/></td>
		<td><input type="text" name="row_file_name_${i}" value="" class="xxinput file_name"/>&nbsp;<input type="file" name="row_file_path_${i}" value="" onchange="getFileName(this)"/></td>
		<td><textarea name="row_remark_${i}" class="xxinput"></textarea></td>
		<td><input type="checkbox" name="row_confirm_${i}" value="Y" onclick="confirmOption(this);"/>&nbsp;YES</td>
		<td style="width:80px">&nbsp;</td>
		<td rowspan="1">
			<input type="button" class="btn" value="Add Detail" brow_index="${i}" srow_index="10" onclick="addsline(this)"/>&nbsp;
		</td>
	</tr>
</%def>