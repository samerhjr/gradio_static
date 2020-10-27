import sys, os
import markdown2
from string import Template
import re

def generate(GRADIO_DIR, GRADIO_DEMO_DIR):
    with open(os.path.join(GRADIO_DIR, "readme_template.md")) as readme_file:
        readme = readme_file.read()
    codes = re.findall(r'\$code_([^\s]*)', readme)
    demos = re.findall(r'\$demo_([^\s]*)', readme)
    readme = re.sub(r'\!\[(.*)\]\(demo.*\/([^\/\.]+\.[^)]+)\)', r'![\1](static/home/img/\2)', readme)
    readme = readme.replace("```python\n", "<pre><code class='lang-python'>").replace("```bash\n", "<pre><code class='lang-bash'>").replace("```", "</code></pre>")
    template_dict = {}
    for code_src in codes:
        with open(os.path.join(GRADIO_DEMO_DIR, code_src + ".py")) as code_file:
            python_code = code_file.read().replace('if __name__ == "__main__":\n    iface.launch()', "iface.launch()")
            template_dict["code_" + code_src] = "<pre><code class='lang-python'>" + python_code + "</code></pre>"
    for i, demo_src in enumerate(demos):
        template_dict["demo_" + demo_src] = "<div id='interface_" + str(i) + "'></div>"
    readme_template = Template(readme)
    readme = readme_template.substitute(template_dict)
    readme_lines = readme.split("\n")
    getting_started_index = [i for i, line in enumerate(readme_lines) if line.startswith("## Getting Started")][0]
    start_index = [i for i, line in enumerate(readme_lines) if line.startswith("### ") and i > getting_started_index][0]
    end_index = [i for i, line in enumerate(readme_lines) if line.startswith("## ") and i > getting_started_index][0]
    getting_started_lines = readme_lines[start_index: end_index]
    getting_started_markdown = "\n".join(getting_started_lines)
    getting_started_html = markdown2.markdown(getting_started_markdown)
    return getting_started_html