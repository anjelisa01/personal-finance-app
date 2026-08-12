from fastapi import FastAPI
from core.handler import register_handlers

#logger
from core.logger import logger

from contextlib import asynccontextmanager

from core.database import Base
from core.database import engine

from api.v1.router import api_router

Base.metadata.create_all(bind=engine) #Models → DB (DB is generated from models)

# @asynccontextmanager
# async def lifespan(app:FastAPI):
#     logger.info("Aplication started")
#     yield
#     logger.info("Application stopped")
# app=FastAPI(lifespan=lifespan)

app=FastAPI()
register_handlers(app)

app.include_router(api_router, prefix="/api/v1")