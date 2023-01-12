FROM python:3.9.2

RUN pip install asyncio aiosqlite aiofiles aiohttp

COPY microservice0.py ./
COPY baza.db ./
COPY fakedataset.json ./

CMD ["python", "./microservice0.py"]