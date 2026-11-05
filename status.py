from aiogram.fsm.state import StatesGroup,State
class AppointmentState(StatesGroup):
    
    name=State()
    phone=State()
    date=State()
    time=State()