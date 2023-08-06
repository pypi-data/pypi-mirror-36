if (!dgenies) {
    throw "dgenies wasn't included!"
}
dgenies.status = {};
dgenies.status.mode = "webserver";

/**
 * initialise the app for status page
 *
 * @param {string} status job status
 * @param {string} mode server mode (standalone or webserver)
 */
dgenies.status.init = function (status, mode) {
    dgenies.status.mode = mode;
    if (status !== "success" && status !== "done" && status !== "no-match" && status !== "fail") {
        dgenies.status.autoreload();
    }
};

/**
 * Page autoreload periodically
 */
dgenies.status.autoreload = function () {
    let get_p = new URLSearchParams(window.location.search);
    let refresh = get_p.get("refresh") !== null ? parseInt(get_p.get("refresh")) : 1;
    let count = get_p.get("count") !== null ? parseInt(get_p.get("count")) : 1;
    if (refresh < 30) {
        if (refresh % 5 === 0) {
            if (count > 3) {
                refresh += 1;
                count = 1;
            }
            else {
                count += 1
            }
        }
        else {
            refresh += 1
        }
    }
    setTimeout(function(){
        if (dgenies.status.mode === "webserver") {
            window.location.replace(`?refresh=${refresh}&count=${count}`);
        }
        else {
            window.location.replace(`?refresh=1&count=1`);
        }
    }, refresh * 1000)
};
