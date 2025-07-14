#!/usr/bin/env python3
"""
Startup script for the MCP Contract Monitor Backend.

This script provides an easy way to start the backend server with
various configuration options.
"""

import uvicorn
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="MCP Contract Monitor Backend")
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--log-level", 
        default="info", 
        choices=["debug", "info", "warning", "error"],
        help="Log level (default: info)"
    )
    
    args = parser.parse_args()
    
    print("Starting MCP Contract Monitor Backend...")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Reload: {args.reload}")
    print(f"Log Level: {args.log_level}")
    print("-" * 50)
    
    try:
        # Use the correct module path based on current directory
        if os.path.exists("app/main.py"):
            # Running from Backend directory
            module_path = "app.main:app"
        else:
            # Running from project root
            module_path = "Backend.app.main:app"
        
        uvicorn.run(
            module_path,
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 