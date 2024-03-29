# OCR-Service-Restapi

## Overview

A FastAPI-based simple web service that accepts images, runs optical character recognition (OCR) on them and returns the extracted text.

## Prerequisites

Before you begin, make sure you have the following prerequisites installed:

- Python 3.10
- Pip (Python package installer)
- Docker
- fastapi
- uvicorn
- python-dotenv
- pyyaml
- python-multipart
- pytesseract
- Pillow

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/99sbr/OCR-Service-Restapi.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd OCR-Service-Restapi
    ```
## Containerize the Service
To run the web service in a Docker container:
1. Build the Docker image: 
```bash 
    docker build -t ocrservice-image  .
 ```
2. Run the Docker container:
```bash
    docker run -p 80:80 ocrservice-image
```
Visit `http://localhost:80/docs` to access the Swagger documentation and interact with the API.

![Api](https://github.com/99sbr/OCR-Service-Restapi/blob/main/cache/Screenshot%202023-12-04%20at%2014.24.10.png)
## API Endpoints
1. POST /imgsync
    - Description: Synchronously extracts text from an image.
    - Request Body: Provide a JSON object with the base64-encoded image data.
    - Response: Returns a JSON object with the extracted text.
2. POST /imgasync
    - Description: Asynchronously extracts text from an image.
    - Request Body: Provide a JSON object with the base64-encoded image data.
    - Response: Returns a JSON object with a job_id for tracking the asynchronous task.
2. GET /ocr_text
    - Description: Asynchronously gets OCR text from Job ID.
    - Request Body: Provide a JSON object with the job-ID data.
    - Response: Returns a JSON object with the extracted text.


## Code Structure

- `api_template:`  Contains all the API-related Code Base.
    - `manage.py:` Only entry point for API. Contains no logic. 
    - `.env:` Most important file for our API and contains global configs. Avoid using application/variable level configs here.
    - `application:`  It contains all our API-related codes and test modules. I prefer keeping the application folder global.
    - `logs`: Logs are self-explanatory. FYI it will not contain any configuration information, just raw logs. Feel free to move according to your comfort but not inside the application folder.
    - `settings:` Logger/DataBase/Model global settings files in yaml/json format.

- `application:` 
    - `main:` priority folder of all your application-related code.
        - `📮 routers:` API routers and they strictly do not contain any business logic
        - `📡 services:` All processing and business logic for routers here at the service layer
        - `⚒ utility:`
            - `logger` Logging module for application
            - `manager` A manager utility contains workers and handlers for Data Related Tasks which can be common for different services.
    - `initializer.py:` Preload/Initialisation of Models and Module common across applications. The preloading model improves inferencing.
    
