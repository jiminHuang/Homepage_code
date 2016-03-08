<script type="text/javascript">
    function imgError(img){
        var t = document.getElementByClassName("proc_pic");
        t.style.display = "none";
        t.style.visibility = "hidden";
        img.style.display = "none";
        img.onerror = null;
    }

    function imgExist(imgUrl){
        var pic = new ActiveXObject("Scripting.FileSystemObject");
        if(pic.FileExists(imgUrl))
            return true;
        return false;
    }
</script>