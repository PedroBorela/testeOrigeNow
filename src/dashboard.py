import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Adiciona o diretório raiz ao sys.path para permitir importações se necessário, 
# mas o Streamlit geralmente resolve arquivos no mesmo diretório diretamente.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Correção: Importando módulos diretamente, pois o Streamlit adiciona a pasta 'src' ao path.
from data_collector import DataCollector
from data_processor import DataProcessor
from ai_analyzer import AIAnalyzer

# Configuração da página do Streamlit
# Define o título da aba do navegador e o layout expandido (wide)
st.set_page_config(page_title="Analisador Automatizado de Produtos", layout="wide")

# Cabeçalho principal da aplicação
st.title("📊 Analisador Automatizado de Produtos")
st.markdown("Coleta, Processamento e Análise de Dados com Inteligência Artificial")

# Barra lateral para controles e ações
st.sidebar.header("Controles")

# Botão para iniciar a coleta de dados
if st.sidebar.button("Buscar Dados"):
    with st.spinner("Buscando dados da API..."):
        # Instancia o coletor e busca os produtos
        collector = DataCollector()
        raw_data = collector.fetch_products()
        
        if raw_data:
            # Salva os dados no 'session_state' para persistirem entre reloads da página
            st.session_state['data'] = raw_data
            st.success(f"Sucesso! {len(raw_data)} produtos coletados.")
        else:
            st.error("Falha ao buscar dados.")

# Verifica se existem dados carregados na sessão
if 'data' in st.session_state:
    data = st.session_state['data']
    
    # Instancia o processador com os dados carregados
    processor = DataProcessor(data)
    # Executa a limpeza e processamento inicial
    df = processor.process_and_clean()

    # Cria abas para organizar a visualização
    tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Visualizações", "Insights de IA", "Análise Avançada"])

    with tab1:
        st.subheader("Dados Brutos")
        # Exibe o DataFrame como uma tabela interativa
        st.dataframe(df)

        st.subheader("Estatísticas Principais")
        # Obtém e exibe as estatísticas por categoria
        stats = processor.get_category_stats()
        st.table(stats)
        
        # Exibe métricas em colunas lado a lado
        col1, col2 = st.columns(2)
        with col1:
             st.metric("Total de Produtos", len(df))
        with col2:
             st.metric("Preço Médio", f"R$ {df['price'].mean():.2f}")

    with tab2:
        st.subheader("Visualizações Gráficas")
        
        # Gráfico 1: Histograma de Distribuição de Preços
        fig_hist = px.histogram(df, x="price", nbins=20, title="Distribuição de Preços")
        # Atualiza labels para português
        fig_hist.update_layout(xaxis_title="Preço ($)", yaxis_title="Contagem")
        st.plotly_chart(fig_hist, width="stretch")

        # Gráfico 2: Barras de Produtos por Categoria
        cat_counts = df['category'].value_counts().reset_index()
        cat_counts.columns = ['Categoria', 'Contagem']
        fig_bar = px.bar(cat_counts, x='Categoria', y='Contagem', title="Produtos por Categoria")
        st.plotly_chart(fig_bar, width="stretch")

    with tab3:
        st.subheader("Análise de Inteligência Artificial")
        st.markdown("Clique no botão abaixo para gerar uma análise qualitativa dos dados usando IA.")
        
        if st.button("Gerar Insights com IA"):
            with st.spinner("Consultando a IA..."):
                analyzer = AIAnalyzer()
                
                # Prepara um resumo textual para enviar ao modelo (prompt context)
                stats_str = stats.to_string()
                summary_prompt = f"Total de Produtos: {len(df)}. Preço Médio: {df['price'].mean():.2f}. Estatísticas por Categoria: \n{stats_str}"
                
                # Chama a API
                insight = analyzer.generate_summary(summary_prompt)
                
                # Exibe o resultado
                st.markdown("### 🤖 Resultado da Análise")
                st.write(insight)
                
                if not analyzer.has_key:
                    st.warning("Nota: Esta é uma resposta simulada pois a chave da API não foi encontrada.")
                    
    with tab4:
        st.markdown("## 📈 Análise Avançada de Negócios")
        st.markdown("Visualizações estratégicas para tomada de decisão em E-commerce.")
        
        # 1. Análise de Portfólio (Preço vs Avaliação)
        st.subheader("1. Análise de Portfólio (Valor Percebido)")
        st.info("Insight: Cruza o Preço com a Nota de Avaliação (Rate). Permite identificar se produtos mais caros estão entregando a satisfação esperada.")
        
        if 'rate' in df.columns:
            fig_portfolio = px.scatter(
                df, 
                x='price', 
                y='rate', 
                color='category', 
                size='count', 
                hover_data=['title'],
                title="Preço vs Satisfação (Bolhas = Volume de Avaliações)"
            )
            fig_portfolio.update_layout(xaxis_title="Preço ($)", yaxis_title="Nota (Rate)")
            st.plotly_chart(fig_portfolio, width="stretch")
        else:
            st.warning("Dados de avaliação não disponíveis para este gráfico.")

        # 2. Matriz de Popularidade
        st.subheader("2. Matriz de Popularidade")
        st.info("Insight: Identifica 'Produtos Estrela' (Alta nota/Alto volume) e 'Oportunidades' (Alta nota/Baixo volume).")
        
        if 'rate' in df.columns and 'count' in df.columns:
            fig_popularity = px.scatter(
                df,
                x='count',
                y='rate',
                color='category',
                hover_data=['title'],
                title="Volume de Avaliações vs Nota Média"
            )
            # Adiciona linhas de quadrante média para referência
            avg_rate = df['rate'].mean()
            avg_count = df['count'].mean()
            fig_popularity.add_hline(y=avg_rate, line_dash="dash", annotation_text="Nota Média")
            fig_popularity.add_vline(x=avg_count, line_dash="dash", annotation_text="Vol. Médio")
            fig_popularity.update_layout(xaxis_title="Volume de Avaliações (Count)", yaxis_title="Nota (Rate)")
            st.plotly_chart(fig_popularity, width="stretch")
        
        # 3. Segmentação de Preços (Boxplot)
        st.subheader("3. Segmentação de Preços por Categoria")
        st.info("Insight: Mostra a dispersão de preços. Caixas longas indicam categorias com produtos de entrada e luxo misturados.")
        fig_box = px.box(df, x='category', y='price', color='category', title="Distribuição de Preços (Boxplot)")
        st.plotly_chart(fig_box, width="stretch")
        
        # 4. Análise de Texto (Palavras-chave em produtos bem avaliados)
        st.subheader("4. Análise de Texto (Produtos 4.0+)")
        st.info("Insight: Termos mais frequentes nas descrições de produtos com alta nota. Ajuda a entender o que valorizar no copy.")
        
        if 'rate' in df.columns:
            from collections import Counter
            import re
            
            # Filtra produtos com nota >= 4.0
            high_rated_df = df[df['rate'] >= 4.0]
            
            if not high_rated_df.empty:
                # Concatena todas as descrições
                text = " ".join(high_rated_df['description'].astype(str).tolist()).lower()
                # Remove caracteres especiais simples
                text = re.sub(r'[^\w\s]', '', text)
                words = text.split()
                # Remove stopwords simples em inglês (já que a API retorna em inglês)
                stopwords = {'the', 'and', 'a', 'of', 'to', 'in', 'with', 'for', 'is', 'on', 'it', 'this', 'that', 'your', 'are', 'from'} 
                filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
                
                # Conta frequência
                word_counts = Counter(filtered_words).most_common(15)
                words_df = pd.DataFrame(word_counts, columns=['Palavra', 'Frequência'])
                
                fig_words = px.bar(words_df, x='Frequência', y='Palavra', orientation='h', title="Top 15 Palavras em Descrições de Sucesso")
                fig_words.update_layout(yaxis=dict(autorange="reversed")) # Inverte para o maior ficar em cima
                st.plotly_chart(fig_words, width="stretch")
            else:
                st.write("Não há produtos com nota >= 4.0 para análise.")
else:
    # Mensagem inicial caso nenhum dado tenha sido carregado
    st.info("Clique em 'Buscar Dados' na barra lateral para começar.")
