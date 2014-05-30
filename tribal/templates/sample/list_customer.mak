<script>
    var createCustomer=function(obj){
        var text=$(obj).prev().val();
        $.getJSON("/sample/ajaxAddCustomer",{"name":text}, function(res) {
            if(res.flag=='0'){
                $('#tableCustomer').find('tbody').eq(0).prepend('<tr><td class="first">'+text+'</td><td><a href="javascript:void(0)" onclick="updateCustomer(this,'+res.customer.id+')">Update</a></td></tr>')
                resetCustomer(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var updateCustomer=function(obj, id){
        var td = $(obj).parent().parent().find('td').eq(0);
        var name = td.text();
        td.html('<input type=text value="'+name+'"/><input type=hidden value="'+id+'"/><input type=button class=btn value=Save onclick=saveCustomer(this) /><input type=hidden value="'+name+'"/>')
    }
    var saveCustomer=function(obj){
        var text=$(obj).prev().prev().val();
        var id=$(obj).prev().val();
        $.getJSON("/sample/ajaxUpdateCustomer",{"name":text, 'customer_id':id}, function(res) {
            if(res.flag=='0'){
                $(obj).parent().html(text);
                resetCustomer(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var removeCustomer=function(obj, id){
        var tr = $(obj).parent().parent();
        tr.remove()
    }
    var resetCustomer=function(data){
        var html = '<option></option>';
        for(var i=0;i<data.length;i++){
            html+= '<option value="'+data[i][0]+'">'+data[i][1]+'</option>'
        }
        $('#customer').html(html);
    }
</script>
<input type="text"/><input type="button" class="btn" value="Create" onclick="createCustomer(this)"/><br/><br/>
<table class="gridTable" id="tableCustomer" border="0" cellpadding="0" cellspacing="0">
    <thead>
        <tr><th class="first">Customer Name</th><th></th></tr>
    </thead>
    <tbody>
        %for i in data:
        <tr><td class="first">${i.name}</td><td><a href="javascript:void(0)" onclick="updateCustomer(this, ${i.id})">Update</a></td></tr>
        %endfor
    </tbody>
</table>
