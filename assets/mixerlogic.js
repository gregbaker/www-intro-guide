function hexFromRGB(r, g, b) {
  var hex = [
    r.toString( 16 ),
    g.toString( 16 ),
    b.toString( 16 )
  ];
  return hex.join( "" ).toUpperCase();
}
function refreshSwatch() {
  var red = $( "#red" ).slider( "value" ),
    green = $( "#green" ).slider( "value" ),
    blue = $( "#blue" ).slider( "value" ),
    hex = hexFromRGB( red, green, blue );
  $( "#swatch" ).css( "background-color", "#" + hex );
  $( "#color" ).html("#" + hex)
}
$(function() {
  $( ".slider" ).slider({
    orientation: "horizontal",
    range: "min",
    max: 15,
    value: 0,
    step: 1,
    slide: refreshSwatch,
    change: refreshSwatch
  });
  $( "#red" ).slider( "value", 0 );
  $( "#green" ).slider( "value", 0 );
  $( "#blue" ).slider( "value", 0 );

  $(document).keydown(function(e) {
    /* move all sliders up/down on right/left arrow keys */
    var change = 0;
    if ( e.which == 37 ) {
      change = -1;
      e.preventDefault();
    } else if ( e.which == 39 ) {
      change = 1;
      e.preventDefault();
    }
    $( ".slider" ).each( function(i, s) {
      var slide = $(s);
      var v = slide.slider("value");
      console.log(v, change);
      slide.slider("value", v+change);
    });
  });
});
