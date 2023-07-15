import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.common.consts import SETTINGS
from app.database.conn import db
from app.middleware.token_validator import TokenValidMiddleware
from app.routes import auth, check


def create_app():
    app = FastAPI(
            title="Nota",
            description="nota project",
            docs_url=f"/{SETTINGS.RANDOM_STRING}/swagger",
            redoc_url=f"/{SETTINGS.RANDOM_STRING}/redoc",
            debug=True
        )

    # init database
    db.init_app(app, SETTINGS)

    # set middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SETTINGS.ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TokenValidMiddleware)

    # set routes
    app.include_router(check.router, tags=["Check"], prefix="/v1")
    app.include_router(auth.router, tags=["Authentication"], prefix="/v1")

    # set because of 307 response
    app.routes.redirect_slashes = False

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
