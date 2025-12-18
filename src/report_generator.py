import pandas as pd
import matplotlib.pyplot as plt
import os

class ReportGenerator:
    """
    Classe responsável por gerar saídas do sistema (arquivos e gráficos).
    Gerencia a criação de diretórios e salvamento em diferentes formatos.
    """

    def __init__(self, output_dir="output"):
        """
        Inicializa o gerador de relatórios.
        Cria o diretório de saída caso ele não exista.
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def save_to_excel(self, df: pd.DataFrame, filename: str = "relatorio_produtos.xlsx"):
        """
        Salva o DataFrame em um arquivo Excel (.xlsx).
        Utiliza a engine 'openpyxl' internamente.
        """
        filepath = os.path.join(self.output_dir, filename)
        try:
            # index=False evita que o número da linha seja salvo como uma coluna extra
            df.to_excel(filepath, index=False)
            print(f"Relatório salvo em: {filepath}")
        except Exception as e:
            print(f"Erro ao salvar relatório Excel: {e}")

    def save_to_csv(self, df: pd.DataFrame, filename: str = "relatorio_produtos.csv"):
        """
        Salva o DataFrame em um arquivo CSV (Comma Separated Values).
        Formato universalmente aceito para dados.
        """
        filepath = os.path.join(self.output_dir, filename)
        try:
            df.to_csv(filepath, index=False)
            print(f"Relatório salvo em: {filepath}")
        except Exception as e:
            print(f"Erro ao salvar relatório CSV: {e}")

    def save_insights(self, text: str, filename: str = "insights_ia.txt"):
        """
        Salva o texto gerado pela IA em um arquivo de texto simples (.txt).
        Utiliza encoding UTF-8 para garantir suporte a acentos.
        """
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Insights salvos em: {filepath}")
        except Exception as e:
            print(f"Erro ao salvar insights: {e}")

    def generate_price_chart(self, df: pd.DataFrame, filename: str = "distribuicao_precos.png"):
        """
        Gera um histograma da distribuição de preços e salva como imagem PNG.
        Utiliza a biblioteca Matplotlib.
        """
        if df.empty:
            return
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Cria uma nova figura com tamanho 10x6 polegadas
        plt.figure(figsize=(10, 6))
        
        # Cria o histograma (distribuição de frequência)
        # bins=20 define o número de "barras" ou intervalos
        plt.hist(df['price'], bins=20, color='skyblue', edgecolor='black')
        
        # Adiciona títulos e rótulos aos eixos (traduzidos)
        plt.title('Distribuição de Preços dos Produtos')
        plt.xlabel('Preço ($)')
        plt.ylabel('Frequência (Qtd Produtos)')
        plt.grid(True) # Adiciona linhas de grade para facilitar leitura
        
        try:
            plt.savefig(filepath)
            plt.close() # Fecha o plot para liberar memória do sistema
            print(f"Gráfico salvo em: {filepath}")
        except Exception as e:
            print(f"Erro ao salvar gráfico: {e}")

if __name__ == "__main__":
    # Teste unitário para geração de gráfico
    df = pd.DataFrame({"price": [10, 20, 30, 40, 50, 60, 100]})
    gen = ReportGenerator()
    gen.generate_price_chart(df)
