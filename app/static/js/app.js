document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chatForm");
  const messageInput = document.getElementById("messageInput");
  const chatMessages = document.getElementById("chatMessages");
  const typingIndicator = document.getElementById("typingIndicator");

  // Elementos de Upload (Fase 4)
  const fileInput = document.getElementById("fileInput");
  const attachBtn = document.getElementById("attachBtn");

  // Rola o chat para baixo ao carregar
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // LÓGICA DE UPLOAD DE ARQUIVOS (Fase 4)
  if (attachBtn && fileInput) {
    attachBtn.addEventListener("click", () => {
      fileInput.click();
    });

    fileInput.addEventListener("change", async () => {
      const file = fileInput.files[0];
      if (!file) return;

      const conversationId = chatForm.dataset.conversationId;
      const formData = new FormData();
      formData.append("file", file);
      formData.append("conversation_id", conversationId);

      // Adiciona mensagem visual de carregamento
      appendMessage(`Enviando arquivo: ${file.name}...`, "user", "Agora");
      showTyping(true);

      try {
        const response = await fetch("/docs/upload", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        showTyping(false);
        fileInput.value = ""; // Limpa o input

        if (data.status === "success") {
          appendMessage(
            data.assistant_message.content,
            "assistant",
            data.assistant_message.created_at,
          );
        } else {
          appendMessage(
            `Erro ao processar: ${data.error}`,
            "assistant",
            "Agora",
          );
        }
      } catch (err) {
        showTyping(false);
        fileInput.value = "";
        appendMessage(
          "Erro na conexão ao enviar o arquivo.",
          "assistant",
          "Agora",
        );
        console.error(err);
      }
    });
  }

  // LÓGICA DE ENVIO DE MENSAGENS (Fase 2)
  if (chatForm) {
    chatForm.addEventListener("submit", async (e) => {
      e.preventDefault(); // IMPEDE A PÁGINA DE RECARREGAR

      const messageText = messageInput.value.trim();
      if (!messageText) return;

      // Limpa o input e estado inicial
      messageInput.value = "";
      const emptyState = document.getElementById("emptyState");
      if (emptyState) emptyState.remove();

      // Mostra a mensagem do usuário e o indicador de digitação
      appendMessage(messageText, "user", "Agora");
      showTyping(true);

      const conversationId = chatForm.dataset.conversationId;

      try {
        const response = await fetch(`/conversation/${conversationId}/send`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: messageText }),
        });

        const data = await response.json();
        showTyping(false);

        if (data.status === "success") {
          appendMessage(
            data.assistant_message.content,
            "assistant",
            data.assistant_message.created_at,
          );

          // Atualiza título da conversa na sidebar
          const activeConvLink = document.querySelector(
            `.conv-item[href*="/conversation/${conversationId}"]`,
          );
          if (activeConvLink && data.conversation_title) {
            activeConvLink.textContent = data.conversation_title;
          }
        } else {
          appendMessage(
            "Desculpe, ocorreu um erro ao processar sua mensagem.",
            "assistant",
            "Agora",
          );
        }
      } catch (err) {
        showTyping(false);
        appendMessage("Erro de conexão com o servidor.", "assistant", "Agora");
        console.error(err);
      }
    });
  }

  // FUNÇÕES AUXILIARES
  function appendMessage(text, sender, timeStr) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    
    let safeText = (text !== null && text !== undefined && text.trim() !== '') 
        ? String(text) 
        : "⚠️ Ocorreu um erro: a resposta chegou vazia ao ecrã.";

    // RENDERIZAÇÃO PROFISSIONAL DE MARKDOWN (Fase 7)
    if (sender === 'assistant') {
        // Processa botões de Quiz personalizados antes do Markdown
        let processedText = safeText.replace(/\[QUIZ:(\d+)\]/g, '<br><button class="btn-quiz-start" onclick="openQuiz($1)">📝 Iniciar Questionário</button><br>');
        
        // Converte Markdown para HTML
        let rawHtml = marked.parse(processedText);
        
        // Limpa o HTML contra ataques XSS garantindo segurança em produção
        bubbleDiv.innerHTML = DOMPurify.sanitize(rawHtml, { ADD_ATTR: ['onclick'] });
    } else {
        // Mensagens do usuário são renderizadas como texto simples por segurança
        bubbleDiv.textContent = safeText;
    }

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = timeStr;

    messageDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(timeDiv);

    if (typingIndicator) {
        chatMessages.insertBefore(messageDiv, typingIndicator);
    } else {
        chatMessages.appendChild(messageDiv);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}  
function showTyping(show) {
    if (!typingIndicator) return;
    typingIndicator.style.display = show ? "flex" : "none";
    if (show) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }
});

// --- LÓGICA DE AVALIAÇÃO (FASE 6) ---
let currentQuizId = null;

async function openQuiz(quizId) {
    currentQuizId = quizId;
    document.getElementById('quizOverlay').style.display = 'flex';
    document.getElementById('quizTitle').innerText = 'Carregando Avaliação...';
    document.getElementById('quizFormContainer').innerHTML = '';
    document.getElementById('submitQuizBtn').style.display = 'none';

    try {
        const response = await fetch(`/api/quizzes/${quizId}`);
        const quizData = await response.json();
        
        document.getElementById('quizTitle').innerText = quizData.topic;
        
        let html = '';
        quizData.questions.forEach((q, index) => {
            html += `<div class="quiz-question" id="q-${q.id}">
                <p>${index + 1}. ${q.text}</p>`;
            for (const [letter, text] of Object.entries(q.options)) {
                html += `<label class="quiz-option">
                    <input type="radio" name="${q.id}" value="${letter}"> <strong>${letter})</strong> ${text}
                </label>`;
            }
            html += `<div class="quiz-feedback-box" id="feedback-${q.id}"></div></div>`;
        });
        
        document.getElementById('quizFormContainer').innerHTML = html;
        document.getElementById('submitQuizBtn').style.display = 'block';
        document.getElementById('submitQuizBtn').onclick = submitQuiz;
    } catch (e) {
        document.getElementById('quizFormContainer').innerHTML = '<p>Erro ao carregar o questionário.</p>';
    }
}

function closeQuizModal() {
    document.getElementById('quizOverlay').style.display = 'none';
}

async function submitQuiz() {
    document.getElementById('submitQuizBtn').innerText = 'Corrigindo...';
    document.getElementById('submitQuizBtn').disabled = true;

    // Coleta as respostas
    const answers = {};
    const questionDivs = document.querySelectorAll('.quiz-question');
    questionDivs.forEach(div => {
        const qId = div.id.replace('q-', '');
        const selected = div.querySelector(`input[name="${qId}"]:checked`);
        if (selected) answers[qId] = selected.value;
    });

    try {
        const response = await fetch(`/api/quizzes/${currentQuizId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers })
        });
        const result = await response.json();
        
        // Exibe o feedback
        result.feedback.forEach(item => {
            const feedbackBox = document.getElementById(`feedback-${item.question.id || Object.keys(answers).find(key => answers[key] === item.user_answer) || Math.random()}`); 
            // Maneira robusta: vamos procurar o ID baseado na resposta do servidor
            // Atualizando o array p/ buscar o input pelo name:
            const qDivs = Array.from(document.querySelectorAll('.quiz-question')).find(el => el.innerHTML.includes(item.question));
            if(qDivs) {
                const fbBox = qDivs.querySelector('.quiz-feedback-box');
                fbBox.style.display = 'block';
                if (item.is_correct) {
                    fbBox.className = 'quiz-feedback-box quiz-correct';
                    fbBox.innerHTML = `✅ <strong>Correto!</strong> ${item.explanation}`;
                } else {
                    fbBox.className = 'quiz-feedback-box quiz-incorrect';
                    fbBox.innerHTML = `❌ <strong>Incorreto.</strong> Você marcou ${item.user_answer || 'nada'}, mas a correta era <strong>${item.correct_answer}</strong>. <br> ${item.explanation}`;
                }
            }
        });

        document.getElementById('quizTitle').innerText = `Resultado: ${result.score}% de acertos! (${result.correct_count}/${result.total})`;
        document.getElementById('submitQuizBtn').style.display = 'none';
        
    } catch (e) {
        alert('Erro ao submeter a prova.');
    } finally {
        document.getElementById('submitQuizBtn').innerText = 'Entregar Prova';
        document.getElementById('submitQuizBtn').disabled = false;
    }
}
// --- LÓGICA DE EXCLUSÃO DE CONVERSA ---
async function deleteChat(conversationId) {
    if (!confirm("Tem certeza que deseja excluir esta conversa permanentemente?")) {
        return;
    }

    try {
        const response = await fetch(`/conversation/${conversationId}/delete`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Recarrega a página principal para atualizar a lista
            window.location.href = '/';
        } else {
            alert('Erro ao excluir: ' + (data.error || 'Desconhecido'));
        }
    } catch (e) {
        console.error(e);
        alert('Erro de conexão ao tentar excluir a conversa.');
    }
}