var $ = require('jQuery');
var $ = require('ScrollMagic');

$(document).ready(function(){

    var controller = new ScrollMagic.Controller();

    var pinAboutBox = new ScrollMagic.Scene({
        triggerelement: '#aboutbox',
        triggerHook: 0

    })
    .setPin('#aboutbox')
    .addTo(controller);

});
