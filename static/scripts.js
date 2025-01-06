function sendSuggestion(element) {
    const suggestionText = element.textContent;
    sendMessage(suggestionText);
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById("messages");
    const typingElement = document.createElement("div");
    typingElement.classList.add("message", "bot-message", "typing-indicator");
    typingElement.id = "typingIndicator";
    typingElement.innerHTML = '<span></span><span></span><span></span>';
    messagesContainer.appendChild(typingElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const typingElement = document.getElementById("typingIndicator");
    if (typingElement) {
        typingElement.remove();
    }
}

document.getElementById("userInput").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

async function sendMessage(message = null) {
    const userInput = document.getElementById("userInput");
    const userMessage = message || userInput.value.trim();
    const messagesContainer = document.getElementById("messages");

    if (userMessage === "") return;

    const userMessageElement = document.createElement("div");
    userMessageElement.classList.add("message", "user-message");
    userMessageElement.textContent = userMessage;
    messagesContainer.appendChild(userMessageElement);

    if (!message) {
        userInput.value = "";
    }

    showTypingIndicator();

    try {
        const response = await fetch("/api/chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: userMessage })
        });

        const data = await response.json();
        removeTypingIndicator();

        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("message", "bot-message");

        // Usando a biblioteca Marked.js para converter o Markdown para HTML
        botMessageElement.innerHTML = marked.parse(data.answer);

        // Cria os botões de feedback
        const feedbackContainer = document.createElement("div");
        feedbackContainer.classList.add("feedback-container");

        const likeButton = document.createElement("i");
        likeButton.classList.add("fas", "fa-thumbs-up", "feedback-btn");
        likeButton.onclick = () => handleFeedback(likeButton, "Obrigado pelo feedback positivo!", "like");

        const dislikeButton = document.createElement("i");
        dislikeButton.classList.add("fas", "fa-thumbs-down", "feedback-btn");
        dislikeButton.onclick = () => handleFeedback(dislikeButton, "Agradecemos o feedback!", "dislike");

        feedbackContainer.appendChild(likeButton);
        feedbackContainer.appendChild(dislikeButton);

        messagesContainer.appendChild(botMessageElement);
        botMessageElement.after(feedbackContainer);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

    } catch (error) {
        console.error("Erro ao enviar a mensagem:", error);
        removeTypingIndicator();
    }
}

function handleFeedback(button, message, type) {
    // Obtém o container de feedback que é o elemento pai do botão clicado
    const feedbackContainer = button.closest('.feedback-container');

    // Remove a classe de feedback de todos os botões no container específico
    const feedbackButtons = feedbackContainer.querySelectorAll('.feedback-btn');
    feedbackButtons.forEach(btn => {
        btn.classList.remove('selected-like', 'selected-dislike');
    });

    // Adiciona a classe apropriada ao botão de feedback clicado
    const isLike = type === "like";
    const feedbackClass = isLike ? "selected-like" : "selected-dislike";
    button.classList.add(feedbackClass);

    // Exibe o toast de feedback
    showFeedbackToast(isLike ? "Obrigado pelo feedback positivo!" : "Agradecemos o feedback! Não hesite em nos informar como podemos melhorar!");
}

function showFeedbackToast(message) {
    const toastBody = document.querySelector('.toast-body');
    toastBody.textContent = message;
    
    const toastElement = new bootstrap.Toast(document.getElementById('feedbackToast'));
    toastElement.show();
}

document.getElementById('compareForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();

    document1 = document.getElementById('document_1').files[0];
    document2 = document.getElementById('document_2').files[0];

    formData.append('document_1', document1);
    formData.append('document_2', document2);

    const messagesContainer = document.getElementById('messages');
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user-message');
    userMessageElement.textContent = `Comparar documentos ${document1.name} e ${document2.name}`;
    messagesContainer.appendChild(userMessageElement);


    const modalElement = document.getElementById('compareModal');
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();

    showTypingIndicator();

    try {
        const response = await fetch('/api/compare_documents', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        removeTypingIndicator();

        // Exibir resposta do bot
        const messagesContainer = document.getElementById('messages');
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');

        // Exibir resposta da comparação
        if (data.comparison) {
            botMessageElement.innerHTML = marked.parse(data.comparison);
        } else {
            botMessageElement.textContent = "Ocorreu um erro. Tente novamente.";
        }

        // Criação de botões de feedback
        const feedbackContainer = document.createElement("div");
        feedbackContainer.classList.add("feedback-container");

        const likeButton = document.createElement("i");
        likeButton.classList.add("fas", "fa-thumbs-up", "feedback-btn");
        likeButton.onclick = () => handleFeedback(likeButton, "Obrigado pelo feedback positivo!", "like");

        const dislikeButton = document.createElement("i");
        dislikeButton.classList.add("fas", "fa-thumbs-down", "feedback-btn");
        dislikeButton.onclick = () => handleFeedback(dislikeButton, "Agradecemos o feedback!", "dislike");

        feedbackContainer.appendChild(likeButton);
        feedbackContainer.appendChild(dislikeButton);

        messagesContainer.appendChild(botMessageElement);
        botMessageElement.after(feedbackContainer);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } catch (error) {
        removeTypingIndicator();
        // Adiciona mensagem de erro ao chat
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');
        botMessageElement.textContent = 'Ocorreu um erro. Tente novamente.';
        messagesContainer.appendChild(botMessageElement);
        console.error('Erro ao comparar documentos:', error);
    }
});

document.getElementById('analysisForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();

    doc = document.getElementById('document').files[0];

    formData.append('document', doc);

    const messagesContainer = document.getElementById('messages');
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user-message');
    userMessageElement.textContent = `Analisar documento ${doc.name}`;
    messagesContainer.appendChild(userMessageElement);


    const modalElement = document.getElementById('analysisModal');
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();

    showTypingIndicator();

    try {
        const response = await fetch('/api/analyse_document', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        removeTypingIndicator();

        // Exibir resposta do bot
        const messagesContainer = document.getElementById('messages');
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');

        // Exibir resposta da análise
        if (data.analysis) {
            botMessageElement.innerHTML = marked.parse(data.analysis);
        } else {
            botMessageElement.textContent = "Ocorreu um erro. Tente novamente.";
        }

        // Criação de botões de feedback
        const feedbackContainer = document.createElement("div");
        feedbackContainer.classList.add("feedback-container");

        const likeButton = document.createElement("i");
        likeButton.classList.add("fas", "fa-thumbs-up", "feedback-btn");
        likeButton.onclick = () => handleFeedback(likeButton, "Obrigado pelo feedback positivo!", "like");

        const dislikeButton = document.createElement("i");
        dislikeButton.classList.add("fas", "fa-thumbs-down", "feedback-btn");
        dislikeButton.onclick = () => handleFeedback(dislikeButton, "Agradecemos o feedback!", "dislike");

        feedbackContainer.appendChild(likeButton);
        feedbackContainer.appendChild(dislikeButton);

        messagesContainer.appendChild(botMessageElement);
        botMessageElement.after(feedbackContainer);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } catch (error) {
        removeTypingIndicator();
        // Adiciona mensagem de erro ao chat
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'bot-message');
        botMessageElement.textContent = 'Ocorreu um erro. Tente novamente.';
        messagesContainer.appendChild(botMessageElement);
        console.error('Erro ao analisar documentos:', error);
    }
});
