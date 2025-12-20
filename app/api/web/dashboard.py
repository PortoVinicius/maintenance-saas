import logging
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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

# Rota para atualizar status
@router.post("/update-status")
def update_status(order_id: int = Form(...), new_status: str = Form(...)):
    for order in fake_orders:
        if order["id"] == order_id:
            old_status = order["status"]
            order["status"] = new_status
            logger.info(f"Ordem {order_id} atualizada: {old_status} -> {new_status}")
            break
    return RedirectResponse(url="/", status_code=303)  # volta para o dashboard