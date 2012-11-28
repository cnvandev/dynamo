Dynamo
======

Dynamo is a dead-simple Python HTML generator. I couldn't find a Python module
to generate HTML in the quick, functional style that I wanted, so I just wrote
my own. There are probably infinitely-better ways to generate HTML underneath
the functions provided, and I welcome all suggestions to improve the library.
Extra-special props will be given to suggestions that simplify or speed up the
generation.

Dynamo will only generate HTML5 elements. Don't bring that `<frameset>` shit in
here, son, cause we'll knock you out the box.

As of now, Dynamo doesn't do much validation on your end...as in it pretty much
doesn't do any. It won't check your style or make things pretty for you, all it
really does is limits the tags you can generate to the tags available. I'd be
interested in doing some validation in the background, but I'm trying to use
this for something so I'll see what I can do at a later time. I take no
responsibility for your terrible HTML or if you try to lay everything out using
tables like it's 1998.

To use, just import `dynamo.py` at the top of your file (`from dynamo import *`)
and then start creating tags by wrapping your text in functions representing the
tags you want. It goes like so:

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
            p("Check it out, this is a page! It's pretty rad, I'm pretty proud of it, to be honest. I hope you like it!", Class="thing"),
            p("There's not much here, I'm just learning, but here's hoping more will come."),
            p(""),
            comment("Important remarks go towards the end."),
            p("Chris Vandevelde is super-hot.")
        )
    )

This will print out:

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
            <!--Version one of my page, thanks for checking out the source.-->
            <h1 state="Jolly">This Is My Page</h1>
            <p Class="thing">Check it out, this is a page! It's pretty rad, I'm pretty proud of it, to be honest. I hope you like it!</p>
            <p>There's not much here, I'm just learning, but here's hoping more will come.</p>
            <p></p>
            <!--Important remarks go towards the end.-->
            <p>Chris Vandevelde is super-hot.</p>
        </body>
    </html>

There are a few caveats from doing it this way, I'd love to be able to work
around them but I haven't yet figured out a method to do so:

1. If you use the sweet Python named-arguments, they **must** go last - it's a
caveat of how Python does it.
2. You gotta give all the non-closed tag functions something. If you want an
empty `<p></p>`, toss in an empty string like `p("")`. Throw it a bone, y'know?

## Reserved Words and Non-Pythonic Words ##

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

    print ul(
        {
            "class": "dropdown_menu",
            "role": "menu",
            "aria-labelledBy": "dropdownMenu",
        },
        (whatever items you want in here)
    )

which will output

    <ul aria-labelledBy="dropdownMenu" role="menu" class="dropdown-menu">
        (whatever items you want in here)
    </ul>

and there you go. Look at that shit, it's beautiful. Just remember to pass the
dictionary last and unpack it with the `**` and you're golden, pony boy.

You can also construct and unpack the dict of keyword parameters yourself, and
pass that to the end of a funciton like so:

    print ul(
        (whatever items you want in here),
        **{
            "class": "dropdown_menu",
            "role": "menu",
            "aria-labelledBy": "dropdownMenu",
        }
    )

but that's a little messier.

## Formatting ##

Dynamo will format HTML for you based the style I was most familiar with when I
was writing the library. All self-contained tags go on their own new line, as
do tags with one or no children - they can be pretty much inlined.

The syntax style is inspired by (and owes a lot of credit to) the absolute
classic Perl module CGI.pm (https://github.com/markstos/CGI.pm), which uses an
awesome functional style
(see http://cpansearch.perl.org/src/LDS/CGI.pm-3.43/cgi_docs.html for examples.)

(Fun fact: This was initially coded (almost) in its entirety to Dr. Octagon's
*Dr. Octagonecologyst*. Maybe that explains some things.)