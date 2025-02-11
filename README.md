# Micro basics


## Usage

### Installation

1. Clone the repository:

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

### Running the Microservices

Start the three microservices using `uvicorn`:

```sh
uvicorn facade_service:app --host 0.0.0.0 --port 8000
uvicorn logging_service:app --host 0.0.0.0 --port 8001
uvicorn message_service:app --host 0.0.0.0 --port 8002
```

### Testing

Once the services are running, you can test the API by visiting:

[http://localhost:8000/docs](http://localhost:8000/docs)

This will open the Swagger UI for the `facade_service` where you can interact with the API.


