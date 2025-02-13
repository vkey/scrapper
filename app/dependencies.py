import asyncio
import contextlib
import os
from typing import TypedDict

from fastapi import FastAPI
from camoufox.async_api import AsyncCamoufox as Browser

from settings import USER_SCRIPTS_DIR, BROWSER_CONTEXT_LIMIT


class State(TypedDict):
    # https://playwright.dev/python/docs/api/class-browsertype
    browser: Browser
    semaphore: asyncio.Semaphore


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    os.makedirs(USER_SCRIPTS_DIR, exist_ok=True)
    semaphore = asyncio.Semaphore(BROWSER_CONTEXT_LIMIT)
    async with Browser(
        humanize=True,
        geoip=True,
        headless="virtual"
    ) as browser:
        yield State(browser=browser, semaphore=semaphore)
