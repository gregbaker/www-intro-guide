visible = 'yes'
toggle = function() {
  if ( visible == 'yes' ) {
    $('.optional').css({'display': 'none'})
    visible = 'no'
  } else {
    $('.optional').css({'display': 'block'})
    visible = 'yes'
  }
}

setup = function() {
  $('#toggle').click(toggle)
}
$(document).ready(setup)
