<%inherit file="tribal.templates.master"/>
<%
	from tribal.util.mako_filter import b
        from tribal.util.common import Date2Text
        from datetime import datetime as dt
        from tribal.util.dba_util import nextMonth
%>
<%
my_page = tmpl_context.paginators.collections
pager = my_page.pager(symbol_first="<<",show_if_single_page=True)
%>

<%def name="extTitle()">r-pac - DIM</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.3/themes/base/jquery-ui.css" />
<link rel="stylesheet" href="/css/jquery.autocomplete.css" />
<link rel="stylesheet" href="/css/nyroModal.css" />
<link rel="stylesheet" href="/css/custom/dba.css" />
<link rel="stylesheet" href="/css/order_form.css" />
</%def>
<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery-ui-1.7.3.custom.min.js"></script>
<script type="text/javascript" src="/js/jquery.autocomplete.pack.js"></script>
<script type="text/javascript" src="/js/jquery.nyroModal-1.6.2.min.js"></script>
<script type="text/javascript" src="/js/numeric.js"></script>
<script type="text/javascript" src="/js/custom/dba.js"></script>
<script>
    $(function(){
        resetBtn();
        $('a.nyroModal').nyroModal();
        $('div.r a').click(function(){
            var undefinded;
            var href = $(this).attr('href');
            href = href.replace(/ids=[^&$]*/, 'ids=' + get_add_ids().join(','));
            if(undefinded != $("input[name=input_add_qty]:first").val()){

                href = href.replace(/old_ids=[^&$]*/, 'old_ids=' + get_add_ids().join('_'));
                href = href.replace(/h_input_add_qty=[^&$]*/, 'h_input_add_qty=' + get_values('input_add_qty').join('_'));
                href = href.replace(/h_add_qty=[^&$]*/, 'h_add_qty=' + get_values('add_qty').join('_'));
                href = href.replace(/h_input_forecast_qty=[^&$]*/, 'h_input_forecast_qty=' + get_values('input_forecast_qty').join('_'));
                href = href.replace(/h_forecast_qty=[^&$]*/, 'h_forecast_qty=' + get_values('forecast_qty').join('_'));
                
            }
           $(this).attr('href', href);
        });
    })
    var resetBtn = function(){
        var addBtn=false,saveBtn=false;
        $(".cboxClass:checked").each(function(i, obj){addBtn=true;})
        $("input[name='input_add_qty']").each(function(i,jq){saveBtn=true;})
        if(!addBtn) disableBtn('#btn_add_to_job', true);
        else disableBtn('#btn_add_to_job', false);
        if(!saveBtn) disableBtn(['#btn_save_to_job'], true);
        else disableBtn(['#btn_save_to_job'], false);
    }
    var addToJob = function(){
        var ids = get_add_ids().length>0 ? get_add_ids()+',' : ''
        $('#ids').val(ids+getCboxStr());
        $('#hidden_po').val($('#po').val());
        $('#hidden_sob').val($('#sob').val());

        var undefinded;

        //alert($("input[name=input_add_qty]:first").val());
        if(undefinded != $("input[name=input_add_qty]:first").val()){
            if('' != ids ){
                $('#old_ids').val(get_add_ids().join('_'));
                $('#h_input_add_qty').val(get_values('input_add_qty').join('_'));
                $('#h_add_qty').val(get_values('add_qty').join('_'));
                $('#h_input_forecast_qty').val(get_values('input_forecast_qty').join('_'));
                $('#h_forecast_qty').val(get_values('forecast_qty').join('_'));
            }
           
        }else{
           $('#old_ids').val('');
           $('#h_input_add_qty').val('');
           $('#h_add_qty').val('');
           $('#h_input_forecast_qty').val('');
           $('#h_forecast_qty').val('');
        }
        toSearch();

    }

    var search_h = function(){
         $('#ids').val(get_add_ids().join(','))
        changeValues()
        toSearch();
    }

    var changeValues = function(){
         var ids = get_add_ids().length>0 ? get_add_ids()+',' : ''

         var undefinded;
        //alert($("input[name=input_add_qty]:first").val());
        if(undefinded != $("input[name=input_add_qty]:first").val()){
            if('' != ids ){
                $('#old_ids').val(get_add_ids().join('_'));
                $('#h_input_add_qty').val(get_values('input_add_qty').join('_'));
                $('#h_add_qty').val(get_values('add_qty').join('_'));
                $('#h_input_forecast_qty').val(get_values('input_forecast_qty').join('_'));
                $('#h_forecast_qty').val(get_values('forecast_qty').join('_'));
            }

        }
    }

    var delItem = function(obj){
        $(obj).parent().parent().remove();
         var ids = get_add_ids()
        $('#ids').val(ids.join(','));
        resetBtn()
        
        $('div.r a').each(function(){
               var href = $(this).attr('href');
               if(href.indexOf('&ids=') > -1){
                    href = href.replace(/&ids=[^&$]*/, '&ids=' + ids.join(','));
                    $(this).attr('href', href);
               }else{
                    $(this).attr('href', href + '&ids=' + ids.join(','));
               }
         });

    }
    var saveToJob = function(){
        var validate=true, msg=[];     
        $("input[name='input_add_qty']").each(function(i, obj){
            if($(obj).val()=='')validate=false;
            //qtys.push($(obj).val())
        })
        $("input[name='add_qty']").each(function(i, obj){
            if($(obj).val()=='')validate=false;
            //qtys.push($(obj).val())
        })
        $("input[name='input_forecast_qty']").each(function(i, obj){
            if($(obj).val()=='')validate=false;
            //forecast_qtys.push($(obj).val())
        })
        $("input[name='forecast_qty']").each(function(i, obj){
            if($(obj).val()=='')validate=false;
            //forecast_qtys.push($(obj).val())
        })
        if('' == $('#po').val()) msg.push('Please input PO#!')
        if('' == $('#bill_to').val()) msg.push('Please input BILL TO!')
        if('' == $('#ship_to').val()) msg.push('Please input SHIP TO!')
        if(!validate) msg.push('Please input qty and forecast qty at all the text field!')
        if(msg.length==0){
            $("#save_form").submit();
        }else{
            showError(msg.join('<br/>'))
        }
    }
    var get_add_ids = function(){
        var ids=[]
        $("input[name='add_id']").each(function(i, obj){ids.push($(obj).val())})
        return ids;
    }

    var get_values = function(str){
        var values=[]
        $("input[name='"+ str +"']").each(function(i, obj){values.push($(obj).val())})
        return values;
    }
    
    var selectAll = function(obj){
        $(obj).attr("checked") ? $("tbody :checkbox").attr("checked","checked") : $("tbody :checkbox").removeAttr("checked")
        resetBtn();
    }
    var selectOne = function(obj){
        $('#header_checkbox').removeAttr("checked");
        resetBtn();
    }
    var autoQty = function(obj, prefix, id){
        $('#' + prefix + id).val(returnQty($(obj).val()));
        changeValues();
    }
    var returnQty=function(qty){
        return_qty = qty<=0?0:qty;
    //alert(return_qty)
        if(qty % 200 > 0){
            return_qty = (Math.floor(qty/200) + 1)*200
        }
        return  return_qty
     }

     
    
</script>
</%def>


<div class="nav-tree">DIM&nbsp;&nbsp;&gt;&nbsp;&nbsp;Order Form</div>

%if add_items and customer:
<div class="box2">
    <div class="toggle1"><a class="hid_a" href="javascript:void(0)" onclick="toggleIcon(this)"></a>Order Setup List</div>
    <div style="margin-left:20px;">
        <p>
            <span class="STYLE3">Note:</span><br />
            <!--1)&nbsp;&nbsp;Please note that online ordering period is in between <span class="STYLE3">5th</span> and <span class="STYLE3">25th</span>.
            The system will close at <span class="STYLE3">25th midnight (HK time)</span> and re-open next month.
            <br />
            2)-->&nbsp;&nbsp;The order quantity will be round up to <span class="STYLE3">200pcs</span>. For example, the order quantity will be rounded up to 2200pcs automatically if it is 2097pcs.
        </p>
    </div>
    <div>
        <form id="save_form" action="/dba/saveOrder" method="post">
        <table class="gridTable" cellpadding="0" cellspacing="0" border="0" >
            <thead>
                <tr>
                    <td colspan="100" style="border-right:0px;border-bottom:0px;">
                        <div class="toolbar">
                            <div class="l">
                                <table class="gridTable" cellpadding="0" cellspacing="0" border="0" width="100%">
                                    <tr>
                                        <td style="border-top:1px solid #CCCCCC;border-left:1px solid #CCCCCC;">Customer Name:</td>
                                        <td style="border-top:1px solid #CCCCCC;">${customer.name}</td>
                                        <td style="border-top:1px solid #CCCCCC;"><span class="STYLE3">Customer PO#</span>:</td>
                                        <td style="border-top:1px solid #CCCCCC;"><input id="po" type="text" name="po" value="${hidden_po}" style="width:96%;"/></td>
                                    </tr>
                                    <tr>
                                        <td style="border-left:1px solid #CCCCCC;"><span class="STYLE3">BILL TO</span>:</td>
                                        <td><textarea id="bill_to" name="bill_to" class="input-width">${customer.bill_to}</textarea></td>
                                        <td><span class="STYLE3">SHIP TO</span>:</td>
                                        <td><textarea id="ship_to" name="ship_to" class="input-width">${customer.ship_to}</textarea></td>
                                    </tr>

                                     <tr>
                                        <td colspan="2" style="border-left:1px solid #CCCCCC;">
                                            &nbsp;
                                        </td>
                                        <td style="border-left:1px solid #CCCCCC;"><span class="STYLE3">SOB#(Optional)</span>:</td>
                                        <td><input id="sob" type="text" name="sob" style="width:96%;" value="${hidden_sob}" /></td>
                                    </tr>

                                    <tr>
                                        <td colspan="2" style="color:red;border-left:1px solid #CCCCCC;">
                                            *According to the normal ordering periods established, <br />
                                            this order will be delivered by the 15th of the incoming month,<br />
                                            if you have any inconvenient with this delivery date, <br />
                                            please put the date you would need in the following window
                                        </td>
                                        <td style="border-left:1px solid #CCCCCC;"><span class="STYLE3">Special Request Ship Date (Optional)</span>:</td>
                                        <td><input id="ship_date" type="text" name="ship_date"  class="datePicker"/></td>
                                    </tr>
                                   
                                </table>
                            </div>
                        </div>
                        <div class="l"><input type="button" id="btn_save_to_job" value="Confirm" class="btn" onclick="saveToJob()" /></div>
                    </td>
                </tr>
                <tr>
                    <td colspan="100" style="border-right:0px;border-bottom:0px">
                        <div class="toolbar">
                            <div class="l"></div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <th><span class="STYLE3">Qty (${Date2Text(dt.now(), '%b/%Y')})</span></th>
                    <th>Qty (Firm PO, ${Date2Text(dt.now(), '%b/%Y')})</th>
                    <th><span class="STYLE3">Forecast Qty (${nextMonth(dt.now())})</span></th>
                    <th>Forecast Qty (For reference only, ${nextMonth(dt.now())})</th>
                    <th>Item Code</th>
                    <th>Category</th>
                    <th>Type</th>
                    <th>Image</th>
                    <th>Flatted Size</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody class="s_text">
               %for i in add_items:

               <%
                    
                        qty1 = ''
                        qty2 = ''
                        qty3 = ''
                        qty4 = ''

                        if id_list and str(i.id) in id_list:
                            qty1 = input_add_qty_list.get(str(i.id), '')
                            qty2 = add_qty_list.get(str(i.id), '')
                            qty3 = input_forecast_qty_list.get(str(i.id), '')
                            qty4 = forecast_qty_list.get(str(i.id), '')
               %>
                <tr>
                    <td class="head">
                        <input type="hidden" name="add_id" value="${i.id}" />
                        <input type="text" name="input_add_qty"  class="numeric" value="${qty1}" onblur="autoQty(this, 'actual_qty_', '${i.id}')"/>
                    </td>
                    <td class="head">
                        <input type="text" name="add_qty" autocomplete="off" value="${qty2}" readonly="readonly" class="readonly" id="actual_qty_${i.id}" />
                    </td>
                    <td class="head"><input type="text" name="input_forecast_qty"  value="${qty3}" class="numeric" onblur="autoQty(this, 'actual_forecast_qty_', '${i.id}')"/></td>
                    <td class="head">
                        <input type="text" name="forecast_qty" value="${qty4}" autocomplete="off" readonly="readonly" class="readonly" id="actual_forecast_qty_${i.id}"/>
                    </td>
                    <td>${i.item_code}</td>
                    <td>${i.category.name}</td>
                    <td>${i.type.name}</td>
                    <td>
                        <a href="/images/dba/${i.image}.jpg" class="nyroModal" title="${i.item_code}(${i.flatted_size})">
                            <img width="60" height="30" src="/images/dba/${i.image}.jpg" />
                        </a>
                    </td>
                    <td>${i.flatted_size|b}</td>
                    <td><a href="#" onclick="delItem(this)">Delete</a></td>
                </tr>
               %endfor
            </tbody>
        </table>
       </form>
    </div>
</div>
%endif
<div class="clear"></div>
    <br />
<div class="box2">
    <div class="clear"></div>
<form id="search_form" action="/dba/index" method="post">
    ${item_search_form(value=kw)|n}

    <input type="hidden" id="old_ids" name="old_ids" value="${'_'.join(id_list)}" />
    <input type="hidden" id="h_input_add_qty" name="h_input_add_qty" value="${'_'.join(input_add_qty_list.values())}" />
    <input type="hidden" id="h_add_qty" name="h_add_qty" value="${'_'.join(add_qty_list.values())}" />
    <input type="hidden" id="h_input_forecast_qty" name="h_input_forecast_qty" value="${'_'.join(input_forecast_qty_list.values())}" />
    <input type="hidden" id="h_forecast_qty" name="h_forecast_qty" value="${'_'.join(forecast_qty_list.values())}" />
    
    <div class="clear"></div>
    <div style="margin-left:15px;">
        <input type="button" class="btn" value="Search" onclick="search_h()"/>
    </div>
</form>
    <div class="toggle1"><a class="hid_a" href="javascript:void(0)" onclick="toggleIcon(this)"></a>Search Item Result</div>
    <div>
        <table class="gridTable" cellpadding="0" cellspacing="0" border="0" style="width:74%">
            <thead>
                <tr>
                    <td colspan="80" style="border-right:0px;border-bottom:0px">
                        <div id="toolbar">
                            <div class="l btns">
                                <input type="button" id="btn_add_to_job" value="Add To Order" class="btn" onclick="addToJob()" />
                            </div>
                            <div class="r">
                                ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <th class="head" style="width:5%;"><input id="header_checkbox" type="checkbox" value="0" onclick="selectAll(this)" /></th>
                    <th style="width:12%">Item Code</th>
                    <th style="width:24%">Category</th>
                    <th style="width:20%">Type</th>
                    <th style="width:22%">Image</th>
                    <th style="width:26%">Flatted Size</th>
                </tr>
            </thead>
            <tbody>
                %for i in collections:
                <tr>
                    <td class="head"><input type="checkbox" class="cboxClass" value="${i.id}" onclick="selectOne(this)" /></td>
                    <td>${i.item_code}</td>
                    <td>${i.category.name}</td>
                    <td>${i.type.name}</td>
                    <td>
                        <a href="/images/dba/${i.image}.jpg" class="nyroModal" title="${i.item_code}(${i.flatted_size})">
                            <img width="60" height="30" src="/images/dba/${i.image}.jpg" />
                        </a>
                    </td>
                    <td>${i.flatted_size|b}</td>
                </tr>
                %endfor
                <tr>
                    <td colspan="80" style="border-right:0px;border-bottom:0px">
                        <div id="toolbar">
                            <div class="r">
                                ${pager}, <span>${my_page.first_item} - ${my_page.last_item}, ${my_page.item_count} records</span>
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</div>