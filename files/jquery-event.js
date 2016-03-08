say_hello = function() {
  alert('Hello world!')
}
setup = function() {
  jQuery('p').click(say_hello)
}
jQuery(document).ready(setup)
