import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.v1.router import api_router
from app.core.constants import BASE_ERRORS
from app.core.errors.base_error import AppError
from app.core.errors.generic_error import ConflictError
from app.core.settings import get_settings

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#   """Application lifespan events"""
#   # Startup
#   async with engine.begin() as conn:
#     await conn.run_sync(Base.metadata.create_all)
#   yield
#   # Shutdown

app = FastAPI(
  title='Runtime App',
  version='1.0.0',
  # lifespan=lifespan,
)


@app.exception_handler(AppError)
async def handle_app_error(request: Request, error: AppError):
  code = error.base_code
  message = BASE_ERRORS.get(error.base_code)
  if not get_settings().PRODUCTION:
    code = error.code
    message = error.message

  return JSONResponse(
    status_code=error.status_code,
    content={
      'base_code': error.base_code,
      'code': code,
      'message': message,
    },
  )


@app.exception_handler(IntegrityError)
async def handle_integrity_error(request: Request, error: IntegrityError):
  return await handle_app_error(request, ConflictError())


# Errores en consola
logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def handle_exception_error(request: Request, error: Exception):
  # Errores en consola
  logger.exception(
    'Unhandled exception: %s %s',
    request.method,
    request.url.path,
  )

  return await handle_app_error(request, AppError())


# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=get_settings().CORS_ORIGINS,
#   allow_credentials=True,
#   allow_methods=['*'],
#   allow_headers=['*'],
# )

app.include_router(api_router, prefix='/api/v1')

application = CORSMiddleware(
  app=app,
  allow_origins=get_settings().CORS_ORIGINS,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

if __name__ == '__main__':
  import uvicorn

  uvicorn.run(
    'app.main:application',
    host='0.0.0.0',
    reload=True,
    port=get_settings().BACKEND_DOCKER_PORT,
  )
