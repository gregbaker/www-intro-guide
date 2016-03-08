p_click = function() {
  jQuery('#changeme').html('Somebody clicked me.')
}
h1_hover = function() {
  jQuery('#changeme').html('Mouse <em>over</em> the &lt;h1&gt;.')
}
setup = function() {
  jQuery('#changeme').click(p_click)
  jQuery('h1').mouseover(h1_hover)
}
jQuery(document).ready(setup)
