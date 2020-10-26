from flask import request, Flask, Response, render_template, jsonify, abort
import sys
import requests
import os
import sys
import generate_docs
import importlib

if len(sys.argv) == 2 and sys.argv[1] == "q":
    print("- quick mode -")
    all_demo_names = ["hello_world", "hello_world", "hello_world"]
else:
    all_demo_names = ["qa", "face_segment", "outbreak"]
all_demo_names += ["hello_world", "hello_world_2", "hello_world_3", "sepia", "calculator", "hello_interpretation", "hello_interpretation_2"]

all_demos, all_code = [], []
for demo_name in all_demo_names:
    all_demos.append(importlib.import_module("demo." + demo_name + ".demo"))
    with open(os.path.join("demo", demo_name, "demo.py")) as demo_code:
        all_code.append(demo_code.read())

app = Flask(__name__)

HUB_URL = "https://gradiohub.com"

@app.route('/')
def home_page():
    demos = all_demos[:3]
    return render_template("index.html", configs=[
        demo.iface.get_config_file() for demo in demos
    ])


@app.route('/getting_started')
def getting_started():
    demos, code = all_demos[3:], all_code[3:]
    return render_template("getting_started.html", configs=[
        demo.iface.get_config_file() for demo in demos
    ], code=code)

docs_data = generate_docs.generate()

@app.route('/docs')
def docs():
    return render_template("docs.html", docs=docs_data)


@app.route('/ml_examples')
def ml_examples():
    return render_template("ml_examples.html")


@app.route('/sharing')
def sharing():
    return render_template("getting_started.html")

hub_data = requests.get(HUB_URL + "/data").json()

@app.route('/hub')
def hub():
    hub_data = requests.get(HUB_URL + "/data").json()
    return render_template("hub.html", hosted_models=hub_data)


@app.route('/hub/<repo>')
def hub_host(repo):
    for model in hub_data:
        if model[3].endswith(repo):
            model_url = model[4]
            break
    else:
        abort(404)

    return render_template("hub_host.html", model_url=model_url, model_config=model[5])


# REMOVE LATER WITH DEMO_HOST.HTML
@app.route('/demo/<repo>')
def demo_host(repo):
    for model in hub_data:
        if model[3].endswith(repo):
            model_url = model[4]
            break
    else:
        abort(404)

    return render_template("demo_host.html", model_url=model_url, model_config=model[5])


@app.route('/model/<m_id>/<action>/', methods=["POST"])
def model_api(m_id, action):
    m_id = int(m_id)
    data = request.get_json(force=True)["data"]
    iface = all_demos[m_id].iface
    if action == "predict":
        output = iface.process(data)
        return jsonify({
            "data": output[0]
        })
    elif action == "interpret":
        output = iface.interpret(data)
        return jsonify(output)


@app.route('/analytics')
def analytics():
    """
    Returns Gradio analytics
    """

    sudoPassword = ''
    command = 'lsof -PiTCP -sTCP:LISTEN'
    open_ports = os.popen('echo %s|sudo -S %s' % (sudoPassword, command)).read()
    num_live_interfaces = 0
    x = open_ports.split("(LISTEN)")

    for i in x:
        if 'paramiko' in i:
            num_live_interfaces = num_live_interfaces + 1

    num_live_interfaces = num_live_interfaces/2
    return render_template("analytics.html",
                           num_live_interfaces=num_live_interfaces)
    # scheduler = BlockingScheduler()
    # scheduler.add_job(get_num_live_interfaces, 'interval', seconds=5)
    # scheduler.start()


def run(debug=False):
    app.run(debug=debug, port=5001)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(debug=True)
    else:
        run(debug=False)
