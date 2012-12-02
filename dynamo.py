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
    if len(children) > 1:
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

    if isinstance(value, collections.iterable):
        string = 
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
    return special_tag("".join([COMMENT, START_CONDITION, condition,
        END_CONDITION]) + text + special_tag("".join([START_CONDITION, "endif",
        END_CONDITION, COMMENT]))

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

def a(text, *children, **args): return tag_with_child("a", *((text,) + children), **args)
def abbr(text, *children, **args): return tag_with_child("abbr", *((text,) + children), **args)
def acronym(text, *children, **args): return tag_with_child("acronym", *((text,) + children), **args)
def address(text, *children, **args): return tag_with_child("address", *((text,) + children), **args)
def applet(text, *children, **args): return tag_with_child("applet", *((text,) + children), **args)
def article(text, *children, **args): return tag_with_child("article", *((text,) + children), **args)
def aside(text, *children, **args): return tag_with_child("aside", *((text,) + children), **args)
def audio(text, *children, **args): return tag_with_child("audio", *((text,) + children), **args)
def b(text, *children, **args): return tag_with_child("b", *((text,) + children), **args)
def bdi(text, *children, **args): return tag_with_child("bdi", *((text,) + children), **args)
def bdo(text, *children, **args): return tag_with_child("bdo", *((text,) + children), **args)
def blockquote(text, *children, **args): return tag_with_child("blockquote", *((text,) + children), **args)
def body(text, *children, **args): return tag_with_child("body", *((text,) + children), **args)
def button(text, *children, **args): return tag_with_child("button", *((text,) + children), **args)
def canvas(text, *children, **args): return tag_with_child("canvas", *((text,) + children), **args)
def caption(text, *children, **args): return tag_with_child("caption", *((text,) + children), **args)
def cite(text, *children, **args): return tag_with_child("cite", *((text,) + children), **args)
def code(text, *children, **args): return tag_with_child("code", *((text,) + children), **args)
def colgroup(text, *children, **args): return tag_with_child("colgroup", *((text,) + children), **args)
def command(text, *children, **args): return tag_with_child("command", *((text,) + children), **args)
def datalist(text, *children, **args): return tag_with_child("datalist", *((text,) + children), **args)
def dd(text, *children, **args): return tag_with_child("dd", *((text,) + children), **args)
def Del(text, *children, **args): return tag_with_child("del", *((text,) + children), **args)
def details(text, *children, **args): return tag_with_child("details", *((text,) + children), **args)
def dfn(text, *children, **args): return tag_with_child("dfn", *((text,) + children), **args)
def div(text, *children, **args): return tag_with_child("div", *((text,) + children), **args)
def dl(text, *children, **args): return tag_with_child("dl", *((text,) + children), **args)
def dt(text, *children, **args): return tag_with_child("dt", *((text,) + children), **args)
def em(text, *children, **args): return tag_with_child("em", *((text,) + children), **args)
def embed(text, *children, **args): return tag_with_child("embed", *((text,) + children), **args)
def fieldset(text, *children, **args): return tag_with_child("fieldset", *((text,) + children), **args)
def figcaption(text, *children, **args): return tag_with_child("figcaption", *((text,) + children), **args)
def figure(text, *children, **args): return tag_with_child("figure", *((text,) + children), **args)
def footer(text, *children, **args): return tag_with_child("footer", *((text,) + children), **args)
def form(text, *children, **args): return tag_with_child("form", *((text,) + children), **args)
def h1(text, *children, **args): return tag_with_child("h1", *((text,) + children), **args)
def h2(text, *children, **args): return tag_with_child("h2", *((text,) + children), **args)
def h3(text, *children, **args): return tag_with_child("h3", *((text,) + children), **args)
def h4(text, *children, **args): return tag_with_child("h4", *((text,) + children), **args)
def h5(text, *children, **args): return tag_with_child("h5", *((text,) + children), **args)
def h6(text, *children, **args): return tag_with_child("h6", *((text,) + children), **args)
def head(text, *children, **args): return tag_with_child("head", *((text,) + children), **args)
def header(text, *children, **args): return tag_with_child("header", *((text,) + children), **args)
def hgroup(text, *children, **args): return tag_with_child("hgroup", *((text,) + children), **args)
def html(text, *children, **args): return tag_with_child("html", *((text,) + children), **args)
def i(text, *children, **args): return tag_with_child("i", *((text,) + children), **args)
def iframe(text, *children, **args): return tag_with_child("iframe", *((text,) + children), **args)
def ins(text, *children, **args): return tag_with_child("ins", *((text,) + children), **args)
def kbd(text, *children, **args): return tag_with_child("kbd", *((text,) + children), **args)
def keygen(text, *children, **args): return tag_with_child("keygen", *((text,) + children), **args)
def label(text, *children, **args): return tag_with_child("label", *((text,) + children), **args)
def legend(text, *children, **args): return tag_with_child("legend", *((text,) + children), **args)
def li(text, *children, **args): return tag_with_child("li", *((text,) + children), **args)
def Map(text, *children, **args): return tag_with_child("map", *((text,) + children), **args)
def mark(text, *children, **args): return tag_with_child("mark", *((text,) + children), **args)
def menu(text, *children, **args): return tag_with_child("menu", *((text,) + children), **args)
def meter(text, *children, **args): return tag_with_child("meter", *((text,) + children), **args)
def nav(text, *children, **args): return tag_with_child("nav", *((text,) + children), **args)
def noscript(text, *children, **args): return tag_with_child("noscript", *((text,) + children), **args)
def Object(text, *children, **args): return tag_with_child("object", *((text,) + children), **args)
def ol(text, *children, **args): return tag_with_child("ol", *((text,) + children), **args)
def optgroup(text, *children, **args): return tag_with_child("optgroup", *((text,) + children), **args)
def option(text, *children, **args): return tag_with_child("option", *((text,) + children), **args)
def output(text, *children, **args): return tag_with_child("output", *((text,) + children), **args)
def p(text, *children, **args): return tag_with_child("p", *((text,) + children), **args)
def pre(text, *children, **args): return tag_with_child("pre", *((text,) + children), **args)
def progress(text, *children, **args): return tag_with_child("progress", *((text,) + children), **args)
def q(text, *children, **args): return tag_with_child("q", *((text,) + children), **args)
def rp(text, *children, **args): return tag_with_child("rp", *((text,) + children), **args)
def rt(text, *children, **args): return tag_with_child("rt", *((text,) + children), **args)
def ruby(text, *children, **args): return tag_with_child("ruby", *((text,) + children), **args)
def s(text, *children, **args): return tag_with_child("s", *((text,) + children), **args)
def samp(text, *children, **args): return tag_with_child("samp", *((text,) + children), **args)
def script(text, *children, **args): return tag_with_child("script", *((text,) + children), **args)
def section(text, *children, **args): return tag_with_child("section", *((text,) + children), **args)
def select(text, *children, **args): return tag_with_child("select", *((text,) + children), **args)
def small(text, *children, **args): return tag_with_child("small", *((text,) + children), **args)
def source(text, *children, **args): return tag_with_child("source", *((text,) + children), **args)
def span(text, *children, **args): return tag_with_child("span", *((text,) + children), **args)
def strong(text, *children, **args): return tag_with_child("strong", *((text,) + children), **args)
def style(text, *children, **args): return tag_with_child("style", *((text,) + children), **args)
def sub(text, *children, **args): return tag_with_child("sub", *((text,) + children), **args)
def summary(text, *children, **args): return tag_with_child("summary", *((text,) + children), **args)
def sup(text, *children, **args): return tag_with_child("sup", *((text,) + children), **args)
def table(text, *children, **args): return tag_with_child("table", *((text,) + children), **args)
def tbody(text, *children, **args): return tag_with_child("tbody", *((text,) + children), **args)
def td(text, *children, **args): return tag_with_child("dt", *((text,) + children), **args)
def textarea(text, *children, **args): return tag_with_child("textarea", *((text,) + children), **args)
def tfoot(text, *children, **args): return tag_with_child("tfoot", *((text,) + children), **args)
def th(text, *children, **args): return tag_with_child("th", *((text,) + children), **args)
def thead(text, *children, **args): return tag_with_child("thead", *((text,) + children), **args)
def time(text, *children, **args): return tag_with_child("time", *((text,) + children), **args)
def title(text, *children, **args): return tag_with_child("title", *((text,) + children), **args)
def tr(text, *children, **args): return tag_with_child("tr", *((text,) + children), **args)
def track(text, *children, **args): return tag_with_child("track", *((text,) + children), **args)
def u(text, *children, **args): return tag_with_child("u", *((text,) + children), **args)
def ul(text, *children, **args): return tag_with_child("ul", *((text,) + children), **args)
def var(text, *children, **args): return tag_with_child("var", *((text,) + children), **args)
def video(text, *children, **args): return tag_with_child("video", *((text,) + children), **args)
def wbr(text, *children, **args): return tag_with_child("wbr", *((text,) + children), **args)
