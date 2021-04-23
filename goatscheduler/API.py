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

        @app.route('/relationships')
        @cross_origin()
        def relationships():
            return json.dumps(scheduler_backend.get_relationships())

        @app.route('/task_data/<task_name>')
        @cross_origin()
        def get_task_data(task_name):
            return json.dumps(scheduler_backend.get_task_log(task_name))


        print('\n\n\n\nbout to start on port 5011\n\n\n\n\n\n')
        threading.Thread(target=app.run, kwargs={'port': 5011}).start()