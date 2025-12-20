import logging
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Função para conectar ao banco
def get_db_connection():
    conn = psycopg2.connect(
        host="maintenance_db",  # nome do serviço no docker-compose
        database="maintenance",
        user="postgres",
        password="postgres"     # ajuste se tiver outra senha
    )
    return conn

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    logger.info("Dashboard acessado")
    
    # Buscar ordens no banco
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM maintenance_orders ORDER BY id;")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "app_name": "Maintenance SaaS",
            "orders": orders
        }
    )

@router.post("/update-status")
def update_status(order_id: int = Form(...), new_status: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE maintenance_orders SET status=%s WHERE id=%s",
        (new_status, order_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    logger.info(f"Ordem {order_id} atualizada para {new_status}")
    return RedirectResponse(url="/", status_code=303)
