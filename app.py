"""
app.py

This module initializes and runs a FastAPI application that serves both HTTP and WebSocket endpoints.
- The HTTP endpoint renders an HTML template using Jinja2.
- The WebSocket endpoint handles real-time communication for processing graph data related to travel planning.

Dependencies:
- FastAPI for web framework
- Uvicorn for ASGI server
- Jinja2 for templating
- dotenv for environment variable management
- A custom Graph class for processing

Usage:
- Run this script to start the server.
- Access the HTTP endpoint at the root URL to view the index page.
- Connect to the WebSocket endpoint at /ws for real-time travel planning.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from backend.graph import Graph  # Adjust this import if necessary 

from dotenv import load_dotenv
load_dotenv('.env')  # Load environment variables from a .env file

# Initialize the FastAPI app
app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):  # Add the type hint here
    # Render the index.html template with the request context
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    try:
        # Receive initial data from the WebSocket client
        data = await websocket.receive_json()
        destination = data.get("destination")
        travel_dates = data.get("travelDate")
        output_format = data.get("outputFormat", "pdf")
        
        # Initialize the Graph with destination, travel dates, and output format
        graph = Graph(destination=destination, travel_dates=travel_dates, output_format=output_format, websocket=websocket)
        
        # Progress callback to send messages back to the client
        async def progress_callback(message):
            await websocket.send_text(message)

        # Run the graph process without additional arguments
        await graph.run(progress_callback=progress_callback)

        # Notify the client that the itinerary is completed
        await websocket.send_text("✔️ Itinerary planning completed.")
    except WebSocketDisconnect:
        print("WebSocket disconnected")  # Log disconnection
    finally:
        await websocket.close()  # Ensure the WebSocket is closed

if __name__ == "__main__":
    # Run the app with Uvicorn server
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=True
    )
   