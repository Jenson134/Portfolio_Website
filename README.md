# Portfolio Website — Flask

This repository contains the source code for my personal portfolio website, built using **Flask (Python)** and deployed as a production web service.

The site showcases my background, education, technical stack, and projects, and includes interactive features such as a constrained chatbot and a secure contact form.

## Architecture Overview

The application follows a conventional Flask project structure:

- `main.py`  
  Core Flask application, routing logic, and service integrations.

- `templates/`  
  Jinja2 HTML templates used for server-side rendering.

- `static/`  
  Static assets including CSS, JavaScript, images, and documents.

- `projects.json`  
  Structured data source for project information.

- `stack.json`  
  Structured data source for technical stack information.

## Features

- Server-rendered portfolio pages using Flask and Jinja2
- Dynamic project and technology stack rendering from JSON
- OpenAI-powered chatbot restricted to a predefined personal context
- Secure contact form sending emails via SendGrid API
- Environment-variable-based configuration for all secrets
- Production-ready deployment using Gunicorn

## Chatbot Design

The chatbot is implemented using the OpenAI API and is intentionally constrained:

- Responses are limited to a predefined personal knowledge base
- General knowledge and speculative questions are disallowed
- System and user prompts are explicitly separated
- Out-of-scope questions return a controlled response

This design prioritizes predictability, safety, and reliability.

## Email Handling

The contact form sends emails using SendGrid with the following characteristics:

- Credentials are injected via environment variables
- Emails include sender information and the message content
- No credentials or secrets are stored in the repository

## Configuration and Environment Variables

The application relies on environment variables for all sensitive configuration.

Required variables in production:

- `OPENAI_API_KEY`  
  API key used for chatbot responses

- `SENDGRID_API_KEY`  
  API key for sending emails via SendGrid

- `SENDGRID_FROM_EMAIL` 
  Sender email used in outgoing emails

- `CONTACT_TO_EMAIL`
  Recipient email address for contact form submissions

The application will fail fast at startup if required variables are missing.

## Local Development

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## License
- This project is provided for demonstration and portfolio purposes.
