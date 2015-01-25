var hex = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'];
var h = 24;
var w = 18;
var fontsz = 14;

jQuery(document).ready(function(){
  var s = Snap("#scale");
  s.attr({
    'xmlns': 'http://www.w3.org/2000/svg',
    'width': w*16,
    'height': h + fontsz*2.5
  });
  var sq, lbl, c;
  for(i=0; i<16; i++) {
    c = "#" + hex[i] + "00";
    sq = s.rect(i*w, 0, w, h);
    sq.attr({
      fill: c,
    });
    
    //lbl = s.text(i*w + w/2, h + fontsz - 2, hex[i]);
    lbl = s.text(h + 3, -i*w - 6, c);
    lbl.attr({
      'font-family': '"Source Code Pro",monospace',
      'font-size': fontsz,
      'transform': 'rotate(90)'
    });
  }
});

