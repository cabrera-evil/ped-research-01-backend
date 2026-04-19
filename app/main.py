from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1 import router
from app.core.config import get_settings
from app.utils.logger import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    logger.info(
        "application_starting",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )

    # Preload sample products to demonstrate hash table behaviour on first load.
    # Deliberate collisions:
    #   P001 and P010 both hash to cell 5  (ASCII sum = 225, 225 % 10 = 5)
    #   P002 and P020 both hash to cell 6  (ASCII sum = 226, 226 % 10 = 6)
    from app.modules.inventory.schemas import ProductCreate
    from app.modules.inventory.service import add_product

    seed_products = [
        ProductCreate(
            code="P001", name="Laptop Stand", price=39.99, quantity=15, category="Electronics"
        ),
        ProductCreate(
            code="P010", name="USB Hub", price=24.99, quantity=30, category="Electronics"
        ),
        ProductCreate(code="P002", name="Stapler", price=8.50, quantity=100, category="Office"),
        ProductCreate(
            code="P020", name="Tape Dispenser", price=5.99, quantity=80, category="Office"
        ),
        ProductCreate(
            code="P003", name="Monitor", price=299.00, quantity=8, category="Electronics"
        ),
        ProductCreate(
            code="P004", name="Keyboard", price=79.00, quantity=20, category="Electronics"
        ),
        ProductCreate(
            code="P005", name="Floor Cleaner", price=12.00, quantity=50, category="Cleaning"
        ),
        ProductCreate(code="P006", name="Desk Lamp", price=45.00, quantity=12, category="Office"),
    ]
    for product in seed_products:
        add_product(product)

    logger.info("inventory_seeded", count=len(seed_products))
    yield
    logger.info("application_shutting_down")


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Generic Python API template built with FastAPI",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.warning("validation_error", errors=exc.errors(), path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_exception", error=str(exc), path=request.url.path, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)},
    )


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router, prefix=settings.api_prefix)


@app.get("/", tags=["Root"], include_in_schema=False)
async def root() -> FileResponse:
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        workers=settings.workers,
    )
