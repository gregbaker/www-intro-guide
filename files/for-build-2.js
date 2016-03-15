setup = function() {
  color_values = '0123456789abcdef'
  paper = Raphael('container', 350, 120)
  for (red = 0; red <= 15; red += 1) {
    r = paper.rect(red*20, red*5, 30, 30)
    rect_attrs = {
      'fill': '#' + color_values.charAt(red) + '00'
    }
    r.attr(rect_attrs)
  }
}
$(document).ready(setup)
