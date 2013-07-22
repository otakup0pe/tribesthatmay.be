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
    window.location = "/game/";
}

function loadImages() {
    $(imageList).each(function() {
                          $('<img/>').
                              attr('src', "images/" + this).
                              //                              attr('height', "240").
                              //                              attr('width', "320").
                              appendTo('#slides').
                              css('display', 'none');
                      });
}

function rollTape() {
    $('#slides').slidesjs({
                              width: 320,
                              height: 240,
                              navigation : {
                                  active : false

                              },
                              pagination : {
                                  active : false
                              },
                              effect : {
                                  fade: {
                                      speed: 250
                                  }
                              },
                              play: {
                                  effect : "fade",
                                  auto : true,
                                  active : false,
                                  interval : 1000
                              },
                              callback : {
                                  complete : function(number) {
                                      if ( number == imageList.length ) {
                                          setTimeout(function() {
                                                         $.cookie('seen_slideshow', "true");
                                                         doRedirect();
                                                     }, 1000);
                                      }
                                  }
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