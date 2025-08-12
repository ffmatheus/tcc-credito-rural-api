from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class TipoSafra(int, Enum):
    MILHO = 0
    SOJA = 1
    TRIGO = 2
    CAFE = 3
    ALGODAO = 4

class StatusSafra(int, Enum):
    PLANTADA = 0
    CRESCENDO = 1
    COLHIDA = 2
    ENTREGUE = 3

class SafraCreateRequest(BaseModel):
    tipo: TipoSafra = Field(..., description="Tipo da safra")
    quantidade: int = Field(..., gt=0, description="Quantidade em kg")
    valor_estimado: int = Field(..., gt=0, description="Valor estimado em centavos")
    localizacao: str = Field(..., min_length=5, description="Localização da fazenda")
    dias_para_colheita: int = Field(..., gt=0, le=365, description="Dias até a colheita")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tipo": 0,
                "quantidade": 1000,
                "valor_estimado": 50000,
                "localizacao": "Fazenda São José - Piracicaba/SP",
                "dias_para_colheita": 120
            }
        }

class SafraTransferRequest(BaseModel):
    token_id: int = Field(..., gt=0, description="ID do token da safra")
    novo_proprietario: str = Field(..., description="Endereço do novo proprietário")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token_id": 1,
                "novo_proprietario": "0x742..."
            }
        }

class SafraStatusUpdateRequest(BaseModel):
    token_id: int = Field(..., gt=0, description="ID do token da safra")
    novo_status: StatusSafra = Field(..., description="Novo status da safra")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token_id": 1,
                "novo_status": 1
            }
        }

class ContaResponse(BaseModel):
    address: str
    balance_wei: int
    balance_eth: float

class TransactionResponse(BaseModel):
    success: bool
    transaction_hash: str
    gas_used: int
    token_id: Optional[int] = None

class SafraResponse(BaseModel):
    token_id: int
    produtor: str
    tipo: int
    tipo_nome: str
    quantidade: int
    valor_estimado: int
    status: int
    status_nome: str
    localizacao: str
    data_plantio: str
    data_colheita_prevista: str
    proprietario_atual: str

class SafraResumoResponse(BaseModel):
    token_id: int
    produtor: str
    tipo: int
    tipo_nome: str
    quantidade: int
    valor_estimado: int
    status: int
    status_nome: str
    localizacao: str
    proprietario_atual: str

class SafraListResponse(BaseModel):
    safras: List[SafraResumoResponse]
    total: int

class EstatisticasResponse(BaseModel):
    total_safras_tokenizadas: int
    proximo_token_id: int
    blockchain_block: int

class APIStatusResponse(BaseModel):
    message: str
    blockchain_connected: bool
    latest_block: Optional[int]
    contract_loaded: bool