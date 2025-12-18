# Analisador Automatizado de Produtos

## Descrição do Projeto
Este projeto é um sistema de automação inteligente desenvolvido para coletar dados de produtos de uma API pública, processá-los aplicando regras de negócio, analisar tendências utilizando Inteligência Artificial e gerar relatórios estruturados. O sistema possui uma interface de linha de comando (CLI) para execução automatizada e um dashboard interativo (GUI) para exploração visual.

## Instruções de Execução

### Pré-requisitos
- Python 3.8+
- [Opcional] Chave de API do Google Gemini para recursos de IA (o sistema funciona com dados simulados se a chave não for fornecida).

### Instalação
1. Clone o repositório ou baixe os arquivos.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configuração da IA:
   - Renomeie ou crie um arquivo `.env` na raiz do projeto.
   - Adicione sua chave: `GOOGLE_API_KEY=sua_chave_aqui`

### Como Executar

**Modo Automático (CLI):**
Executa todo o fluxo (coleta -> processamento -> IA -> relatórios) e salva os arquivos na pasta `output`.
```bash
python main.py
```

**Modo Visual (Dashboard):**
Inicia a interface web para interagir com os dados.
```bash
streamlit run src/dashboard.py
```

## API Utilizada
O sistema consome dados da **FakeStoreAPI**:
- **URL Base**: `https://fakestoreapi.com/products`
- **Dados Coletados**: ID, Título, Preço, Categoria, Descrição e Imagem.

## Aplicação da IA
A Inteligência Artificial foi integrada para fornecer análises qualitativas sobre os dados quantitativos.
- **Onde**: Módulo `src/ai_analyzer.py`.
- **Como**: O sistema resume estatísticas dos produtos (média de preços, contagem por categoria) e envia um prompt para o modelo **Google Gemini**. O modelo retorna insights de negócios em linguagem natural, destacando tendências de preços e distribuição de estoque.
- **Integração**: Utiliza a biblioteca `google-generativeai`. Foi implementado um sistema de *fallback* (mock), onde o sistema gera uma resposta padrão caso a chave de API não esteja configurada, garantindo que a aplicação não quebre.

## Principais Decisões Técnicas
1.  **Arquitetura Modular**: O código foi separado em módulos específicos (`data_collector`, `data_processor`, `ai_analyzer`, `report_generator`) dentro da pasta `src`. Isso facilita a manutenção e testes unitários.
2.  **Uso de Streamlit**: Escolhido para a interface gráfica por permitir a criação rápida de dashboards de dados interativos com Python puro, sem necessidade de HTML/CSS complexos.
3.  **Pandas para Dados**: Utilizado como a estrutura central de dados (DataFrame) devido à sua eficiência em filtragem, agrupamento e exportação para múltiplos formatos (Excel, CSV).
4.  **Tratamento de Erros**: Implementação robusta de blocos `try/except` na coleta de dados e integração com IA para garantir que falhas de rede não interrompam o fluxo abruptamente.

## Dificuldades Encontradas
1.  **Gerenciamento de Dependências**: Inicialmente, a biblioteca `matplotlib` não estava listada no `requirements.txt`, o que causou erro na geração de gráficos na primeira execução. Isso foi corrigido adicionando a dependência e reinstalando.
2.  **Integração Segura com API**: Garantir que o sistema funcionasse mesmo sem a chave de API da IA ser fornecida pelo usuário. A solução foi criar uma verificação inicial e usar dados simulados (mock) quando a chave está ausente, permitindo que avaliadores testem o fluxo básico sem configuração complexa.
3.  **Formatação de Dados**: Alguns dados da API poderiam vir inconsistentes. Foi necessário implementar uma etapa de limpeza (`process_and_call`) para garantir tipos numéricos corretos e preencher valores nulos.
