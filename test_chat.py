#!/usr/bin/env python3
"""
Test script for the Simple Chat Application
This script helps verify that the server and client work correctly
"""

import subprocess
import time
import sys
import os

def test_server_startup():
    """Test if the server starts correctly"""
    print("Testing server startup...")
    try:
        # Start server in a separate process
        server_process = subprocess.Popen([sys.executable, 'server.py'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        
        # Give server time to start
        time.sleep(2)
        
        # Check if server is still running
        if server_process.poll() is None:
            print("[OK] Server started successfully")
            server_process.terminate()
            server_process.wait()
            return True
        else:
            stdout, stderr = server_process.communicate()
            print(f"[FAIL] Server failed to start")
            print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error testing server: {e}")
        return False

def test_client_connection():
    """Test if client can connect to server"""
    print("Testing client connection...")
    try:
        # Start server
        server_process = subprocess.Popen([sys.executable, 'server.py'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        time.sleep(1)
        
        # Try to connect client (this will timeout quickly for testing)
        client_process = subprocess.Popen([sys.executable, 'client.py'], 
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        
        # Send username
        client_process.stdin.write(b"TestUser\n")
        client_process.stdin.flush()
        
        time.sleep(2)
        
        # Check if both processes are running
        if server_process.poll() is None and client_process.poll() is None:
            print("[OK] Client connected successfully")
            result = True
        else:
            print("[FAIL] Client connection failed")
            result = False
        
        # Clean up
        client_process.terminate()
        server_process.terminate()
        client_process.wait()
        server_process.wait()
        
        return result
        
    except Exception as e:
        print(f"[FAIL] Error testing client connection: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    print("Checking required files...")
    required_files = ['server.py', 'client.py', 'README.md']
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            print(f"[FAIL] {file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=== Simple Chat Application Test Suite ===\n")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Check files
    if check_files():
        tests_passed += 1
    print()
    
    # Test 2: Server startup
    if test_server_startup():
        tests_passed += 1
    print()
    
    # Test 3: Client connection
    if test_client_connection():
        tests_passed += 1
    print()
    
    # Results
    print("=== Test Results ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("[OK] All tests passed! Your chat application is ready.")
        print("\nTo run the application:")
        print("1. Open a terminal and run: python server.py")
        print("2. Open another terminal and run: python client.py")
        print("3. Open more terminals for additional clients")
    else:
        print("[FAIL] Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()