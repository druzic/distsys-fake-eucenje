import asyncio
import aiosqlite
import aiofiles
import json
from aiohttp  import web

routes = web.RouteTableDef()

async def insertData():
    print("jedan")
    async with aiofiles.open('fakedataset.json', mode='r') as f:
        print("dva")
        i = 0
        async for x in f:
            async with aiosqlite.connect("baza.db") as db:

                await db.execute("INSERT INTO tablica (username,ghlink,filename,content) VALUES (?,?,?,?)",(json.loads(x)["repo_name"].split("/")[0],
                    "https://github.com/" + json.loads(x)["repo_name"], json.loads(x)["path"].split("/")[-1], json.loads(x)["content"],),)
                await db.commit()
                i+=1
                print(i)
            if i == 1000:
                print("Baza popunjena")
                return

async def checkData():
    async with aiosqlite.connect("baza.db") as db:
            async with db.execute("SELECT COUNT(*) FROM tablica") as cur:
                var = await cur.fetchall()
                print(var)

                if var[0][0] == 0:
                    print("Prazna baza. Popunjavam bazu...")
                    await insertData()
                else:
                    print("Baza nije prazna. Brišem podatke iz baze...")

                    await db.execute("DELETE FROM tablica")
                    await db.commit()
                    print("Baza izbrisana. Popunjavam bazu...")
                    await insertData()
                    return


@routes.get("/M0")
async def M0(request):
    try:
        response = {
            "service_id":0,
            "data":[]
        }

        async with aiosqlite.connect("baza.db") as db:
            async with db.execute("SELECT * FROM tablica ORDER BY RANDOM() LIMIT 100") as cur:
                async for row in cur:
                    response["data"].append({'username': row[1], 'githubLink': row[2], 'filename': row[3], 'content': row[4]})
                await db.commit()

        return web.json_response(response)

    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)}, status=500)

asyncio.run(checkData())
app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8080)