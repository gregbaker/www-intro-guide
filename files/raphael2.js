setup = function() {
  paper = Raphael('container', 200, 100)
  elli = paper.ellipse(50, 20, 40, 10)
  elli.attr({
    'fill': '#0f0',
    'stroke': '#999',
    'stroke-width': '4'
  })
  caption = paper.text(100, 50, 'I think this is going well.')
  caption.attr({
    'font-size': '14',
    'font-family': 'serif'
  })
  rect = paper.rect(150, 50, 40, 30)
  rect.attr({
    'transform': 'r30',
    'stroke': '#070'
  })
}
jQuery(document).ready(setup)
