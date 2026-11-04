# ClaudIA — Professora Inteligente com Arquitetura Multi-Vetorial, RAG e Multiagentes

A ClaudIA é uma plataforma de aprendizagem assistida por IA. Ela funciona como uma professora virtual capaz de consultar documentos locais (RAG), gerar provas estruturadas e orquestrar múltiplos agentes.

## 🚀 Arquitetura
- **Backend:** Python 3.11+, Flask, SQLAlchemy, Flask-Login.
- **Frontend:** HTML5, CSS3 Vanilla, JavaScript (Marked.js, DOMPurify).
- **IA e Orquestração:** Azure OpenAI (Agente Supervisor, Professor e Avaliador).
- **Memória Vetorial (RAG):** Azure AI Search + Embeddings.
- **Processamento de Arquivos:** PyMuPDF, python-docx.

## ⚙️ Instalação Local (Desenvolvimento)

1. Clone o repositório e crie o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows