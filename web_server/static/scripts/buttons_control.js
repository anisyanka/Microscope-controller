var interval_id = 0;
var timeout_id = 0;
var was_btn_released = 0;
var new_req_started = 0;
var is_mobile = 0

plus = 0;
minus = 0;
up = 0;
left = 0;
right = 0;
down = 0;

plus_def_style = "";
minus_def_style = "";
up_def_style = "";
left_def_style = "";
right_def_style = "";
down_def_style = "";

function dom_loaded() {
    plus = document.getElementById("focus-plus-btn");
    minus = document.getElementById("focus-minus-btn");
    up = document.getElementById("arrow-up-btn");
    left = document.getElementById("arrow-left-btn");
    right = document.getElementById("arrow-right-btn");
    down = document.getElementById("arrow-down-btn");
}

var polling_time_ms = 0;
function button_control_set_poll_time(poltime) {
    polling_time_ms = poltime;
}

function button_set_mobile_button_type(is_btn_type_mobile) {
    is_mobile = is_btn_type_mobile
}

function button_control_pressed(req, variable, value) {
    was_btn_released = 0;

    if (timeout_id == 0) {
        timeout_id = setTimeout(function() {button_control_check_was_release(req, variable, value);}, 400);
    }
}

function button_control_released(req, variable, value) {
    was_btn_released = 1;
    button_control_stop(req, variable, value);
    clearTimeout(timeout_id);
    timeout_id = 0;
}

function button_control_check_was_release(req, variable, value) {
    if (was_btn_released == 0) { /* the user is still pressing the button */
        button_control_change_repeatedly(req, variable, value);
    }
    timeout_id = 0;
}

function hover_on(req, value) {
    if (req == "focus_control") {
        if (value == "upper") {
            plus.style.backgroundColor = plus_def_style;
        } else {
            minus.style.backgroundColor = minus_def_style;
        }
    } else if (req == "motor_control") {
        if (value == "up") {
            up.style.backgroundColor = up_def_style;
        } else if (value == "left") {
            left.style.backgroundColor = left_def_style;
        } else if (value == "right") {
            right.style.backgroundColor = right_def_style;
        } else {
            down.style.backgroundColor = down_def_style;
        }
    }
}

function hover_off(req, value) {
    if (req == "focus_control") {
        if (value == "upper") {
            plus.style.backgroundColor = "rgb(255, 255, 255)";
        } else {
            minus.style.backgroundColor = "rgb(255, 255, 255)";
        }
    } else if (req == "motor_control") {
        if (value == "up") {
            up.style.backgroundColor = "rgb(255, 255, 255)";
        } else if (value == "left") {
            left.style.backgroundColor = "rgb(255, 255, 255)";
        } else if (value == "right") {
            right.style.backgroundColor = "rgb(255, 255, 255)";
        } else {
            down.style.backgroundColor = "rgb(255, 255, 255)";
        }
    }
}

function button_control(req, variable, value, is_retention) {
    var request = new XMLHttpRequest();

    request.onload = function() {
        if (request.response == "OK") {
            console.log("Request <" + req + "> OK! Parameter <" + variable + "> became " + value + "; retention=" + is_retention);
        } else {
            console.log("[ERR] HTTP request answer internal server error");
        }
        new_req_started = 0;
    }

    // Send a request
    if (new_req_started == 0) {
        request.responseType = 'json';
        request.open("GET", "/" + req + "?" + variable + "=" + value + "&retention=" + is_retention, true);
        request.send();
        new_req_started = 1;
    }
}

function button_control_change_repeatedly(req, variable, value) {
    if (interval_id == 0) {
        plus_def_style = window.getComputedStyle(plus).backgroundColor;
        minus_def_style = window.getComputedStyle(minus).backgroundColor;
        up_def_style = window.getComputedStyle(up).backgroundColor;
        left_def_style = window.getComputedStyle(left).backgroundColor;
        right_def_style = window.getComputedStyle(right).backgroundColor;
        down_def_style = window.getComputedStyle(down).backgroundColor;

        if (polling_time_ms == 0) {
            interval_id = window.setInterval(function() {button_control(req, variable, value, "yes");}, 200);
        } else {
            interval_id = window.setInterval(function() {button_control(req, variable, value, "yes");}, polling_time_ms);
        }
        console.log("Repeat proccess started");
    }
}

function button_control_stop(req, variable, value) {
    was_btn_released = 1;

    if (interval_id) {
        clearInterval(interval_id);
        interval_id = 0;
        new_req_started = 0;
        console.log("Repeat proccess stoped");
        setTimeout(function() { button_control(req, variable, value, "released"); }, 100);
    }
}
