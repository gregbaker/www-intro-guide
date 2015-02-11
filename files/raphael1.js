setup = function() {
  paper = Raphael('container', 50, 50);
  circ = paper.circle(25, 25, 24);
  circ.attr({
    'fill': '#f00',
    'stroke': '#000',
    'stroke-width': 2
  });
}
jQuery(document).ready(setup);
