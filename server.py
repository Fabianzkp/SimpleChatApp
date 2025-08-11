#!/usr/bin/env python3
"""
Simple Chat Server
Handles multiple client connections and supports:
- Broadcast messages to all clients
- List connected users
- Private messages between users
"""

import socket
import threading
import json
import time

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        """Initialize the chat server with host and port"""
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to store client connections {username: socket}
        self.server_socket = None
        
    def start_server(self):
        """Start the server and listen for client connections"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"Chat server started on {self.host}:{self.port}")
            print("Waiting for client connections...")
            
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")
                
                # Start a new thread to handle this client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            self.cleanup_server()
    
    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        username = None
        try:
            # Get username from client
            welcome_msg = {"type": "system", "message": "Enter your username:"}
            client_socket.send(json.dumps(welcome_msg).encode('utf-8'))
            
            username_data = client_socket.recv(1024).decode('utf-8')
            username_msg = json.loads(username_data)
            username = username_msg.get('username', f"User_{client_address[1]}")
            
            # Add client to the clients dictionary
            self.clients[username] = client_socket
            
            # Notify all clients about new user
            join_msg = {
                "type": "system",
                "message": f"{username} joined the chat",
                "timestamp": time.strftime("%H:%M:%S")
            }
            self.broadcast_message(join_msg, exclude_user=username)
            
            # Send welcome message to the new user
            welcome_msg = {
                "type": "system", 
                "message": f"Welcome {username}! Type '/help' for commands.",
                "timestamp": time.strftime("%H:%M:%S")
            }
            client_socket.send(json.dumps(welcome_msg).encode('utf-8'))
            
            # Handle client messages
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                message_data = json.loads(data)
                self.process_message(username, message_data)
                
        except Exception as e:
            print(f"Error handling client {username}: {e}")
        finally:
            self.disconnect_client(username, client_socket)
    
    def process_message(self, sender, message_data):
        """Process different types of messages from clients"""
        message_type = message_data.get('type', 'message')
        content = message_data.get('message', '')
        
        if message_type == 'message':
            if content.startswith('/'):
                self.handle_command(sender, content)
            else:
                # Regular broadcast message
                broadcast_msg = {
                    "type": "message",
                    "sender": sender,
                    "message": content,
                    "timestamp": time.strftime("%H:%M:%S")
                }
                self.broadcast_message(broadcast_msg, exclude_user=sender)
        
        elif message_type == 'list_users':
            self.send_user_list(sender)
            
        elif message_type == 'private':
            target_user = message_data.get('target')
            self.send_private_message(sender, target_user, content)
    
    def handle_command(self, sender, command):
        """Handle special commands from clients"""
        if command == '/help':
            help_msg = {
                "type": "system",
                "message": "Commands: /help, /users, /private <username> <message>",
                "timestamp": time.strftime("%H:%M:%S")
            }
            self.clients[sender].send(json.dumps(help_msg).encode('utf-8'))
            
        elif command == '/users':
            self.send_user_list(sender)
            
        elif command.startswith('/private'):
            parts = command.split(' ', 2)
            if len(parts) >= 3:
                target_user = parts[1]
                private_msg = parts[2]
                self.send_private_message(sender, target_user, private_msg)
            else:
                error_msg = {
                    "type": "system",
                    "message": "Usage: /private <username> <message>",
                    "timestamp": time.strftime("%H:%M:%S")
                }
                self.clients[sender].send(json.dumps(error_msg).encode('utf-8'))
    
    def send_user_list(self, requester):
        """Send list of connected users to the requester"""
        user_list = list(self.clients.keys())
        user_msg = {
            "type": "system",
            "message": f"Connected users: {', '.join(user_list)}",
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.clients[requester].send(json.dumps(user_msg).encode('utf-8'))
    
    def send_private_message(self, sender, target_user, message):
        """Send private message between two users"""
        if target_user in self.clients:
            # Send to target user
            private_msg = {
                "type": "private",
                "sender": sender,
                "message": message,
                "timestamp": time.strftime("%H:%M:%S")
            }
            self.clients[target_user].send(json.dumps(private_msg).encode('utf-8'))
            
            # Confirm to sender
            confirm_msg = {
                "type": "system",
                "message": f"Private message sent to {target_user}",
                "timestamp": time.strftime("%H:%M:%S")
            }
            self.clients[sender].send(json.dumps(confirm_msg).encode('utf-8'))
        else:
            # User not found
            error_msg = {
                "type": "system",
                "message": f"User '{target_user}' not found",
                "timestamp": time.strftime("%H:%M:%S")
            }
            self.clients[sender].send(json.dumps(error_msg).encode('utf-8'))
    
    def broadcast_message(self, message, exclude_user=None):
        """Broadcast message to all connected clients except excluded user"""
        message_json = json.dumps(message)
        disconnected_users = []
        
        for username, client_socket in self.clients.items():
            if username != exclude_user:
                try:
                    client_socket.send(message_json.encode('utf-8'))
                except:
                    disconnected_users.append(username)
        
        # Remove disconnected users
        for username in disconnected_users:
            self.disconnect_client(username, self.clients[username])
    
    def disconnect_client(self, username, client_socket):
        """Handle client disconnection"""
        if username and username in self.clients:
            del self.clients[username]
            
            # Notify other clients
            leave_msg = {
                "type": "system",
                "message": f"{username} left the chat",
                "timestamp": time.strftime("%H:%M:%S")
            }
            self.broadcast_message(leave_msg)
            print(f"{username} disconnected")
        
        try:
            client_socket.close()
        except:
            pass
    
    def cleanup_server(self):
        """Clean up server resources"""
        if self.server_socket:
            self.server_socket.close()
        print("Server shut down")

if __name__ == "__main__":
    server = ChatServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.cleanup_server()