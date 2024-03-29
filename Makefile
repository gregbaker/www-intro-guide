
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
    $(patsubst %.svg, %.png, $(SVG_FIGURES)) \
    $(BITMAP_FIGURES)

    #$(patsubst %.svg, %.svgz, $(SVG_FIGURES)) \

DIRECTORIES = assets content figures files floats
GENERATED_PAGES = term_index.html
STYLES = style.css
ASSETS = $(filter-out %~, $(wildcard assets/*) $(wildcard files/*))

# all files required in _site and _polished_site
DEPS = $(DIRECTORIES) $(ASSETS) $(STYLES) $(FIGURES) $(PAGES) $(GENERATED_PAGES)
SITE_PAGES = $(foreach f, $(PAGES), _site/$(f))
SITE_DEPS = $(foreach f, $(DEPS), _site/$(f))
VALIDATE_DEPS = $(filter-out %invalid.html, $(filter %.html, $(SITE_DEPS)))
POLISHED_SITE_DEPS = $(foreach f, $(DEPS), _polished_site/$(f))

SITE_DIRECTORIES = _site $(foreach d, $(DIRECTORIES), _site/$(d))
POLISHED_SITE_DIRECTORIES = _polished_site $(foreach d, $(DIRECTORIES), _polished_site/$(d))

# extra dependencies to make sure we rebuild HTML files when necessary
LAYOUTS = _layouts/base.html _layouts/chapterbase.html _layouts/sectionbase.html _layouts/appendixbase.html contents.json _markup/jinja_environment.py


build: site


# rules to build in _site

_site/term_index.html: $(SITE_PAGES) _markup/generate_index.py
	python3 _markup/generate_index.py $@ $(SITE_PAGES)

_site/%.html: %.html $(LAYOUTS) _site/content
	python3 _markup/jinja.py $< $@

_site/figures/%.svg: figures/%.svg _site/figures
	cp $< $@

_site/figures/%.svgz: _site/figures/%.svg _site/figures
	gzip -c < $< > $@

_site/figures/%.png: figures/%.svg
	inkscape -y 255 -b "#fff" -d 90 -o $@ $<

_site/figures/%.png: figures/%.png
	cp $< $@

_site/figures/%.jpg: figures/%.jpg
	cp $< $@

_site/floats/%.png: floats/%.png _site/floats
	gm convert -resize 160x240 $< $@

_site/floats/%.jpg: floats/%.jpg _site/floats
	gm convert -resize 160x240 $< $@

_site/%.css: %.scss
	sass --style expanded $< $@

_site/assets/%: assets/% _site/assets
	cp $< $@

_site/files/%.html: files/%.html _site/files
	python3 _markup/jinja.py $< $@
_site/files/%.css: files/%.css _site/files
	python3 _markup/rstrip.py $< $@
_site/files/%.js: files/%.js _site/files
	python3 _markup/rstrip.py $< $@

_site/files/%: files/% _site/files
	cp $< $@

$(SITE_DIRECTORIES): %:
	mkdir -p $@

site: $(SITE_DEPS)


# rules to build the _polished_site with extra final-version polish

$(POLISHED_SITE_DIRECTORIES): %:
	mkdir -p $@

# pngquant and optipng all PNG images (let pngquant fail if quality is bad)
_polished_site/%.png: _site/%.png
	pngquant --quality 90-100 - < $< > $@ || true \
	&& optipng -q $@

# scour all SVG images
_polished_site/%.svg: _site/%.svg
	/usr/bin/scour --enable-id-stripping --enable-comment-stripping --shorten-ids -q -i $< -o $@
_polished_site/%.svgz: _polished_site/%.svg
	gzip -c < $< > $@

# files with no special rule can be copied as-is
_polished_site/%: _site/%
	cp $< $@

polished-site: validate $(POLISHED_SITE_DEPS)


upload-draft: polished-site
	rsync -aP --delete _polished_site/* ggbaker@rcga-linux-ts1.dc.sfu.ca:web/cs/165-draft/
upload: polished-site
	rsync -aP --delete _polished_site/* ggbaker@rcga-linux-ts1.dc.sfu.ca:web/165common/study-guide/

watch:
	watch -n 1 make

validate: $(VALIDATE_DEPS)
	python3 _markup/validate.py $(VALIDATE_DEPS)

validate-remote: validate $(foreach f, $(VALIDATE_DEPS), $(f)-validate-remote)
%-validate-remote: %
	python3 _markup/w3c-validator.py $<

check-links: $(SITE_DEPS)
	python3 _markup/check_links.py _site/content/*.html _site/files/*.html

clean:
	rm -rf _site _polished_site _figure_build/*.jpeg _figure_build/*.png .link_cache.json
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;

.PHONY: all do-polished-build site polished-site upload-draft watch validate validate-remote clean
