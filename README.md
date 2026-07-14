# AgentDesk API

API para gerenciamento e execução de agentes de IA, integrada com o Ollama para processamento de linguagem natural.

## 🚀 Tecnologias

- **Python 3.12+**
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy 2.0** - ORM para manipulação do banco de dados
- **SQLite** - Banco de dados (configurável para PostgreSQL/MySQL)
- **Pydantic** - Validação de dados e configurações
- **httpx** - Cliente HTTP assíncrono
- **Ollama** - Serviço de IA local para execução de modelos

## 📁 Estrutura do Projeto

```
agentdesk-api/
├── app/
│   ├── api/                 # Rotas e dependências da API
│   │   ├── dependencies.py  # Injeção de dependências
│   │   └── routes/
│   │       ├── agents.py    # Rotas de agentes
│   │       └── runs.py      # Rotas de execuções
│   ├── core/               # Configurações e exceções
│   │   ├── config.py       # Configurações do aplicativo
│   │   ├── enums.py        # Enumerações (RunStatus)
│   │   └── exceptions.py   # Exceções customizadas
│   ├── db/                 # Configurações do banco de dados
│   │   ├── base.py         # Base declarativa do SQLAlchemy
│   │   ├── init_db.py      # Inicialização das tabelas
│   │   └── session.py      # Gerenciamento de sessões
│   ├── integrations/       # Integrações externas
│   │   └── ollama.py       # Cliente do Ollama
│   ├── models/             # Modelos do banco de dados
│   │   ├── agent.py        # Modelo Agent
│   │   └── run.py          # Modelo Run
│   ├── repositories/       # Repositórios de dados
│   │   ├── agent_repository.py
│   │   └── run_repository.py
│   ├── schemas/            # Schemas Pydantic
│   │   ├── agent.py        # Schemas de Agent
│   │   ├── health.py       # Schema de health check
│   │   └── run.py          # Schemas de Run
│   ├── services/           # Lógica de negócio
│   │   ├── agent_service.py
│   │   └── run_service.py
│   └── main.py             # Entry point da aplicação
├── config/                 # Arquivos de configuração adicionais
├── tests/                  # Testes automatizados
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
└── requirements.txt        # Dependências do Python
```

## 📡 Rotas da API

### Health Check

- **GET /health** - Verifica o status da API

### Agents

- **POST /agents** - Cria um novo agente
- **GET /agents** - Lista todos os agentes (paginado)
- **GET /agents/{slug}** - Obtém um agente específico pelo slug
- **PATCH /agents/{slug}** - Atualiza um agente
- **DELETE /agents/{slug}** - Deleta um agente

### Runs

- **POST /agents/{agent_slug}/runs** - Executa um agente com um prompt
- **GET /runs** - Lista todas as execuções (paginado)
- **GET /runs/{run_id}** - Obtém uma execução específica pelo ID

## 🔧 Instalação

### Pré-requisitos

- Python 3.12 ou superior
- Ollama instalado e rodando em `http://localhost:11434`
- Virtual environment recomendado

### Passos

1. Clone o repositório:
```bash
git clone <https://github.com/JaoJaoGo/agentdesk-api.git>
cd agentdesk-api
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

5. Execute a aplicação:
```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## ⚙️ Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `APP_NAME` | Nome da aplicação | `AgentDesk API` |
| `APP_ENV` | Ambiente (development/testing/production) | `development` |
| `APP_DEBUG` | Modo debug | `true` |
| `DATABASE_URL` | URL de conexão com o banco de dados | `sqlite:///./agentdesk.db` |
| `OLLAMA_BASE_URL` | URL do serviço Ollama | `http://localhost:11434` |
| `HTTP_TIMEOUT_SECONDS` | Timeout para requisições HTTP (segundos) | `30` |

## 📊 Modelos de Dados

### Agent

- `id`: Identificador único
- `name`: Nome do agente (3-100 caracteres)
- `slug`: Slug único para identificação (3-80 caracteres, formato kebab-case)
- `description`: Descrição opcional (máx 500 caracteres)
- `system_prompt`: Prompt do sistema para o modelo (10-10.000 caracteres)
- `model`: Modelo do Ollama a ser utilizado (padrão: `qwen2.5:7b`)
- `temperature`: Temperatura para geração (0.0-2.0, padrão: 0.2)
- `active`: Status de ativação do agente
- `created_at`: Data de criação
- `updated_at`: Data de última atualização

### Run

- `id`: Identificador único
- `agent_id`: ID do agente relacionado
- `prompt`: Prompt enviado pelo usuário (3-20.000 caracteres)
- `response`: Resposta gerada pelo modelo
- `status`: Status da execução (pending/completed/failed)
- `model`: Modelo utilizado
- `duration_ms`: Duração da execução em milissegundos
- `prompt_tokens`: Número de tokens do prompt
- `completion_tokens`: Número de tokens da resposta
- `error_message`: Mensagem de erro (caso falhe)
- `created_at`: Data de criação
- `completed_at`: Data de conclusão

## 🔍 Exemplos de Uso

### Criar um Agente

```bash
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Assistente de Código",
    "slug": "code-assistant",
    "description": "Agente especializado em ajudar com código",
    "system_prompt": "Você é um assistente especializado em programação. Ajude o usuário com suas dúvidas sobre código.",
    "model": "qwen2.5:7b",
    "temperature": 0.3
  }'
```

### Executar um Agente

```bash
curl -X POST http://localhost:8000/agents/code-assistant/runs \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Como criar uma função em Python?"
  }'
```

### Listar Agentes

```bash
curl http://localhost:8000/agents?offset=0&limit=20
```

### Listar Execuções

```bash
curl http://localhost:8000/runs?offset=0&limit=20
```

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas com separação de responsabilidades:

- **Routes**: Manipulam as requisições HTTP e respostas
- **Services**: Contêm a lógica de negócio
- **Repositories**: Responsáveis pelo acesso aos dados
- **Models**: Representam as tabelas do banco de dados
- **Schemas**: Definem a estrutura de entrada/saída de dados
- **Integrations**: Encapsulam comunicações com serviços externos

## 🧪 Testes

Para executar os testes (quando implementados):

```bash
pytest
```

## 📝 Documentação da API

Após iniciar a aplicação, a documentação interativa estará disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.
