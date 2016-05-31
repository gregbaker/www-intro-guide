"use strict";

SyntaxHighlighter.defaults['light'] = true;
SyntaxHighlighter.defaults['auto-links'] = false;
SyntaxHighlighter.all();

var cookiename = 'cmpt165_lynda';
var lynda_base_default = 'https://www.lynda.com';
var lynda_base_urls = {
	lynda: 'https://www.lynda.com',
	sfu: 'https://wwwlyndacom.proxy.lib.sfu.ca',
};
var lynda_choices = {
	lynda: 'main Lynda.com',
	sfu: 'SFU library Lynda.com',
};

function update_lynda_link(base, elt) {
	var base_url = lynda_base_urls[base];
	if ( base_url ) {
		var url = base_url + elt.getAttribute('data-path');
		elt.setAttribute('href', url);
	}
}
function lynda_annotate(base, elt) {
}

function lynda_button(elt) {
	var base = elt.getAttribute('data-base');
	elt.addEventListener('click', function() { lynda_set(base); } );
}

function lynda_set(base) {
	Cookies.set(cookiename, base, { expires: 365, path: '/' });
	alert('Lynda links here will now direct you to the ' + lynda_choices[base] + ' site. You may have to reload pages if you go back.')
}

function lynda_setup() {
	var base = Cookies.get(cookiename);
	var lyndas = document.getElementsByClassName('lynda');
	var elt;
	for ( var i=0; i<lyndas.length; i++ ) {
		elt = lyndas[i];
		if ( elt.tagName == 'A' || elt.tagName == 'a' ) {
			/* a link we care about */
			update_lynda_link(base, elt);
		} else if ( elt.tagName == 'ASIDE' || elt.tagName == 'aside' ) {
			/* an aside block needing annotation */
			lynda_annotate(base, elt);
		} else if ( elt.tagName == 'BUTTON' || elt.tagName == 'button' ) {
			/* an aside block needing annotation */
			lynda_button(elt);
		}
	}
}

document.addEventListener("DOMContentLoaded", lynda_setup);
