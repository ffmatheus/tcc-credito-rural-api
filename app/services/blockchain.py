from web3 import Web3
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

from app.core.config import settings
from app.models.schemas import SafraCreateRequest, SafraTransferRequest, SafraStatusUpdateRequest

class BlockchainService:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.contract_address = settings.CONTRACT_ADDRESS
        self._initialize_connection()
        
    def _initialize_connection(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_URL))
            
            if not self.w3.is_connected():
                raise Exception("Não foi possível conectar ao blockchain")
            
            contract_abi = self._load_contract_abi()
            
            self.contract = self.w3.eth.contract(
                address=self.contract_address, 
                abi=contract_abi
            )
            
            print(f"✅ Conectado ao blockchain: {settings.BLOCKCHAIN_URL}")
            print(f"✅ Contrato carregado: {self.contract_address}")
            
        except Exception as e:
            print(f"❌ Erro ao conectar com blockchain: {e}")
            raise e
    
    def _load_contract_abi(self) -> List[Dict]:
        try:
            with open(settings.CONTRACT_ABI_PATH, 'r') as file:
                contract_json = json.load(file)
                return contract_json['abi']
        except FileNotFoundError:
            raise Exception(f"Arquivo {settings.CONTRACT_ABI_PATH} não encontrado")
        except json.JSONDecodeError:
            raise Exception("Erro ao decodificar JSON do contrato")
    
    def is_connected(self) -> bool:
        return self.w3 is not None and self.w3.is_connected()
    
    def get_latest_block(self) -> Optional[int]:
        if self.is_connected():
            return self.w3.eth.block_number
        return None
    
    def get_accounts(self) -> List[Dict[str, Any]]:
        if not self.is_connected():
            raise Exception("Blockchain não conectado")
        
        accounts = self.w3.eth.accounts
        balances = []
        
        for account in accounts:
            balance = self.w3.eth.get_balance(account)
            balances.append({
                "address": account,
                "balance_wei": balance,
                "balance_eth": float(self.w3.from_wei(balance, 'ether'))
            })
        
        return balances
    
    def tokenizar_safra(
        self, 
        safra_data: SafraCreateRequest, 
        conta_produtor: Optional[str] = None
    ) -> Dict[str, Any]:
        if not self.contract:
            raise Exception("Contrato não carregado")
        
        if not conta_produtor:
            conta_produtor = self.w3.eth.accounts[0]
        
        timestamp_colheita = int(datetime.now().timestamp()) + (
            safra_data.dias_para_colheita * 24 * 60 * 60
        )
        
        try:
            tx_hash = self.contract.functions.tokenizarSafra(
                safra_data.tipo.value,
                safra_data.quantidade,
                safra_data.valor_estimado,
                safra_data.localizacao,
                timestamp_colheita
            ).transact({'from': conta_produtor})
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            token_id = self._extract_token_id_from_receipt(receipt)
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "token_id": token_id,
                "gas_used": receipt.gasUsed
            }
            
        except Exception as e:
            raise Exception(f"Erro ao tokenizar safra: {str(e)}")
    
    def obter_safra(self, token_id: int) -> Dict[str, Any]:
        if not self.contract:
            raise Exception("Contrato não carregado")
        
        try:
            safra_data = self.contract.functions.obterSafra(token_id).call()
            
            tipo_nomes = ["Milho", "Soja", "Trigo", "Café", "Algodão"]
            status_nomes = ["Plantada", "Crescendo", "Colhida", "Entregue"]
            
            return {
                "token_id": token_id,
                "produtor": safra_data[0],
                "tipo": safra_data[1],
                "tipo_nome": tipo_nomes[safra_data[1]],
                "quantidade": safra_data[2],
                "valor_estimado": safra_data[3],
                "status": safra_data[4],
                "status_nome": status_nomes[safra_data[4]],
                "localizacao": safra_data[5],
                "data_plantio": datetime.fromtimestamp(safra_data[6]).strftime('%Y-%m-%d'),
                "data_colheita_prevista": datetime.fromtimestamp(safra_data[7]).strftime('%Y-%m-%d'),
                "proprietario_atual": safra_data[8]
            }
            
        except Exception as e:
            raise Exception(f"Erro ao obter safra {token_id}: {str(e)}")
    
    def transferir_propriedade(
        self, 
        transfer_data: SafraTransferRequest, 
        conta_atual: Optional[str] = None
    ) -> Dict[str, Any]:
        if not self.contract:
            raise Exception("Contrato não carregado")
        
        if not conta_atual:
            conta_atual = self.w3.eth.accounts[0]
        
        try:
            tx_hash = self.contract.functions.transferirPropriedade(
                transfer_data.token_id,
                transfer_data.novo_proprietario
            ).transact({'from': conta_atual})
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "gas_used": receipt.gasUsed
            }
            
        except Exception as e:
            raise Exception(f"Erro ao transferir safra: {str(e)}")
    
    def atualizar_status_safra(
        self, 
        status_data: SafraStatusUpdateRequest, 
        conta_produtor: Optional[str] = None
    ) -> Dict[str, Any]:
        if not self.contract:
            raise Exception("Contrato não carregado")
        
        if not conta_produtor:
            conta_produtor = self.w3.eth.accounts[0]
        
        try:
            tx_hash = self.contract.functions.atualizarStatus(
                status_data.token_id,
                status_data.novo_status.value
            ).transact({'from': conta_produtor})
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "gas_used": receipt.gasUsed
            }
            
        except Exception as e:
            raise Exception(f"Erro ao atualizar status: {str(e)}")
    
    def listar_todas_safras(self) -> Dict[str, Any]:
        if not self.contract:
            raise Exception("Contrato não carregado")
        
        try:
            token_ids = self.contract.functions.todasSafras().call()
            safras = []
            
            tipo_nomes = ["Milho", "Soja", "Trigo", "Café", "Algodão"]
            status_nomes = ["Plantada", "Crescendo", "Colhida", "Entregue"]
            
            for token_id in token_ids:
                safra_data = self.contract.functions.obterSafra(token_id).call()
                safras.append({
                    "token_id": token_id,
                    "produtor": safra_data[0],
                    "tipo": safra_data[1],
                    "tipo_nome": tipo_nomes[safra_data[1]],
                    "quantidade": safra_data[2],
                    "valor_estimado": safra_data[3],
                    "status": safra_data[4],
                    "status_nome": status_nomes[safra_data[4]],
                    "localizacao": safra_data[5],
                    "proprietario_atual": safra_data[8]
                })
            
            return {"safras": safras, "total": len(safras)}
            
        except Exception as e:
            raise Exception(f"Erro ao listar safras: {str(e)}")
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        if not self.contract:
            raise Exception("Contrato não carregado")
        
        try:
            stats = self.contract.functions.obterEstatisticas().call()
            
            return {
                "total_safras_tokenizadas": stats[0],
                "proximo_token_id": stats[1],
                "blockchain_block": self.get_latest_block()
            }
            
        except Exception as e:
            raise Exception(f"Erro ao obter estatísticas: {str(e)}")
    
    def _extract_token_id_from_receipt(self, receipt) -> Optional[int]:
        for log in receipt.logs:
            try:
                event = self.contract.events.SafraTokenizada().process_log(log)
                return event['args']['tokenId']
            except:
                continue
        return None

blockchain_service = BlockchainService()