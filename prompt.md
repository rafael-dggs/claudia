# PROJETO: ClaudIA — Professora Inteligente com Arquitetura Multi-Vetorial, RAG e Multiagentes



## 1. Visão geral do projeto



Desenvolver uma plataforma de aprendizagem assistida por Inteligência Artificial, denominada **ClaudIA**, que atuará como uma professora virtual capaz de auxiliar os usuários no aprendizado, compreensão e aprofundamento de qualquer assunto solicitado.



A solução utilizará uma arquitetura multiagente integrada ao **Azure AI Foundry**, com implementação de um sistema RAG (Retrieval-Augmented Generation) multivetorial, permitindo consultar diferentes fontes de conhecimento, interpretar documentos enviados pelos usuários e fornecer respostas contextualizadas.



O objetivo não é criar apenas um chatbot convencional, mas uma experiência de ensino personalizada, na qual a IA acompanhe o raciocínio do aluno, explique conceitos, identifique dúvidas e adapte suas explicações conforme a necessidade.



## 2. Identidade e personalidade da ClaudIA



A agente principal será chamada **ClaudIA** e deverá assumir a personalidade de uma professora virtual.



### Personalidade

- Acolhedora, paciente e didática.

- Inteligente, comunicativa e profissional.

- Atenciosa, sem ser excessivamente formal.

- Aconchegante e simpática, sem parecer artificial ou exageradamente melosa.

- Capaz de adaptar sua linguagem ao nível de conhecimento do usuário.



### Comportamento pedagógico

- Explicar conceitos progressivamente.

- Utilizar exemplos práticos, analogias e comparações.

- Dividir assuntos complexos em etapas menores.

- Identificar dificuldades de entendimento e reformular explicações.

- Incentivar o pensamento crítico e a autonomia do estudante.

- Adequar a profundidade das respostas ao contexto e à solicitação.



A ClaudIA deve transmitir a sensação de estar conversando com uma professora experiente, acessível e genuinamente interessada no aprendizado do aluno.



## 3. Stack tecnológica



Utilizar preferencialmente as seguintes tecnologias:



### Backend

- **Python 3.11+:** linguagem principal.

- **Flask:** framework responsável pela aplicação web e API.

- **Flask Blueprints:** organização modular das rotas.

- **Flask-SQLAlchemy:** ORM e gerenciamento das entidades.

- **Flask-Login:** gerenciamento de autenticação e sessões.

- **Pydantic:** validação e estruturação de dados.



### Frontend

- **HTML5:** estrutura da interface.

- **CSS3:** identidade visual e estilização personalizada.

- **JavaScript (ES6+):** interatividade e comunicação com o backend.

- **Jinja2:** templates dinâmicos integrados ao Flask.

- **Bootstrap Icons ou Lucide:** biblioteca de ícones.



A interface deverá ser construída com identidade visual própria, evitando a aparência padrão de templates administrativos ou chatbots genéricos.



Não utilizar frameworks frontend complexos sem necessidade. Priorizar uma aplicação leve, organizada e responsiva.



### Inteligência Artificial

- **Azure AI Foundry:** infraestrutura central de IA.

- Modelos de linguagem disponibilizados por deployments do Azure AI Foundry.

- Modelos de embeddings disponibilizados por deployments compatíveis.

- SDKs oficiais da Microsoft ou APIs REST documentadas.

- Orquestração própria dos agentes, integrada aos recursos disponíveis no Foundry.



Os modelos deverão ser configuráveis por variáveis de ambiente, permitindo substituições sem alterações estruturais no código.



### RAG e armazenamento vetorial

- **Azure AI Search:** mecanismo principal de indexação e recuperação vetorial.

- Busca vetorial e híbrida (semântica + lexical).

- Embeddings para representação semântica dos documentos.

- Múltiplos campos vetoriais e estratégias de recuperação.

- Filtros por usuário, documento e coleção.

- Reranking para melhorar a relevância dos resultados.



A arquitetura multivetorial deverá permitir diferentes representações de conhecimento, como conteúdo textual, títulos, resumos e informações contextuais.



### Banco de dados

- **SQLite:** ambiente inicial de desenvolvimento.

- **PostgreSQL:** opção para produção e expansão.

- **Azure Blob Storage:** armazenamento de arquivos enviados pelos usuários, quando necessário.



O banco relacional deverá armazenar informações de usuários, conversas, mensagens, documentos, questionários e resultados.



### Processamento documental

Bibliotecas recomendadas:

- PyMuPDF ou pypdf para PDF.

- python-docx para DOCX.

- python-pptx para PPTX.

- openpyxl para XLSX.

- Bibliotecas nativas para TXT e CSV.



A camada de processamento deverá ser extensível para incorporar novos formatos futuramente.



### Ferramentas auxiliares

- Git e GitHub para versionamento.

- python-dotenv para variáveis de ambiente.

- pytest para testes automatizados.

- logging para registros e diagnóstico.

- requirements.txt para gerenciamento das dependências Python.



## 4. Arquitetura de Inteligência Artificial



Implementar uma arquitetura multiagente modular, utilizando o Azure AI Foundry.



### Agente supervisor

Responsável por:

- Interpretar a solicitação do usuário.

- Identificar a intenção da interação.

- Decidir quais agentes ou ferramentas devem ser acionados.

- Distribuir tarefas.

- Consolidar os resultados.

- Elaborar a resposta final utilizando a personalidade da ClaudIA.



### Agentes especializados



**Agente Professor**

- Explicações didáticas.

- Tutoria personalizada.

- Exemplos e analogias.

- Aprofundamento de conceitos.



**Agente RAG**

- Consulta às bases vetoriais.

- Recuperação de informações relevantes.

- Busca híbrida.

- Organização e apresentação das fontes recuperadas.



**Agente Documental**

- Interpretação de documentos.

- Extração de informações.

- Identificação de conceitos importantes.

- Comparação entre arquivos.

- Preparação de conteúdo para indexação.



**Agente Avaliador**

- Criação de questionários.

- Elaboração de simulados.

- Correção de respostas.

- Avaliação de desempenho.

- Identificação de dificuldades.



Os agentes poderão compartilhar ferramentas e modelos quando apropriado. Não é obrigatório utilizar um deployment independente para cada agente.



## 5. Sistema RAG multivetorial



Desenvolver um pipeline próprio de ingestão e recuperação de conhecimento.



### Pipeline de ingestão



1. Receber o documento.

2. Validar formato e tamanho.

3. Extrair o conteúdo.

4. Limpar e normalizar o texto.

5. Dividir o conteúdo em chunks.

6. Preservar metadados e referências de origem.

7. Gerar embeddings.

8. Indexar os vetores no Azure AI Search.



### Pipeline de recuperação



1. Receber a pergunta do usuário.

2. Interpretar a intenção e o contexto.

3. Gerar embeddings da consulta.

4. Executar buscas nas representações vetoriais pertinentes.

5. Combinar resultados de diferentes estratégias.

6. Aplicar filtros e reranking.

7. Construir o contexto.

8. Encaminhar as informações ao agente responsável pela resposta.



### Requisitos

- Suporte a múltiplas coleções e índices.

- Metadados associados aos documentos.

- Recuperação contextualizada.

- Identificação das fontes utilizadas.

- Separação dos conhecimentos por usuário.

- Possibilidade de reindexação.

- Tratamento de documentos duplicados.

- Estratégia para atualização e exclusão de documentos.



A ClaudIA deverá evitar respostas inventadas quando não houver informações suficientes nas fontes disponíveis.



## 6. Upload e análise de arquivos



O usuário poderá enviar arquivos a qualquer momento durante a conversa.



Formatos desejados:

- PDF.

- DOCX.

- TXT.

- PPTX.

- XLSX.

- CSV.



Após o envio, deverá ser possível:



- Solicitar resumos.

- Fazer perguntas específicas.

- Pedir explicações de trechos.

- Comparar documentos.

- Identificar conceitos importantes.

- Criar materiais de estudo.

- Gerar questionários baseados nos documentos.

- Utilizar os arquivos como referência durante a conversa.



Os documentos deverão possuir identificação própria e associação ao usuário e à conversa correspondente.



A experiência deve ser fluida, sem exigir que o usuário inicie uma nova conversa para cada arquivo.



## 7. Geração de questionários e avaliações



A ClaudIA deverá funcionar como ferramenta de avaliação e fixação de conhecimento.



Recursos:

- Múltipla escolha.

- Questões dissertativas.

- Verdadeiro ou falso.

- Diferentes níveis de dificuldade.

- Quantidade personalizada de questões.

- Simulados.

- Correção automática.

- Explicação das respostas.

- Feedback sobre desempenho.

- Identificação de assuntos que precisam ser revisados.



As questões deverão ser fundamentadas no material de referência quando o usuário solicitar avaliações baseadas em documentos específicos.



## 8. Interface gráfica e experiência do usuário



Desenvolver uma interface própria utilizando Flask, HTML, CSS e JavaScript.



### Identidade visual

- Design moderno, limpo e acolhedor.

- Paleta de cores suaves e harmoniosas.

- Tipografia confortável para leitura.

- Animações discretas.

- Elementos visuais organizados.

- Layout responsivo.

- Identidade visual consistente com a personalidade da ClaudIA.



### Funcionalidades da interface

- Área principal de conversação.

- Campo de mensagem intuitivo.

- Upload de arquivos acessível durante a conversa.

- Identificação dos arquivos anexados.

- Histórico de conversas.

- Gerenciamento de documentos.

- Indicadores de processamento.

- Apresentação organizada de questionários.

- Exibição de fontes e referências.

- Área de configurações do usuário.



A interface deve transmitir conforto, organização e confiança, fazendo com que o usuário tenha vontade de permanecer estudando na plataforma.



## 9. Banco de dados e gerenciamento de informações



Estruturar as entidades necessárias para o funcionamento da aplicação.



Entidades iniciais sugeridas:

- Users.

- Conversations.

- Messages.

- Documents.

- DocumentChunks.

- Quiz.

- QuizQuestions.

- QuizAnswers.

- QuizResults.



As informações deverão possuir relacionamentos adequados, permitindo recuperar o histórico de interações e os materiais associados a cada usuário.



O sistema deverá respeitar o isolamento dos dados, impedindo que um usuário consulte documentos ou conversas pertencentes a outro.



## 10. Segurança e confiabilidade



Implementar:

- Gerenciamento seguro de credenciais.

- Variáveis de ambiente para chaves e endpoints.

- Validação de arquivos enviados.

- Limites de tamanho e formatos permitidos.

- Proteção contra acessos não autorizados.

- Isolamento de documentos por usuário.

- Tratamento de erros nas integrações.

- Logs sem exposição de informações sensíveis.

- Proteção contra prompt injection proveniente de documentos.

- Verificação de permissões antes de consultar ou excluir recursos.



Os documentos enviados deverão ser tratados como fontes de informação, nunca como instruções capazes de substituir as regras internas dos agentes.



## 11. Organização e arquitetura do código



O projeto deverá seguir uma estrutura modular, evitando concentrar toda a aplicação em um único arquivo Python.



Estrutura inicial sugerida:



```text

ClaudIA/

│

├── app/

│   ├── __init__.py

│   ├── config.py

│   │

│   ├── routes/

│   │   ├── auth.py

│   │   ├── chat.py

│   │   ├── documents.py

│   │   └── quizzes.py

│   │

│   ├── agents/

│   │   ├── supervisor.py

│   │   ├── professor.py

│   │   ├── rag_agent.py

│   │   ├── document_agent.py

│   │   └── evaluator.py

│   │

│   ├── rag/

│   │   ├── ingestion.py

│   │   ├── chunking.py

│   │   ├── embeddings.py

│   │   ├── vector_store.py

│   │   └── retrieval.py

│   │

│   ├── services/

│   │   ├── ai_service.py

│   │   ├── document_service.py

│   │   └── quiz_service.py

│   │

│   ├── models/

│   │   ├── user.py

│   │   ├── conversation.py

│   │   ├── document.py

│   │   └── quiz.py

│   │

│   ├── templates/

│   │   ├── base.html

│   │   ├── index.html

│   │   ├── chat.html

│   │   └── login.html

│   │

│   └── static/

│       ├── css/

│       │   └── style.css

│       ├── js/

│       │   └── app.js

│       └── assets/

│

├── tests/

├── uploads/

├── .env.example

├── .gitignore

├── requirements.txt

├── config.py

├── run.py

└── README.md

```



A estrutura poderá ser adaptada conforme as necessidades reais da implementação, mas deverá preservar a separação de responsabilidades.



## 12. Orientações obrigatórias para criação dos códigos



A IA responsável pelo desenvolvimento deverá seguir rigorosamente estas diretrizes:



### 12.1. Desenvolvimento incremental



- Desenvolver o projeto em etapas funcionais.

- Não tentar implementar toda a aplicação de uma só vez.

- Priorizar primeiro a estrutura e a inicialização do projeto.

- Implementar e validar cada módulo antes de avançar.

- Evitar alterações desnecessárias em módulos já funcionais.

- Manter compatibilidade entre todos os componentes.



### 12.2. Qualidade do código



- Utilizar nomes de variáveis, funções e classes claros.

- Priorizar funções pequenas e reutilizáveis.

- Utilizar programação orientada a objetos quando fizer sentido.

- Aplicar type hints sempre que possível.

- Documentar funções e classes importantes.

- Evitar duplicação de código.

- Implementar tratamento adequado de exceções.

- Não concentrar lógica de negócio nas rotas Flask.

- Manter as responsabilidades dos agentes separadas.



### 12.3. Entrega dos arquivos



Sempre que implementar ou modificar um módulo:



- Informar o caminho exato do arquivo.

- Fornecer o conteúdo completo do arquivo, não apenas fragmentos isolados.

- Informar quais dependências precisam ser instaladas.

- Explicar como executar e testar a implementação.

- Identificar quais outros arquivos precisam ser criados ou modificados.

- Garantir que imports, nomes e interfaces estejam compatíveis com os demais módulos.



Não utilizar pseudocódigo quando a solicitação for a implementação de código funcional.



Não utilizar funções fictícias, endpoints inexistentes ou integrações inventadas.



### 12.4. Configuração e dependências



- Centralizar configurações em arquivos apropriados.

- Utilizar `.env` para credenciais e parâmetros sensíveis.

- Fornecer `.env.example` com todas as variáveis necessárias.

- Nunca inserir chaves diretamente no código.

- Manter `requirements.txt` atualizado.

- Fixar versões compatíveis das dependências.

- Verificar a compatibilidade dos SDKs e APIs utilizados com a documentação oficial atual.



### 12.5. Integração com Azure AI Foundry



- Não presumir que deployments já existem.

- Não inventar nomes de modelos ou endpoints.

- Diferenciar endpoint do recurso, deployment de LLM e deployment de embeddings.

- Explicitar quais recursos precisam ser criados e configurados no Azure.

- Implementar validação das variáveis de ambiente.

- Fornecer mensagens de erro claras para falhas de autenticação, deployment inexistente e indisponibilidade de serviços.

- Não misturar SDKs incompatíveis ou versões diferentes de APIs sem justificativa.

- Manter as integrações desacopladas para facilitar substituições futuras.



### 12.6. Testes e validação



Cada módulo deverá ser validado antes de ser considerado concluído.



Implementar:

- Testes unitários.

- Testes de integração.

- Validação de endpoints.

- Testes do pipeline de ingestão.

- Testes de recuperação vetorial.

- Testes de comunicação com os agentes.

- Testes de isolamento entre usuários.



Não afirmar que um código foi testado se sua execução não foi realizada.



Quando houver erros, analisar a causa e corrigir a implementação, em vez de adicionar soluções improvisadas.



### 12.7. Documentação



Manter um README.md atualizado contendo:

- Descrição do projeto.

- Arquitetura geral.

- Requisitos de instalação.

- Configuração do ambiente.

- Criação dos recursos no Azure.

- Configuração dos deployments.

- Configuração do banco vetorial.

- Como executar localmente.

- Como executar os testes.

- Principais funcionalidades.

- Estrutura de diretórios.



## 13. Estratégia de implementação



O desenvolvimento deverá ser dividido em fases:



**Fase 1 — Fundação**

- Estrutura do projeto.

- Configuração do Flask.

- Interface inicial.

- Banco de dados.

- Configuração de variáveis de ambiente.

- Integração inicial com Azure AI Foundry.



**Fase 2 — Chat inteligente**

- Implementação do agente ClaudIA.

- Histórico de conversas.

- Personalidade e instruções pedagógicas.

- Comunicação frontend/backend.



**Fase 3 — RAG multivetorial**

- Configuração do Azure AI Search.

- Deployment de embeddings.

- Pipeline de ingestão.

- Chunking e indexação.

- Recuperação vetorial e híbrida.

- Respostas fundamentadas em fontes.



**Fase 4 — Upload e análise documental**

- Upload de arquivos.

- Extração de conteúdo.

- Indexação dos documentos.

- Consultas contextualizadas.

- Gerenciamento dos materiais.



**Fase 5 — Arquitetura multiagente**

- Agente supervisor.

- Agentes especializados.

- Orquestração de tarefas.

- Integração com o RAG.

- Tratamento de falhas e resultados.



**Fase 6 — Avaliações**

- Criação de questionários.

- Correção automática.

- Feedback pedagógico.

- Histórico de resultados.



**Fase 7 — Refinamento e produção**

- Melhorias visuais.

- Segurança.

- Otimização.

- Testes gerais.

- Documentação.

- Preparação para deploy.



## 14. Objetivo final



Entregar uma plataforma funcional de aprendizagem baseada em IA, na qual a ClaudIA seja capaz de:



1. Conversar naturalmente com o usuário.

2. Ensinar assuntos de diferentes níveis de complexidade.

3. Consultar múltiplas bases de conhecimento.

4. Analisar documentos enviados durante a conversa.

5. Responder perguntas fundamentadas nesses documentos.

6. Criar questionários e simulados personalizados.

7. Corrigir avaliações e fornecer feedback pedagógico.

8. Manter histórico e contexto das interações.

9. Oferecer uma experiência visual própria, agradável e intuitiva.



**Princípio central:** a ClaudIA não deve ser apenas uma IA que responde perguntas, mas uma professora virtual que utiliza inteligência artificial, recuperação de conhecimento e estratégias pedagógicas para tornar o processo de aprendizagem mais acessível, organizado e eficiente.



**Instrução final para a IA desenvolvedora:** atue como arquiteto de software e engenheiro de IA sênior durante todo o desenvolvimento. Priorize soluções funcionais, modulares, documentadas e tecnicamente justificadas. Antes de implementar cada fase, apresente brevemente sua proposta técnica, identifique as dependências necessárias e explique como ela se integra à arquitetura existente. Em seguida, implemente os arquivos completos e forneça os procedimentos de execução e validação. Não avance silenciosamente sobre erros ou dependências pendentes.