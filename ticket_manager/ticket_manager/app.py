
from fastapi import FastAPI

from ticket_manager.routers import auth, clients, tickets, users

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.include_router(users.users_router)
app.include_router(clients.clients_router)
app.include_router(auth.auth_router)
app.include_router(tickets.ticket_router)
