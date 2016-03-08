slide = function() {
  final = {
    'width': '15',
    'height': '15',
    'transform': 't130,0'
  }
  sq.animate(final, 2000)
}
spin = function() {
  initial = {
    'transform': 'r0'
  }
  final = {
    'transform': 'r360'
  }
  sq.attr(initial)
  sq.animate(final, 2000)
}
setup = function() {
  paper = Raphael('container', 200, 200)
  sq = paper.rect(50, 50, 100, 100)
  $('#spin').click(spin)
  $('#slide').click(slide)
}
$(document).ready(setup)
