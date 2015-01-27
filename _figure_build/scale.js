var hex = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'];
var fontsz = 14;

create_scale = function(id,  clr) {
  var h = 24;
  var w = 18;
  s = Snap("#" + id);
  s.attr({
    'xmlns': 'http://www.w3.org/2000/svg',
    'width': w*16,
    'height': h + fontsz*2.75
  });
  var sq, lbl, c;
  for(i=0; i<16; i++) {
    c = '#' + clr(i)
    
    sq = s.rect(i*w, 0, w, h);
    sq.attr({
      'fill': c,
    });
    
    lbl = s.text(h + 3, -i*w - 6, c);
    lbl.attr({
      'font-family': '"Source Code Pro",monospace',
      'font-size': fontsz,
      'transform': 'rotate(90)'
    });
  }
}

colour_sample = function(id, clrs, lblchars) {
  var h = 32;

  s = Snap("#" + id);
  s.attr({
    'xmlns': 'http://www.w3.org/2000/svg',
    'width': h + fontsz*lblchars,
    'height': (h + 4)*(clrs.length) + 4
  });
  $(clrs).each(function(i, c){
    var offset = i*(h+4);
    sq = s.rect(2, offset + 4, h, h);
    sq.attr({
      'style': 'fill:'+c,
      'stroke': 'black',
      'stroke-width': '1'
    });
    lbl = s.text(h + 5, offset + h/2 + fontsz/2, c);
    lbl.attr({
      'font-family': '"Source Code Pro",monospace',
      'font-size': fontsz,
    });
  });
  
}

jQuery(document).ready(function(){
  create_scale("scale1", function(i) { return hex[i] + "00" });
  create_scale("scale2", function(i) { return hex[i] + hex[i] + hex[i] });
  create_scale("scale3", function(i) { return "f" + hex[i] + hex[i] });
  create_scale("scale4", function(i) { return "ff" + hex[i] });
  colour_sample("samp1", ["#ff0", "#ffa"], 4)
  colour_sample("samp2", ["#b5123b", "#b13"], 6)
  colour_sample("samp3", ["#f70", "#ff7700", "rgb(255, 119, 0)", "rgba(255, 119, 0, 255)", "rgb(100%, 47%, 0%)", "hsl(28, 100%, 50%)"], 14)
});

