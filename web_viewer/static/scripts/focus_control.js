var interval_id = 0

function focus_control(sign) {
    var request = new XMLHttpRequest()

    if (interval_id != 0) {
        clearInterval(interval_id)
        interval_id = window.setInterval(function() {focus_control(sign); }, 100);
    }

    request.onload = function() {
        if (request.response == "OK") {
            if (sign == "upper") {
                console.log("Focus: + OK")
            } else if (sign == "lower") {
                console.log("Focus: - OK")
            }
        } else {
            console.log("Focus: Unable to change focus --> HTTP request error")
        }
    }

    // Send a request
    request.responseType = 'json';
    request.open("GET", "/focus_control?sign=" + sign, true);
    request.send();
}

function focus_control_change_repeatedly(sign) {
    interval_id = window.setInterval(function() {focus_control(sign); }, 10);
    console.log("Change focus repeadatly started")
}

function focus_control_stop() {
    clearInterval(interval_id)
    interval_id = 0
    console.log("Change focus repeadatly stoped")
}
