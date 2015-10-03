$(document).ready(function(){
    $(".list_loading_more").click(
        function(){
            if($("ul.media-list").data("load")=="-1"){
                $(".list_loading_more").css("display", "none");                
            }
            else{
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
                        $("li.media:last").after(data["write_str"]);
                        $("ul.media-list").data("load", query_num+1);
                    }
                );
            }
        }
    );
});
