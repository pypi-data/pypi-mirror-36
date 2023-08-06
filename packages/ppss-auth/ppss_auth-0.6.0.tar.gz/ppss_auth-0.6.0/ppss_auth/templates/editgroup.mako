<%inherit file="${context['midtpl']}" />


<form action="${request.route_url('ppss:group:edit',elementid=groupid)}" method="POST">
    
    <input type="text" name="name" placeholder="group name" value="${group.name if group else ""}">
    <br/>

    <label for="enablecheck">Enable:</label>
    <input id="enablecheck" name="enablecheck" type="checkbox" value="1" ${'checked="checked"' if group.enabled else ""}>
    <br/>
    <input type="submit" name="submit" value="Apply"/>

    <p>${msg}</p>
</form>
<a href="${request.route_url('ppss:perm:delete',elementid=group.id)}">remove group</a>

<div class="alluser">
    <ul>
    %for user in group.users:
            <li data-userid="${user.id}"> ${user.username}<span class="command deleteuser">x</span></a></li>
    %endfor
    </ul>
</div>


<div class="allperm">
    <h3>Perm to remove</h3>
    <ul>
    %for perm in group.permissions:
            <li data-id="${perm.id}"> ${perm.name}<span class="command deleteperm">x</span></a></li>
    %endfor
    </ul>
    <h3>Perm to add</h3>
    <ul>
    %for perm in allperm:
            <li data-id="${perm.id}"> ${perm.name}<span class="command addperm">x</span></a></li>
    %endfor
    </ul>

</div>

<script type="text/javascript">
    $(".deleteuser").on("click",function(ev){
        $.ajax("${request.route_url('ppss:group:removeuser',targetid=-1,elementid=group.id)}".replace("-1",$(this).closest("li").attr("data-userid")  ),
            {datatype:"json",
            success:function(res){console.log("success");},
            error:function(res){console.log("error");}
            });
    });


    $(".deleteperm").on("click",function(ev){
        $.ajax("${request.route_url('ppss:group:removeperm',targetid=-1,elementid=group.id)}".replace("-1",$(this).closest("li").attr("data-id")  ),
            {datatype:"json",
            success:function(res){console.log("success");},
            error:function(res){console.log("error");}
            });
    });
    $(".addperm").on("click",function(ev){
        $.ajax("${request.route_url('ppss:group:addperm',targetid=-1,elementid=group.id)}".replace("-1",$(this).closest("li").attr("data-id")  ),
            {datatype:"json",
            success:function(res){console.log("success");},
            error:function(res){console.log("error");}
            });
    });
</script>