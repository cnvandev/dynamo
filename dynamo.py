#!/usr/bin/python

'''
Dynamo
======

Dynamo is a super-quick HTML generator written by Chris Vandevelde
(chris.vandevelde@uwaterloo.ca). You can quickly write HTML in a sweet,
functional style that mimics actually writing HTML (methinks), so you can get
away from constructing objects and get back to writin' some HTML code. There
are awesome libraries for templating (check out Jinja!) and parsing/generating
HTML in other styles, this one's for someone looking to quickly and
programmatically generate HTML. Dump it to a file or write it to a request
stream and you're all good!

More information can be found in the README.md file, a usage sample can be
found in sample.py, or take a look at the code to see how it works. If you're
still having problems, let me know and I'll help out if I can.

The project page is at http://github.com/cnvandev/dynamo, feel free to
contribute or make requests!

'''

import collections

# Some constants for us.
START_BRACKET = "<"
END_BRACKET = ">"
START_CONDITION = "["
END_CONDITION = "["
CLOSER = "/"
NEWLINE = "\n"
TAB = "\t"
SPECIAL_MARKER = "!"
COMMENT = "--"


def tag_with_child(tag, *children, **args):
    ''' Return a string representation of an XML tag that can contain a child
    element.

    '''

    # If we have more than one child, pad the children by one tab and drop the
    # child list by one newline.
    open_padding = ""
    close_padding = ""
    if len(children) > 1 and children[0]:
        # If our first child is a dictionary, we're being given the arguments
        # first. Set args to this dict.
        if isinstance(children[0], dict):
            children = list(children)
            args = children.pop(0)

        if children[0].startswith(START_BRACKET):
            children = map(lambda child: child.replace(NEWLINE, NEWLINE + TAB),
                           children)
            open_padding = NEWLINE + TAB
            close_padding = NEWLINE
    else:
        children = []

    return make_tag(tag, **args) + open_padding + (NEWLINE + TAB).join(
        children) + close_padding + close_tag(tag)


def make_tag(tag, **args):
    ''' Given 'string' and a dict of args, returns <string arg1="blah">
    (etc. for more args, you get the idea)

    '''

    return START_BRACKET + tag + format_args(**args) + END_BRACKET


def close_tag(tag, **args):
    ''' Given 'string', returns </string> '''

    return make_tag(CLOSER + tag)


def closed_tag(tag, *children, **args):
    ''' Returns a self-contained XML tag that cannot contain a child
    element. Think <img src="image.jpg" />.

    '''

    # Allow the possibility of a single dict child argument.
    if len(children) > 0:
        if len(children) > 1 or not isinstance(children[0], dict):
            raise AssertionError("Your self-contained <%s /> tag contains a \
                non-hash child - you are doing it wrong." % tag)

        # If our first child is a dictionary, we're being given the arguments
        # first. Set args to this dict.
        children = list(children)
        args = children.pop(0)

    return make_tag(tag + format_args(**args) + " " + CLOSER)


def special_tag(tag):
    ''' Returns a 'special' tag of the form <!tag>, used for doctypes and
    comments in HTML5.

    '''

    return make_tag(SPECIAL_MARKER + tag)


def format_args(**args):
    ''' Returns a string of XML tag arguments from an unpacked dict. '''

    if not args:
        return ""

    return " " + " ".join([format_arg_value(key, value) for key, value in
           args.iteritems()])


def format_arg_value(key, value):
    ''' Returns a string representing an HTML attribute as a key-value pair
    presented like key="value". If the value is iterable, will return 

    '''

    if isinstance(value, collections.Iterable) and not isinstance(value,
        basestring):
        string = format_list_attribute(value)
    else:
        string = value

    return "%s=\"%s\"" % (key, string)


def format_list_attribute(list):
    ''' Returns a "list" value suitable for HTML (for now it's
    space-delimited strings).

    '''

    return " ".join(value)


# Here it gets boring - these functions are just convenient wrappers for
# the functions above. To add new acceptable HTML tags, add a new function
# under this comment.
###############################################################################


# "Special" tags.

def comment(text): return special_tag(" ".join([COMMENT, text, COMMENT]))
def doctype(text): return special_tag(" ".join(["DOCTYPE", text]))
def conditional_comment(condition, text):
    return special_tag(COMMENT + START_CONDITION + condition + END_CONDITION) + text + special_tag(START_CONDITION + "endif" + END_CONDITION + COMMENT)

# Self-closing tags.

def area(*children, **args): return closed_tag("area", *children, **args)
def base(*children, **args): return closed_tag("base", *children, **args)
def br(*children, **args): return closed_tag("br", *children, **args)
def col(*children, **args): return closed_tag("col", *children, **args)
def hr(*children, **args): return closed_tag("hr", *children, **args)
def img(*children, **args): return closed_tag("img", *children, **args)
def Input(*children, **args): return closed_tag("input", *children, **args)
def link(*children, **args): return closed_tag("link", *children, **args)
def meta(*children, **args): return closed_tag("meta", *children, **args)
def param(*children, **args): return closed_tag("param", *children, **args)

# Regular tags.

def a(*children, **args): return tag_with_child("a", *children, **args)
def abbr(*children, **args): return tag_with_child("abbr", *children, **args)
def acronym(*children, **args): return tag_with_child("acronym", *children, **args)
def address(*children, **args): return tag_with_child("address", *children, **args)
def applet(*children, **args): return tag_with_child("applet", *children, **args)
def article(*children, **args): return tag_with_child("article", *children, **args)
def aside(*children, **args): return tag_with_child("aside", *children, **args)
def audio(*children, **args): return tag_with_child("audio", *children, **args)
def b(*children, **args): return tag_with_child("b", *children, **args)
def bdi(*children, **args): return tag_with_child("bdi", *children, **args)
def bdo(*children, **args): return tag_with_child("bdo", *children, **args)
def blockquote(*children, **args): return tag_with_child("blockquote", *children, **args)
def body(*children, **args): return tag_with_child("body", *children, **args)
def button(*children, **args): return tag_with_child("button", *children, **args)
def canvas(*children, **args): return tag_with_child("canvas", *children, **args)
def caption(*children, **args): return tag_with_child("caption", *children, **args)
def cite(*children, **args): return tag_with_child("cite", *children, **args)
def code(*children, **args): return tag_with_child("code", *children, **args)
def colgroup(*children, **args): return tag_with_child("colgroup", *children, **args)
def command(*children, **args): return tag_with_child("command", *children, **args)
def datalist(*children, **args): return tag_with_child("datalist", *children, **args)
def dd(*children, **args): return tag_with_child("dd", *children, **args)
def Del(*children, **args): return tag_with_child("del", *children, **args)
def details(*children, **args): return tag_with_child("details", *children, **args)
def dfn(*children, **args): return tag_with_child("dfn", *children, **args)
def div(*children, **args): return tag_with_child("div", *children, **args)
def dl(*children, **args): return tag_with_child("dl", *children, **args)
def dt(*children, **args): return tag_with_child("dt", *children, **args)
def em(*children, **args): return tag_with_child("em", *children, **args)
def embed(*children, **args): return tag_with_child("embed", *children, **args)
def fieldset(*children, **args): return tag_with_child("fieldset", *children, **args)
def figcaption(*children, **args): return tag_with_child("figcaption", *children, **args)
def figure(*children, **args): return tag_with_child("figure", *children, **args)
def footer(*children, **args): return tag_with_child("footer", *children, **args)
def form(*children, **args): return tag_with_child("form", *children, **args)
def h1(*children, **args): return tag_with_child("h1", *children, **args)
def h2(*children, **args): return tag_with_child("h2", *children, **args)
def h3(*children, **args): return tag_with_child("h3", *children, **args)
def h4(*children, **args): return tag_with_child("h4", *children, **args)
def h5(*children, **args): return tag_with_child("h5", *children, **args)
def h6(*children, **args): return tag_with_child("h6", *children, **args)
def head(*children, **args): return tag_with_child("head", *children, **args)
def header(*children, **args): return tag_with_child("header", *children, **args)
def hgroup(*children, **args): return tag_with_child("hgroup", *children, **args)
def html(*children, **args): return tag_with_child("html", *children, **args)
def i(*children, **args): return tag_with_child("i", *children, **args)
def iframe(*children, **args): return tag_with_child("iframe", *children, **args)
def ins(*children, **args): return tag_with_child("ins", *children, **args)
def kbd(*children, **args): return tag_with_child("kbd", *children, **args)
def keygen(*children, **args): return tag_with_child("keygen", *children, **args)
def label(*children, **args): return tag_with_child("label", *children, **args)
def legend(*children, **args): return tag_with_child("legend", *children, **args)
def li(*children, **args): return tag_with_child("li", *children, **args)
def Map(*children, **args): return tag_with_child("map", *children, **args)
def mark(*children, **args): return tag_with_child("mark", *children, **args)
def menu(*children, **args): return tag_with_child("menu", *children, **args)
def meter(*children, **args): return tag_with_child("meter", *children, **args)
def nav(*children, **args): return tag_with_child("nav", *children, **args)
def noscript(*children, **args): return tag_with_child("noscript", *children, **args)
def Object(*children, **args): return tag_with_child("object", *children, **args)
def ol(*children, **args): return tag_with_child("ol", *children, **args)
def optgroup(*children, **args): return tag_with_child("optgroup", *children, **args)
def option(*children, **args): return tag_with_child("option", *children, **args)
def output(*children, **args): return tag_with_child("output", *children, **args)
def p(*children, **args): return tag_with_child("p", *children, **args)
def pre(*children, **args): return tag_with_child("pre", *children, **args)
def progress(*children, **args): return tag_with_child("progress", *children, **args)
def q(*children, **args): return tag_with_child("q", *children, **args)
def rp(*children, **args): return tag_with_child("rp", *children, **args)
def rt(*children, **args): return tag_with_child("rt", *children, **args)
def ruby(*children, **args): return tag_with_child("ruby", *children, **args)
def s(*children, **args): return tag_with_child("s", *children, **args)
def samp(*children, **args): return tag_with_child("samp", *children, **args)
def script(*children, **args): return tag_with_child("script", *children, **args)
def section(*children, **args): return tag_with_child("section", *children, **args)
def select(*children, **args): return tag_with_child("select", *children, **args)
def small(*children, **args): return tag_with_child("small", *children, **args)
def source(*children, **args): return tag_with_child("source", *children, **args)
def span(*children, **args): return tag_with_child("span", *children, **args)
def strong(*children, **args): return tag_with_child("strong", *children, **args)
def style(*children, **args): return tag_with_child("style", *children, **args)
def sub(*children, **args): return tag_with_child("sub", *children, **args)
def summary(*children, **args): return tag_with_child("summary", *children, **args)
def sup(*children, **args): return tag_with_child("sup", *children, **args)
def table(*children, **args): return tag_with_child("table", *children, **args)
def tbody(*children, **args): return tag_with_child("tbody", *children, **args)
def td(*children, **args): return tag_with_child("dt", *children, **args)
def textarea(*children, **args): return tag_with_child("textarea", *children, **args)
def tfoot(*children, **args): return tag_with_child("tfoot", *children, **args)
def th(*children, **args): return tag_with_child("th", *children, **args)
def thead(*children, **args): return tag_with_child("thead", *children, **args)
def time(*children, **args): return tag_with_child("time", *children, **args)
def title(*children, **args): return tag_with_child("title", *children, **args)
def tr(*children, **args): return tag_with_child("tr", *children, **args)
def track(*children, **args): return tag_with_child("track", *children, **args)
def u(*children, **args): return tag_with_child("u", *children, **args)
def ul(*children, **args): return tag_with_child("ul", *children, **args)
def var(*children, **args): return tag_with_child("var", *children, **args)
def video(*children, **args): return tag_with_child("video", *children, **args)
def wbr(*children, **args): return tag_with_child("wbr", *children, **args)
