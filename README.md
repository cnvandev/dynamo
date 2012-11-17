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

To use, just import `dynamo.py` at the top of your file (`import dynamo`) and
then start creating tags by wrapping your text in functions representing the
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
            p("Check it out, this is a page! It's pretty rad, I'm pretty proud of it, to be honest. I hope you like it!", classish="thing"),
            p("There's not much here, I'm just learning, but here's hoping more will come."),
            p("&nbsp;"),
            comment("Important remarks go towards the end."),
            p("Chris Vandevelde is super-hot.")
        )
    )

This will print out:

    <html><head><title>My Page, Yo</title>
    <link media="all" href="markup.css" type="text/css" rel="stylesheet" /><meta content="This is my page, yo." name="description" /><meta content="this, is, my, page, awesome, cool" name="keywords" /><meta charset="UTF-8" /></head>
    <body><!--Version one of my page, thanks for checking out the source.-->
    <h1 state="Jolly">This Is My Page</h1>
    <p classish="thing">Check it out, this is a page! It's pretty rad, I'm pretty proud of it, to be honest. I hope you like it!</p>
    <p>There's not much here, I'm just learning, but here's hoping more will come.</p>
    <p>&nbsp;</p>
    <!--Important remarks go towards the end.-->
    <p>Chris Vandevelde is super-hot.</p>
    </body>
    </html>

There are a few caveats from doing it this way, I'd love to be able to work
around them but I haven't yet figured out a method to do so:
    1. The only thing here which I would consider not-immediately-obvious is
       that your named parameters **must** go last - it's a caveat of the **kwargs
       stuff in Python.
    2. You gotta give all the non-closed tag functions something. If you want an
       empty `<p></p>`, toss in an empty string like `p("")`. Throw it a bone,
       y'know?

Formatting is also iffy.

The syntax style is inspired by (and owes a lot of credit to) the absolute
classic Perl module CGI.pm (https://github.com/markstos/CGI.pm), which uses an
awesome functional style
(see http://cpansearch.perl.org/src/LDS/CGI.pm-3.43/cgi_docs.html for examples.)

(Fun fact: This was initially coded (almost) in its entirety to Dr. Octagon's
"Dr. Octagonecologyst." Maybe that explains some things.)