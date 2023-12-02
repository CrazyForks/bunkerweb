# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required

from middleware.validator import model_validator

from utils import get_core_format_res, get_req_data
import json
from os import environ
from ui import UiConfig

UI_CONFIG = UiConfig("ui", **environ)

CORE_API = UI_CONFIG.CORE_ADDR
PREFIX = "/api/config"

config = Blueprint("config", __name__)


@config.route(f"{PREFIX}", methods=["GET"])
@jwt_required()
@model_validator(queries={"method": "Method", "new_format": "NewFormat"})
def get_config():
    """Get complete config"""
    args, data, methods, new_format = [get_req_data(request, ["methods", "new_format"])[k] for k in ("args", "data", "methods", "new_format")]
    return get_core_format_res(f"{CORE_API}/config?methods={methods if methods else 'ui'}&new_format={new_format if new_format else 'true'}", "GET", "", "Retrieve config")


@config.route(f"{PREFIX}", methods=["PUT"])
@jwt_required()
@model_validator(body="Config", queries={"method": "Method"})
def update_config():
    """Update whole config"""
    args, data, method = [get_req_data(request, ["method"])[k] for k in ("args", "data", "method")]
    return get_core_format_res(f"{CORE_API}/config?method={method if method else 'ui'}", "PUT", config, "Update config")


@config.route(f"{PREFIX}/global", methods=["PUT"])
@jwt_required()
@model_validator(body="Config", queries={"method": "Method"})
def update_global_config():
    """Update global config"""
    args, data, method = [get_req_data(request, ["method"])[k] for k in ("args", "data", "method")]
    return get_core_format_res(f"{CORE_API}/config/global?method={method if method else 'ui'}", "PUT", data, "Update global config")


@config.route(f"{PREFIX}/service/<string:service_name>", methods=["PUT"])
@jwt_required()
@model_validator(body="Config", queries={"method": "Method"}, params={"service_name": "ServiceName"})
def update_service_config(service_name):
    """Create or update service config"""
    args, data, method = [get_req_data(request, ["method"])[k] for k in ("args", "data", "method")]
    return get_core_format_res(f"{CORE_API}/config/service/{service_name}?method={method if method else 'ui'}", "PUT", data, f"Create / update service config {service_name}")


@config.route(f"{PREFIX}/service/<string:service_name>", methods=["DELETE"])
@jwt_required()
@model_validator(queries={"method": "Method"}, params={"service_name": "ServiceName"})
def delete_service_config(service_name):
    """Delete service config"""
    args, data, method = [get_req_data(request, ["method"])[k] for k in ("args", "data", "method")]
    return get_core_format_res(f"{CORE_API}/config/service/{service_name}?method={method if method else 'ui'}", "DELETE", "", f"Delete service config {service_name}")