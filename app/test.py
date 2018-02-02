from aiohttp import web
import aiohttp_jinja2
import jinja2
import asyncpg
import json
from aiohttp_session import get_session, setup, cookie_storage
import aiohttp_session
import time

async def pg():
    conn = await asyncpg.connect(user='postgres', password='12345678',
                                database='test1', host='localhost:5432', port=5432)
    print('Connect OK')

async def test_get(request):
    try:
        info = {'status': 'success'}
        name = request.query['name']
        print(name)
        conn = await asyncpg.connect(user='postgres', password='12345678', database='test1', host='localhost', port=5432)
        print('Connect OK')
        values = await conn.fetch('''SELECT * FROM test_table WHERE name = $1 ;''', name)
        print(values)
        await conn.close()
        print('Connect close')
        return web.Response(text=json.dumps(info), status=200)
    except Exception as e:
        info = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(info), status=500)

async def test_post(request):
    try:
        user = await request.post()
        name = user['login']
        print(user)
        print(name)
        info = {'status': 'success', 'message': "OK"}
        conn = await asyncpg.connect(user='postgres', password='12345678', database='test1', host='localhost',
                                     port=5432)
        print('Connect OK')
        values = await conn.fetch('''INSERT INTO test_table (id, name, price) VALUES (1, $1, 500)''', name)
        print(values)
        await conn.close()
        print('Connect close')
        return web.Response(text=json.dumps(info), status=200)

    except Exception as e:
        info = {'status': 'failed', 'message': str(e)}
        return web.Response(text=json.dumps(info), status=500)

class Button(web.View):
    async def Button(web.View):
        session = get_session()

        print(session)

        try:
            print(self.request.rel_url)
            print(self.request.match_info)
            context = {'name': 'Alex', 'surname': 'Svetlov'}
            response = aiohttp_jinja2.render_template('template/index.html',
                                                      self.request,
                                                      context)
            response.headers['Content-Language'] = 'ru'
            return response
        except Exception as e:
          info = {'status': 'failed', 'message': str(e)}
          return web.Response(text=json.dumps(info), status=500)


app = web.Application()
aiohttp_jinja2.setup(app,
                     # loader=jinja2.FileSystemLoader('C:/Users/Алексей/PycharmProjects/Guardian/'))
                     loader=jinja2.FileSystemLoader('C:/Users/MaksyaginAV/PycharmProjects/testhttp'))
app.router.add_get('/', test_get)
app.router.add_post('/send/', test_post)
app.router.add_get('/auth/', Button)
web.run_app(app)
