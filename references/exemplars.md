# Exemplars and where to take from them

This skill deliberately ships no example gallery. Public TikZ galleries already exist and are
better at breadth than anything maintained here would be. Use them for *technique*, use this
skill for *production*.

## PetarV-/TikZ — https://github.com/PetarV-/TikZ

Dozens of standalone machine-learning diagrams: neural network layers, convolutional stacks,
attention patterns, graphical models.

Take: how to fake depth with layered rectangles and transparency; how to draw repeated units with
`\foreach` and a shared style; how much a figure improves when the same node style is applied to
every element.

Do not take: the coordinate conventions. Each example is tuned to its own canvas, so copying a
fragment into a different layout rarely lands where you expect.

## TeXample.net — https://texample.net/tikz/

The long-running gallery, indexed by domain (physics, chemistry, computer science, timelines).
Its value is the `decorations` and `patterns` examples, which are tedious to derive from the
manual.

Take: brace annotations, calendar and timeline constructions, 3D coordinate systems.

## tikz.dev — https://tikz.dev

The HTML rendering of the PGF/TikZ manual, with a usable search. When a key does not behave as
expected, this is faster than the PDF manual and more reliable than a blog post.

Take: exact semantics of `text width`, `minimum height`, `aspect`, `execute at begin node`, and
the `positioning` library. Most layout bugs in this skill's `pitfalls.md` are misreadings of these
five keys.

## CTAN — https://ctan.org/pkg/pgf

The canonical package. Check the version when a feature from a tutorial does not compile: the
`arrows.meta` syntax replaced `arrows` in 2014 and a lot of circulating examples still use the
old form.

## What the galleries do not give you

- a palette that keeps meaning stable across nine figures
- equal-height cells without manual adjustment
- a check that the canvas is the width you intended
- export rules for Word and publisher portals
- captions that state what the figure must not be read as

That gap is the reason this skill exists.

## On republishing other people's figures

Social-media figure threads, blog posts, and gallery images are usually someone's original work
under default copyright, even when the code is posted. Do not copy screenshots into a public
repository. Instead:

- reproduce the *technique* in your own source, with your own content;
- link to the original post rather than mirroring it;
- if the source is explicitly MIT or CC-licensed, keep the licence text and attribution.

The figures in `examples/` are original work produced with this skill and are covered by this
repository's licence.
