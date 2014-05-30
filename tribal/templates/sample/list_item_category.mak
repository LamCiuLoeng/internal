<script>
    var createItemCategory=function(obj){
        var text=$(obj).prev().val();
        $.getJSON("/sample/ajaxAddItemCategory",{"name":text}, function(res) {
            if(res.flag=='0'){
                $('#tableItemCategory').find('tbody').eq(0).prepend('<tr><td class="first">'+text+'</td><td><a href="javascript:void(0)" onclick="updateItemCategory(this,'+res.item_category.id+')">Update</a></td></tr>')
                resetItemCategory(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var updateItemCategory=function(obj, id){
        var td = $(obj).parent().parent().find('td').eq(0);
        var name = td.text();
        td.html('<input type=text value="'+name+'"/><input type=hidden value="'+id+'"/><input type=button class=btn value=Save onclick=saveItemCategory(this) /><input type=hidden value="'+name+'"/>')
    }
    var saveItemCategory=function(obj){
        var text=$(obj).prev().prev().val();
        var id=$(obj).prev().val();
        $.getJSON("/sample/ajaxupdateItemCategory",{"name":text, 'item_category_id':id}, function(res) {
            if(res.flag=='0'){
                $(obj).parent().html(text);
                resetItemCategory(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var removeItemCategory=function(obj, id){
        var tr = $(obj).parent().parent();
        tr.remove()
    }
    var resetItemCategory=function(data){
        var html = '<option></option>';
        for(var i=0;i<data.length;i++){
            html+= '<option value="'+data[i][0]+'">'+data[i][1]+'</option>'
        }
        $('#item_category').html(html);
    }
</script>
<input type="text"/><input type="button" class="btn" value="Create" onclick="createItemCategory(this)"/><br/><br/>
<table class="gridTable" id="tableItemCategory" border="0" cellpadding="0" cellspacing="0">
    <thead>
        <tr><th class="first">Item Category Name</th><th></th></tr>
    </thead>
    <tbody>
        %for i in data:
        <tr><td class="first">${i.name}</td><td><a href="javascript:void(0)" onclick="updateItemCategory(this, ${i.id})">Update</a></td></tr>
        %endfor
    </tbody>
</table>
