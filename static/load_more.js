let page = 1;
let is_in=false;
let search_add = window.location.href.toLowerCase().indexOf("/search/") > -1;
document.addEventListener('DOMContentLoaded', function(e) {
    document.addEventListener('scroll', function(e) {
        let documentHeight = document.body.scrollHeight;
        let currentScroll = window.scrollY + window.innerHeight;
        // When the user is [modifier]px from the bottom, fire the event.
        let modifier = 200; 
        if(!is_in&&(currentScroll + modifier > documentHeight)) {
            is_in=true;
            document.getElementById("loader").hidden = false;
            page++;
            fetch((search_add ? "/Search/" : "")+"/"+(/[^/]*$/.exec(window.location.href)[0])+"/"+page)
            .then((response) => response.text())
            .then((data) => {
                document.getElementsByClassName("grid-wrapper")[0].innerHTML+=data;
                document.getElementById("loader").hidden = true;
                is_in=false;
            });
        }
    })
});