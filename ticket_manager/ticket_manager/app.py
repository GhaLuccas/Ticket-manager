
from fastapi import FastAPI

from ticket_manager.routers import (
    auth, 
    clients, 
    tickets, 
    users
    )

app = FastAPI()
app.include_router(users.users_router)
app.include_router(clients.clients_router)
app.include_router(auth.auth_router)
app.include_router(tickets.tickets.routers)
