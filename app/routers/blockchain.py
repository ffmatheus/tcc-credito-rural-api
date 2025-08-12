from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.schemas import ContaResponse, EstatisticasResponse, APIStatusResponse
from app.services.blockchain import blockchain_service
from app.utils.auth import verify_token, get_auth_header_example
from app.core.config import settings

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])

@router.get("/auth/token")
async def obter_token_demonstracao():
    """
    Obtém o token de acesso para demonstração
    
    **⚠️ Em produção, isso seria feito via login ou outra forma de autenticação.**
    """
    return {
        "token": settings.API_TOKEN,
        "tipo": "Bearer",
        "exemplo_uso": get_auth_header_example(),
        "instrucoes": "Use este token no header Authorization: Bearer <token>"
    }

@router.get("/status", response_model=APIStatusResponse)
async def status_api():
    """
    Verifica o status da API e conexão com blockchain
    """
    try:
        return APIStatusResponse(
            message="API Crédito Rural funcionando",
            blockchain_connected=blockchain_service.is_connected(),
            latest_block=blockchain_service.get_latest_block(),
            contract_loaded=blockchain_service.contract is not None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contas", response_model=List[ContaResponse])
async def listar_contas(token: str = Depends(verify_token)):
    """
    Lista todas as contas disponíveis no Ganache com seus saldos
    """
    try:
        accounts = blockchain_service.get_accounts()
        return [ContaResponse(**account) for account in accounts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/estatisticas", response_model=EstatisticasResponse)
async def obter_estatisticas(token: str = Depends(verify_token)):
    """
    Obtém estatísticas gerais do sistema de tokenização
    """
    try:
        stats = blockchain_service.obter_estatisticas()
        return EstatisticasResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))