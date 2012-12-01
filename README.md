Dynamo
======

Dynamo is a dead-simple Python HTML generator. I couldn't find a Python module
to generate HTML in the quick, functional style that I wanted, so I just wrote
my own. There are probably infinitely-better ways to generate HTML underneath
the functions provided, and I welcome all suggestions to improve the library.
Extra-special props will be given to suggestions that simplify or speed up the
generation.

Validation
----------
Dynamo will only generate HTML5 elements. Don't bring that `<frameset>` shit in
here, son, cause we'll knock you out the box.

As of now, Dynamo doesn't do much validation on your end...as in it pretty much
doesn't do any. It won't check your style or make things pretty for you, all it
really does is limits the tags you can generate to the tags available. I'd be
interested in doing some validation in the background, but I'm trying to use
this for something so I'll see what I can do at a later time. I take no
responsibility for your terrible HTML or if you try to lay everything out using
tables like it's 1998.

Usage
-----
To use, just import `dynamo.py` at the top of your file (`from dynamo import *`)
and then start creating tags by wrapping your text in functions representing the
tags you want. It goes like so:

```python
    print doctype("html")
    print html(
        head(
            title("My Page, Yo"),
            link(href="markup.css", rel="stylesheet", type="text/css", media="all"),
            meta(name="description", content="This is my page, yo."),
            meta(name="keywords", content="this, is, my, page, awesome, cool"),
            meta(charset="UTF-8")
        ),
        body(
            comment("Version one of my page, thanks for checking out the source."),
            h1("This Is My Page", state="Jolly"),
            p({"class": "thing"}, "Check it out, this is a page! It's pretty rad, I'm pretty proud of it, to be honest. I hope you like it!"),
            p("There's not much here, I'm just learning, but here's hoping more will come."),
            p(),
            comment("Important remarks go towards the end."),
            p("Chris Vandevelde is super-hot.")
        )
    )
```

This will print out:

```html
    <!DOCTYPE html>
    <html>
        <head>
            <title>My Page, Yo</title>
            <link media="all" href="markup.css" type="text/css" rel="stylesheet" />
            <meta content="This is my page, yo." name="description" />
            <meta content="this, is, my, page, awesome, cool" name="keywords" />
            <meta charset="UTF-8" />
        </head>
        <body>
            <!-- Version one of my page, thanks for checking out the source. -->
            <h1 state="Jolly">This Is My Page</h1>
            <p class="thing">Check it out, this is a page! It's pretty rad, I'm pretty proud of it, to be honest. I hope you like it!</p>
            <p>There's not much here, I'm just learning, but here's hoping more will come.</p>
            <p></p>
            <!-- Important remarks go towards the end. -->
            <p>Chris Vandevelde is super-hot.</p>
        </body>
    </html>
```

Validation
----------
Dynamo will only generate HTML5 elements. Don't bring that `<frameset>` shit in
here, son, cause we'll knock you out the box.

As of now, Dynamo doesn't do much validation on your end...as in it pretty much
doesn't do any. It won't check your style or make things pretty for you, all it
really does is limits the tags you can generate to the tags available. I'd be
interested in doing some validation in the background, but I'm trying to use
this for something so I'll see what I can do at a later time. I take no
responsibility for your terrible HTML or if you try to lay everything out using
tables like it's 1998.

Formatting & Style
------------------
Dynamo will format HTML for you based the style I was most familiar with when I
was writing the library. All self-contained tags go on their own new line, as
do tags with one or no children - they can be pretty much inlined. An example of
the style can be seen above.

Tabs are done with `\t`s, which is probably a bad idea, I don't know. If you
want to change it to spaces (and any number of spaces! 4, or 2, or whatever man,
just don't shoot me! Put the gun down, man, it's customizable!), just download
the source and modify the `TAB` constant. The source is super-tiny, so it's just
in one place.

The syntax style is inspired by (and owes a lot of credit to) the absolute
classic Perl module CGI.pm (https://github.com/markstos/CGI.pm), which uses an
awesome functional style
(see http://cpansearch.perl.org/src/LDS/CGI.pm-3.43/cgi_docs.html for examples.)

Reserved Words and Non-Pythonic Words
-------------------------------------
Some HTML tags are reserved keywords or functions in Python - it's a bummer.
They are `del`, `input`, `map`, and `object`; in addition, `class` is a reserved
keyword and can't be used in tag attributes. You'll be needing it all over the
place if you want to generate any HTML of consequence, so to get around that
limitation, use a capital letter at the start of the word and everthing will be
A-OK. This method works for functions and attributes, although attributes are
freeform so I don't do any lowercasing there.

If you want more flexibility over what words you can use for tag attributes, the
easiest way is to pass a dict as the first child; Dynamo will automatically
use that as tag attributes for you. For example, Twitter Bootstrap wants hyphens
in attributes, which Python won't let you do, and needs to use classes all over
the place. To get around that, you can do:

```python
    print ul(
        {
            "class": "dropdown_menu",
            "role": "menu",
            "aria-labelledBy": "dropdownMenu",
        },
        (whatever items you want in here)
    )
```

which will output

```html
    <ul aria-labelledBy="dropdownMenu" role="menu" class="dropdown-menu">
        (whatever items you want in here)
    </ul>
```

and there you go. Look at that shit, it's beautiful.

You can also construct and unpack the dict of keyword parameters yourself, and
pass that to the end of a funciton like so:

```python
    print ul(
        (whatever items you want in here),
        **{
            "class": "dropdown_menu",
            "role": "menu",
            "aria-labelledBy": "dropdownMenu",
        }
    )
```

but that's a little messier. Regardless, just remember to pass the
dictionary last and unpack it with the `**` and you're golden, pony boy.

Caveats
-------
The only caveat I've run across is that if you use the sweet Python named
arguments, they **must** go last - it's a caveat of how Python does named
arguments with unpacked dicts and whatnot.

(Fun fact: This was initially coded (almost) in its entirety to Dr. Octagon's
*Dr. Octagonecologyst*. Maybe that explains some things.)