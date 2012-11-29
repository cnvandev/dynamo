from dynamo import *

print doctype("html")
print html(
    head(
        title("My Page, Yo"),
        link(href="markup.css", rel="stylesheet", type="text/css", media="all"),
        meta(name="description", content="This is my page, yo."),
        meta(name="keywords", content="this, is, my, page, awesome, cool"),
        meta({"charset":"UTF-8"})
    ),
    body(
        comment("Version one of my page, thanks for checking out the source."),
        h1({"state": "jolly", "stuff": "awesome", "no-really": "this is fucking rad"}, "This Is My Page"),
        p({"class": "thing"}, "Check it out, this is a page! It's pretty rad, I'm pretty proud of it, to be honest. I hope you like it!"),
        p("There's not much here, I'm just learning, but here's hoping more will come."),
        p(),
        comment("Important remarks go towards the end."),
        p("Chris Vandevelde is super-hot.")
    )
)