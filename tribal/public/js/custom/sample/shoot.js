var shoot_html_tempalte = '<div class="shoot_html_template" style="display:none;">\
  <p>Select The Visible View(s)</p>\
  <table>\
      <tr>\
          <td width="25"><input type="radio" name="top_bottom" value="TOP"/></td>\
          <td>Top Side</td>\
          <td width="25"><input type="radio" name="top_bottom" value="BOTTOM"/></td>\
          <td>Bottom Side</td>\
      </tr>\
      <tr>\
          <td width="25"><input type="radio" name="left_right" value="LEFT"/></td>\
          <td>Left Side</td>\
          <td width="25"><input type="radio" name="left_right" value="RIGHT"/></td>\
          <td>Right Side</td>\
      </tr>\
      <tr>\
          <td width="25"><input type="radio" name="front_back" value="FRONT"/></td>\
          <td>Front Side</td>\
          <td width="25"><input type="radio" name="front_back" value="BACK"/></td>\
          <td>Back Side</td>\
      </tr>\
  </table>\
</div>' ; 


function add_shoot(parent_id){
    var content = '<tr><td width="35"><img title="Add" src="/images/plus.gif" onclick="add_shoot(\'shoot_ul\')"/><img title="Delete" src="/images/minus.gif" onclick="remove_shoot(this)"/></td><td width="350"><input type="text" class="shoot_widget input-300px" value="" ref=""/></td></tr>';
    var node = $(content);
    $('#'+parent_id).append(node);
    $('.shoot_widget',node).shoot_popup();
}


function remove_shoot(obj){
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
        shoot_popup: function(options) {

            //Set the default values, use comma to separate the settings, example:
            var defaults = {
                width : 260,
                height : 230,
                afterSave : function(){}
            }
            var options =  $.extend(defaults, options);
			var obj = $(this);
			
			function reset_values(){
                $("input[name='top_bottom']").removeAttr('checked');
				$("input[name='left_right']").removeAttr('checked');
				$("input[name='front_back']").removeAttr('checked');
			}
			
			function fill_values(v){
			    $("input[name='top_bottom']").radioval(v['top_bottom']);
                $("input[name='left_right']").radioval(v['left_right']);
                $("input[name='front_back']").radioval(v['front_back']);
			}
				
			function summary_values(v){
			    var txt = new Array();
			    if(v['top_bottom']=='TOP'){
			        txt.push("Top Side");
			    }else if(v['top_bottom']=='BOTTOM'){
                    txt.push("Bottom Side");
                }
                
                if(v['left_right']=='LEFT'){
                    txt.push("Left Side");
                }else if(v['left_right']=='RIGHT'){
                    txt.push("Right Side");
                }
                
                if(v['front_back']=='FRONT'){
                    txt.push("Front Side");
                }else if(v['front_back']=='BACK'){
                    txt.push("Back Side");
                }
			    
			    return txt.join("/");
			}
			
			function validate_values(v){
			    var msg = new Array();
			    if(!v['top_bottom'] && !v['left_right'] && !v['front_back']){
			        msg.push("Please select the 'Top/Bottom Side' or 'Left/Right Side' or 'Front/Back Side'.");
			    }		    
			    return msg;
			}
			
			function save_values(field){
			    var v = {};
			    v['top_bottom'] = $("input[name='top_bottom']").radioval();
                v['left_right'] = $("input[name='left_right']").radioval();
                v['front_back'] = $("input[name='front_back']").radioval();
			    v['SHOW_TEXT'] = summary_values(v);
			    var result = validate_values(v);
			    
			    if(result.length > 0){
			        alert(result.join('\n'));
			    }else{
			        field.attr('ref',JSON.stringify(v));
				    field.val(v['SHOW_TEXT']);			    
                    reset_values();
                    options.afterSave();
				    close_dialog();
			    }
			}
				   
			
			function show_dialog(field){               
                $(".shoot_html_template").dialog( "option", "buttons", 
				    {
				        "Save" : function() { save_values(field); }
				    }
				);
				$(".shoot_html_template").dialog('open');
			}
			
			function close_dialog(){
			    $(".shoot_html_template").dialog('close');
			}
            
            if($('.shoot_html_template').length<1){ 
                $("body").append(shoot_html_tempalte);
                $(".shoot_html_template .numeric").numeric();
                
				$(".shoot_html_template").dialog({ 
				    title : "Number Of Shoot(s)",
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

