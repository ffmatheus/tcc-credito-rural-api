from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional

from app.models.schemas import (
    SafraCreateRequest, SafraTransferRequest, SafraStatusUpdateRequest,
    TransactionResponse, SafraResponse, SafraListResponse
)
from app.services.blockchain import blockchain_service
from app.utils.auth import verify_token

router = APIRouter(prefix="/safras", tags=["Safras"])

@router.post("/tokenizar", response_model=TransactionResponse)
async def tokenizar_safra(
    safra: SafraCreateRequest,
    conta_produtor: Optional[str] = Query(None, description="Endereço da conta do produtor (se não informado, usa a primeira conta)"),
    token: str = Depends(verify_token)
):
    """
    Tokeniza uma nova safra no blockchain
    
    - **tipo**: 0=Milho, 1=Soja, 2=Trigo, 3=Café, 4=Algodão
    - **quantidade**: Quantidade em kg
    - **valor_estimado**: Valor estimado em centavos (ex: 50000 = R$ 500,00)
    - **localizacao**: Localização da fazenda
    - **dias_para_colheita**: Número de dias até a colheita prevista
    - **conta_produtor**: Endereço da conta que será proprietária (opcional)
    
    ⚠️ **Importante**: Anote qual conta usou para poder transferir depois!
    """
    try:
        resultado = blockchain_service.tokenizar_safra(safra, conta_produtor)
        return TransactionResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{token_id}", response_model=SafraResponse)
async def obter_safra(token_id: int, token: str = Depends(verify_token)):
    """
    Obtém dados detalhados de uma safra específica
    """
    try:
        safra_data = blockchain_service.obter_safra(token_id)
        return SafraResponse(**safra_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transferir", response_model=TransactionResponse)
async def transferir_propriedade(
    transfer: SafraTransferRequest,
    conta_atual: Optional[str] = Query(None, description="Endereço da conta atual proprietária (OBRIGATÓRIO se não for a primeira conta)"),
    token: str = Depends(verify_token)
):
    """
    Transfere a propriedade de uma safra para outro endereço
    
    ⚠️ **IMPORTANTE**: 
    - Apenas o proprietário atual pode transferir
    - Use GET /safras/{token_id} para ver quem é o proprietário atual
    - Se não informar conta_atual, usará a primeira conta (accounts[0])
    
    **Fluxo típico:**
    1. Produtor cria safra (torna-se proprietário)
    2. Produtor transfere para investidor como garantia
    3. Após pagamento, investidor transfere de volta
    """
    try:
        resultado = blockchain_service.transferir_propriedade(transfer, conta_atual)
        return TransactionResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/atualizar-status", response_model=TransactionResponse)
async def atualizar_status(
    status_update: SafraStatusUpdateRequest,
    conta_produtor: Optional[str] = Query(None, description="Endereço da conta do produtor"),
    token: str = Depends(verify_token)
):
    """
    Atualiza o status de uma safra
    
    - **novo_status**: 0=Plantada, 1=Crescendo, 2=Colhida, 3=Entregue
    
    Apenas o produtor original pode atualizar o status
    """
    try:
        resultado = blockchain_service.atualizar_status_safra(status_update, conta_produtor)
        return TransactionResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=SafraListResponse)
async def listar_todas_safras(token: str = Depends(verify_token)):
    """
    Lista todas as safras tokenizadas no sistema
    """
    try:
        resultado = blockchain_service.listar_todas_safras()
        return SafraListResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))