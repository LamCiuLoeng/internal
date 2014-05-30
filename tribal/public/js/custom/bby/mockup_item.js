function ajaxSelect(queryString,parname){
    $.ajax({
	type:"GET",
	dataType:"json",
	data:{"component":queryString,'parname':parname},
	url: "/bbymockup/ajaxMaterialSpec",
	success: function(data,textStatus){
		if(data.active == 0){
			base_material  = data.base_material;
			base_spec = data.base_spec;
			base_front_color = data.base_front_color;
			base_back_color  = data.base_back_color;
			
			var material    = data.material?data.material.replace("{","").replace("}","").split(","):false
			var spec 	    = data.spec?data.spec.replace("{","").replace("}","").split(","):false
			var front_color = data.front_color?data.front_color.replace("{","").replace("}","").split(","):false
			var back_color  = data.back_color?data.back_color.replace("{","").replace("}","").split(","):false
			
			parse($("select[name='c_material_id"+parname+"']"),'c_material_id_x_y',material);
			parse($("select[name='c_coating_id"+parname+"']"),'c_coating_id_x_y',spec);
			parse($("select[name='c_front_color_id"+parname+"']"),'c_front_color_id_x_y',front_color);
			parse($("select[name='c_back_color_id"+parname+"']"),'c_back_color_id_x_y',back_color);
		}
		if(data.active == 1){
			$("select[name='c_material_id"+parname+"']").html("").html("<option></option>");
			$("select[name='c_coating_id"+parname+"']").html("").html("<option></option>");
			$("select[name='c_front_color_id"+parname+"']").html("").html("<option></option>");
			$("select[name='c_back_color_id"+parname+"']").html("").html("<option></option>");
		}
	},
	error: function(){
		alert(data.Msg)
	}
});
}
function parse(obj,cpobj,list){
	var options;
	var cpyobj = $("select[name='"+cpobj+"']")
	if(list){
    	if(list.toString().search(",")>-1){
    		var temp = []
	    	for( i in list ){
	    		temp.push($("<div></div>").append(cpyobj.children("option[value='"+list[i]+"']").clone()).html());
	    	}
	    	options = temp.join()
	    }else{
	    	options = $("<div></div>").append(cpyobj.children("option[value='"+list+"']").clone()).html();
	    }
    }
    else{
    	options = "<option></option>"
    }
    obj.html("").html(options)
    var name = obj.attr('name')
    if(name.search('c_material_id')>-1 && base_material){
    	obj.val(base_material)
    }
    if(name.search('c_coating_id')>-1 && base_spec){
    	obj.val(base_spec)
    }
    if(name.search('c_front_color_id')>-1 && base_front_color){
    	obj.val(base_front_color)
    }
    if(name.search('c_back_color_id')>-1 && base_back_color){
    	obj.val(base_back_color)
    }
    
}
var initSelete = function(){
	$("select").change(function(){
    	var name = $(this).attr("name");
    	var parname = name.substring(11);
    	if(name.search("format")>-1){
    		var queryString = $(this).val();
			ajaxSelect(queryString,parname);
		}
	})
}
var base_material;
var base_spec;
var base_front_color;
var base_back_color;
$(document).ready(function(){
	initSelete();
	$("select").each(function(){
		var name = $(this).attr("name")
		if(name.search("c_format_id")>-1){
			if(name.search("c_format_id_x_")==-1){
				var name_curr = name.substring(name.indexOf('_id_'));
				//base_material  = $("select[name='c_material"+name_curr+"']").val();
				//base_spec = $("select[name='c_coating"+name_curr+"']").val();
				//base_front_color = $("select[name='c_front_color"+name_curr+"']").val();
				//base_back_color  = $("select[name='c_back_color"+name_curr+"']").val();
				var parname = name.substring(11);
				var queryString = $(this).val();
				ajaxSelect(queryString,parname);
			}
		}
	})
	
	
})

function toSave(){
	if($(":checkbox[name^='o_final'][checked]").length > 1){
		alert("There's more than 1 option checked with 'Final',please modify before you save!");
		return;
	}
	
	var isOK = true;
	$("input[name^='o_name_'][name!='o_name_x']").each(function(){
		if($(this).val()){
			var id = $(this).attr("name").replace('o_name_','' );
			$("select[name^='c_format_id_" + id + "_']").each(function(){
				if(!$(this).val()){
					isOK = false;
				}
			});
		}
	});
	
	if(!isOK){
		alert('Please select at lease one component for the option!');
		return;
	}
	
	$(".bline,.sline").remove();
    $("form").submit();
}




function addbline(){
	var t = $(".bline");
	var n = t.clone();
	n.removeClass("bline");
	
	var index = count++;   	
	$("input,textarea,select",n).each(function(){
		var tmp = $(this);
		var new_name = tmp.attr("name").replace("_x","_"+index);
		tmp.attr("name",new_name);
		});
		
	$(".addDetail",n).attr("brow_index",index);    		
	$(t.parents("table")[0]).append(n);
	
	initSelete();
  }
  
function addsline(obj){
  	var btn = $(obj);
  
  	var t = $(".sline");
	var n = t.clone();
	n.removeClass("sline");
	
	var bindex = btn.attr("brow_index");
	var sindex = parseInt(btn.attr("srow_index"))+1;

	$("input,textarea,select",n).each(function(){
		var tmp = $(this);
		var new_name = tmp.attr("name").replace("_x","_"+bindex).replace("_y","_"+sindex);
		tmp.attr("name",new_name);
	});
	
	btn.attr("srow_index",sindex);
	var tr = $(btn.parents("tr")[0]);
	   	
	$("td:first-child,td:last-child,td:nth-child(11)",tr).each(function(){
		var tmp = $(this);
		tmp.attr("rowspan",parseInt(tmp.attr("rowspan")) + 1);
	});
	
	if(tr.hasClass("final")){
		n.addClass("final");
	}
	
	var nexttr = tr.nextAll("tr:has(input[name*='o_name_'])");
	if(nexttr.length>0){
		$(nexttr[0]).before(n);
	}else{
		$(tr.parents("table")[0]).append(n);
	}
	
	initSelete();
	
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
  	if($("input[name*='o_name_']",tr).length <1 ){	
	  	var btr = tr.prevAll("tr:has(input[name*='o_name_'])")[0];
    	
    	$("td:first-child,td:last-child,td:nth-child(11)",btr).each(function(){
    		var tmp = $(this);
    		tmp.attr("rowspan",parseInt(tmp.attr("rowspan")) - 1);
    	});	    	
  	}	  	
  	tr.remove();
  }

function final(obj){
	var t = $(obj);
	var tr = $(t.parents("tr")[0]);
	var r = parseInt($("td:first-child",tr).attr("rowspan"))-1;
	
	if(t.attr("checked")){
		tr.addClass("final");
		tr.nextAll("tr").each(function(){
	  		if(r>0){ 
	  			$(this).addClass("final");
	  			r--;
	  		}
	  	});
	
	}else{
		tr.removeClass("final");
		tr.nextAll("tr").each(function(){
	  		if(r>0){ 
	  			$(this).removeClass("final");
	  			r--;
	  		}
	  	});
	}
}

function copybline(obj){
	var tr = $($(obj).parents("tr")[0]);
	var table = $($(obj).parents("table")[0]);
	var new_id = count++;   	
	
	var n = tr.clone();
	var input_round = $("input[name^='o_name_']",n);
	var name = input_round.attr("name");
	var tokens = name.split("_")
	var old_id = tokens[tokens.length-1]; 
	input_round.attr("name",name.replace("_"+old_id,"_"+new_id));
	
	var input_final = $("input[name^='o_final_']",n);
	input_final.attr("name",input_final.attr("name").replace("_"+old_id,"_"+new_id));
	rename(n,old_id,new_id);
	$("input[brow_index]",n).attr("brow_index",new_id);
	table.append(n);
	
  	var rows = $("td:first-child",tr).attr("rowspan");
  	var r = parseInt(rows)-1; 	  	
  	tr.nextAll("tr").each(function(){
  		if(r>0){ 
  			var p = $(this).clone();
  			rename(p,old_id,new_id);
  			table.append(p);
  			r--;
  		}
  	});
  	
  	initSelete();
}


function rename(obj,old_id,new_id){
	var tr = (obj);
	$("input,select,textarea",tr).each(function(){
		var tmp = $(this);
		tmp.attr("name",tmp.attr("name").replace("_"+old_id+"_","_"+new_id+"_"));
	});
}
	