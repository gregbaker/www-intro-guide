setup = function() {
  for (step = 1; step <= 10; step += 1) {
    $('#example1').append('<p>One more paragraph.</p>')
  }

  for (n = 1; n <= 6; n += 1) {
    $('#example2').append('<p>Paragraph #' + n + '</p>')
  }
  
  paper = Raphael('container', 400, 200)
  circle_attrs = {
    'stroke': '#c50',
    'stroke-width': '2'
  }
  rect_attrs = {
    'fill': '#292',
    'stroke-width': '1.5'
  }
  for (count = 1; count <= 12; count += 1) {
    c = paper.circle(10 + count*14, 20 + count*12, 6)
    c.attr(circle_attrs)
    r = paper.rect(250, 100, 40, 40)
    r.attr(rect_attrs)
    r.rotate(count*3)
    r.scale(3 - count*0.25)
  }

}
$(document).ready(setup)
