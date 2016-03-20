move = function() {
  dir = $('#direction').val()
  if ( dir == 'up' ) {
    trans = 't0,-20'
  }
  if ( dir == 'down' ) {
    trans = 't0,20'
  }
  
  attr = {
	'transform': trans
  }
  shape.animate(attr, 1000)
}
setup = function() {
  paper = Raphael('container', 200, 200)
  shape = paper.circle(100, 100, 10)
  $('#move').click(move)
}
$(document).ready(setup)
