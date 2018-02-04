from aiohttp import web
import aiohttp_jinja2
import asyncpg
import json
from aiohttp_session import get_session


class AuthView(web.View):
    async def get(self):
        session = await get_session(self.request)
        print(session)
        # if session['new'] == True:
        #     print('NEW', session.new)

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

    async def post(self):
        try:
            user = await self.request.post()
            name = user['login']
            print(user)
            print(name)
            info = {'status': 'success', 'message': "OK"}
            conn = await asyncpg.connect(user='postgres', password='12345678', database='test1', host='localhost',
                                         port=5432)
            print('Connect OK')
            values = await conn.insert('''INSERT INTO test_table (id, name, price) VALUES (1, $1, 500)''', name)
            print(values)
            await conn.close()
            print('Connect close')
            return web.Response(text=json.dumps(info), status=200)

        except Exception as e:
            info = {'status': 'failed', 'message': str(e)}
            return web.Response(text=json.dumps(info), status=500)
