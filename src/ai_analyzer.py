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

    def _generate_local_insight(self, dataframe_summary: str) -> str:
        """
        Gera um insight local (sem IA) baseado no resumo dos dados fornecido.
        Usado como fallback quando a API não está disponível.
        """
        return f"""
        ### 🤖 Análise Automática (Modo Offline)
        
        Não foi possível conectar à Inteligência Artificial no momento (Chave de API ausente ou inválida).
        No entanto, aqui está o resumo dos dados processados:
        
        {dataframe_summary}
        
        **Interpretação Básica:**
        1. Observe quais categorias possuem o maior 'Preço Médio' para identificar seus produtos de alto valor.
        2. Verifique a 'Contagem de Produtos' para entender como seu inventário está distribuído.
        3. Se houver grande disparidade nos preços médios, considere segmentar sua estratégia de marketing.
        """

    def generate_summary(self, dataframe_summary: str) -> str:
        """
        Gera um resumo ou insight de negócios com base nos dados fornecidos.
        Tenta usar vários modelos em sequência caso o limite de cota seja atingido.
        Se falhar, gera um insight local.
        
        Args:
            dataframe_summary (str): Uma representação textual dos dados (ex: estatísticas).
            
        Retorna:
            str: O texto gerado pela IA ou o insight local em caso de falha.
        """
        # Se não tiver chave, usa o fallback local imediatamente
        if not self.has_key:
            return self._generate_local_insight(dataframe_summary)

        # Prompt em português instruindo a IA sobre o que fazer
        prompt = f"""
        Analise o seguinte resumo de dados de produtos e forneça 3 insights de negócios importantes em tom profissional.
        Foque em tendências de preços e distribuição de categorias.
        Responda em Português do Brasil.
        
        Resumo dos Dados:
        {dataframe_summary}
        """

        # Lista de modelos para tentar (Fallback strategy)
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
                
                # Se for problema de chave inválida, pare de tentar e vá pro fallback local
                if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
                    return self._generate_local_insight(dataframe_summary)

                # Se for erro de cota (429) ou não encontrado (404), continua para o próximo modelo
                if "429" in error_msg or "404" in error_msg or "Quota exceeded" in error_msg:
                    continue
                else:
                    # Se for outro erro, tenta o local também (melhor que crashar ou mostrar erro feio)
                    return self._generate_local_insight(dataframe_summary)

        # Se esgotou todos os modelos e não conseguiu
        return self._generate_local_insight(dataframe_summary)

if __name__ == "__main__":
    # Teste unitário da classe
    analyzer = AIAnalyzer()
    print(analyzer.generate_summary("Categoria A: 10 itens, Preço Médio R$50. Categoria B: 5 itens, Preço Médio R$200."))
