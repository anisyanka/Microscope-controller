function video_switch_resolution(new_res) {
    var request = new XMLHttpRequest()

    request.onload = function() {
        if (request.response == "OK") {
            if (new_res == "1080p") {
                console.log("Stream resolution has been changed to 1080p");
                document.querySelector(".video-stream-mode-text").innerHTML = "Video: <span style=\"color:DodgerBlue\">1080p</span>";
            } else if (new_res == "4k") {
                console.log("Stream resolution has been changed to 4k");
                document.querySelector(".video-stream-mode-text").innerHTML = "Video: <span style=\"color:DodgerBlue\">4k</span>";
            }
        } else {
            console.log("[ERR] stream resolution changing HTTP response != OK");
            document.querySelector(".video-stream-mode-text").innerHTML = "Video: <span style=\"color:Tomato\">unavailable</span>";
        }
    }

    // Send a request
    request.responseType = 'json';
    request.open("GET", "/video_control?new_res=" + new_res, true);
    request.send();
}
