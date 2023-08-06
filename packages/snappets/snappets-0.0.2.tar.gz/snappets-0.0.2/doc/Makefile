# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = Snappets
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
# |:here:|

SNIPPETS = snippets.pl
SNC_ = $(SNIPPETS)
SNC = $(SNC_) --cat
SNR_ = $(SNIPPETS) --replace --process
SNR = $(SNR_) --cat

# |:here:| generic rules

%.png: %.msc
	mscgen -T png -F FreeSans -o $@ $<

_static/%.png: %.msc
	mscgen -T png -F FreeSans -o $@ $<

%.png: %.eps
	convert $(CONVERT_IN_OPTS) $< $(CONVERT_OUT_OPTS) $@

_static/%.png: %.eps
	convert $(CONVERT_IN_OPTS) $< $(CONVERT_OUT_OPTS) $@

%.eps: %.iwk
	$(tooldir)/iwps.pl $(IWPS_OPTS) $<
	$(PS2EPSI) $<.ps
	rm -f $<.ps
	mv $<.epsi $@

_static/%.eps: %.iwk
	$(tooldir)/iwps.pl $(IWPS_OPTS) $<
	$(PS2EPSI) $<.ps
	rm -f $<.ps
	mv $<.epsi $@

%.png: %.dot
	dot -T png -o $@ $<

_static/%.png: %.dot
	dot -T png -o $@ $<

%.png: %.svg
	convert $< $@

_static/%.png: %.svg
	convert $< $@

_static/%.svg: %.html
	webvector $< $@ svg

%.svg: %.html
	webvector $< $@ svg

_static/%.pdf: _static/%.svg
	convert $< $@

_static/%.pdf: %.svg
	convert $< $@

%.pdf: %.svg
	convert $< $@

_static/%.txt: %.xlsx
	@(						\
	echo '.. table:: $<';				\
	echo '   :class: longtable';			\
	echo;						\
	xlsx-dump.sh --rest $< | sed 's,^,   ,';	\
	) >$@

# |:here:| chapters

# CHAPTERS += ../README-topic.txt
# |:chapter:|
CHAPTERS_RST := $(patsubst ../README-%.txt, %.rst.auto, $(CHAPTERS))

index: index.rst.auto overview.rst.auto
	@printf ""

index.rst.auto: ../README.txt doc_defs.snip index-header.snip index-footer.snip
	@(							\
	export SNIPS_PATH="..:.:$SNIPS_PATH";			\
	echo "$(SNR_) --key doc_index --cat $< >$@";		\
	$(SNR_) --key doc_index --cat  $< >$@ || rm -f $@;	\
	test -s $@ || rm -f $@;					\
	)

overview.rst.auto: ../README.txt doc_defs.snip overview-header.snip overview-footer.snip
	@(							\
	export SNIPS_PATH="..:.:$SNIPS_PATH";			\
	echo "$(SNR_) --key doc_overview --cat $< >$@";		\
	$(SNR_) --key doc_overview --cat  $< >$@ || rm -f $@;	\
	test -s $@ || rm -f $@;					\
	)

%.rst.auto: ../README-%.txt doc_defs.snip chapter-header.snip chapter-footer.snip
	@(							\
	export SNIPS_PATH="..:.:$SNIPS_PATH";			\
	echo "$(SNR_) --key doc_chapter --cat $< >$@";		\
	$(SNR_) --key doc_chapter --cat $< >$@ || rm -f $@;	\
	test -s $@ || rm -f $@;					\
	)

# |:here:| images

# IMAGES += base_init_seq.png
IMAGES_STATIC := $(patsubst %, _static/%, $(IMAGES))

# IMAGES_PNG += base_init_seq.png
# IMAGES_HTML += emacs-buffer-html-svg.html
IMAGES_STATIC_SVG := $(patsubst %.html, _static/%.svg, $(IMAGES_HTML))
IMAGES_STATIC_PDF := $(patsubst %.html, _static/%.pdf, $(IMAGES_HTML))

IMAGES = $(IMAGES_PNG) $(IMAGES_HTML)
IMAGES_STATIC += $(IMAGES_STATIC_SVG)
IMAGES_STATIC += $(IMAGES_STATIC_PDF)

# |:here:| tables

# TABLES += matrix.xlsx
TABLES_STATIC := $(patsubst %.xlsx, _static/%.txt, $(TABLES))

# |:here:| diagrams

UML_EXTRACT = line_diversion.py

# fillme_SOURCE   = ../bin/fillme.sh
# fillme_SFX      = _act
# fillme_MATCH    = '^a'
# fillme_NAME     = $(lastword $(subst /, ,$(fillme_SOURCE)))
# fillme_EXT      = $(lastword $(subst ., ,$(fillme_NAME)))
# fillme_BASE     = $(patsubst %.$(fillme_EXT),%,$(fillme_NAME))
# fillme_PUML     = _static/$(fillme_BASE)$(fillme_SFX).puml
# DIAGRAM_SOURCES += $(fillme_SOURCE)
# DIAGRAMS        += $(fillme_PUML)
# $(fillme_PUML): $(fillme_SOURCE)
# 	$(UML_EXTRACT) --match $(fillme_MATCH) $< >$@

# |:here:| local targets

chapters: $(CHAPTERS_RST)
	@printf ""

images: $(IMAGES_STATIC)
	@printf ""

tables: $(TABLES_STATIC)
	@printf ""

diagrams: $(DIAGRAMS)
	@printf ""

all-local: index chapters images tables diagrams
	@printf ""

html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext: all-local

# existing files must have a more specific rule than the default
../README.txt \
doc_defs.snip \
standalone-header.snip standalone-footer.snip \
index-header.snip index-footer.snip \
overview-header.snip overview-footer.snip \
chapter-header.snip chapter-footer.snip \
$(CHAPTERS) $(IMAGES) $(TABLES) $(DIAGRAM_SOURCES):
	@printf ""

# :ide: COMPILE: Standard
# . (let ((args "")) (compile (concat "make -k " args)))

# :ide: COMPILE: all-local
# . (let ((args "all-local")) (compile (concat "make -k " args)))

# :ide: COMPILE: epub
# . (let ((args "epub")) (compile (concat "make -k " args)))

# :ide: COMPILE: latexpdf
# . (let ((args "latexpdf")) (compile (concat "make -k " args)))

# :ide: COMPILE: html
# . (let ((args "html")) (compile (concat "make -k " args)))
