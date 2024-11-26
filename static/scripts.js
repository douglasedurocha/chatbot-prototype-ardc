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

    if (userMessage == "Elabore uma análise detalhada em formato de gráficos sobre o transporte coletivo de Goiânia nos últimos dois trimestres, considerando todos os principais padrões de análise de custos.") {
        await new Promise(resolve => setTimeout(resolve, 1800));

        removeTypingIndicator();
    
        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("message", "bot-message");
        botMessageElement.innerHTML = `<img src="${graficoImageUrl}" alt="Gráfico" style="max-width: 100%;">`;
    
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
        return;
    }

    if (userMessage.toLowerCase().substring(0, 10) === "quantas li") {
        await new Promise(resolve => setTimeout(resolve, 1800));

        removeTypingIndicator();

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

        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("message", "bot-message");
        botMessageElement.innerHTML = "Atualmente, <b>50 licitações estão em situação de risco</b>, sendo que o principal critério que leva a essa classificação é a presença de anomalias no orçamento."

        messagesContainer.appendChild(botMessageElement);
        botMessageElement.after(feedbackContainer);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        return;
    }

    if (userMessage.toLowerCase().substring(0, 9) === "me ensine") {
        await new Promise(resolve => setTimeout(resolve, 1800));

        removeTypingIndicator();

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

        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("message", "bot-message");
        botMessageElement.innerHTML = "<p>Claro! Posso guiar o seu acesso pela web até encontrar o site do ComprasNet, vamos lá?</p>";

        const guideButton = document.createElement("button");
        guideButton.classList.add("guide-btn");
        guideButton.textContent = "Começar Acesso Guiado";
        botMessageElement.appendChild(guideButton);
        guideButton.onclick = () => {
            fetch("http://localhost:5000/api/guideaccess")
                .then(response => response.json())
                .catch(error => {
                    console.error("Erro ao iniciar o acesso guiado:", error);
                });
        }

        messagesContainer.appendChild(botMessageElement);
        botMessageElement.after(feedbackContainer);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        return;
    }

    try {
        const response = await fetch("http://localhost:5000/api/chatbot", {
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
        botMessageElement.textContent = data.result;

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
