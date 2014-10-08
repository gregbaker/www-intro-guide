
# files we need to generate in _site/
PAGES = $(filter-out _%.html, \
          $(filter-out files/%, \
            $(wildcard *.html */*.html) \
          )\
        )

SVG_FIGURES = $(wildcard figures/*.svg) $(wildcard floats/*.svg)
BITMAP_FIGURES = $(wildcard figures/*.png) $(wildcard floats/*.png) \
                 $(wildcard figures/*.jpg) $(wildcard floats/*.jpg)
FIGURES = \
    $(SVG_FIGURES) \
    $(patsubst %.svg, %.svgz, $(SVG_FIGURES)) \
    $(patsubst %.svg, %.png, $(SVG_FIGURES)) \
    $(BITMAP_FIGURES)

DIRECTORIES = assets content figures files floats
STYLES = style.css
ASSETS = $(filter-out %~, $(wildcard assets/*) $(wildcard files/*))

# all files required in _site and _polished_site
DEPS = $(DIRECTORIES) $(ASSETS) $(STYLES) $(FIGURES) $(PAGES)
SITE_DEPS = $(foreach f, $(DEPS), _site/$(f))
POLISHED_SITE_DEPS = $(foreach f, $(DEPS), _polished_site/$(f))

SITE_DIRECTORIES = _site $(foreach d, $(DIRECTORIES), _site/$(d))
POLISHED_SITE_DIRECTORIES = _polished_site $(foreach d, $(DIRECTORIES), _polished_site/$(d))

# extra dependencies to make sure we rebuild HTML files when necessary
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
	inkscape -y 255 -b "#fff" -d 96 -e $@ $<

_site/figures/%.png: figures/%.png
	cp $< $@

_site/floats/%.png: floats/%.png # TODO: srcset resizes
	gm convert -resize 160x240 $< $@

_site/floats/%.jpg: floats/%.jpg
	gm convert -resize 160x240 $< $@

_site/%.css: %.scss
	sass --scss --style expanded $< $@

_site/assets/%: assets/% _site/assets _site/files
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

polished-site: validate $(POLISHED_SITE_DEPS)


upload-draft: polished-site
	rsync -aP --delete _polished_site/* ggbaker@oak.fas.sfu.ca:web/cs/165-draft/

watch:
	watch -n 1 make

validate: $(SITE_DEPS)
	python _markup/validate.py $(SITE_DEPS)

clean:
	rm -rf _site _polished_site
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;

.PHONY: all do-polished-build site polished-site upload-draft watch validate clean
