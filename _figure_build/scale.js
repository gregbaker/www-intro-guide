var hex = '0123456789abcdef';
var fontsz = 14;

create_scale = function(id,  clr) {
  var h = 24;
  var w = 18;
  paper = Raphael(id, w*16, h + fontsz*2.75);
  var sq, lbl, c;
  for(i=0; i<16; i++) {
    c = '#' + clr(i)
    
    sq = paper.rect(i*w, 0, w, h);
    sq.attr({
      'fill': c,
      'stroke': 'none',
    });
    
    lbl = paper.text(i*w-5, h+20, c);
    lbl.attr({
      'text-anchor': 'start',
      'font-family': '"Source Code Pro",monospace',
      'font-size': fontsz,
      'transform': 'r 90',
      'style': 'font-family: "Source Code Pro",monospace'
    });
  }
}

colour_sample = function(id, clrs, lblchars) {
  var h = 32;

  paper = Raphael(id, h + fontsz*lblchars, (h + 4)*(clrs.length) + 4);
  
  $(clrs).each(function(i, c){
    var offset = i*(h+4);
    sq = paper.rect(2, offset + 4, h, h);
    sq.attr({
      'fill': c,
      'stroke': 'black',
      'stroke-width': '1'
    });
    // goddamnit, I'm trying to make a point here. Raphael recalculates colours (for compatability?)
    sq.node.setAttribute('fill', c);
    
    lbl = paper.text(h + 5, offset + h/2 + fontsz/2 - 2, c);
    lbl.attr({
      'text-anchor': 'start',
      'font-family': '"Source Code Pro",monospace',
      'font-size': fontsz,
    });
  });
}

jQuery(document).ready(function(){
  create_scale("scale1", function(i) { return hex[i] + "00" });
  create_scale("scale2", function(i) { return hex[i] + hex[i] + hex[i] });
  create_scale("scale3", function(i) { return "f" + hex[i] + hex[i] });
  colour_sample("samp1", ["#ff0", "#ffa"], 4)
  colour_sample("samp2", ["#b5123b", "#b13"], 6)
  colour_sample("samp3", ["#f70", "#ff7700", "rgb(255, 119, 0)", "rgba(255, 119, 0, 255)", "rgb(100%, 47%, 0%)", "hsl(28, 100%, 50%)"], 14)
});

