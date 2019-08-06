from flask import Flask
import rq_dashboard

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")


@app.route("/")
def hello():
    return "Databird monitor: not much here yet."


def run_server(host="0.0.0.0", port=9180):
    print("Web monitor listens at http://{}:{}/rq".format(host, port))
    app.run(host=host, port=port)
