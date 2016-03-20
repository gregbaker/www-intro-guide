move = function() {
  dir = $('#direction').val()
  if ( dir == 'up' ) {
    y = -20
  }
  if ( dir == 'down' ) {
    y = 20
  }
  trans = {
	'transform': 't0,' + y
  }
  console.log(trans)
  shape.animate(trans, 1000)
}
setup = function() {
  paper = Raphael('container', 200, 200)
  shape = paper.circle(100, 100, 10)
  $('#move').click(move)
}
$(document).ready(setup)
