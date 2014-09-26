HTML_PAGES = $(wildcard *.html */*.html)
MD_PAGES = $(patsubst %.md, %.html, $(wildcard *.md */*.md))
ALL_PAGES = $(filter-out _%.html, $(HTML_PAGES) $(MD_PAGES))
PAGES = $(foreach p,$(ALL_PAGES),_site/$(p))

SVG_FIGURES = $(foreach f,$(wildcard figures/*.svg),_site/$(f))
FIGURES = \
    $(SVG_FIGURES) \
    $(patsubst %.svg, %.svgz, $(SVG_FIGURES)) \
    $(patsubst %.svg, %.png, $(SVG_FIGURES))

DIRECTORIES = assets content figures
SITE_DIRECTORIES = $(foreach d, $(DIRECTORIES), _site/$(d))

LAYOUTS = _layouts/base.html
STYLES = _site/style.css
ASSETS = _site/assets/cc-by-sa.png

all: site

_site/%.html: %.html $(LAYOUTS)
	python _markup/jinga.py $< $@

_site/figures/%.svg: figures/%.svg
	if [ x$(POLISH) = x1 ]; then \
	  python /usr/share/pyshared/scour.py -q -i $< -o $@; \
	else \
	  cp $< $@; \
	fi

_site/figures/%.svgz: _site/figures/%.svg
	gzip -c < $< > $@

_site/figures/%.png: figures/%.svg
	gm convert $< $@
#	inkscape -y 255 -b "#fff" -d 96 -e $@ $<
	if [ x$(POLISH) = x1 ]; then optipng -q $@; fi

_site/%.css: %.scss
	sass --scss --style expanded $< $@

_site/assets/%: assets/%
	cp $< $@

$(SITE_DIRECTORIES): %:
	mkdir -p $@

site: $(SITE_DIRECTORIES) $(ASSETS) $(STYLES) $(FIGURES) $(PAGES)

do-polished-build:
	# turn on various final-version-only optimizations of output
	$(eval POLISH = 1)

final-site: do-polished-build site

clean:
	rm -rf _site/*
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;

.PHONY: all site clean
