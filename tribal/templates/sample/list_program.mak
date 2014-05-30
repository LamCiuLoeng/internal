<script>
    var createProgram=function(obj){
        var text=$(obj).prev().val();
        $.getJSON("/sample/ajaxAddProgram",{"program_name":text}, function(res) {
            if(res.flag=='0'){
                $('#tableProgram').find('tbody').eq(0).prepend('<tr><td class="first">'+text+'</td><td><a href="javascript:void(0)" onclick="updateProgram(this,'+res.program.id+')">Update</a></td></tr>')
                resetProgram(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var updateProgram=function(obj, id){
        var td = $(obj).parent().parent().find('td').eq(0);
        var name = td.text();
        td.html('<input type=text value="'+name+'"/><input type=hidden value="'+id+'"/><input type=button class=btn value=Save onclick=saveProgram(this) /><input type=hidden value="'+name+'"/>')
    }
    var saveProgram=function(obj){
        var text=$(obj).prev().prev().val();
        var id=$(obj).prev().val();
        $.getJSON("/sample/ajaxUpdateProgram",{"program_name":text, 'program_id':id}, function(res) {
            if(res.flag=='0'){
                $(obj).parent().html(text);
                resetProgram(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var removeProgram=function(obj, id){
        var tr = $(obj).parent().parent();
        tr.remove()
    }
    var resetProgram=function(data){
        var html = '<option></option>';
        for(var i=0;i<data.length;i++){
            html+= '<option value="'+data[i][0]+'">'+data[i][1]+'</option>'
        }
        $('#program').html(html);
    }
</script>
<input type="text"/><input type="button" class="btn" value="Create" onclick="createProgram(this)"/><br/><br/>
<table class="gridTable" id="tableProgram" border="0" cellpadding="0" cellspacing="0">
    <thead>
        <tr><th class="first">Program Name</th><th></th></tr>
    </thead>
    <tbody>
        %for i in data:
        <tr><td class="first">${i.name}</td><td><a href="javascript:void(0)" onclick="updateProgram(this, ${i.id})">Update</a></td></tr>
        %endfor
    </tbody>
</table>