var interval_id = 0;
var timeout_id = 0;
var was_btn_released = 0;

function focus_control_pressed(sign) {
    was_btn_released = 0;

    if (timeout_id == 0) {
        timeout_id = setTimeout(function() {focus_control_check_was_release(sign);}, 400);
    }
}

function focus_control_released(sign) {
    was_btn_released = 1;
    focus_control_stop();

    if (timeout_id) {
        clearTimeout(timeout_id);
        timeout_id = 0;
    }
}

function focus_control_check_was_release(sign) {
    if (was_btn_released == 0) { /* the user is still pressing the button */
        focus_control_change_repeatedly(sign);
    }
    timeout_id = 0;
}

function focus_control(sign) {
    var request = new XMLHttpRequest();

    request.onload = function() {
        if (request.response == "OK") {
            if (sign == "upper") {
                console.log("Focus: + OK");
            } else if (sign == "lower") {
                console.log("Focus: - OK");
            }
        } else {
            console.log("Focus: Unable to change focus --> HTTP request error");
        }
    }

    // Send a request
    request.responseType = 'json';
    request.open("GET", "/focus_control?sign=" + sign, true);
    request.send();
}

function focus_control_change_repeatedly(sign) {
    if (interval_id == 0) {
        interval_id = window.setInterval(function() {focus_control(sign);}, 100);
        console.log("Change focus repeadatly started");
    }
}

function focus_control_stop() {
    was_btn_released = 1;

    if (interval_id) {
        clearInterval(interval_id);
        interval_id = 0;
        console.log("Change focus repeadatly stoped");
    }
}
