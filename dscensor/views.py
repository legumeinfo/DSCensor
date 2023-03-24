import logging

from aiohttp import web

#from petstore.data import NewPet
#from petstore.shortcuts import get_pet_or_404
from rororo import openapi_context, OperationTableDef
from rororo.openapi import get_validated_data, get_validated_parameters


logger = logging.getLogger(__name__)

# ``OperationTableDef`` is analogue of ``web.RouteTableDef`` but for OpenAPI
# operation handlers
operations = OperationTableDef()


@operations.register("getGenus")
async def list_genus(request: web.Request) -> web.Response:
    with openapi_context(request) as context:
        return web.json_response([request.app["genus"]])


@operations.register("getSpecies")
async def list_genus(request: web.Request) -> web.Response:
    with openapi_context(request) as context:
        return web.json_response([request.app["species"]])
