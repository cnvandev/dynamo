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
import __builtin__

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

CLOSED_TAGS = ["base", "br", "col", "hr", "img", "input", "link", "meta",
               "param"]
OPEN_TAGS = ["a", "abbr", "acronym", "address", "applet", "article", "aside",
             "audio", "b", "bdi", "bdo", "blockquote", "body", "button",
             "canvas", "caption", "cite", "code", "colgroup", "command",
             "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt", "em",
             "embed", "fieldset", "figcaption", "figure", "footer", "form",
             "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup",
             "html", "i", "iframe", "ins", "kbd", "keygen", "label", "legend",
             "li", "map", "mark", "menu", "meter", "nav", "noscript", "object",
             "ol", "optgroup", "option", "output", "p", "pre", "progress", "q",
             "rp", "rt", "ruby", "s", "samp", "script", "section", "select",
             "small", "source", "span", "strong", "style", "sub", "summary",
             "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead",
             "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr"]


def tag_with_child(tag, *children, **args):
    ''' Return a string representation of an XML tag that can contain a child
    element. All children after the first child must be strings.

    '''

    open_padding = ""
    close_padding = ""
    if len(children) > 1 and children[0]:
        # If our first child is a dictionary, we're being given the arguments
        # first. Set args to this dict.
        if isinstance(children[0], dict):
            children = list(children)

            # If we have both named arguments and first-child arguments, merge
            # the two.
            first_child_args = children.pop(0)
            if args:
                args = merge_dicts(args, first_child_args)

        # If we have more than one child, pad the children by one tab and drop
        # the child list by one newline.
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
    presented like key="value". If the value is iterable, will return all values
    given, joined by spaces.

    '''

    if isinstance(value, collections.Iterable) and not isinstance(value,
        basestring):
        string = format_list_attribute(value)
    else:
        string = value

    return "%s=\"%s\"" % (key, string)


def format_list_attribute(list_attribute):
    ''' Returns a "list" value suitable for HTML (for now it's
    space-delimited strings).

    '''

    return " ".join(list_attribute)


def merge_dicts(hash1, hash2):
    ''' Merges two dicts together. If one dict contains items in the other dict,
    the resulting value will be a list containing all values from both dicts.

    '''

    for (key, value) in hash1.iteritems():
        if key in hash2:
            # If either values aren't lists, make them so!
            value = ensure_list(value)
            hash2[key] = ensure_list(hash2[key])

            # Join the two lists in holy matrimony.
            hash2[key].extend(value)
        else:
            hash2[key] = value

    return hash2


def ensure_list(potential_list):
    ''' Not sure if the given value is a list-like object? Pass it through this
    and you will be sure.

    '''

    if isinstance(potential_list, collections.Iterable) and \
       not isinstance(potential_list, basestring):
        return potential_list
    else:
        return [potential_list]


def add_leaf_tag_function(tag):
    ''' Adds a function to generate a specific self-closing/"leaf" tag (like 
        <img src="blah" />, with the slash) to the current module.

    '''

    docstring = "Returns a self-closing <%s /> tag with" % tag + \
                           " provided children and attributes."
    add_tag_function(tag, docstring, closed_tag)


def add_parent_tag_function(tag):
    ''' Adds a function to generate a specific XML tag (like <a href="blah">
        link</a>) to the current module.

    '''

    docstring = "Returns a <%s> tag with provided children" % tag + \
                           " and attributes."
    add_tag_function(tag, docstring, tag_with_child)


def add_tag_function(tag, docstring, inner_function, ):
    # Make sure we don't run into any namespace conflicts!
    if tag in dir(__builtin__):
        tag = tag.capitalize()

    current_module = __import__(__name__)
    def tag_function(*children, **args):
        return inner_function(tag, *children, **args)

    tag_function.__doc__ = docstring
    tag_function.__name__ = "%s" % tag
    setattr(current_module, tag_function.__name__, tag_function)    


# Functions for "special" tags.
def comment(text):
    return special_tag(" ".join([COMMENT, text, COMMENT]))

def doctype(text):
    return special_tag(" ".join(["DOCTYPE", text]))

def conditional_comment(condition, text):
    return special_tag(COMMENT + START_CONDITION + condition + END_CONDITION) \
           + text + special_tag(START_CONDITION + "endif" + END_CONDITION +
           COMMENT)


# Generate the functions for us to use! Oooohh, DRY code.
for tag in CLOSED_TAGS:
    add_leaf_tag_function(tag)

for tag in OPEN_TAGS:
    add_parent_tag_function(tag)