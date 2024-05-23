$('.top-down-link').click(function(e) {
    window.scrollTo(0,0)
})

$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();
    if(selectedVal != "reset"){
        var sort = selectedVal.split("_")[0];
        var direction = selectedVal.split("_")[1];

        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");

        window.location.replace(currentUrl);
    }
})

(function($) {window.fnames = new Array(); 
    window.ftypes = new Array();
    names[0]='EMAIL';
    types[0]='email';
    fnames[1]='FNAME';
    ftypes[1]='text';
    fnames[2]='LNAME';
    ftypes[2]='text';
    fnames[3]='ADDRESS';
    ftypes[3]='address';
    fnames[4]='PHONE';
    ftypes[4]='phone';
    fnames[5]='BIRTHDAY';
    ftypes[5]='birthday';
}
(jQuery));
var $mcj = jQuery.noConflict(true);
