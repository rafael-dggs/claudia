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
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    const bubbleDiv = document.createElement("div");
    bubbleDiv.className = "message-bubble";

    // Proteção contra XSS e formatação básica de markdown/quebras de linha
    bubbleDiv.innerHTML = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/\n/g, "<br>");

    const timeDiv = document.createElement("div");
    timeDiv.className = "message-time";
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
