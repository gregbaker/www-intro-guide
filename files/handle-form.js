show_result = function() {
  typed = jQuery('#something').val();
  jQuery('#result').html('You typed this: ' + typed);
}
setup = function() {
  jQuery('#resultbutton').click(show_result);
}
jQuery(document).ready(setup);
