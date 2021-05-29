import json

from aiohttp import web
from aiohttp_security import check_authorized, forget, remember
from passlib.handlers.sha2_crypt import sha256_crypt

from backend.auth.models import User


class SignupView(web.View):
    async def post(self):
        """
        ---
        summary: Signup form.
        description: New user registration.
        requestBody:
            required: true
            content:
                application/x-www-form-urlencoded:
                    schema:
                        type: object
                        properties:
                            login:
                                type: string
                            password:
                                type: string
                            confirmed_password:
                                type: string
                        required:
                            - login
                            - password
                            - confirmed_password
        responses:
            '200':
                description: OK
        """
        form = await self.request.post()
        login = form.get("login")
        password = form.get("password")
        confirmed_password = form.get("confirmed_password")
        if password != confirmed_password:
            raise web.HTTPBadRequest(text="Passwords don't match")
        user = User(login=login, password=sha256_crypt.hash(password))
        await user.save(self.request.app.async_session)
        return web.HTTPFound("/")


class LoginView(web.View):
    async def post(self):
        """
        ---
        summary: Login form.
        description: Current user login.
        requestBody:
            required: true
            content:
                application/x-www-form-urlencoded:
                    schema:
                        type: object
                        properties:
                            login:
                                type: string
                            password:
                                type: string
                        required:
                            - login
                            - password
        responses:
            '200':
                description: OK
        """
        response = web.HTTPFound("/")
        form = await self.request.post()
        login = form.get("login")
        password = form.get("password")
        if await User.check_credentials(self.request.app.async_session, login,
                                        password):
            await remember(self.request, response, login)
            return response

        raise web.HTTPUnauthorized(
            text="Invalid username/password combination")


class LogoutView(web.View):
    async def get(self):
        """
        ---
        summary: Logout.
        description: Current user logout.
        responses:
            '200':
                description: OK
        """
        await check_authorized(self.request)
        response = web.Response(body="You have been logged out")
        await forget(self.request, response)
        return response
