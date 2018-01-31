
Documentation
=============

TIC uses Markdown and Restructured Text to document the project. Markdown
and Restructured Text are text files with additional notation to control how
the text is displayed. You are able to include images, references, titles,
etc into your document. Yet the document is still readable using just a text editor
or cat-ing the files in a Unix terminal.

The Markdown and ReStructured text files are converted into HTML files with
the Python tool Sphinx. http://www.sphinx-doc.org/en/stable/index.html.  If you
want to view the TIC documentation you can open up the index.rst,
$TIC_PATH/docs/source/index.rst, in our favorite browser.  On aging1a/aging2a
we have created the TIC alias, tic_help, to launch the TIC HTML pages in
FireFox.


Creating Your Own documentation
-------------------------------

The TIC documentation is created with text files written in Markdown or
Restructured text. This allows anyone to write documentation and have it added
directly to the TIC help.  Even you don't know Markdown and Restructured text
you can still insert plain text into the TIC documentation.  These files can
be edited by someone who knows Markdown and/or Restructured Text.


Adding Your Own Documentation to TIC Repository
-----------------------------------------------

Creating your own documentation is a four simple step process

1) Write the documentation as text file in either Markdown or ReStructured
Text.  Sphinx in the TIC project has been configured to support both.

2) Add the document to the TIC repository by copying the file to the
$TIC_PATH/source

3) Add, commit, and push the document to the TIC repository.

    1) git add <filename>
    1) git commit -m "Adding new file to the TIC documentation
    1) git push

4) Add the file you just created into the TIC index.rst file in the toctree
section.

5) Rebuild the documentation. This may be accomplished with the TIC alias tic_make_docs.



References
----------

For Markdown

* https://blog.ghost.org/markdown/
* https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet


For ReStructured Text

* https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#include-other-rst-files-with-the-toctree-directive



