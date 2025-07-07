Telegram Bot with LLM and Operator Web Interface

Overview

This project implements a Telegram bot integrated with a Large Language Model (LLM) and a web interface for operators. The bot saves user messages to a SQLite database, generates responses using TinyLLaMA via Ollama, and allows operators to moderate responses through a Vue.js web interface. The system is deployed using Docker Compose.

Requirements
Docker and Docker Compose installed
Internet access for pulling dependencies
A valid Telegram bot token (replace in docker-compose.yml)

Setup and Running

Clone the repository:
git clone <repository>
cd <project_folder>

Ensure the directory structure matches the above.
Update the Telegram bot token in docker-compose.yml:
environment:
  - TOKEN=<your_bot_token>

Run the project:
docker-compose up --build
This builds and starts all services: Telegram bot, LLM service, web backend, web frontend, database, and Ollama.