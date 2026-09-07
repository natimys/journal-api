import logging
from typing import Literal

import exceptions
from httpx import AsyncClient, HTTPStatusError, Response
from resources.user_info import UserInfoResource

logger = logging.getLogger(__name__)


class JournalAPI:
    def __init__(self, username: str, password: str):
        self._client = AsyncClient(
            base_url="https://msapi.top-academy.ru/api/v2/",
        )
        self._username = username
        self._password = password
        self.__access_token = None

        # resources
        self.info = UserInfoResource(client=self)

    async def _send(
        self,
        method: Literal["GET", "POST", "DELETE", "OPTION", "PUT"],
        url: str,
        data: dict | None = None,
        **kwargs,
    ) -> Response:
        response = await self._client.request(
            method=method, url=url, data=data, **kwargs
        )
        response.raise_for_status()
        return response

    async def _login(self) -> None:
        response = await self._send(
            method="POST",
            url="auth/login",
            data={
                "application_key": "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
                "username": self._username,
                "password": self._password,
            },
        )
        response.raise_for_status()
        self.__access_token = response.json()["access_token"]
        self._client.headers = {
            "Authorization": self.__access_token,
        }
        logger.info(f"Logged in as {self._username} successfully")

    async def request(
        self, method, url: str, data: dict | None = None, **kwargs
    ) -> Response | None:
        if self.__access_token is None:
            try:
                await self._login()

            except HTTPStatusError as e:
                if e.response.status_code == 401:
                    logger.exception(f"401 Unauthorized\n{e.request.url}")
                    raise exceptions.UnauthorizedException() from e

        try:
            response = await self._send(method=method, url=url, data=data, **kwargs)
            return response
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.exception(
                    f"401 Unauthorized\n{e.request.url}\n{e.request.headers}"
                )
                raise exceptions.UnauthorizedException() from e

            elif e.response.status_code == 403:
                logger.exception(f"403 Forbidden\n{e.request.url}\n{e.request.headers}")
                raise exceptions.ForbiddenException() from e

            elif e.response.status_code == 404:
                logger.exception(f"404 Not Found\n{e.request.url}")
                raise exceptions.NotFoundException() from e

    async def get(self, url):
        return await self.request(method="GET", url=url)

    async def post(self, url, data):
        return await self._send(method="POST", url=url, data=data)
