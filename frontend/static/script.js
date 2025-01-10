/**
 * @fileoverview This script handles the client-side logic for initiating travel planning,
 *               managing WebSocket connections, and updating the UI based on server responses.
 *               It includes functions for input validation, WebSocket communication,
 *               and user interaction with the generated itinerary.
 */

let ws;
let currentMarkdownContent = '';

/**
 * Validates the user inputs for destination and travel date.
 * @returns {boolean} True if inputs are valid, otherwise false.
 */
function validateInputs() {
    const destination = document.getElementById("destination").value.trim();
    const travelDate = document.getElementById("travelDate").value.trim();
    
    if (!destination) {
        alert("Please enter a destination");
        return false;
    }
    
    if (!travelDate) {
        alert("Please enter a travel date");
        return false;
    }
    
    return true;
}

/**
 * Initiates the travel planning process by validating inputs, clearing previous results,
 * and establishing a WebSocket connection to the server.
 */
function startPlanning() {
    if (!validateInputs()) {
        return;
    }
    
    const progressDiv = document.getElementById("progress");
    const optionSelectionDiv = document.getElementById("option-selection");
    const itineraryDiv = document.getElementById("itinerary");
    const copyButton = document.getElementById("copyButton");
    
    // Clear previous content
    progressDiv.innerHTML = "";
    itineraryDiv.innerHTML = "";
    optionSelectionDiv.style.display = "none";
    copyButton.style.display = "none";
    currentMarkdownContent = '';
    
    // Open WebSocket connection
    ws = new WebSocket("ws://127.0.0.1:5000/ws");
    
    ws.onmessage = function(event) {
        const message = event.data;
        if (message.includes("Please review the options and select the correct option")) {
            optionSelectionDiv.style.display = "block";
        }
        // Handle final itinerary differently
        if (message.startsWith("Itinerary generated successfully!")) {
            currentMarkdownContent = message.replace("Itinerary generated successfully!", "").trim();
            // Render Markdown content
            itineraryDiv.innerHTML = marked.parse(currentMarkdownContent);
            // Show copy button
            copyButton.style.display = "block";
        } else {
            // Create message element for all other messages
            const messageElement = document.createElement("div");
            messageElement.className = "progress-message";
            messageElement.textContent = message;
            progressDiv.appendChild(messageElement);
        }
        // Ensure automatic scrolling to the latest message
        requestAnimationFrame(() => {
            progressDiv.scrollTop = progressDiv.scrollHeight;
        });
    };
}

/**
 * Sends the selected cluster to the server via WebSocket.
 */
function submitClusterSelection() {
    const clusterSelection = document.getElementById("cluster-input").value;
    if (ws && clusterSelection) {
        ws.send(clusterSelection);
        document.getElementById("cluster-selection").style.display = "none";
        document.getElementById("cluster-input").value = "";
    }
}

/**
 * Copies the generated report content to the clipboard.
 * Displays a temporary confirmation message upon success.
 */
async function copyReport() {
    if (currentMarkdownContent) {
        try {
            await navigator.clipboard.writeText(currentMarkdownContent);
            const copyButton = document.getElementById("copyButton");
            const originalText = copyButton.textContent;
            copyButton.textContent = "Copied!";
            setTimeout(() => {
                copyButton.textContent = originalText;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    }
}