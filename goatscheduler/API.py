from flask import Flask, current_app, jsonify
from flask_cors import CORS, cross_origin
import threading
import os
import json  



class BackendAPI:

    def __init__(
        self,
        scheduler_backend
    ):
        app = Flask(__name__, static_folder='frontend')
        cors = CORS(app)
        app.debug = False

        @app.route('/component_list')
        @cross_origin()
        def component_list():
            return json.dumps(scheduler_backend.get_components())

        @app.route('/dependencies_list')
        @cross_origin()
        def dependency_list():
            return json.dumps(scheduler_backend.get_dependencies())

        threading.Thread(target=app.run, kwargs={'port': 5011}).start()