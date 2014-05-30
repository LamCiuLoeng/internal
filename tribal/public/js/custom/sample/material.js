var material_html_tempalte = '<div class="material_html_template" style="display:none;">\
  <ul class="form-ul">\
    <li>\
      <input type="radio" id="material_type_cards" onclick="check(this)" value="FOLDING_CARDS" name="material_type">\
      Folding Cards\
      <ul>\
        <li>\
          <input type="radio" onclick="check(this)" value="CCNB" name="folding_cards_type" id="material_CCNB">\
          <label for="material_CCNB">CCNB</label>\
          <input type="radio" onclick="check(this)" value="C1S" name="folding_cards_type" id="material_C1S">\
          <label for="material_C1S">C1S</label>\
          <input type="radio" onclick="check(this)" value="C2S" name="folding_cards_type" id="material_C2S">\
          <label for="material_C2S">C2S</label>\
          <input type="radio" onclick="check(this)" value="OTHER" name="folding_cards_type" id="material_Other">\
          <label for="material_Other">Other </label>\
          <input type="text" value="" name="folding_cards_other" id="material_Others" class="input-150px inputText">\
        </li>\
        <li>\
          <table>\
                <tr>\
                    <td width="100">Specification</td>\
                    <td>\
                      <input type="radio" id="paper_thicknesss" onclick="check(this)" value="PAPER" name="paper_thickness_type">\
                      Paper Thickness\
                      <input type="text" class="input-50px numeric" value="" id="paper_thickness" name="paper_thickness">\
                      &nbsp;&nbsp;\
                      <input type="radio" onclick="check(this)" value="pt" name="paper_thickness_unit" id="paper_thickness_unit_pt">\
                      <label for="paper_thickness_unit_pt">pt</label>\
                      <input type="radio" onclick="check(this)" value="mm" name="paper_thickness_unit" id="paper_thickness_unit_mm">\
                      <label for="paper_thickness_unit_mm">mm</label>\
                    </td>\
                </tr>\
                <tr>\
                    <td>&nbsp;</td>\
                    <td>\
                      <input type="radio" id="paper_gramage" onclick="check(this)" value="GRAMAGE" name="paper_thickness_type">\
                      <label for="gramage">Grammage:</label>\
                      <input type="text" class="input-50px numeric" value="" id="gramage" name="gramage_gsm"> gsm \
                    </td>\
                </tr>\
                <tr>\
                    <td>&nbsp;</td>\
                    <td>\
                        <input type="radio" id="paper_gramage" onclick="check(this)" value="NO" name="paper_thickness_type"> No Specification Details \
                    </td>\
                </tr>\
            </table>\
        </li>\
      </ul>\
    </li>\
  </ul>\
  <ul class="form-ul">\
    <li>\
      <input type="radio" id="material_corrugated" onclick="check(this)" value="CORRUGATED" name="material_type">\
      Corrugated\
      <ul>\
        <li>\
          <input type="text" class="input-150px" value="" id="flute" name="flute">\
          <label for="flute"> Flute </label>\
          <p></p>\
          <p>\
            <input type="radio" onclick="check(this)" value="KRAFT" name="flute_type" id="flute_type_kraft">\
            <label for="flute_type_kraft">Kraft Top</label>\
            <input type="radio" onclick="check(this)" value="MOTTLE" name="flute_type" id="flute_type_mottle">\
            <label for="flute_type_mottle">Mottle White Top</label>\
            <input type="radio" onclick="check(this)" value="CCNB" name="flute_type" id="flute_type_ccnb">\
            <label for="flute_type_gsm">CCNB Top</label>\
            <input type="text" class="input-100px numeric" value="" id="flute_type_gsm" name="flute_type_gsm">\
            gsm </p>\
        </li>\
        <li>\
          <table>\
                <tr>\
                    <td width="100">Specification</td>\
                    <td><input type="radio" onclick="check(this)" value="BURSTING" name="corrugated_spec">Bursting:</td>\
                    <td><input type="text" class="input-100px numeric" value="" id="bursting" name="bursting"></td>\
                </tr>\
                <tr>\
                    <td>&nbsp;</td>\
                    <td><input type="radio" onclick="check(this)" value="ECT" name="corrugated_spec">ECT:</td>\
                    <td><input type="text" class="input-100px numeric" value="" id="ect" name="ect"></td>\
                </tr>\
                <tr>\
                    <td>&nbsp;</td>\
                    <td><input type="radio" onclick="check(this)" value="GRAMMAGE" name="corrugated_spec">Grammage:</td>\
                    <td><input type="text" class="input-100px" value="" id="gramage" name="gramage"></td>\
                </tr>\
                <tr>\
                    <td>&nbsp;</td>\
                    <td colspan="2"><input type="radio" onclick="check(this)" value="NO" name="corrugated_spec">No Specification Details</td>\
                </tr>\
            </table>\
        </li>\
      </ul>\
    </li>\
  </ul>\
  <ul class="form-ul">\
    <li>\
      <input type="radio" onclick="check(this)" value="OTHER" name="material_type" id="material_type_other">\
      <label for="material_type_other">Other</label>\
      <input type="text" class="input-300px" value="" id="material_type_other_content" name="material_type_other_content">\
    </li>\
    <li>\
      <input type="radio" onclick="check(this)" value="PROVIDED" name="material_type" id="material_provided">\
      <label for="material_provided">Material Provided</label>\
    </li>\
    <li>\
      <input type="radio" onclick="check(this)" value="SUGGESTED" name="material_type" id="according_files">\
      <label for="according_files">Suggested By PD Team</label>\
    </li>\
  </ul>\
</div>' ; 


function dump_props(obj, objName) {
   var result = ""
   for (var i in obj) {
      result += objName + "." + i + " = " + obj[i] + "<BR>"
   }
   result += "<HR>"
   return result
} 


function add_material(parent_id){
    var content = '<tr><td width="35"><img title="Add" src="/images/plus.gif" onclick="add_material(\'material_ul\')"/><img title="Delete" src="/images/minus.gif" onclick="remove_material(this)"/></td><td width="350"><input type="text" class="material_widget input-300px" value="" ref=""/></td></tr>';
    var node = $(content);
    $('#'+parent_id).append(node);
    $('.material_widget',node).material_popup();
}


function remove_material(obj){
    $($(obj).parents("tr")[0]).remove();
}


(function($){
    $.fn.extend({ 
        //pass the options variable to the function
        radioval: function() {
            if(arguments.length < 1){
                return $(this).filter("[checked]").val();
            }else{
                $(this).removeAttr('checked');
                //add   .attr('defaultChecked','true') to fix the IE problem             
                $(this).filter("[value='" + arguments[0] +"']").attr('defaultChecked','true').attr('checked','true'); 
            }
        }
    })
})(jQuery);





(function($){
    $.fn.extend({ 
        //pass the options variable to the function
        material_popup: function(options) {

            //Set the default values, use comma to separate the settings, example:
            var defaults = {
                width : 530,
                height : 480,
                afterSave : function(){}
            }
            var options =  $.extend(defaults, options);
			var obj = $(this);
			
			function reset_values(){
                $("input[name='material_type']").removeAttr('checked');
				$("input[name='folding_cards_type']").removeAttr('checked');
                $("input[name='folding_cards_other']").val('');
                $("input[name='paper_thickness_type']").removeAttr('checked');
                $("input[name='paper_thickness']").val('');
                $("input[name='paper_thickness_unit']").removeAttr('checked');
                $("input[name='gramage_gsm']").val('');
			    $("input[name='flute']").val('');
			    $("input[name='flute_type']").removeAttr('checked');
			    $("input[name='flute_type_gsm']").val('');
                $("input[name='bursting']").val('');
                $("input[name='ect']").val('');
                $("input[name='gramage']").val('');
                $("input[name='material_type_other_content']").val('');
                $("input[name='corrugated_spec']").removeAttr('checked');
			}
			
			function fill_values(v){
			    //$("input[name='material_type']").radioval('CORRUGATED');
			    for (var i in v) {v[i] = rpb(v[i]);}
			    $("input[name='material_type']").radioval(v['material_type']);
                $("input[name='folding_cards_type']").radioval(v['folding_cards_type']);
                $("input[name='folding_cards_other']").val(v['folding_cards_other']);
                $("input[name='paper_thickness_type']").radioval(v['paper_thickness_type']);
                $("input[name='paper_thickness']").val(v['paper_thickness']);
                $("input[name='paper_thickness_unit']").radioval(v['paper_thickness_unit']);
                $("input[name='gramage_gsm']").val(v['gramage_gsm']);
                $("input[name='flute']").val(v['flute']);
                $("input[name='flute_type']").radioval(v['flute_type']);
                $("input[name='flute_type_gsm']").val(v['flute_type_gsm']);
                $("input[name='bursting']").val(v['bursting']);
                $("input[name='ect']").val(v['ect']);
                $("input[name='gramage']").val(v['gramage']);
                $("input[name='material_type_other_content']").val(v['material_type_other_content']);
                $("input[name='corrugated_spec']").radioval(v['corrugated_spec']);
			}
				
			function summary_values(v){
			    var txt = '';
			    if(v['material_type']=="OTHER"){ txt = v['material_type_other_content'];
			    }else if(v['material_type']=="PROVIDED"){ txt = "Material Provided";
			    }else if(v['material_type']=="SUGGESTED"){ txt = "Suggested By PD Team";
			    }else if(v['material_type']=="FOLDING_CARDS"){
			    
			        var prefix='';
			        var subfix = '';
			        
			        if(v['paper_thickness_type']=='PAPER'){
			            prefix = v['paper_thickness'] + v['paper_thickness_unit'];
			        }else if(v['paper_thickness_type']=='GRAMAGE'){
			            prefix = v['gramage_gsm'] + 'g';
			        }

			        if(v['folding_cards_type'] == 'OTHER'){ 
			            subfix = v['folding_cards_other'];
			        }else{
			            subfix = v['folding_cards_type'];
			        }

			        if(prefix){
			            txt = prefix + ' ' + subfix;
			        }else{
			            txt = subfix;
			        }

			    }else if(v['material_type']=="CORRUGATED"){
			       if(v['flute_type'] == 'KRAFT'){
			           if(v['corrugated_spec']=='BURSTING'){ txt = v['bursting']+'#'+v['flute']+'-Kraft'; }
			           else if(v['corrugated_spec']=='ECT'){ txt = v['ect']+'ECT '+v['flute']+'-Kraft'; }
			           else if(v['corrugated_spec']=='GRAMMAGE'){ txt = v['flute']+'-Kraft'+'('+v['gramage']+'g)'; }
			           else{ txt = v['flute']+'-Kraft' }
			       }else if(v['flute_type'] == 'MOTTLE'){
			           if(v['corrugated_spec']=='BURSTING'){ txt = v['bursting']+'#'+v['flute']+'-MW'; }
                       else if(v['corrugated_spec']=='ECT'){ txt = v['ect']+'ECT '+v['flute']+'-MW'; }
                       else if(v['corrugated_spec']=='GRAMMAGE'){ txt = v['flute']+'-MW'+'('+v['gramage']+'g)'; }
			           else{ txt = v['flute']+'-MW'; }
			       }else if(v['flute_type'] == 'CCNB'){
			           if(v['corrugated_spec']=='BURSTING'){ txt = v['flute_type_gsm']+'g CCNB + '+v['flute']+'-Flute ('+v['bursting']+'#)'; }
                       else if(v['corrugated_spec']=='ECT'){ txt = v['flute_type_gsm']+'g CCNB + '+v['flute']+'-Flute ('+v['ect']+'ECT)'; }
                       else if(v['corrugated_spec']=='GRAMMAGE'){ txt = v['flute_type_gsm']+'g CCNB + '+v['flute']+'-Flute ('+v['gramage']+'g)'; }
			           else{ txt = v['flute_type_gsm']+'g CCNB + '+v['flute']+'-Flute'; }
			       }
			    }
			    return txt;
			}
			
			function validate_values(v){
			    var msg = new Array();
			    if(!v['material_type']){
			        msg.push("Please select the 'Material'.");
			    }		    
			    if(v['material_type'] == 'FOLDING_CARDS'){
			        if(!v['folding_cards_type']){ msg.push("Please select the 'Folding Cards' type."); }
			        if(v['folding_cards_type']=='OTHER' && !v['folding_cards_other']){ 
			            msg.push("Please input the content also if you select the 'Others' option.");
			        }else if(v['folding_cards_type']!='OTHER'){
				        if(!v['paper_thickness_type']){ msg.push("Please select the 'Folding Cards Specification'."); }
				        if(v['paper_thickness_type'] == 'PAPER' ){
				            if(!v['paper_thickness']){ msg.push("Please input the content also if you select the 'Paper thickness' option."); }
				            if(!v['paper_thickness_unit']){ msg.push("Please select the unit also if you select the 'Paper thickness' option."); }
				        }
				        if(v['paper_thickness_type']=='GRAMAGE' && !v['gramage_gsm']){ msg.push("Please input the content also if you select the 'Grammage' option."); }
			        } 
			    }else if(v['material_type'] == 'CORRUGATED'){
			        if(!v['flute']){ msg.push("Please input the 'Flute'."); }
			        if(!v['flute_type']){ msg.push("Please select the content also if you select the 'Corrugated' option."); }
			        if(v['flute_type']== 'CCNB' && !v['flute_type_gsm']){ msg.push("Please input the CCNB Top value."); }
			        
			        if(!v['corrugated_spec']){
			            msg.push("Please select the Corrugated Specification.");
			        }else{
			            if(v['corrugated_spec'] == 'BURSTING' && !v['bursting']){
			                msg.push("Please input the content if you select 'Bursting' in Corrugated Specification.");
			            }else if(v['corrugated_spec'] == 'ECT' && !v['ect']){
			                msg.push("Please input the content if you select 'ECT' in Corrugated Specification.");
			            }else if(v['corrugated_spec'] == 'GRAMMAGE' && !v['gramage']){
			                msg.push("Please input the content if you select 'Grammage' in Corrugated Specification.");
			            }
			        }
 
			        //if(!v['bursting'] &&!v['ect'] &&!v['gramage']){ msg.push("Please input either Bursting or ECT or Grammage."); }
			        
			    }else if(v['material_type'] == 'OTHER'){
			        if(!v['material_type_other_content']){ msg.push("Please fill in the content if you select the 'other' option.'."); }
			    }
			    
			    return msg;
			}
			
			function save_values(field){
			    var v = {};
			    v['material_type'] = $("input[name='material_type']").radioval();
			    v['folding_cards_type'] = $("input[name='folding_cards_type']").radioval();
			    v['folding_cards_other'] = $("input[name='folding_cards_other']").val();
			    v['paper_thickness_type'] = $("input[name='paper_thickness_type']").radioval();
			    v['paper_thickness'] = $("input[name='paper_thickness']").val();
			    v['paper_thickness_unit'] = $("input[name='paper_thickness_unit']").radioval();
			    v['gramage_gsm'] = $("input[name='gramage_gsm']").val();
			    v['flute'] = $("input[name='flute']").val();
			    v['flute_type'] = $("input[name='flute_type']").radioval();
			    v['flute_type_gsm'] = $("input[name='flute_type_gsm']").val();
			    v['bursting'] = $("input[name='bursting']").val();
			    v['ect'] = $("input[name='ect']").val();
			    v['gramage'] = $("input[name='gramage']").val();
			    v['material_type_other_content'] = $("input[name='material_type_other_content']").val();
			    v['corrugated_spec'] = $("input[name='corrugated_spec']").radioval();
			    v['SHOW_TEXT'] = summary_values(v);
			    
			    var result = validate_values(v);
			    
			    if(result.length > 0){
			        alert(result.join('\n'));
			    }else{
				    field.val(v['SHOW_TEXT']);    
			    	for (var i in v) {v[i] = rp(v[i]);}
			        field.attr('ref',JSON.stringify(v));
                    reset_values();
                    options.afterSave();
				    close_dialog();
			    }
			}
				   
			
			function show_dialog(field){               
                $(".material_html_template").dialog( "option", "buttons", 
				    {
				        "Save" : function() { save_values(field); }
				    }
				);
				$(".material_html_template").dialog('open');
			}
			
			function close_dialog(){
			    $(".material_html_template").dialog('close');
			}
			
			function rp(v){
				if( v == undefined ) { return v ;}
				return v.replace(/"/g,"%22").replace(/'/g,"%27").replace(/</g,"%3C").replace(/>/g,"%3E");
				//return escape(v);
			}

			function rpb(v){
			    if( v == undefined ) { return v ;}
				return v.replace(/%22/g,'"').replace(/%27/g,"'").replace(/%3C/g,"<").replace(/%3E/g,">");
				//return unescape(v);
			}
            
            if($('.material_html_template').length<1){ 
                $("body").append(material_html_tempalte);
                $(".material_html_template .numeric").numeric();
                
				$(".material_html_template").dialog({ 
				    title : "Material Info",
				    autoOpen: false,
				    width : options.width,
				    height : options.height,
				    modal : true,
				    bgiframe:true,
					close: function(event, ui) {
					   reset_values();
					} 
				});
				
            }
			
				    
            return obj.each(function(){
                var item = $(this);
				//bind the handler to the click event
				item.bind('click',function(){
				    var store_values = item.attr('ref');
				    if(!store_values){ store_values = '{}';}
				    fill_values(JSON.parse(store_values));
				    show_dialog(item);
				})
            });
            			
        }
    });
     
})(jQuery);

