# Getting Started with Semantic Router

### Update: Docker Setup

A Docker setup has been created for running both `main.py` and `debug.py`. The code for this setup is available in the `docker-setup` branch.

### Running the Code with Docker

1. **Create a `.env` File:**
   Ensure you create a `.env` file in the code directory. This file should contain the API keys, as shown below:

    ```plaintext
    OPENAI_API_KEY='Place your OpenAI API key here'
    API_KEY='Place your API key here'
    ```

   Note: The `.env` file is not uploaded to the repository for security reasons.

2. **Start Docker:**
   Make sure the Docker application is running in the background.

3. **Build Docker Image:**
   Open your IDE and run the following command to build the Docker image:

    ```bash
    docker-compose build
    ```

4. **Running the Docker Containers:**
   - To run both `main.py` and `debug.py` simultaneously, use:

     ```bash
     docker-compose up
     ```

     This command will run both applications on different ports: `main.py` will be on port 8001, and `debug.py` will be on port 8002.

   - To run only the `main.py` container, use:

     ```bash
     docker-compose up app
     ```

   - To run only the `debug.py` container, use:

     ```bash
     docker-compose up debug
     ```

### Accessing the API
Make sure to run and test the code using Postman.
