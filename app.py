from flask import request, Flask, Response, render_template, jsonify, redirect
from demo.qa import demo as demo2
from demo.face_segment import demo as demo3
from demo.outbreak import demo as demo4

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template("index.html",
        config2=demo2.iface.get_config_file(),
        config3=demo3.iface.get_config_file(),
        config4=demo4.iface.get_config_file())


@app.route('/getting_started')
def getting_started():
    return render_template("getting_started.html")


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
    if m_id == 2:
        output = demo2.iface.process(data)
    elif m_id == 3:
        output = demo3.iface.process(data)
    elif m_id == 4:
        output = demo4.iface.process(data)
    else:
        raise ValueError
    return jsonify({
        "data": output
    })


def run():
    app.run(port=5001)


if __name__ == "__main__":
    run()
