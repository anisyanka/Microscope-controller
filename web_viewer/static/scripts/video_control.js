function video_switch_resolution(new_res) {
    var request = new XMLHttpRequest()

    request.onload = function() {
        if (request.response == "OK") {
            if (new_res == "1080p") {
                console.log("Stream resolution has been changed to 1080p")
                //document.getElementById("floor-lamp-image").src = "/static/images/floor-lamp-on.jpg"
                //document.getElementById("floor-lamp-card-text").innerHTML = "Status: <b>on</b>"
            } else if (new_res == "4k") {
                console.log("Stream resolution has been changed to 4k")
                //document.getElementById("floor-lamp-image").src = "/static/images/floor-lamp-off.jpg"
                //document.getElementById("floor-lamp-card-text").innerHTML = "Status: <b>off</b>"
            }
        } else {
            console.log("Stream resolution changing HTTP response != OK")
            //document.getElementById("floor-lamp-image").src = "..."
            //document.getElementById("floor-lamp-card-text").innerHTML = "Status: <b>error</b>"
        }
    }

    // Send a request
    request.responseType = 'json';
    request.open("GET", "/video_control?new_res=" + new_res, true);
    request.send();
}
