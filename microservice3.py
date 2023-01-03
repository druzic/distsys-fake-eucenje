import aiohttp
from aiohttp  import web

routes = web.RouteTableDef()


@routes.post("/WT2")
async def WT2(request):
    try:
        print("RADIM LI WT2")
        async with aiohttp.ClientSession() as session:
            data = await request.json()
            print(len(data["data"]))

            filtered_data = [
            row for row in data["data"] if row["username"].startswith("d")]
            print(len(filtered_data))
            x = await session.post("http://127.0.0.1:8084/gatherData", json=filtered_data)
            print(x)
        return web.json_response({"status": "ok",}, status=200,)


    except Exception as e:
        return web.json_response({"status": "failed WT2", "message": str(e)}, status=500)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8083)