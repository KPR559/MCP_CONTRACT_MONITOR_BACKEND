# MCP Contract Monitor Backend

A FastAPI-based backend service for the MCP Contract Monitor system that provides real-time contract updates to web and Omniverse frontends.

## Features

- **Real-time WebSocket Communication**: Live contract updates to all clients
- **REST API Endpoints**: Contract management and status queries
- **MCP Integration**: External contract system integration via MCPClient
- **Comprehensive Logging**: Detailed system monitoring

## Project Structure

```
Backend/
├── app/
│   ├── API/
│   │   ├── endpoints/          # REST and WebSocket endpoints
│   │   └── router/            # API routing
│   ├── API_clients/
│   │   └── mcp_clients/       # MCP contract system client
│   ├── configs/               # Configuration and logging
│   ├── models/                # Pydantic data models
│   ├── resource/              # Enums and resources
│   ├── services/              # Business logic services
│   └── utils/                 # Utility functions
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend

### Development Mode
```bash
uvicorn Backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
gunicorn Backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### WebSocket Endpoints

- **`/ws`** - WebSocket connection for real-time updates
  - Supports contract updates, heartbeats, and status queries
  - Accepts JSON messages for various operations

### REST Endpoints

#### Contract Management
- **`POST /update`** - Send contract update
  - **Required fields:**
    - `contract_id` (str)
    - `location` (str: "Chennai", "Mumbai", "Bengaluru", "Hyderabad")
    - `status` (str: "active", "inactive")
    - `timestamp` (ISO8601 string)
- **`POST /test/update`** - Test contract update

#### Query Endpoints
- **`GET /contracts/history`** - Get contract history
- **`GET /contracts/status`** - Get system status
- **`GET /ws/status`** - Get WebSocket connection status

## WebSocket Message Format

### Contract Updates
```json
{
  "type": "contract_update",
  "data": {
    "contract_id": "uuid",
    "location": "Chennai",
    "status": "active",
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

### Heartbeat
```json
{
  "type": "heartbeat",
  "timestamp": "2024-01-01T12:00:00",
  "client_id": "uuid"
}
```

### Client Commands
```json
{
  "type": "get_history",
  "limit": 10
}
```

## Configuration

### Environment Variables
- `WS_URI` - WebSocket URI (default: `ws://localhost:8000/api/ws`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

## MCPClient Integration

The backend provides an external integration point via the MCPClient. This allows external systems to send contract updates to the backend REST API.

**Example usage:**
```python
from Backend.app.API_clients.mcp_clients.clients import MCPClient

client = MCPClient()
client.send_contract({
    "contract_id": "external-123",
    "location": "Mumbai",
    "status": "active",
    "timestamp": "2024-01-01T12:00:00"
})
```

## Development

### Running Tests
```bash
pytest Backend/tests/
```

### Code Formatting
```bash
black Backend/
isort Backend/
```

### Type Checking
```bash
mypy Backend/
```

## Monitoring and Logging

The backend includes comprehensive logging:
- Connection events
- Contract updates
- Error handling
- Performance metrics

Logs are available via the configured logging system and can be viewed in real-time.

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check if the backend is running on the correct port
   - Verify CORS settings for browser clients

2. **Contract Updates Not Received**
   - Check WebSocket connection status
   - Verify contract data format
   - Check logs for error messages

3. **422 Unprocessable Entity (REST API)**
   - Ensure all required fields (`contract_id`, `location`, `status`, `timestamp`) are present in the request body
   - Check that `location` and `status` values match the allowed enums

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 