# Portfolio Website - Flask

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
- Secure contact form sending emails via the Resend API
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

The contact form sends emails using Resend with the following characteristics:

- Credentials are injected via environment variables
- Emails include sender information and the message content
- No credentials or secrets are stored in the repository

## Configuration and Environment Variables

The application relies on environment variables for all sensitive configuration.

Required variables in production:

- `OPENAI_API_KEY`  
  API key used for chatbot responses

- `RESEND_API_KEY`  
  API key for sending emails via Resend

- `RESEND_FROM_EMAIL`  
  Sender address used in outgoing emails

- `CONTACT_TO_EMAIL`
  Recipient email address for contact form submissions

Optional variables:

- `SITE_URL`  
  Public address of the site, for example `https://example.com`. Used for the canonical link and social preview tags. When unset, the address of the incoming request is used.

- `TRUSTED_PROXY_COUNT`  
  Number of reverse proxies in front of the application. Defaults to `1`. Set to `0` when the application is exposed directly.

The application will fail fast at startup if `OPENAI_API_KEY` is missing. The email variables are checked when the contact form is submitted, which returns a generic error if any of them are absent.

## Security Measures

- Request bodies are capped at 32 KB, and chat and contact form input is validated for type and length
- Per-address and daily rate limits on the chat and contact endpoints
- Content Security Policy and other security headers on every response
- Chat replies are rendered as plain text in the browser

## Local Development

1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root containing the four variables above, one per line in the form `NAME=value`. The file is excluded from version control.
4. Start the development server:
   ```bash
   python main.py
   ```
   The site is served at `http://127.0.0.1:5000`.

## Production

Run the application with Gunicorn and set the same four variables in the hosting platform's environment settings:

```bash
gunicorn main:app
```

## License
- This project is provided for demonstration and portfolio purposes.
