import pdfkit
import sys
import os
from jinja2 import Environment, BaseLoader

# 🧠 تحديد اللغة
lang = sys.argv[1] if len(sys.argv) > 1 else "de"
section_folder = os.path.join("sections", lang)

if not os.path.exists(section_folder):
    print(f"❌ اللغة غير مدعومة أو المجلد غير موجود: {lang}")
    sys.exit(1)

# ✅ تحميل الأقسام
sections = []
for filename in sorted(os.listdir(section_folder)):
    with open(os.path.join(section_folder, filename), encoding="utf-8") as f:
        sections.append(f.read())

# 🧠 تحميل قالب index.html
with open("templates/index.html", encoding="utf-8") as f:
    index_template_content = f.read()

# 🔧 محاكاة url_for
def fake_url_for(endpoint, **values):
    if endpoint == 'static':
        return f"static/{values.get('filename', '')}"
    return ""

# 🧠 تهيئة Jinja
env = Environment(loader=BaseLoader())
env.globals['url_for'] = fake_url_for
template = env.from_string(index_template_content)
rendered_html = template.render(sections=sections)

# 📄 حفظ HTML مؤقت في مجلد المشروع
temp_html_path = f"cv_{lang}.html"
with open(temp_html_path, "w", encoding="utf-8") as f:
    f.write(rendered_html)

# 📤 توليد PDF
output_dir = "pdf"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"Tamer_Hamad_Faour_CV_{lang.upper()}.pdf")

path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

options = {
    'enable-local-file-access': None,
    'page-size': 'A4',
    'margin-top': '10mm',
    'margin-right': '10mm',
    'margin-bottom': '10mm',
    'margin-left': '10mm',
    'encoding': "UTF-8"
}

try:
    pdfkit.from_file(temp_html_path, output_path, configuration=config, options=options)
    print(f"✅ تم حفظ PDF بنجاح في: {output_path}")
except Exception as e:
    print(f"❌ فشل توليد PDF: {e}")
finally:
    os.remove(temp_html_path)
