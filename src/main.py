import logging
import contextlib

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .settings import DEBUG
from .exceptions import exception_handlers
from .models import set_context

BUILDS = {}

logging.basicConfig(format="%(levelname)s:%(name)s - %(message)s")
logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    global BUILDS
    BUILDS = set_context()
    yield


async def get_tasks(receive: Request):
    data = await receive.json()
    try:
        build = BUILDS[data['build']]
    except KeyError:
        return JSONResponse({'Status': 'Error',
                             'Result': 'Not found such build'})
    except TypeError:
        return JSONResponse({'Status': 'Error',
                             'Result': 'Something is wrong with data'})
    return JSONResponse({'Tasks': build.get_ordered_tasks()})


routes = [Route('/get_tasks', get_tasks, methods=['POST'])]


build_app = Starlette(debug=DEBUG, routes=routes,
                      lifespan=lifespan, exception_handlers=exception_handlers)
