import os
from typing import Optional

class Settings:
    APP_NAME: str = "API Crédito Rural Blockchain"
    APP_DESCRIPTION: str = "Sistema de tokenização de safras para microfinanciamento"
    APP_VERSION: str = "1.0.0"
    
    BLOCKCHAIN_URL: str = "http://127.0.0.1:7545"
    CONTRACT_ADDRESS: Optional[str] = "0x0240F83eb93490CdD2a07Ab44718428f07b1bc51"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    ALLOWED_ORIGINS: list = ["*"]
    
    CONTRACT_ABI_PATH: str = "contracts/SafraToken.json"
    
    API_TOKEN: str = "credito-rural-2024-token-blockchain-api"
    
    def __init__(self):
        self.BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL", self.BLOCKCHAIN_URL)
        self.CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", self.CONTRACT_ADDRESS)
        self.HOST = os.getenv("API_HOST", self.HOST)
        self.PORT = int(os.getenv("API_PORT", self.PORT))

settings = Settings()