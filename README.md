# Scibian 9 HPC Cluster Installation Guide

## Read

The document is available online:
https://scibian.github.io/scibian-hpc-install-guide

## Build

To build this doc, install the following packages:

* asciidoctor >= 0.1.4
* asciidoctor-scibian-tpl-latex
* rubber
* texlive-latex-extra
* inkscape

Then, run:

```
make
```

## Publish

In order to publish new versions of the document online, commit updated html
and pdf outputs of the document in *gh-pages* branch and update `index.html`
file accordingly.

Please also mind to update scibian.org website documentation page accordingly:
https://github.com/scibian/scibian.org/blob/master/content/docs.html
