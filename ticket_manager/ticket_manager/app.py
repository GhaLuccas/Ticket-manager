
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ticket_manager.routers import auth, clients, tickets, users

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.users_router)
app.include_router(clients.clients_router)
app.include_router(auth.auth_router)
app.include_router(tickets.ticket_router)
