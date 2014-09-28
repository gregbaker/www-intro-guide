
# files we need to generate in _site/
PAGES = $(filter-out _%.html, $(wildcard *.html */*.html))

SVG_FIGURES = $(wildcard figures/*.svg)
FIGURES = \
    $(SVG_FIGURES) \
    $(patsubst %.svg, %.svgz, $(SVG_FIGURES)) \
    $(patsubst %.svg, %.png, $(SVG_FIGURES))

DIRECTORIES = assets content figures
STYLES = style.css
ASSETS = assets/cc-by-sa.png

# all files required in _site and _polished_site
DEPS = $(DIRECTORIES) $(ASSETS) $(STYLES) $(FIGURES) $(PAGES)
SITE_DEPS = $(foreach f, $(DEPS), _site/$(f))
POLISHED_SITE_DEPS = $(foreach f, $(DEPS), _polished_site/$(f))

SITE_DIRECTORIES = _site $(foreach d, $(DIRECTORIES), _site/$(d))
POLISHED_SITE_DIRECTORIES = _polished_site $(foreach d, $(DIRECTORIES), _polished_site/$(d))

# extradependencies to make sure we rebuild HTML files when necessary
LAYOUTS = _layouts/base.html contents.json _markup/jinja_environment.py


build: site


# rules to build in _site

_site/%.html: %.html $(LAYOUTS) _site/content
	python _markup/jinga.py $< $@

_site/figures/%.svg: figures/%.svg _site/figures
	cp $< $@

_site/figures/%.svgz: _site/figures/%.svg _site/figures
	gzip -c < $< > $@

_site/figures/%.png: figures/%.svg
	gm convert $< $@
#	inkscape -y 255 -b "#fff" -d 96 -e $@ $<

_site/%.css: %.scss
	sass --scss --style expanded $< $@

_site/assets/%: assets/% _site/assets
	cp $< $@

$(SITE_DIRECTORIES): %:
	mkdir -p $@

site: $(SITE_DEPS)


# rules to build the _polished_site with extra final-version polish

$(POLISHED_SITE_DIRECTORIES): %:
	mkdir -p $@

# optipng all PNG images
_polished_site/%.png: _site/%.png
	cp $< $@
	optipng $@

# scour all SVG images
_polished_site/%.svg: _site/%.svg
	python /usr/share/pyshared/scour.py -q -i $< -o $@
_polished_site/%.svgz: _polished_site/%.svg
	gzip -c < $< > $@

# files with no special rule can be copied as-is
_polished_site/%: _site/%
	cp $< $@

polished-site: $(POLISHED_SITE_DEPS)


upload-draft: polished-site
	rsync -aP --delete _polished_site/* ggbaker@oak.fas.sfu.ca:web/cs/165-draft/

watch:
	watch -n 1 make

clean:
	rm -rf _site _polished_site
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;

.PHONY: all do-polished-build site polished-site upload-draft watch clean
