/**
 * @fileoverview This script handles the client-side logic for initiating research,
 *               managing WebSocket connections, and updating the UI based on server responses.
 *               It includes functions for input validation, WebSocket communication,
 *               and user interaction with the generated report.
 */

let ws;
let currentMarkdownContent = '';

/**
 * Validates the user inputs for company name and URL.
 * @returns {boolean} True if inputs are valid, otherwise false.
 */
function validateInputs() {
    const companyName = document.getElementById("companyName").value.trim();
    const companyUrl = document.getElementById("companyUrl").value.trim();
    
    if (!companyName) {
        alert("Please enter a company name");
        return false;
    }
    
    if (!companyUrl) {
        alert("Please enter a company URL");
        return false;
    }
    
    // Basic URL validation
    try {
        new URL(companyUrl);
    } catch (error) {
        alert("Please enter a valid URL (including http:// or https://)");
        return false;
    }
    
    return true;
}

/**
 * Initiates the research process by validating inputs, clearing previous results,
 * and establishing a WebSocket connection to the server.
 */
function startResearch() {
    if (!validateInputs()) {
        return;
    }
    
    const progressDiv = document.getElementById("progress");
    const clusterSelectionDiv = document.getElementById("cluster-selection");
    const reportDiv = document.getElementById("report");
    const copyButton = document.getElementById("copyButton");
    
    // Clear previous content
    progressDiv.innerHTML = "";
    reportDiv.innerHTML = "";
    clusterSelectionDiv.style.display = "none";
    copyButton.style.display = "none";
    currentMarkdownContent = '';
    
    // Open WebSocket connection
    ws = new WebSocket("ws://127.0.0.1:5000/ws");
    
    ws.onmessage = function(event) {
        const message = event.data;
        if (message.includes("Please review the options and select the correct cluster")) {
            clusterSelectionDiv.style.display = "block";
        }
        // Handle final report differently
        if (message.startsWith("Report generated successfully!")) {
            currentMarkdownContent = message.replace("Report generated successfully!", "").trim();
            // Render Markdown content
            reportDiv.innerHTML = marked.parse(currentMarkdownContent);
            // Show copy button
            copyButton.style.display = "block";
            // Add progress message
            // const messageElement = document.createElement("div");
            // messageElement.className = "progress-message";
            // messageElement.textContent = "Report generated successfully!";
            // progressDiv.appendChild(messageElement);
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
    
    ws.onopen = function() {
        const companyName = document.getElementById("companyName").value;
        const companyUrl = document.getElementById("companyUrl").value;
        const outputFormat = document.getElementById("outputFormat").value;
        const payload = { companyName, companyUrl, outputFormat };
        console.log("Sending WebSocket payload:", payload);
        ws.send(JSON.stringify(payload));
    };
    
    ws.onerror = function(error) {
        const messageElement = document.createElement("div");
        messageElement.className = "progress-message";
        messageElement.textContent = "Error: " + error.message;
        messageElement.style.borderLeftColor = "#FE363B"; // Red border for errors
        progressDiv.appendChild(messageElement);
        progressDiv.scrollTop = progressDiv.scrollHeight;
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