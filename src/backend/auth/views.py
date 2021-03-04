from aiohttp import web
from aiohttp_security import check_authorized, forget, remember
from passlib.handlers.sha2_crypt import sha256_crypt

from backend.auth.models import User


class SignupView(web.View):
    async def post(self):
        form = await self.request.post()
        login = form.get('login')
        password = form.get('password')
        user = User(login=login, password=sha256_crypt.hash(password))
        await user.save(self.request.app.async_session)
        return web.HTTPFound('/')


class LoginView(web.View):
    async def post(self):
        response = web.HTTPFound('/')
        form = await self.request.post()
        login = form.get('login')
        password = form.get('password')
        if await User.check_credentials(self.request.app.async_session, login,
                                        password):
            await remember(self.request, response, login)
            raise response

        raise web.HTTPUnauthorized(
            body=b'Invalid username/password combination')


class LogoutView(web.View):
    async def get(self):
        await check_authorized(self.request)
        response = web.Response(body=b'You have been logged out')
        await forget(self.request, response)
        return response