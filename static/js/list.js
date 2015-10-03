$(document).ready(function(){
    $(".list_loading_more").click(
        function(){
            $.post(
                "#",
                {
                    last_element : $("li.media").data("id"), 
                    _xsrf : getCookie("xsrf"),
                },
                function(data){
                    alert(data);
                }
            );
        }
    );
});
