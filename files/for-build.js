do_animation = function() {
  paper = Raphael('container2', 140, 140)
  rect_attrs = {
    'fill': '#292',
    'stroke-width': '1.5'
  }
  for (count = 0; count <= 11; count += 1) {
    r = paper.rect(50, 50, 40, 40)
    r.attr(rect_attrs)
    anim_attrs = {
      'transform': 'r' + (count*3) + 's' + (3 - count*0.25)
    }
    r.animate(anim_attrs, 2000)
  }
}

setup = function() {
  paper = Raphael('container1', 150, 150)
  for (count = 1; count <= 6; count += 1) {
    r = paper.rect(30, 30, 90, 90)
    animation_attrs = {
      'transform': 'r' + (count*15)
    }
    r.attr(animation_attrs)
  }


  $('#container2').html('')
  $('button').click(do_animation)
  do_animation()
  
  for (count = 0; count <= 11; count += 1) {
    t = 'r' + (count*3) + 's' + (3 - count*0.25)
    $('#transforms').append('count=' + count + '... \'' + t + '\'\n')
  }
}
$(document).ready(setup)
