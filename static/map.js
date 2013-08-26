function notification(message, css_class) {
    $elm = $("#notification");
    $elm.attr('class','').addClass(css_class);
    $elm = $("#notification_text");
    $elm.attr('class','').addClass(css_class);
    $elm.text(message);
    $elm = $("#notification_likesbar");
    $elm.attr('class','').addClass(css_class);
}

$(document).ready(function(){
    // $("#map_canvas").css("width", "1024px");
    var width = $("#map_canvas").width();
    $("#map_canvas").css("height", "512px");

    var centre_lon = 30;
    var centre_lat = 8;
    if(window.initial_centre) {
        centre_lon = window.initial_centre;
    } else {
        $.getJSON('http://api.wipmania.com/jsonp?callback=?', function (data) {
            centre_lon = Math.round(data.longitude);
            map.panTo(new google.maps.LatLng(centre_lat, centre_lon));
        });
    }

    var mapOptions = {
        zoom: 2,
        maxZoom: 2,
        draggable: true,
        zoomControl: false,
        panControl: true,
        panControlOptions: {
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        scrollwheel: false,
        disableDoubleClickZoom: true,
        disableDefaultUI: true,
        center: new google.maps.LatLng(centre_lat, centre_lon),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        styles: [
                {
                    "featureType": "administrative",
                    "stylers": [
                        { "visibility": "off" }
                    ]
                },{
                    "featureType": "landscape",
                    "stylers": [
                        { "color": "#ffffff" }
                    ]
                },{
                    "featureType": "water",
                    "stylers": [
                        { "color": "#309CC0" }
                    ]
                }
            ]
    };
    var map = new google.maps.Map(document.getElementById('map_canvas'),
            mapOptions);
    var AustraliaBoxCoords = [
        new google.maps.LatLng(-6, 100),
        new google.maps.LatLng(-46, 100),
        new google.maps.LatLng(-46, -170),
        new google.maps.LatLng(-6, -170),
        new google.maps.LatLng(-6, 100)
    ];
    var AustraliaBox = new google.maps.Polyline({
        path: AustraliaBoxCoords,
        strokeColor: "#043566",
        strokeOpacity: 0.2,
        strokeWeight: 1
    });
    AustraliaBox.setMap(map);

    var Ausmarker = new google.maps.Marker({
        url: 'australia',
        icon: 'static/zoomin.png',
        map: map
    });
    google.maps.event.addListener(Ausmarker, 'click', function() {
        window.location.href = Ausmarker.url;
    });
    Ausmarker.setPosition(new google.maps.LatLng(-16, -175));

    $(document).ajaxStart(function(){
        $('div.map_notification_container').block({
            message: '<div style="font-size:18px"><img src="/static/busy.gif" /> Now computing spread of marine plastics...</div>',
            css:{padding: '30px', width: '400px'}
        });
    });
    $(document).ajaxStop(function(){
        $('div.map_notification_container').unblock();
    });

    var heatMapData = [];
    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatMapData,
        radius: 1
    });
    var image = '/static/' + window.icon_filename;
    var marker = new google.maps.Marker({
        map:map,
        icon: image
    });
    var run_counter = 0;
    var secperframe = 250;
    if (cssua.ua.mobile) {
        secperframe = 500;
    }

    function drawHeatMapData(j, expected_run_counter) {
        if (run_counter != expected_run_counter) return;
        if (j == 0) {
            for(var i = 0; i < heatMapData[j].length; i++) {
                var x = heatMapData[j][i].location;
                heatMapData[j][i].location = new google.maps.LatLng(x.lat, x.lng);
            }
            pointArray = new google.maps.MVCArray(heatMapData[j]);
            heatmap = new google.maps.visualization.HeatmapLayer({
                data: pointArray,
                radius: 10,
                maxIntensity : 100,
                opacity : 1,
            });
            heatmap.setMap(map);
        } else {
            pointArray.clear();
            for(var i = 0; i < heatMapData[j].length; i++) {
                var x = heatMapData[j][i].location;
                y = new google.maps.LatLng(x.lat, x.lng)
                y.weight = heatMapData[j][i].weight;
                pointArray.push(y);
            }
        }
        setTimeout(function(){
            var years = Math.floor((j+1)/6);
            var months = (j+1)%6*2;
            notification("Marine plastics after " + years + " years and " + months + " months");
        },0);
        if (j + 1 < heatMapData.length) {
            setTimeout(function() {
                drawHeatMapData(j+1, expected_run_counter);
            },secperframe);
        }
    }
    last_lat = null;
    last_lng = null;
    function run(latLng) {
        lat = Math.round(10 * latLng.lat()) / 10;
        lng = Math.round(10 * latLng.lng()) / 10;
        last_lat = lat;
        last_lng = lng;
        if (latLng != window.initial_tracer) {
            History.pushState({}, document.title, "map?lat="+lat+"&lng="+lng+"&centre="+centre_lon);
        }
        run_counter++;
        marker.setPosition(latLng);
        $.getJSON("/run?lat="+lat+"&lng="+lng, function(data) {
            if (data.substring) {
                heatmap.setMap(null);
                notification(data, "error");
            } else if (data[0].length == 0) {
                heatmap.setMap(null);
                notification("You clicked on land, please click on the ocean", "error");
            } else {
                setTimeout(function(){
                    heatmap.setMap(null);
                    heatMapData = data;
                    drawHeatMapData(0, run_counter);
                },secperframe)
            }
        });
    }
    google.maps.event.addListener(map, 'click', function(mouseEvent) {
        run(mouseEvent.latLng);
    });
    google.maps.event.addListenerOnce(map, 'bounds_changed', function(){
        if (window.initial_tracer) {
            run(window.initial_tracer);
        }
    });
    google.maps.event.addListener(map, 'center_changed', function() {
        var newCenter = map.getCenter();
        centre_lon = Math.round(10 * ((newCenter.lng()%360 + 540)%360 - 180)) / 10;
        if (last_lat) {
            History.pushState({}, document.title, "map?lat="+last_lat+"&lng="+last_lng+"&centre="+centre_lon);
        }
        if (Math.abs(newCenter.lat()-centre_lat) > 1e-4) {
            map.panTo(new google.maps.LatLng(centre_lat, newCenter.lng()));
        }
    });
});
if (window.open_page) {
    $(document).ready(function(){$(".colorbox").colorbox({open:true,href:window.open_page,width:"850px", top:top_px+"px", maxHeight:"510px", opacity:0.50});});
}
