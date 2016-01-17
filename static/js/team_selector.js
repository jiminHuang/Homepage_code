$(document).ready(function(){
    $(".team_selection li").click(function(){
        $(".team_selection li.active").removeClass("active");
        $(".team_view .row>div").css("display", "none");
        $(this).addClass("active");
        var index = $(this).text();
        if(index=='All'){
            $(".team_view .row>div").css("display", "inline-block");
        }
        else{
            $(".team_view .row>div[data-type="+index+"]").css("display", "inline-block");
        }
    });  
});
