from aiohttp import web
import aiohttp_jinja2
import jinja2
import asyncpg
import json
from aiohttp_session import get_session, setup, cookie_storage
import aiohttp_session
import time

from app import auth


async def pg():
    conn = await asyncpg.connect(user='postgres', password='12345678',
                                 database='test1', host='localhost:5432', port=5432)
    print('Connect OK')


async def test_get(request):
    try:
        info = {'status': 'success'}
        name = request.query['name']
        print(name)
        conn = await asyncpg.connect(user='postgres', password='12345678', database='test1', host='localhost',
                                     port=5432)
        print('Connect OK')
        values = await conn.fetch('''SELECT * FROM test_table WHERE name = $1 ;''', name)
        print(values)
        await conn.close()
        print('Connect close')
        return web.Response(text=json.dumps(info), status=200)
    except Exception as e:
        info = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(info), status=500)


app = web.Application(middlewares=[aiohttp_session.session_middleware(aiohttp_session.SimpleCookieStorage())])
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('C:/Users/Алексей/PycharmProjects/testhttp/'))
# loader=jinja2.FileSystemLoader('C:/Users/MaksyaginAV/PycharmProjects/testhttp'))

app.router.add_get('/', test_get)
app.router.add_get('/auth/', auth.AuthView, name='auth:get')
app.router.add_post('/auth/', auth.AuthView, name='auth:post')

web.run_app(app)
