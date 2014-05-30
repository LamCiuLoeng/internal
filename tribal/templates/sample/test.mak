<%inherit file="tribal.templates.master"/>

<form action="/sample/upload" method="post" enctype="multipart/form-data">
   <input type="file" name="attachment"/>
   <input type="text" name="attachment_name"/>
   <input type="file" name="attachment"/>
   <input type="text" name="attachment_name"/>
   <input type="submit" value="upload"/>
</form>
