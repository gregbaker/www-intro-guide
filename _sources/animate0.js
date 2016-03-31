initial_attr = {
  'fill': '#fff',
  'stroke-width': '1'
}
final_attr = {
  'fill': '#f00',
  'stroke-width': '5'
}
rect = paper.rect(10, 10, 20, 20)
rect.attr(initial_attr)
rect.animate(final_attr, 2000)
