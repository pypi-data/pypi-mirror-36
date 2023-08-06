<%inherit file="${context['midtpl']}" />


<form action="${request.route_url('ppss:perm:edit',elementid=perm.id)}" method="POST">
    
    <input type="text" name="name" placeholder="permissionname" value="${perm.name}">
    <br/>
    
    <input type="submit" name="submit" value="Apply"/>

</form>