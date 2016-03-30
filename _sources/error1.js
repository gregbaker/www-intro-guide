something_click = function() {
  console.log('something_click running')
  ⋮
}
setup = function() {
  console.log('setup running')
  jQuery('#something').click(something_click)
}
jQuery(document).ready(setup)
