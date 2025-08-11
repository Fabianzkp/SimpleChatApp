# Simple Chat Application

## Overview

This project is a Simple Chat Application built using Python's TCP socket programming. As a software engineer, I created this application to deepen my understanding of network programming, client-server architecture, and real-time communication protocols. The application demonstrates fundamental networking concepts including socket programming, multi-threading, and message broadcasting.

The software consists of two main components: a server that manages multiple client connections and handles message routing, and a client that provides a command-line interface for users to participate in chat conversations. Users can send broadcast messages to all connected clients, send private messages to specific users, and view a list of currently connected users.

The purpose of writing this software was to gain hands-on experience with network programming concepts, understand how real-time communication applications work under the hood, and practice implementing concurrent server applications that can handle multiple clients simultaneously.

[Software Demo Video](http://youtube.link.goes.here)

## Network Communication

The application uses a **Client-Server architecture** where multiple clients connect to a central server that manages all communication and user sessions.

The system uses **TCP (Transmission Control Protocol)** on **port 12345** for reliable, connection-oriented communication between clients and the server. TCP ensures that messages are delivered in order and without loss, which is crucial for chat applications.

The message format uses **JSON (JavaScript Object Notation)** encoded in UTF-8 for structured communication between client and server. Each message contains the following fields:

- `type`: Indicates the message type ("message", "system", "private", "list_users")
- `message`: The actual message content
- `sender`: Username of the message sender (for regular messages)
- `target`: Target username (for private messages)
- `timestamp`: Time when the message was sent (HH:MM:SS format)

Example message formats:
```json
// Broadcast message
{"type": "message", "sender": "Alice", "message": "Hello everyone!", "timestamp": "14:30:25"}

// Private message
{"type": "private", "sender": "Bob", "message": "Hi there!", "timestamp": "14:31:10"}

// System message
{"type": "system", "message": "Alice joined the chat", "timestamp": "14:29:45"}
```

## Development Environment

The software was developed using the following tools and technologies:

**Development Tools:**
- Visual Studio Code as the primary code editor
- Git for version control
- Windows Command Prompt for testing and running the applications

**Programming Language and Libraries:**
- **Python 3.x** - Main programming language
- **socket** - Built-in Python library for network communication
- **threading** - Built-in Python library for handling multiple client connections concurrently
- **json** - Built-in Python library for message serialization and deserialization
- **time** - Built-in Python library for timestamp generation

## Useful Websites

During the development of this project, the following resources were particularly helpful:

* [Python Socket Programming Documentation](https://docs.python.org/3/library/socket.html) - Official Python documentation for socket programming
* [Real Python - Socket Programming Guide](https://realpython.com/python-sockets/) - Comprehensive tutorial on Python socket programming
* [Python Threading Documentation](https://docs.python.org/3/library/threading.html) - Official documentation for Python threading
* [JSON in Python](https://docs.python.org/3/library/json.html) - Official documentation for JSON handling in Python
* [TCP/IP Protocol Suite Overview](https://en.wikipedia.org/wiki/Internet_protocol_suite) - Background information on TCP/IP networking
* [OSI Model Explained](https://en.wikipedia.org/wiki/OSI_model) - Understanding network communication layers

## Future Work

Several enhancements could be made to improve the functionality and user experience of this chat application:

* Add a graphical user interface (GUI) using tkinter or PyQt for better user experience
* Implement user authentication and secure login system
* Add support for chat rooms or channels for organized conversations
* Implement message history and persistence using a database
* Add file sharing capabilities between users
* Implement end-to-end encryption for secure private messaging
* Add support for emoji and rich text formatting
* Create a web-based client interface using HTML/CSS/JavaScript
* Add administrative features like user moderation and chat logging
* Implement reconnection handling for improved reliability