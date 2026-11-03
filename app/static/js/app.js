document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const messageText = messageInput.value.trim();
            if (!messageText) return;

            // Limpa o input
            messageInput.value = '';

            // Remove o estado vazio se presente
            const emptyState = document.getElementById('emptyState');
            if (emptyState) {
                emptyState.remove();
            }

            // Adiciona a mensagem do usuário imediatamente na interface
            appendMessage(messageText, 'user', 'Agora mesmo');
            
            // Mostra o indicador de digitação da ClaudIA
            showTyping(true);

            const conversationId = chatForm.dataset.conversationId;

            try {
                const response = await fetch(`/conversation/${conversationId}/send`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: messageText })
                });

                const data = await response.json();
                
                // Esconde o indicador de digitação
                showTyping(false);

                if (data.status === 'success') {
                    // Adiciona a resposta da ClaudIA
                    appendMessage(data.assistant_message.content, 'assistant', data.assistant_message.created_at);
                    
                    // Atualiza o título na barra lateral se mudou
                    const activeConvLink = document.querySelector(`.conv-item[href*="/conversation/${conversationId}"]`);
                    if (activeConvLink && data.conversation_title) {
                        activeConvLink.textContent = data.conversation_title;
                    }
                } else {
                    appendMessage('Desculpe, ocorreu um erro ao processar sua mensagem.', 'assistant', 'Agora');
                }
            } catch (err) {
                showTyping(false);
                appendMessage('Erro de conexão com o servidor. Verifique sua rede.', 'assistant', 'Agora');
                console.error(err);
            }
        });
    }

    function appendMessage(text, sender, timeStr) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        // Formatação básica de quebras de linha
        bubbleDiv.innerHTML = escapeHtml(text).replace(/\n/g, '<br>');

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = timeStr;

        messageDiv.appendChild(bubbleDiv);
        messageDiv.appendChild(timeDiv);

        // Insere antes do indicador de digitação se ele existir
        if (typingIndicator) {
            chatMessages.insertBefore(messageDiv, typingIndicator);
        } else {
            chatMessages.appendChild(messageDiv);
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping(show) {
        if (!typingIndicator) return;
        typingIndicator.style.display = show ? 'flex' : 'none';
        if (show) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function escapeHtml(string) {
        return String(string)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }
});