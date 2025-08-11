# Simple Chat Application - Usage Guide

## How to Run the Application

### Step 1: Start the Server
1. Open a command prompt or terminal
2. Navigate to the project directory
3. Run the server:
   ```
   python server.py
   ```
4. You should see: "Chat server started on localhost:12345"

### Step 2: Connect Clients
1. Open a new command prompt/terminal (keep the server running)
2. Navigate to the same project directory
3. Run a client:
   ```
   python client.py
   ```
4. Enter a username when prompted
5. Start chatting!

### Step 3: Connect Multiple Clients
- Repeat Step 2 in additional terminals to connect more users
- Each client needs a unique username

## Available Commands

### For All Users:
- **Regular message**: Just type your message and press Enter
- **/help**: Show available commands
- **/users**: List all connected users
- **/private <username> <message>**: Send a private message
- **/quit**: Exit the chat

### Examples:
```
Hello everyone!                    # Broadcast message
/users                            # List connected users
/private Alice How are you?       # Send private message to Alice
/quit                            # Exit the application
```

## Features Demonstrated

### 1. Broadcast Messages
- Messages sent by one user are received by all other connected users
- Shows real-time communication between multiple clients

### 2. User List Request
- Users can request a list of currently connected users
- Demonstrates server maintaining client state

### 3. Private Messages
- Users can send direct messages to specific users
- Shows targeted message routing by the server

## Testing the Three Request Types

### Test Broadcast Messages:
1. Connect 2+ clients with different usernames
2. Type a message in one client
3. Verify it appears in all other clients

### Test User List:
1. Connect multiple clients
2. Type `/users` in any client
3. Verify you see all connected usernames

### Test Private Messages:
1. Connect 2+ clients (e.g., "Alice" and "Bob")
2. In Alice's client, type: `/private Bob Hello Bob!`
3. Verify Bob receives the private message
4. Verify other clients don't see the private message

## Troubleshooting

### Server Won't Start:
- Check if port 12345 is already in use
- Try running as administrator
- Check firewall settings

### Client Can't Connect:
- Ensure server is running first
- Check that you're using the correct host/port
- Verify network connectivity

### Messages Not Appearing:
- Check that both server and client are running
- Verify username was entered correctly
- Check for error messages in the terminal

## Network Details

- **Protocol**: TCP (Transmission Control Protocol)
- **Port**: 12345
- **Message Format**: JSON encoded in UTF-8
- **Architecture**: Client-Server model
- **Concurrency**: Multi-threaded server handles multiple clients