import asyncio
import websockets
import json

# Function to load configuration from a JSON file
def load_config(config_file="config.json"):
    with open(config_file, "r") as file:
        return json.load(file)

async def connect_and_send(config):
    # Extracting values from the config
    server_uuid = config["server_uuid"]
    external_server_ip = config["external_server_ip"]
    server_port = config["server_port"]
    server_private_key = config["server_private_key"]
    uri = config["websocket_uri"]

    # Form the message with the dynamic values
    message = {
        "From": server_uuid,
        "To": "API",
        "Type": "SERVER_INFO",
        "Content": json.dumps({
            "Type": "DIRECTORY",
            "Address": external_server_ip,
            "Port": server_port,
            "ServerPrivateKey": server_private_key
        })
    }

    # Convert the message to JSON
    message_json = json.dumps(message)

    # Connect to the WebSocket
    async with websockets.connect(uri) as websocket:
        print("Connected to the server.")
        
        # Send the initial message
        await websocket.send(message_json)
        print("Message sent to the server.")
        
        # Keep the connection alive (or handle any incoming messages)
        try:
            while True:
                # Optionally send periodic updates or just keep the connection alive
                # For example, send a ping message or log every X seconds
                await asyncio.sleep(10)  # Adjust sleep time as needed
                # You could also listen for incoming messages:
                # response = await websocket.recv()
                # print(f"Received message from server: {response}")
        except websockets.ConnectionClosed:
            print("Connection closed unexpectedly.")

# Load the configuration from the file
config = load_config("config.json")

# Run the connection and message sending
asyncio.run(connect_and_send(config))
