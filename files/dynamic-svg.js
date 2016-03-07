radius = 20
more = function() {
  paper.circle(25, 25, radius)
  radius = radius - 3
}
setup = function() {
  paper = Raphael('container', 50, 50)
  $('#draw').click(more)
}
$(document).ready(setup)
