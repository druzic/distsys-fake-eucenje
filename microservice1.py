import asyncio
import aiosqlite
import aiofiles
import json
import aiohttp
from aiohttp  import web

routes = web.RouteTableDef()


@routes.get("/M1")
async def M1(request):
    try:
        async with aiohttp.ClientSession() as session:
            podaci = []

            task = await session.get("http://127.0.0.1:8080/M0")
            data = await task.json()

            podaci.append(asyncio.create_task(session.post("http://127.0.0.1:8082/WT1", json=data)))
            podaci.append(asyncio.create_task(session.post("http://127.0.0.1:8083/WT2", json=data)))
            print("podaci")
            x = asyncio.gather(*podaci)
            await x
            return web.json_response({"status": "ok",}, status=200,)


    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)}, status=500)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)