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
uvicorn messages_service:app --host 0.0.0.0 --port 8002
```

### Testing

Once the services are running, you can test the API by visiting:

[http://localhost:8000/docs](http://localhost:8000/docs)

This will open the Swagger UI for the `facade_service` where you can interact with the API.


Create message with POST request:

![Screenshot from 2025-02-11 16-48-28](https://github.com/user-attachments/assets/22b7cf64-5b70-4204-bb91-2423ff57a1de)


After some creations of new messages logging_service prints following:

![Screenshot from 2025-02-11 16-49-28](https://github.com/user-attachments/assets/34d08a58-dac0-4d6c-9829-54b95d950b90)


And finally lets try to get all message via GET request:

![Screenshot from 2025-02-11 16-48-59](https://github.com/user-attachments/assets/1a2c2d14-3673-4c6a-887c-2a7e44313ec4)


