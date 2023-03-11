import os
import logging

from flask import Flask, make_response, redirect, render_template, request, send_file

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "secret_l801#+#a&^1mz)_p&qyq51j51@20_74c-xi%&i)b*u_dt^2=2key"
)

# Add input validation for the scale and width parameters in get_template_fields function
def get_template_fields(progress):
    title = request.args.get("title")

    scale = 100
    try:
        scale = int(request.args.get("scale"))
        if scale <= 0:
            scale = 100  # Set a default value if scale is invalid
    except (TypeError, ValueError):
        pass

    progress_width = 60 if title else 90
    try:
        progress_width = int(request.args.get("width"))
        if progress_width <= 0:
            progress_width = 60  # Set a default value if progress_width is invalid
    except (TypeError, ValueError):
        pass

    return {
        "title": title,
        "title_width": 10 + 6 * len(title) if title else 0,
        "title_color": request.args.get("color", "428bca"),
        "scale": scale,
        "progress": progress,
        "progress_width": progress_width,
        "progress_color": get_progress_color(progress, scale),
        "suffix": request.args.get("suffix", "%"),
    }

# Add logging statements
logging.basicConfig(level=logging.INFO)

# Move the get_template_fields function to a separate module and import it
from template_fields import get_template_fields

@app.route("/<int:progress>/")
def get_progress_svg(progress):
    template_fields = get_template_fields(progress)

    template = render_template("progress.svg", **template_fields)

    response = make_response(template)
    response.headers["Content-Type"] = "image/svg+xml"

    logging.info("SVG generated with parameters: %s", template_fields)

    return send_file(response, mimetype="image/svg+xml")

@app.route("/")
def redirect_to_github():
    return redirect("https://github.com/fredericojordan/progress-bar", code=302)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
