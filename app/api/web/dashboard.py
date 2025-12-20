import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Criando logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Lista de ordens fake
fake_orders = [
    {"id": 1, "descricao": "Troca de óleo", "status": "pendente"},
    {"id": 2, "descricao": "Revisão elétrica", "status": "em andamento"},
    {"id": 3, "descricao": "Limpeza de filtros", "status": "concluída"},
]

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    logger.info("Dashboard acessado")  # <-- aqui
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "app_name": "Maintenance SaaS",
            "orders": fake_orders
        }
    )
