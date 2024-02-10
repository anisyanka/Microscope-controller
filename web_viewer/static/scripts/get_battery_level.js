function get_battery_level() {
    var request = new XMLHttpRequest()

    request.onload = function() {
        if (request.response["level"]) {
            var battery_fill = document.querySelector(".battery-fill");
            var battery_percentage = document.querySelector(".battery-percentage");

            battery_fill.style.width = request.response["level"] + "%";
            battery_percentage.innerHTML = request.response["level"] + "%";
        } else {
            console.log("Obtain battery status failed");
        }
    }

    // Send a request
    request.responseType = 'json';
    request.open("GET", "/get_battery_level", true);
    request.send();
}

function get_battery_level_start() {
    window.setInterval(function() {get_battery_level(); }, 10000);
    console.log("Obtaining battery level repeadatly started")
}
