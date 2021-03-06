from flask import Flask, render_template, json, jsonify, request, url_for, redirect
import jinja2
import datetime
import sys
import os
from conf import *
import cf_deployment_tracker

app = Flask(__name__)

# Emit Bluemix deployment event
cf_deployment_tracker.track()
# CloudFoundry env
if os.getenv("VCAP_APP_PORT"):
    port = int(os.getenv("VCAP_APP_PORT"))
else:
    port = 8080

@app.route('/')
def main():
    return render_template("portal_home.html")

@app.route('/system_metrics', methods=['GET'])
def get_system_metrics():
    args = request.args
    if valid_config_params( args ):
        return apply_template('templates/system_metrics.html', args)
    # TODO: throw custom error page
    else:
        return render_template("portal_home.html")

@app.route('/benchmarks', methods=['GET'] )
def get_benchmark_page():
    args = request.args
    if valid_config_params( args ):
        return apply_template('templates/benchmark.html', args)
    # TODO: throw custom error page
    else:
        return render_template("portal_home.html")

# Helper method for applying jinja templates
def apply_template(template_path, args):
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    template = template_env.get_template(template_path)
    t_vars = {}
    t_vars['server'] = str( args['server'] )
    t_vars['netdata_port'] = str( args['netdata_port'] )
    t_vars['dellve_port'] = str( args['dellve_port'] )
    return template.render(t_vars)

# TODO:
# Verify that user provided server configuration has
# a proper dellve installation and dependecies
def valid_config_params(params):
    if params['server'] == '10.157.26.8' and params['netdata_port'] == '5555':
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
