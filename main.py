import sys
from src.data_collector import DataCollector
from src.data_processor import DataProcessor
from src.ai_analyzer import AIAnalyzer
from src.report_generator import ReportGenerator

def main():
    """
    Função principal que orquestra todo o fluxo de automação via linha de comando.
    """
    print("--- Analisador Automatizado de Produtos ---")
    
    # 1. Coleta (Etapa 1 de 4)
    print("[1/4] Coletando dados...")
    collector = DataCollector()
    raw_data = collector.fetch_products()
    
    # Se a coleta falhar (retornar vazio), encerra o programa
    if not raw_data:
        print("Falha ao coletar dados. Encerrando.")
        return

    # 2. Processamento (Etapa 2 de 4)
    print("[2/4] Processando dados...")
    processor = DataProcessor(raw_data)
    df = processor.process_and_clean()
    
    print(f"      Processados {len(df)} produtos com sucesso.")
    stats = processor.get_category_stats()
    print("      Estatísticas por Categoria:\n", stats)

    # 3. Análise de IA (Etapa 3 de 4)
    print("[3/4] Gerando Insights com IA...")
    analyzer = AIAnalyzer()
    
    # Prepara o resumo dos dados para enviar ao modelo
    stats_str = stats.to_string()
    summary_for_ai = f"Total de Produtos: {len(df)}. Preço Médio: {df['price'].mean():.2f}. Estatísticas: \n{stats_str}"
    
    # Chama a API da IA
    insight = analyzer.generate_summary(summary_for_ai)
    print("      Insight de IA gerado.")
    print("-" * 20)
    print(insight)
    print("-" * 20)

    # 4. Geração de Relatórios (Etapa 4 de 4)
    # print("[4/4] Gerando Relatórios e Arquivos...")
    # generator = ReportGenerator()
    
    # # Gera Excel, CSV, Texto e Gráfico
    # generator.save_to_excel(df)
    # generator.save_to_csv(df)
    # generator.save_insights(insight)
    # generator.generate_price_chart(df)
    
    # print("Concluído! Verifique a pasta 'output'.")

if __name__ == "__main__":
    # Verifica argumentos de linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        print("Para rodar a interface gráfica, use o comando: streamlit run src/dashboard.py")
    else:
        main()
