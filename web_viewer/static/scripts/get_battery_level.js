function get_battery_level() {
    var request = new XMLHttpRequest()

    request.onload = function() {
        if (request.response["level"]) {
            var battery_fill = document.querySelector(".battery-fill");
            var battery_percentage = document.querySelector(".battery-percentage");

            battery_fill.style.height = request.response["level"] + "%";
            battery_percentage.innerHTML = request.response["level"] + "%";
        } else {
            console.log("[ERR] obtainning battery status failed");
        }
    }

    // Send a request
    request.responseType = 'json';
    request.open("GET", "/get_battery_level", true);
    request.send();
}

function get_battery_level_start(bat_polling_period_ms) {
    window.setInterval(function() {get_battery_level(); }, bat_polling_period_ms);
    console.log("Obtaining battery level repeadatly started")
}
