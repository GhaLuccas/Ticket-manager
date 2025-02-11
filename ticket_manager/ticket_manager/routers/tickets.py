from fastapi import APIRouter , Depends
from ticket_manager.database import session_db
from ticket_manager.schema import TicketSchema
from ticket_manager.security import login_required
from ticket_manager.models import Ticket

tickets_routers = APIRouter(prefix='/ticket', tags=['ticket'])


@tickets_routers.post('/')
def create_ticket(
    db : session_db , 
    ticket : TicketSchema,
    user = Depends(login_required) ,
    ):
    
    new_ticket = Ticket(
        
    )