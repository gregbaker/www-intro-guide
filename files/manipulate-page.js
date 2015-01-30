h1_hover = function() {
  jQuery('#changeme').html('Mouse <em>over</em> the &lt;h1&gt;.');
}
p_click = function() {
  jQuery('#changeme').html('Somebody clicked me.');
}
setup = function() {
  jQuery('#changeme').click(p_click);
  jQuery('h1').mouseover(h1_hover);
}
jQuery(document).ready(setup);
