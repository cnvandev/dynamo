#!/usr/bin/python

'''
Dynamo
======

Dynamo is a super-quick code generator written by Chris Vandevelde
(chris.vandevelde@uwaterloo.ca). You can quickly write code in a sweet,
functional style that makes everything pretty straightforward. Dump it
to a file or write it to a request stream and you're all good!

More information can be found in the README.md file, a usage sample can be
found in sample.py, or take a look at the code to see how it works. If you're
still having problems, let me know and I'll help out if I can.

The project page is at http://github.com/cnvandev/dynamo, feel free to
contribute or make requests!

'''

import __builtin__
import collections
import json
import copy


# Parse language definition files.
def load_definition(language):
    language_dict = json.load(open("languages/" + language + ".json"))
    language = collections.namedtuple('Language', language_dict.keys())(*language_dict.values())
    return language


def block_with_child(block, *children, **args):
    ''' Return a string representation of a code block that can contain a child
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
        if children[0].startswith(language.start_block):
            children = map(lambda child: child.replace(language.newline, language.newline + language.indent),
                           children)
            open_padding = language.newline + language.indent
            close_padding = language.newline

    return open_block_with_args(block, **args) + open_padding + (language.newline + language.indent).join(
        children) + close_padding + close_block(block)


def open_block_with_args(block, **args):
    ''' Given 'string' and a dict of args, returns <string arg1="blah">
    (etc. for more args, you get the idea)

    '''

    return language.start_block + block + format_args(**args) + language.end_block


def close_block(block, **args):
    ''' Given 'string', returns </string> '''

    return open_block_with_args(language.closer + block)


def closed_block(block, *children, **args):
    ''' Returns a self-contained XML block that cannot contain a child
    element. Think <img src="image.jpg" />.

    '''

    # Allow the possibility of a single dict child argument.
    if len(children) > 0:
        if len(children) > 1 or not isinstance(children[0], dict):
            raise AssertionError("Your self-contained <%s /> block contains a \
                non-hash child - you are doing it wrong." % block)

        # If our first child is a dictionary, we're being given the arguments
        # first. Set args to this dict.
        children = list(children)
        args = children.pop(0)

    return open_block_with_args(block + format_args(**args) + language.delimeter + language.closer)


def format_args(**args):
    ''' Returns a string of XML block arguments from an unpacked dict. '''

    if not args:
        return ""

    return language.delimeter + language.delimeter.join([format_arg_value(key, value) for key, value in
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

    return language.arg_format % (key, string)


def format_list_attribute(list_attribute):
    ''' Returns a "list" value suitable for HTML (for now it's
    space-delimited strings).

    '''

    return language.delimeter.join(list_attribute)


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


def add_leaf_block_function(block):
    ''' Adds a function to generate a specific self-closing/"leaf" block (like 
        <img src="blah" />, with the slash) to the current module.

    '''

    docstring = "Returns a self-closing <%s /> block with" % block + \
                           " provided children and attributes."
    add_block_function(block, docstring, closed_block)


def add_parent_block_function(block):
    ''' Adds a function to generate a specific XML block (like <a href="blah">
        link</a>) to the current module.

    '''

    docstring = "Returns a <%s> block with provided children" % block + \
                           " and attributes."
    add_block_function(block, docstring, block_with_child)


def add_block_function(block, docstring, inner_function, ):
    # Make sure we don't run into any namespace conflicts!
    if block in dir(__builtin__):
        block = block.capitalize()

    current_module = __import__(__name__)
    def block_function(*children, **args):
        return inner_function(block, *children, **args)

    block_function.__doc__ = docstring
    block_function.__name__ = str("%s" % block)
    setattr(current_module, block_function.__name__, block_function)


# Functions for "special" blocks, defined in the JSON.
def add_special_function(name, definition_items):
    def special_function(*children, **args):
        # Copy the function definition so we can modify it here.
        function_definition = copy.copy(definition_items)
        
        # Do some mangling of the arguments list. If it's null, we sub in an
        # argument from the arguments list (content, other special stuff for the
        # function definition), if it's the name of a language prop, sub that
        # in.
        argument_index = 1 # The first child is the function name, so skip it.
        for index, item in enumerate(function_definition):
            if item is None:
                function_definition[index] = language.delimeter + children[argument_index]

                # If we're not the last tag in the list, add another delimeter.
                if (argument_index +2 != len(function_definition)):
                    function_definition[index] += language.delimeter

                argument_index += 1
            elif hasattr(language, item):
                function_definition[index] = getattr(language, item)

        tag_content = "".join(function_definition)
        return open_block_with_args(tag_content + "".join(children[argument_index:]), **args)

    add_block_function(name, "", special_function)


language = load_definition("html")


# Generate the functions for us to use! Oooohh, DRY code.
for block in language.closed_blocks:
    add_leaf_block_function(block)

for block in language.open_blocks:
    add_parent_block_function(block)
    
for (special_function, definition_items) in language.special_functions.iteritems():
    add_special_function(special_function, definition_items)