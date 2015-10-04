$(document).ready(function(){
    if($("ul.media-list").data("load")=="-1"){
        $(".list_loading_more").css("display", "none");                
    }
    $(".list_loading_more").click(
        function(){
            query_num = $("ul.media-list").data("load");
            $.post(
                "#",
                {
                    query_num : query_num, 
                    _xsrf : getCookie("_xsrf"),
                },
                function(data){
                    if(data=="failed"){
                        $(".list_loading_more").html("load fail");
                        $(".list_loading_more").addclass("disable");
                    }
                    if(data["load_more"]=="-1"){
                        $(".list_loading_more").css("display", "none");                
                    }
                    $("ul.media-list>hr:last").after(data["write_str"]);
                    $("ul.media-list").data("load", query_num+1);
                }
            );
        }
    );
});
