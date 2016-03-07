labels = function() {
  paper.text(30, 20, 'p1')
  paper.text(30, 40, 'p2')
  paper.text(30, 60, 'p3')
  paper.text(30, 80, 'p4')
  paper.text(30, 120, 'p5')
  paper.text(180, 120, 'p6')
  paper.text(30, 220, 'p7')
}

setup = function() {
  paper = Raphael('container', 400, 270)

  p1 = paper.path('M50,20 L390,30')
  p1.attr({'stroke': '#f00', 'stroke-width': '3'})

  p2 = paper.path('M50,40 L260,10 L280,40 L390,40')
  p2.attr({'stroke': '#0c0', 'stroke-width': '3'})

  p3 = paper.path('M50,60 L260,30 L280,60 Z')
  p3.attr({'stroke': '#00d', 'stroke-width': '3'})
  
  p4 = paper.path('M50,80 T150,80 T150,100 T390,80')
  p4.attr({'stroke': '#f70', 'stroke-width': '3'})
  paper.circle(150, 80, 3)
  paper.circle(150, 100, 3)

  p5 = paper.path('M50,120 S150,180 150,120')
  p5.attr({'stroke': '#a0f', 'stroke-width': '3'})
  paper.circle(150, 180, 3)

  p6 = paper.path('M200,120 S380,170 300,120')
  p6.attr({'stroke': '#dd0', 'stroke-width': '3'})
  paper.circle(380, 170, 3)

  p7 = paper.path(
    'M50,220 L180,260 S220,260 220,220 S350,220 300,240 Z')
  p7.attr({'stroke': '#000', 'stroke-width': '3'})

  labels()
}
$(document).ready(setup)
