import aiohttp
from aiohttp  import web

routes = web.RouteTableDef()


@routes.post("/WT1")
async def WT1(request):
    try:
        print("RADIM LI")
        async with aiohttp.ClientSession() as session:
            data = await request.json()
            print(len(data["data"]))

            filtered_data = [row for row in data["data"] if row["username"].startswith("w")]
            print(len(filtered_data))

            await session.post("http://127.0.0.1:8084/gatherData", json=filtered_data)

        return web.json_response({"status": "ok",}, status=200,)

    except Exception as e:
        return web.json_response({"status": "failed WT1", "message": str(e)}, status=500)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8082)