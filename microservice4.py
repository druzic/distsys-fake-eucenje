import aiofiles
from aiohttp  import web

routes = web.RouteTableDef()
allData = []

async def create_files():
    print(len(allData), "a")
    for x in allData:
        print(x["filename"])
        async with aiofiles.open(f'folder/{x["filename"]}', "w") as t:
            await t.write(x["content"])




@routes.post("/gatherData")
async def gatherData(request):
    try:
        data = await request.json()
        allData.extend(data)
        #print(len(allData))

        if len(allData) > 10:
            await create_files()

        return web.json_response({"status": "ok"}, status=200)
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)}, status=500)

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8084)