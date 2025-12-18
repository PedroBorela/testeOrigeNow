import requests
from typing import List, Dict, Any

class DataCollector:
    """
    Classe responsável pela coleta de dados de APIs externas.
    Esta classe encapsula a lógica de requisição HTTP, tratamento de erros e retorno dos dados brutos.
    """
    
    # URL base da API pública FakeStoreAPI que fornece dados de produtos simulados
    BASE_URL = "https://fakestoreapi.com/products"

    def fetch_products(self) -> List[Dict[str, Any]]:
        """
        Busca a lista de produtos da FakeStoreAPI.
        
        Realiza uma requisição GET para o endpoint de produtos.
        Inclui tratamento para diversos tipos de exceções que podem ocorrer durante a comunicação de rede.

        Retorna:
            List[Dict[str, Any]]: Uma lista de dicionários, onde cada dicionário representa um produto.
                                  Retorna uma lista vazia em caso de falha.
        """
        try:
            # Tenta realizar a requisição HTTP GET para a URL definida
            # O parâmetro timeout=10 garante que o código não fique travado indefinidamente se a API não responder
            response = requests.get(self.BASE_URL, timeout=10)
            
            # Verifica se o código de status da resposta indica sucesso (2xx)
            # Se o status for 4xx ou 5xx, lança uma exceção HTTPError
            response.raise_for_status() 
            
            # Converte o conteúdo da resposta (JSON) para objetos Python (listas/dicionários)
            data = response.json()
            return data
            
        except requests.exceptions.Timeout:
            # Captura erro de timeout (tempo limite excedido)
            print("Erro: A requisição excedeu o tempo limite.")
            return []
        except requests.exceptions.ConnectionError:
            # Captura erros de conexão (ex: sem internet, DNS falhou)
            print("Erro: Não foi possível conectar à API.")
            return []
        except requests.exceptions.HTTPError as e:
            # Captura erros de protocolo HTTP (ex: 404 Not Found, 500 Internal Server Error)
            print(f"Erro HTTP: {e}")
            return []
        except requests.exceptions.RequestException as e:
            # Captura qualquer outra exceção relacionada à biblioteca requests
            print(f"Ocorreu um erro inesperado: {e}")
            return []

if __name__ == "__main__":
    # Bloco de teste para execução direta do arquivo
    # Isso permite testar a coleta de dados isoladamente sem rodar o sistema todo
    collector = DataCollector()
    products = collector.fetch_products()
    print(f"Coletados {len(products)} produtos.")
    if products:
        print(f"Exemplo de produto: {products[0]}")
