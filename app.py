from flask import Flask, render_template, request, redirect
from pathlib import Path
import os


app = Flask(__name__)


@app.route("/")
@app.route("/<lang>")
def index(lang="de"):
    """
    Renders the index page with section content based on the language parameter.

    Args:
        lang (str): Language code (default is 'de').

    Returns:
        str or tuple: Rendered HTML template with section contents or an error message with status code.
    """
    sections_root = "sections"
    supported_languages = [
        d for d in os.listdir(sections_root)
        if os.path.isdir(os.path.join(sections_root, d))
    ]

    if lang not in supported_languages:
        lang = "de"

    section_folder = os.path.join(sections_root, lang)

    if not os.path.exists(section_folder):
        return (
            "<h2 style='color:red; text-align:center;'>Content not available for language: {}</h2>".format(lang),
            404
        )

    sections = []
    for filename in sorted(os.listdir(section_folder)):
        with open(os.path.join(section_folder, filename), encoding="utf-8") as f:
            sections.append(f.read())

    return render_template("index.html", sections=sections)

from flask import request, redirect

@app.route("/edit/<lang>/<filename>", methods=["GET", "POST"])
def edit_section(lang, filename):
    section_path = Path(f"sections/{lang}/{filename}")
    
    if not section_path.exists():
        return f"❌ الملف غير موجود: {section_path}", 404

    if request.method == "POST":
        new_content = request.form["content"]
        section_path.write_text(new_content, encoding="utf-8")
        return redirect(f"/{lang}")

    content = section_path.read_text(encoding="utf-8")
    return render_template("editor.html", content=content, filename=filename, lang=lang)



if __name__ == "__main__":
    app.run(debug=True)
