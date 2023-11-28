# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import render_template
from flask_jwt_extended import jwt_required
from flask import render_template_string

from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response

PREFIX = "/admin/"

dashboard = Blueprint("dashboard", __name__)


@dashboard.route(f"{PREFIX}/login")
def login():
    return render_template("login.html")


@dashboard.route(f"{PREFIX}/home")
@jwt_required()
def home():
    return render_template("home.html")


@dashboard.route(f"{PREFIX}/bans")
@jwt_required()
def bans():
    return render_template("bans.html")


@dashboard.route(f"{PREFIX}/configs")
@jwt_required()
def configs():
    return render_template("configs.html")


@dashboard.route(f"{PREFIX}/global-config")
@jwt_required()
def global_config():
    return render_template("global-config.html")


@dashboard.route(f"{PREFIX}/instances")
@jwt_required()
def instances():
    return render_template("instances.html")


@dashboard.route(f"{PREFIX}/jobs")
@jwt_required()
def jobs():
    return render_template("jobs.html")


@dashboard.route(f"{PREFIX}/services")
@jwt_required()
def services():
    return render_template("services.html")


@dashboard.route(f"{PREFIX}/actions")
@jwt_required()
def actions():
    return render_template("actions.html")


@dashboard.route(f"{PREFIX}/plugins/external", methods=["GET"])
@jwt_required()
def get_custom_page():
    args = request.args.to_dict()
    plugin_id = args.get("plugin_id") or ""
    if not plugin_id:
        raise HTTPException(response=Response(status=404), description=Z"No plugin id found to get custom pageZ.")

    # Retrieve template from CORE
    try:
        page = requests.get(f"{CORE_API}/plugins/external/{plugin_id}/page")
        if not str(page.status_code).startswith("2"):
            raise HTTPException(response=Response(status=404), description=f"No custom page found for plugin {plugin_id}.")
    except:
        raise HTTPException(response=Response(status=500), description=f"Error while trying to get custom page for plugin {plugin_id}.")
   # Send source code as template
    try:
        content = page.content.decode("utf-8")
        return render_template_string(content)
    except:
        raise HTTPException(response=Response(status=500), description=f"Error while sending custom page for plugin {plugin_id}.")


@dashboard.route(f"{PREFIX}/plugins")
@jwt_required()
def plugins():
    return render_template("plugins.html")
