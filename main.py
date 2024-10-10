from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from database import models
from database.database import engine
from fastapi.middleware.cors import CORSMiddleware

from middleware.log import APIGatewayMiddleware
from routers import user
app = FastAPI()

router_list = [
    user.router
]
for router in router_list:
    app.include_router(router=router)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], #  allows requests from any origin 
    allow_credentials=True,
    allow_methods=['*'], # allows all HTTP methods
    allow_headers=['*'], # allows all headers
)

app.add_middleware(APIGatewayMiddleware)

models.Base.metadata.create_all(engine)