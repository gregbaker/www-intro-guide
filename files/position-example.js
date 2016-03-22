// from http://stackoverflow.com/a/901144/1236542
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    url = url.toLowerCase(); // This is just to avoid case sensitiveness  
    name = name.replace(/[\[\]]/g, "\\$&").toLowerCase();// This is just to avoid case sensitiveness for query parameter name
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}


change_style = function () {
  n = $('#style').val()
  $('#demostyle').attr({'href': 'position' + n + '.css'})
  $('div#css-code blockquote').hide()
  $('div#css-code blockquote#code-position'+n).show()
}

change_width = function () {
  wid = $('#width').val()
  if ( wid == 'guide' ) {
    $('main').attr('class', 'guidewidth')
  } else if ( wid == 'phone' ) {
    $('main').attr('class', 'phonewidth')
  } else if ( wid == 'natural' ) {
    $('main').removeAttr('class')
  }
}

setup = function () {
  $('#style').change(change_style)
  $('#width').change(change_width)
  $('main').attr('class', 'guidewidth')
  
  style = getParameterByName('style')
  if ( style != null ) {
    $('#style').val(style)
  }
  change_style()
  change_width()
}
$(document).ready(setup)
