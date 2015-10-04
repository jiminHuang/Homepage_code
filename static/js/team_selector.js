$(document).ready(function(){
    $(".team_selection li").click(function(){
        $(".team_selection li.active").removeClass("active");
        $(".team_view .row>div").css("display", "none");
        $(this).addClass("active");
        var index = parseInt($(".team_selection li").index(this));
        if(index==0){
            $(".team_view .row>div").css("display", "inline-block");
        }
        else{
            $(".team_view .row>div[data-type="+index+"]").css("display", "inline-block");
        }
    });  
});
