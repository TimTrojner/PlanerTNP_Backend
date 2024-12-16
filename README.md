# Prerequisites

Create a virtual environment and activate it.

```bash
python3 -m venv venv
```
Run the following command to activate the virtual environment:

- Linux/MacOS:
```bash
source venv/bin/activate
```

- Windows:
```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

# Docker

## Prerequisites

You will need to have the following installed on your system:

- git
- docker
- docker compose

## Instructions

Create a .env file in the root of the backend project and fill in the variables with your values:
```
BACKEND_PORT=1234
FRONTEND_PORT=8080
```

Run `./setup_docker.sh` script.

