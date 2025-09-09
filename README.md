# Javshnebi

![Python](https://img.shields.io/badge/Python-3.10-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Docker](https://img.shields.io/badge/Docker-Ready-lightgrey)

**Javshnebi** is a Python-based open-source project that monitors available city exam slots for driving licenses in Georgia. When a slot becomes available, it sends an email notification to subscribed users. The application checks for new slots every **9 minutes**, ensuring you always get the latest updates.

This project is **completely free and open-source**.

---

## Features

- Monitors driving license exam slots in Georgia.
- Sends email notifications to subscribed users when a slot becomes available.
- Checks for updates every 9 minutes automatically.
- Easy setup using Docker and Docker Compose.
- Completely free and open-source.

---

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/varsimashviliLuka/Javshnebi.git
cd Javshnebi
```

2. **Create a `.env` file** in the project root and fill it with your credentials:

```env
# ==== Flask / JWT ====
SECRET_KEY=
JWT_SECRET_KEY=

# ==== MySQL ====
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_HOST=
MYSQL_PORT=

# ==== Mail ====
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_SERVER=
MAIL_PORT=
```
3. **Make the Docker entrypoint executable and start the container**

```bash
chmod +x docker-entrypoint.sh
docker-compose up --build -d
```
> ✅ As long as the Docker container is running and the `.env` file is correctly configured, everything will work perfectly.

---

## Contributing

Contributions are welcome! You can:

- Open an issue if you encounter a bug or have a feature request.
- Submit a pull request to improve the project.

---


## Contact

For questions or suggestions, you can:

- Open an issue on GitHub.
- Contact [Luka / varsimashviliLuka].
