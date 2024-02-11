var interval_id = 0;
var timeout_id = 0;
var was_btn_released = 0;

function button_control_pressed(req, variable, value) {
    was_btn_released = 0;

    if (timeout_id == 0) {
        timeout_id = setTimeout(function() {button_control_check_was_release(req, variable, value);}, 400);
    }
}

function button_control_released() {
    was_btn_released = 1;
    button_control_stop();

    if (timeout_id) {
        clearTimeout(timeout_id);
        timeout_id = 0;
    }
}

function button_control_check_was_release(req, variable, value) {
    if (was_btn_released == 0) { /* the user is still pressing the button */
        button_control_change_repeatedly(req, variable, value);
    }
    timeout_id = 0;
}

function button_control(req, variable, value) {
    var request = new XMLHttpRequest();

    request.onload = function() {
        if (request.response == "OK") {
            console.log("Request <" + req + "> OK! Parameter <" + variable + "> became " + value);
        } else {
            console.log("[ERR] HTTP request answer internal server error");
        }
    }

    // Send a request
    request.responseType = 'json';
    request.open("GET", "/" + req + "?" + variable + "=" + value, true);
    request.send();
}

function button_control_change_repeatedly(req, variable, value) {
    if (interval_id == 0) {
        interval_id = window.setInterval(function() {button_control(req, variable, value);}, 100);
        console.log("Repeat proccess started");
    }
}

function button_control_stop() {
    was_btn_released = 1;

    if (interval_id) {
        clearInterval(interval_id);
        interval_id = 0;
        console.log("Repeat proccess stoped");
    }
}
