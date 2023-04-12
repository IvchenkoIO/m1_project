var OPENAI_API_KEY = "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";
document.addEventListener("DOMContentLoaded", function() {
    const conversationItems = document.querySelectorAll("#conversations li");
    const messagesDiv = document.getElementById("messages");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    
    


    // Exemple de données pour les conversations
    const conversations = {
conversation1: [
    { author: "Teacher", content: "What is the square root of 16?" }
],
conversation2: [
    { author: "Teacher", content: "What is the capital of France?" }
],
conversation3: [
    { author: "Teacher", content: "What is the largest mammal on Earth?" }
]
};

   

async function fetchGptResponse(conversation) {
    // Convert the conversation history into a message string
    const messageString = conversation.map((message) => `${message.role}: ${message.content}`).join('\n');

    const response = await fetch("https://api.openai.com/v1/completions", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${OPENAI_API_KEY}`,
        },
        body: JSON.stringify({
            model: "text-davinci-003", // Use the "davinci" model
            prompt: messageString + "\nteacher:", // Add a newline character and "assistant:" to the end of the prompt
            max_tokens: 400, // Set the desired response length
            n: 1,
            stop: ["\nyou:", "\nteacher:"], // Stop generating when the next user or assistant message starts
            temperature: 0.4,
            top_p: 0.7,
        }),
    });

    const data = await response.json();
    return data.choices[0].text.trim();
}



function displayConversation(conversationId) {
    const conversation = conversations[conversationId];

    messagesDiv.innerHTML = "";
    for (let message of conversation) {
        const messageElem = document.createElement("div");
        messageElem.classList.add(message.author.toLowerCase());
        
        messageElem.innerHTML = `<strong>${message.author}</strong>: ${message.content}`;
        messagesDiv.appendChild(messageElem);
    }
}


    // Afficher la première conversation par défaut et la marquer comme sélectionnée
    conversationItems[0].classList.add("selected");
    displayConversation(conversationItems[0].dataset.conversationId);

    conversationItems.forEach(function(item) {
        item.addEventListener("click", function() {
            // Désélectionner l'élément précédemment sélectionné
            document.querySelector("#conversations li.selected").classList.remove("selected");

            // Sélectionner l'élément actuel et afficher la conversation correspondante
            item.classList.add("selected");
            displayConversation(item.dataset.conversationId);
        });
    });

    messageForm.addEventListener("submit", async function (event) {
        event.preventDefault();
    
        const currentConversationId = document.querySelector("#conversations li.selected").dataset.conversationId;
        const newMessage = {
            role: "system",
            content: `You are a teacher who askes a question to a student. Say if the student is right, wrong or partially correct and give him a hint if he is wrong. Do not give him the answer before. After 3 tries, give him the answer.If the student ask for help, give him a hint. If he wants explanation, give him an explanation.`,
       };
    
        conversations[currentConversationId].push(newMessage);
    
        const userMessage = {
            role: "You",
            content: messageInput.value,
        };
    
        conversations[currentConversationId].push(userMessage);
    
        const messageElem = document.createElement("div");
        messageElem.classList.add(userMessage.role.toLowerCase());
        messageElem.innerHTML = `<strong>${userMessage.role}</strong>: ${userMessage.content}`;
        messagesDiv.appendChild(messageElem);
    
        // Get GPT-3.5-turbo response and add it to the conversation
        const gptResponse = await fetchGptResponse(conversations[currentConversationId]);
        const assistantMessage = {
            role: "Teacher",
            content: gptResponse,
        };
    
        conversations[currentConversationId].push(assistantMessage);
    
        const assistantMessageElem = document.createElement("div");
        assistantMessageElem.classList.add(assistantMessage.role.toLowerCase());
        assistantMessageElem.innerHTML = `<strong>${assistantMessage.role}</strong>: ${assistantMessage.content}`;
        messagesDiv.appendChild(assistantMessageElem);
    
        // Reset the message input
        messageInput.value = "";
    });
});