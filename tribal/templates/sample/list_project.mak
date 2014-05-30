<script>
    var createProject=function(obj){
        var text=$(obj).prev().val();
        $.getJSON("/sample/ajaxAddProject",{"project_name":text, 'program_id':'${program_id}'}, function(res) {
            if(res.flag=='0'){
                $('#tableProject').find('tbody').eq(0).prepend('<tr><td class="first">'+text+'</td><td><a href="javascript:void(0)" onclick="updateProject(this,'+res.project.id+')">Update</a></td></tr>')
                resetProject(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var updateProject=function(obj, id){
        var td = $(obj).parent().parent().find('td').eq(0);
        var name = td.text();
        td.html('<input type=text value="'+name+'"/><input type=hidden value="'+id+'"/><input type=button class=btn value=Save onclick=saveProject(this) /><input type=hidden value="'+name+'"/>')
    }
    var saveProject=function(obj){
        var text=$(obj).prev().prev().val();
        var id=$(obj).prev().val();
        $.getJSON("/sample/ajaxUpdateProject",{"project_name":text, 'project_id':id, 'program_id':'${program_id}'}, function(res) {
            if(res.flag=='0'){
                $(obj).parent().html(text);
                resetProject(res.data);
            }else if(res.flag=='2'){
            	alert('Duplicate Name Exists, please try other name.')
            }
        })
    }
    var removeProject=function(obj, id){
        var tr = $(obj).parent().parent();
        tr.remove()
    }
    var resetProject=function(data){
        var html = '';
        for(var i=0;i<data.length;i++){
            html+= '<option value="'+data[i][0]+'">'+data[i][1]+'</option>'
        }
        $('#project').html(html);
    }
</script>
<input type="text"/><input type="button" class="btn" value="Create" onclick="createProject(this)"/><br/><br/>
<table class="gridTable" id="tableProject" border="0" cellpadding="0" cellspacing="0">
    <thead>
        <tr><th class="first">Project Name</th><th></th></tr>
    </thead>
    <tbody>
        %for i in data:
        <tr><td class="first">${i.name}</td><td><a href="javascript:void(0)" onclick="updateProject(this, ${i.id})">Update</a></td></tr>
        %endfor
    </tbody>
</table>
