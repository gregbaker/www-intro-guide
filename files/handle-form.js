show_result = function() {
  typed = $('#something').val();
  $('#result').html('You typed this: ' + typed);
}
setup = function() {
  $('#resultbutton').click(show_result);
}
$(document).ready(setup);
