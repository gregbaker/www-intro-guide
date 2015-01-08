do_something = function() {
  alert('Hello world!');
}
setup = function() {
  jQuery('p').click(do_something);
}
jQuery(document).ready(setup);

