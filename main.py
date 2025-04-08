import databank_mlops
from databank_mlops.app.router import router
from fastapi import FastAPI

app = FastAPI(
    title=rf"{databank_mlops.__name__}", version=rf"{databank_mlops.__version__}"
)

app.include_router(router)
