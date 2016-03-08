mouse_arrived = function() {…}
mouse_left = function() {…}
setup = function() {
  jQuery("#hoverable").mouseenter(mouse_arrived)
  jQuery("#hoverable").mouseleave(mouse_left)
}
jQuery(document).ready(setup)


