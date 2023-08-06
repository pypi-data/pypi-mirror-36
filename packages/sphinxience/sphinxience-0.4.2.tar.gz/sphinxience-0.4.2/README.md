# Sphinxience

A Sphinx extension to assist in publishing scientific writing in either HTML or PDF. 

This extension mainly consists of a number of roles and directives, so that you can use most LaTeX macros more easily than writing inline LaTeX in Sphinx. This extension will also change the LaTeX output, to conform to what is expected of scientific papers submitted to conferences/journals. By default, Sphinxience uses the `article` documentclass in LaTeX, but below there are instructions on how to fork Sphinxience so you can start to tweak every aspect of it.

Sphinxience is pronounced either like "Sphinx science" or rhyming with "experience". It's up to you.

## How to use this

There are only a few options to set in the `conf.py` file in your Sphinx project, but the easiest way is probably to copy this template and to follow the instructions: https://github.com/bgeron/sphinxience-template .

Because Sphinxience modifies the internals of Sphinx's LaTeX rendering, it is unfortunately rather coupled to a specific version of Sphinx. Currently, that is Sphinx version 1.7. If you use Sphinxience via this template, then Poetry will make sure that you always use a compatible version of Sphinx.

## How to fork and tweak this

If you writing substantive documents with this, you might well feel the need to further customize the available widgets and their LaTeX output. The best way is probably to

1.  Fork this Sphinxience project locally,
2.  Change the `sphinxience` line in the `pyproject.toml` for your Sphinx project:

        sphinxience = {path = "/your/sphinxience/checkout"}

3.  Use the local checkout in the virtualenv, by running

        poetry install --develop=sphinxience

If you now run `make html` or `make latexpdf` again, then the local checkout of Sphinxience will be used.

This documentation will turn out useful: [Developing extensions for Sphinx](http://www.sphinx-doc.org/en/master/extdev/index.html).

Note that if you change the intermediate doctrees that Sphinx produces, then it will not suffice to run `make html` or `make latexpdf` and you must additionally run `make clean`.

## Status

**Warning: I'm still in the (slow) process of open sourcing this.**

This works:

-   HTML output
-   LaTeX output
-   A `skip` directive that includes some vertical space, in both HTML and LaTeX:

        .. skip:: big

    (The `big` size corresponds to a LaTeX `\bigskip`.)

This is still to do:

-   Come up with a good way to write preambles for both the HTML and the LaTeX output. (In my PhD thesis, I have a rather hacky mechanism.)
-   Some reasonable amount of documentation
-   Open source my theorems/lemmas/etc directive, and the proof directive
-   Open source my convenient role for `\ref`
-   Open source miscellaneous roles and directives


## General note

The code here should work and be reasonable clean, but it could e.g. use a linter to catch unused imports. Patches are welcome! Also if you developed a new directive or role.

