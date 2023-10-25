from typing import Annotated, Dict
from fastapi import Body, APIRouter
from utils import get_core_format_res
from models import ResponseModel
import json
import os
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("CORE_ADDR")

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get(
    "",
    response_model=ResponseModel,
    summary="Get complete config",
)
async def get_config(methods: bool = False, new_format: bool = False):
    return get_core_format_res(f"{API}/config?methods={methods}&new_format={new_format}", "GET", "", "Retrieve config")


@router.put(
    "",
    response_model=ResponseModel,
    summary="Update whole config",
)
async def update_config(config: Dict[str, str], method: str):
    return get_core_format_res(f"{API}/config?method={method}", "PUT", config, "Update config")


@router.put(
    "/global",
    response_model=ResponseModel,
    summary="Update global config",
)
async def update_global_config(config: Annotated[dict, Body()], method: str):
    data = json.dumps(config, skipkeys=True, allow_nan=True, indent=6)
    return get_core_format_res(f"{API}/config/global?method={method}", "PUT", data, "Update global config")


@router.put(
    "/service/{service_name}",
    response_model=ResponseModel,
    summary="Update service config",
)
async def update_service_config(config: Annotated[dict, Body()], method: str, service_name: str):
    data = json.dumps(config, skipkeys=True, allow_nan=True, indent=6)
    return get_core_format_res(f"{API}/config/service/{service_name}?method={method}", "PUT", data, f"Update service config {service_name}")


@router.delete(
    "/service/{service_name}",
    response_model=ResponseModel,
    summary="Delete service config",
)
async def delete_service_config(method: str, service_name: str):
    return get_core_format_res(f"{API}/config/service/{service_name}?method={method}", "DELETE", "", f"Delete service config {service_name}")