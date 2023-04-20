
const hamburgerIcon = document.querySelector('.hamburger-icon');
const closeIcon = document.querySelector('.close-icon');
const menuList = document.querySelector('.menu-list');

hamburgerIcon.addEventListener('click', function() {
hamburgerIcon.style.display = 'none';
closeIcon.style.display = 'block';
menuList.style.display = 'block';
});

closeIcon.addEventListener('click', function() {
hamburgerIcon.style.display = 'block';
closeIcon.style.display = 'none';
menuList.style.display = 'none';
});

var OPENAI_API_KEY = "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";
document.addEventListener("DOMContentLoaded", function() {
    const conversationItems = document.querySelectorAll("#conversations li");
    const messagesDiv = document.getElementById("messages");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");

    
    


    // Exemple de données pour les conversations

        const conversations = {
conversation1: [
    { role: "Teacher", content: "2+2" }
],
conversation2: [
    { role: "Teacher", content: "4+4" }
],
conversation3: [
    { role: "Teacher", content: "2*2*3" }
],
conversation4: [
    { role: "Teacher", content: "What is IP" }
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
    else if ( gptResponse.includes("correct") ) {   // gptResponse.includes("correct") || gptResponse.includes("Correct") || gptResponse.includes("Right")|| gptResponse.includes("right")
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

    messagesDiv.innerHTML = "";
    for (let message of conversation) {
        if (message.role !== "system") { // Add this condition
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
            content: `You are a teacher who askes a question to a student. Say if the student is right, wrong or partially correct and give him a hint if he is wrong. Do not give him the answer before. After 3 tries, give him the answer.If the student ask for help, give him a hint. If he wants explanation, give him an explanation. `,
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