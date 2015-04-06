$(document).ready(function(){
    $("#pb").hide();


    $("#upload").click(function(){
    $("#mywrapper").hide();
    $("#pb").show();
        $(function() {
        $(".progress").each(function() {
            $(this)
	            .data("origWidth", $(this).width())
	            .width(0)
	            .animate({
		            width: $(this).data("origWidth")
	            }, 5500);
                });
        });
    });


    $("#url").click(function(){
    $("#mywrapper").hide();
    $("#pb").show();
        $(function() {
        $(".progress").each(function() {
            $(this)
	            .data("origWidth", $(this).width())
	            .width(0)
	            .animate({
		            width: $(this).data("origWidth")
	            }, 6000);
                });
        });
    });
});
