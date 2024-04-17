from ninja import NinjaAPI
from .views import router as user_router

app = NinjaAPI()

app.add_router('/users/',user_router)