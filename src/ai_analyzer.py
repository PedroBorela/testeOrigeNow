import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (onde a chave da API deve estar salva)
load_dotenv()

class AIAnalyzer:
    """
    Classe responsável pela interação com modelos de Inteligência Artificial.
    Atualmente integra com o Google Gemini para gerar análises de texto.
    """

    def __init__(self):
        """
        Inicializa o analisador de IA.
        Tenta carregar a chave de API e configurar o cliente.
        Se a chave não existir, ativa o modo de fallback (sem erro crítico).
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        self.has_key = False
        self.api_key = api_key
        
        if api_key:
            # Configura a biblioteca do Gemini com a chave fornecida
            genai.configure(api_key=api_key)
            self.has_key = True
        else:
            # Avisa no console que a chave não foi encontrada
            print("Aviso: GOOGLE_API_KEY não encontrada. Funcionalidades de IA usarão dados simulados.")

    def generate_summary(self, dataframe_summary: str) -> str:
        """
        Gera um resumo ou insight de negócios com base nos dados fornecidos.
        Tenta usar vários modelos em sequência caso o limite de cota seja atingido.
        
        Args:
            dataframe_summary (str): Uma representação textual dos dados (ex: estatísticas).
            
        Retorna:
            str: O texto gerado pela IA com a análise.
        """
        # Se não tiver chave, retorna um texto padrão para não quebrar a aplicação
        if not self.has_key:
            return "Análise de IA (Simulada): O conjunto de dados contém diversos produtos. Os preços variam significativamente. Eletrônicos parecem ser a categoria mais cara."

        # Prompt em português instruindo a IA sobre o que fazer
        prompt = f"""
        Analise o seguinte resumo de dados de produtos e forneça 3 insights de negócios importantes em tom profissional.
        Foque em tendências de preços e distribuição de categorias.
        Responda em Português do Brasil.
        
        Resumo dos Dados:
        {dataframe_summary}
        """

        # Lista de modelos para tentar (Fallback strategy)
        # Se o primeiro falhar (cota estourada), tenta o próximo
        models_to_try = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-flash-latest',
            'gemini-pro-latest'
        ]

        for model_name in models_to_try:
            try:
                # print(f"Tentando gerar insights com o modelo: {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                error_msg = str(e)
                # print(f"Erro com {model_name}: {error_msg}")
                # Se for erro de cota (429) ou não encontrado (404), continua para o próximo
                if "429" in error_msg or "404" in error_msg or "Quota exceeded" in error_msg:
                    continue
                else:
                    # Se for outro erro grave, retorna logo
                    return f"Erro ao gerar insight com IA ({model_name}): {error_msg}"

        return "Erro: Falha ao gerar insights em todos os modelos tentados (Cota excedida ou erro de API)."

if __name__ == "__main__":
    # Teste unitário da classe
    analyzer = AIAnalyzer()
    print(analyzer.generate_summary("Categoria A: 10 itens, Preço Médio R$50. Categoria B: 5 itens, Preço Médio R$200."))
