import contextlib
from datetime import datetime

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .settings import DEBUG
from .exceptions import exception_handlers
from .models import set_context, BUILDS


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    set_context()
    yield
    print('stop')


async def get_tasks(receive: Request):
    data = await receive.json()
    try:
        build = BUILDS[data['build']]
    except KeyError:
        return JSONResponse({'Status': 'Error',
                             'Result': 'Not found such build'})
    return JSONResponse({'Tasks': []})


routes = [Route('/get_tasks', get_tasks, methods=['POST'])]


build_app = Starlette(debug=DEBUG, routes=routes,
                      lifespan=lifespan, exception_handlers=exception_handlers)
