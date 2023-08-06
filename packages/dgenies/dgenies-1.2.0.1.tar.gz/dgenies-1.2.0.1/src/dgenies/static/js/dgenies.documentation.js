if (!dgenies) {
    throw "dgenies wasn't included!"
}
dgenies.documentation = {};

/**
 * Initialise app for documentation page
 */
dgenies.documentation.init = function () {
    $("table").addClass("table table-striped");
    dgenies.documentation.fix_links_headers();
};

/**
 * Fix link in headers behavior (due to top bar fixed position - CSS)
 */
dgenies.documentation.fix_links_headers = function() {
    $("#plan").on("click", "a", function (e) {
        e.preventDefault();
        dgenies.documentation.goto(this);
    })
};

/**
 * Scroll to a JQuery element
 * @param elem JQuery element
 */
dgenies.documentation.goto = function (elem) {
    let top = $($(elem).attr("href")).offset()["top"];
    $(window).scrollTop(top-55);
    $(elem).blur();
};