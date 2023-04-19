
var OPENAI_API_KEY = "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";
document.addEventListener("DOMContentLoaded", function() {
    const conversationItems = document.querySelectorAll("#conversations li");
    const messagesDiv = document.getElementById("messages");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    
    


    // Exemple de données pour les conversations

        const conversations = {
conversation1: [
    { role: "Teacher", content: "What is the square root of 16?" }
],
conversation2: [
    { role: "Teacher", content: "Solve : 3x -2 = 0 " }
],
conversation3: [
    { role: "Teacher", content: "Solve : -5x - 5 = 10" }
],
conversation4: [
    { role: "Teacher", content: "Solve : 42x - 72 = 100" }
],
conversation5: [
    { role: "Teacher", content: "What is a database ?" }
],
conversation6: [
    { role: "Teacher", content: "What is the largest mammal on Earth?" }
]
};

async function checkResponse(conversationId, gptResponse) {
    // Check if the response is considered correct
    if (gptResponse.includes("incorrect") || gptResponse.includes("not correct") ||gptResponse.includes("wrong")) {
        const conversationItem = document.querySelector(`#conversations li[data-conversation-id='${conversationId}']`);
        if (conversationItem) {
            conversationItem.style.backgroundColor = "red";
        }
    }
    else if (gptResponse.includes("partially") || gptResponse.includes("Partially") || gptResponse.includes("not quite right")){
        const conversationItem = document.querySelector(`#conversations li[data-conversation-id='${conversationId}']`);
        if (conversationItem) {
            conversationItem.style.backgroundColor = "yellow";
        }
    }
    else if ( gptResponse.includes("CORRECT") ) {   // gptResponse.includes("correct") || gptResponse.includes("Correct") || gptResponse.includes("Right")|| gptResponse.includes("right")
        const conversationItem = document.querySelector(`#conversations li[data-conversation-id='${conversationId}']`);
        if (conversationItem) {
            conversationItem.style.backgroundColor = "green";
        }
    }
}

    

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
            temperature: 0.1,
            top_p: 0.7,
        }),
    });

    const data = await response.json();
    return data.choices[0].text.trim();
}



function displayConversation(conversationId) {
    const conversation = conversations[conversationId];

    if (!conversation) {
        console.error(`Conversation "${conversationId}" not found.`);
        return;
    }

    // Videz les messages précédents uniquement pour la conversation active
    const activeConversation = document.querySelector(`#conversations li[data-conversation-id='${conversationId}']`);
    if (activeConversation) {
        messagesDiv.innerHTML = "";
    }

    for (let message of Object.keys(conversation)) {
        if (message.role !== "system") {
            const messageElem = document.createElement("div");
            messageElem.classList.add(message.role);

            messageElem.innerHTML = `<strong>${message.role}</strong>: ${message.content}`;
            messagesDiv.appendChild(messageElem);
        }
    }
}





    // Afficher la première conversation par défaut et la marquer comme sélectionnée
    conversationItems[0].classList.add("selected");
    displayConversation(conversationItems[0].dataset.conversationId);

    conversationItems.forEach(function(item) {
        item.addEventListener("click", function() {
            // Remove the following lines as we don't want to deselect the previous item or replace the messages.
            // document.querySelector("#conversations li.selected").classList.remove("selected");
            // item.classList.add("selected");
            // Désélectionnez l'élément actif précédent
            document.querySelector("#conversations li.selected").classList.remove("selected");

            // Sélectionner l'élément actuel et afficher la conversation correspondante
            item.classList.add("selected");
            // Call the displayConversation function to add the clicked conversation's content to the current conversation.
            displayConversation(item.dataset.conversationId);
        });
    });

    messageForm.addEventListener("submit", async function (event) {
        event.preventDefault();
    
        const currentConversationId = document.querySelector("#conversations li.selected").dataset.conversationId;
        const newMessage = {
            role: "system",
            content: `
            You are a teacher who asks a question to a student. It is crucial that you DO NOT provide the direct answer to the question under any circumstances. Instead, guide the student towards the answer using only hints, suggestions, or explanations. If he give the right answer, say "YOU ARE CORRECT !" and stop talking.            
            If the answer lacks informations, say "That's partially correct. Try again." and continue the conversation.
            `,
       
        };
    
        conversations[currentConversationId].push(newMessage);
    
        const userMessage = {
            role: "You",
            content: messageInput.value,
        };
    
        conversations[currentConversationId].push(userMessage);
    
        const messageElem = document.createElement("div");
        messageElem.classList.add(userMessage.role);
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
        assistantMessageElem.classList.add(assistantMessage.role);
        assistantMessageElem.innerHTML = `<strong>${assistantMessage.role}</strong>: ${assistantMessage.content}`;
        messagesDiv.appendChild(assistantMessageElem);
        checkResponse(currentConversationId,gptResponse);
        // Reset the message input
        messageInput.value = "";
    });
});