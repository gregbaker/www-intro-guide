y = 0
move = function() {
  dir = $('#direction').val()
  if ( dir == 'up' ) {
    y = y - 20
  } else {
    y = y + 20
  }
  
  attr = {
	'transform': 't0,' + y
  }
  shape.animate(attr, 500)
}
setup = function() {
  paper = Raphael('container', 200, 200)
  shape = paper.circle(100, 100, 10)
  $('#move').click(move)
}
$(document).ready(setup)
