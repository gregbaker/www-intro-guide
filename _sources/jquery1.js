setup = function() {
  all_paragraphs = jQuery('p')
  all_paragraphs.click(say_hello)
}
jquery_doc = jQuery(document)
jquery_doc.ready(setup)
