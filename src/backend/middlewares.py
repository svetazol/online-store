import logging

from aiohttp import web

logger = logging.getLogger(__name__)

@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except web.HTTPException as ex:
        return web.json_response(
            {"status": "error", "reason": ex.reason}, status=ex.status
        )
    except Exception as ex:
        logger.exception(ex)
        return web.json_response(
            {"status": "failed", "reason": str(ex)}, status=500
        )

    return response
