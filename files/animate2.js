anim_right = function() {
  new_attr = {
    'transform': 't100,0'
  }
  circ.animate(new_attr, 1000, 'linear', anim_left)
}
anim_left = function() {
  new_attr = {
    'transform': 't0,0'
  }
  circ.animate(new_attr, 1000, 'linear', anim_right)
}
setup = function() {
  paper = Raphael('container', 200, 100)
  circ = paper.circle(50, 50, 30)
  anim_right()
}
$(document).ready(setup)
