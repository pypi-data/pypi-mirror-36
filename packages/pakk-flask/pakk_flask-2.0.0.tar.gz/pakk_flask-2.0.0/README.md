# pakk flask

Utilities for working with pakk files in a flask web application.

## Getting Started

Install pakk and pakk_flask:

```sh
$ python3 -m pip install pakk pakk_flask
```

Then you can use pakk_flask to send pakked assets as static files in a flask web application:

```py
from pakk_flask import send_from_directory

@APP.route("/static/<path:path>")
def get_static_file(path):
    with open("./files.pakk", "rb") as in_file:
        unpakked = unpakk(KEY, in_file)
        if unpakked.has_blob(path):
            return send_from_directory(unpakked, path)
        else:
            return send_from_directory("./static", path)
```

You can also use pakk_flask to render templates from pakk files:

```py
from pakk_flask import render_template, PakkTemplate

@APP.route("/home")
def get_home_page():
    with open("./files.pakk", "rb") as in_file:
        unpakked = unpakk(KEY, in_file)
        render_template(PakkTemplate(unpakked, "index.html"),
            some_value="Hello, ",
            another_value="World!")
```
