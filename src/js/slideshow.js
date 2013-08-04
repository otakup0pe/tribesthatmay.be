function queryStrBit(ji) {
    hu = window.location.search.substring(1);
    gy = hu.split("&");
    for (i=0;i<gy.length;i++) {
        ft = gy[i].split("=");
        if (ft[0] == ji) {
            return ft[1];
        } else {
            return "";
        }
    }
}


function doRedirect() {
    window.location = "/";
}

function loadImages() {
    $(imageList).each(function() {
                          $('<li><img src="images/' + this + '"/></li>').
                              appendTo('#slides').
                              css('display', 'none');
                      });
}

function rollTape() {
    $('.flexslider').flexslider({
                                    slideshowSpeed: 1000,
                                    animationSpeed: 250,
                                    controlNav: false,
                                    directionNav: false,
                                    keyboard: false,
                                    end:  function() {
                                        $.cookie('seen_slideshow', "true");
                                        doRedirect();
                                  }
                              });
}

function doStuff() {
    if ( queryStrBit("force") != "true" && $.cookie('seen_slideshow') == "true" ) {
        doRedirect();
    } else {
        loadImages();
        rollTape();
    }

}