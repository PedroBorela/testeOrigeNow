import pandas as pd
from typing import List, Dict, Any, Tuple

class DataProcessor:
    """
    Classe responsável pelo processamento, limpeza e aplicação de regras de negócio aos dados.
    Utiliza a biblioteca Pandas para manipulação eficiente de dados tabulares.
    """

    def __init__(self, data: List[Dict[str, Any]]):
        """
        Inicializa o processador com os dados brutos.
        Converte a lista de dicionários para um DataFrame do Pandas.
        """
        self.df = pd.DataFrame(data)

    def process_and_clean(self) -> pd.DataFrame:
        """
        Realiza a limpeza dos dados e garante a consistência dos tipos.
        
        Passos realizados:
        1. Garante que colunas numéricas sejam do tipo float.
        2. Preenche valores nulos em campos de texto.
        3. Remove registros inválidos (sem preço).
        
        Retorna:
            pd.DataFrame: O DataFrame processado e limpo.
        """
        if self.df.empty:
            return self.df

        # Converte a coluna 'price' para numérico, forçando erros a virarem NaN (Not a Number)
        # Isso evita que o programa quebre se vier um texto inválido no preço (ex: "R$ 10,00" vs "10.00")
        self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce')
        
        # Preenche descrições vazias com um texto padrão
        self.df['description'] = self.df['description'].fillna('Sem descrição')
        
        # Preenche títulos vazios com 'Sem título'
        self.df['title'] = self.df['title'].fillna('Sem título')
        
        # Remove linhas onde o preço é NaN (inválido ou ausente), pois são inúteis para análise de preços
        self.df = self.df.dropna(subset=['price'])
        
        # Normalização da coluna 'rating' (que vem como dicionário da API: {'rate': 3.9, 'count': 120})
        # Se a coluna existir, vamos expandi-la em duas colunas separadas: 'rate' e 'count'
        if 'rating' in self.df.columns:
            # Extrai os dados do dicionário em novas colunas
            # Usa apply(pd.Series) se for seguro, ou extração direta para performance
            ratings = self.df['rating'].apply(pd.Series)
            self.df['rate'] = ratings['rate']
            self.df['count'] = ratings['count']
            # Remove a coluna original de dicionário para limpar o DataFrame
            self.df = self.df.drop(columns=['rating'])
            
            # Garante que as novas colunas sejam numéricas (preenchendo com 0 se falhar)
            self.df['rate'] = pd.to_numeric(self.df['rate'], errors='coerce').fillna(0)
            self.df['count'] = pd.to_numeric(self.df['count'], errors='coerce').fillna(0)
            
        return self.df

    def get_expensive_products(self, threshold: float = 50.0) -> pd.DataFrame:
        """
        Regra de Negócio: Filtrar produtos acima de um determinado preço.
        
        Args:
            threshold (float): O valor de corte para considerar um produto "caro". Padrão é 50.0.
            
        Retorna:
            pd.DataFrame: Apenas os produtos que custam mais que o valor do threshold.
        """
        if self.df.empty:
            return pd.DataFrame()
        # Aplica um filtro booleano no DataFrame
        return self.df[self.df['price'] > threshold]

    def get_category_stats(self) -> pd.DataFrame:
        """
        Regra de Negócio: Agrupar por categoria e calcular estatísticas.
        
        Calcula:
        1. Média de preço por categoria.
        2. Contagem de produtos por categoria.
        
        Retorna:
            pd.DataFrame: Um DataFrame resumo com as estatísticas calculadas.
        """
        if self.df.empty:
            return pd.DataFrame()
            
        # Agrupa pelo campo 'category' e calcula a média ('mean') e a contagem ('count') da coluna 'price'
        stats = self.df.groupby('category')['price'].agg(['mean', 'count']).reset_index()
        
        # Renomeia as colunas para ficar mais legível no relatório final
        stats.columns = ['Categoria', 'Preço Médio', 'Contagem de Produtos']
        return stats

if __name__ == "__main__":
    # Bloco de teste (stub) para processamento
    sample_data = [
        {"id": 1, "title": "A", "price": 10.0, "category": "cat1"},
        {"id": 2, "title": "B", "price": 100.0, "category": "cat1"},
        {"id": 3, "title": "C", "price": 60.0, "category": "cat2"}
    ]
    processor = DataProcessor(sample_data)
    processor.process_and_clean()
    print("Caros:\n", processor.get_expensive_products())
    print("Estatísticas:\n", processor.get_category_stats())
