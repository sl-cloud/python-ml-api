# python-ml-api
Python API for ML

This script is a Python application that uses the FastAPI framework to create an API for making predictions using a pre-trained machine learning model. 
It also includes authentication using JSON Web Tokens (JWT) for securing the API endpoints.

To use this script, follow these steps:

Install the required dependencies:

Make sure you have uvicorn installed, which is the ASGI server used by FastAPI. You can install it using pip:

pip3 install uvicorn

Set up the environment variables:

Create a .env file in the same directory as the script.

In the .env file, set the following variables:

SECRET_KEY='your_secret_key'

USERNAME='api_user'

Replace 'your_secret_key' with a strong secret key value of your choice.

Replace 'api_user' with the desired username for API access.

Run the script:

Start the server using the uvicorn command:

uvicorn api:app --host 0.0.0.0 --port 8000 --reload

The api:app argument specifies the module (api) and the FastAPI application instance (app) to be served by Uvicorn.

The --host 0.0.0.0 flag ensures the server listens on all available network interfaces.

The --port 8000 flag sets the port number to 8000, but you can change it to a different port number if needed.

The --reload flag enables auto-reloading, which automatically restarts the server when code changes are detected.

Access the API:

The API will be available at http://localhost:8000 (or the appropriate host and port combination you specified).

You can use an API client, such as cURL or Postman, to send requests to the API endpoints.

Make sure to include the required authentication token in the request headers for authenticated endpoints.
