#!/usr/bin/env python3
"""
Simple Chat Client
Connects to the chat server and allows users to:
- Send broadcast messages
- Send private messages
- List connected users
- View received messages
"""

import socket
import threading
import json
import sys

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        """Initialize the chat client with server host and port"""
        self.host = host
        self.port = port
        self.client_socket = None
        self.username = None
        self.connected = False
        
    def connect_to_server(self):
        """Connect to the chat server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to chat server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
    
    def start_client(self):
        """Start the client and handle user interaction"""
        if not self.connect_to_server():
            return
        
        # Start thread to receive messages from server
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Handle username setup
        self.setup_username()
        
        # Display help message
        print("\n=== Simple Chat Client ===")
        print("Commands:")
        print("  /help - Show this help message")
        print("  /users - List connected users")
        print("  /private <username> <message> - Send private message")
        print("  /quit - Exit the chat")
        print("  Just type a message to broadcast to all users")
        print("=" * 30)
        
        # Main message loop
        self.message_loop()
    
    def setup_username(self):
        """Handle username setup with the server"""
        try:
            # Wait for server's username request
            import time
            time.sleep(0.1)  # Small delay to ensure server message is received
            
            while not self.username:
                username = input("Enter your username: ").strip()
                if username:
                    username_msg = {"username": username}
                    self.client_socket.send(json.dumps(username_msg).encode('utf-8'))
                    self.username = username
                    break
                else:
                    print("Username cannot be empty!")
        except Exception as e:
            print(f"Error setting up username: {e}")
    
    def receive_messages(self):
        """Continuously receive messages from the server"""
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                self.display_message(message)
                
            except Exception as e:
                if self.connected:
                    print(f"Error receiving message: {e}")
                break
    
    def display_message(self, message):
        """Display received message based on its type"""
        msg_type = message.get('type', 'message')
        timestamp = message.get('timestamp', '')
        
        if msg_type == 'system':
            print(f"[{timestamp}] SYSTEM: {message['message']}")
            
        elif msg_type == 'message':
            sender = message.get('sender', 'Unknown')
            content = message.get('message', '')
            print(f"[{timestamp}] {sender}: {content}")
            
        elif msg_type == 'private':
            sender = message.get('sender', 'Unknown')
            content = message.get('message', '')
            print(f"[{timestamp}] PRIVATE from {sender}: {content}")
    
    def message_loop(self):
        """Main loop for handling user input and sending messages"""
        while self.connected:
            try:
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                if user_input == '/quit':
                    self.disconnect()
                    break
                    
                elif user_input == '/help':
                    self.send_command_message(user_input)
                    
                elif user_input == '/users':
                    self.request_user_list()
                    
                elif user_input.startswith('/private'):
                    self.send_command_message(user_input)
                    
                else:
                    # Regular broadcast message
                    self.send_broadcast_message(user_input)
                    
            except KeyboardInterrupt:
                self.disconnect()
                break
            except Exception as e:
                print(f"Error in message loop: {e}")
                break
    
    def send_broadcast_message(self, message):
        """Send a broadcast message to all users"""
        try:
            msg_data = {
                "type": "message",
                "message": message
            }
            self.client_socket.send(json.dumps(msg_data).encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def request_user_list(self):
        """Request list of connected users from server"""
        try:
            msg_data = {"type": "list_users"}
            self.client_socket.send(json.dumps(msg_data).encode('utf-8'))
        except Exception as e:
            print(f"Error requesting user list: {e}")
    
    def send_command_message(self, command):
        """Send command message to server for processing"""
        try:
            msg_data = {
                "type": "message",
                "message": command
            }
            self.client_socket.send(json.dumps(msg_data).encode('utf-8'))
        except Exception as e:
            print(f"Error sending command: {e}")
    
    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        print("Disconnected from server")

def main():
    """Main function to start the client"""
    print("Simple Chat Client")
    
    # Allow custom server address
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = 'localhost'
    
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = 12345
    
    client = ChatClient(host, port)
    try:
        client.start_client()
    except KeyboardInterrupt:
        print("\nExiting...")
        client.disconnect()

if __name__ == "__main__":
    main()