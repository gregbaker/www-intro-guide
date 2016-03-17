y = 8
add = function() {
  entered_text = $('#txt-input').val()
  len = entered_text.length
  txt = paper.text(100, y, entered_text)
  rect = paper.rect(200, y-5, len*8, 10)
  y = y + 12
}
setup = function() {
  paper = Raphael('container', 400, 100)
  $('#add').click(add)
}
$(document).ready(setup)
