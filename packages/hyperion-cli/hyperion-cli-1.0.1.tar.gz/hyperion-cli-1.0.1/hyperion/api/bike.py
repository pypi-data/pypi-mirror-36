from typing import Optional

from aiohttp import web

from hyperion.models import CachingError
from hyperion.models.util import get_bikes, get_postcode_random
from .util import str_json_response


async def api_bikes(request):
    """
    Gets stolen bikes within a radius of a given postcode.
    :param request: The aiohttp request.
    :return: The bikes stolen with the given range from a postcode.
    """
    postcode: Optional[str] = request.match_info.get('postcode', None)

    try:
        radius = int(request.match_info.get('radius', 1))
    except ValueError:
        raise web.HTTPBadRequest(text="Invalid Radius")

    try:
        postcode = (await get_postcode_random()) if postcode == "random" else postcode
        bikes = await get_bikes(postcode, radius)
    except CachingError as e:
        raise web.HTTPInternalServerError(text=e.status)
    else:
        if bikes is None:
            raise web.HTTPNotFound(text="Post code does not exist.")
        else:
            return str_json_response([bike.serialize() for bike in bikes])
