from flask import request, Flask, Response, render_template, jsonify, redirect
import sys

from demo.qa import demo as qa
from demo.face_segment import demo as face_segment
from demo.outbreak import demo as outbreak
from demo.double import demo as double
from demo.hello_world import demo as hello_world
from demo.hello_world_2 import demo as hello_world_2
from demo.hello_world_3 import demo as hello_world_3
from demo.sepia import demo as sepia

app = Flask(__name__)


@app.route('/')
def home_page():
    demos = [qa, face_segment, outbreak]
    return render_template("index.html", configs=[
        demo.iface.get_config_file() for demo in demos
    ])


@app.route('/getting_started')
def getting_started():
    demos = [
        double,
        hello_world, 
        hello_world_2, 
        hello_world_3,
        sepia,
    ]
    return render_template("getting_started.html", configs=[
        demo.iface.get_config_file() for demo in demos
    ])


@app.route('/docs')
def docs():
    return render_template("docs.html")


@app.route('/ml_examples')
def ml_examples():
    return render_template("ml_examples.html")


@app.route('/sharing')
def sharing():
    return render_template("getting_started.html")


@app.route('/hub')
def hub():
    return redirect("http://hub.gradio.app", code=302)


@app.route('/model/<m_id>', methods=["POST"])
def model_api(m_id):
    m_id = int(m_id)
    data = request.get_json(force=True)["data"]
    demos = [
        qa, 
        face_segment, 
        outbreak, 
        double,
        hello_world, 
        hello_world_2, 
        hello_world_3, 
        sepia, 
    ]
    output = demos[m_id].iface.process(data)
    return jsonify({
        "data": output[0]
    })


def run(debug=False):
    app.run(debug=debug, port=5001)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(debug=True)
    else:
        run(debug=False)
