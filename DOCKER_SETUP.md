# Docker Setup Instructions for FastAPI Calculator

## Current Status
✅ Repository cloned successfully  
✅ Docker configuration files created:
- `Dockerfile` - FastAPI application container
- `docker-compose.yml` - Multi-container orchestration
- `.env` - Environment variables configuration
- `.dockerignore` - Docker build optimization

❌ Docker is not installed/accessible in your WSL2 environment

## Setup Docker in WSL2

### Option 1: Docker Desktop (Recommended)

1. **Download and Install Docker Desktop for Windows**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Windows
   - Run the installer

2. **Enable WSL2 Integration**
   - Open Docker Desktop
   - Go to Settings → Resources → WSL Integration
   - Enable integration with your WSL2 distro (Ubuntu/Debian)
   - Click "Apply & Restart"

3. **Verify Installation**
   ```bash
   docker --version
   docker compose version
   ```

### Option 2: Install Docker Engine in WSL2

If you prefer not to use Docker Desktop:

```bash
# Update packages
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker service
sudo service docker start

# Add your user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
```

## Running the Application

Once Docker is installed, navigate to the project directory and run:

```bash
cd /home/ishit/sql/assignment_8
docker compose up --build
```

This will:
1. Build the FastAPI application image
2. Pull PostgreSQL and pgAdmin images
3. Start all three containers
4. Set up networking between them

## Accessing the Services

After running `docker compose up --build`, you can access:

### 📊 FastAPI Calculator
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 🐘 PostgreSQL Database
- **Host**: localhost
- **Port**: 5432
- **Database**: calculator_db
- **Username**: calculator_user
- **Password**: calculator_pass

### 🔧 pgAdmin
- **URL**: http://localhost:5050
- **Email**: admin@calculator.com
- **Password**: admin

## Connecting to PostgreSQL via pgAdmin

1. Open http://localhost:5050 in your browser
2. Login with:
   - Email: `admin@calculator.com`
   - Password: `admin`

3. Add a new server:
   - Right-click "Servers" → "Register" → "Server"
   
4. General Tab:
   - Name: `Calculator DB` (or any name you prefer)
   
5. Connection Tab:
   - Host: `postgres` (this is the service name in docker-compose)
   - Port: `5432`
   - Database: `calculator_db`
   - Username: `calculator_user`
   - Password: `calculator_pass`
   
6. Click "Save"

## Stopping the Services

To stop all containers:
```bash
docker compose down
```

To stop and remove volumes (delete database data):
```bash
docker compose down -v
```

## Viewing Logs

View logs from all services:
```bash
docker compose logs
```

View logs from specific service:
```bash
docker compose logs fastapi
docker compose logs postgres
docker compose logs pgadmin
```

Follow logs in real-time:
```bash
docker compose logs -f
```

## Configuration

All configuration is stored in the `.env` file. You can modify:
- Database credentials
- Port mappings
- pgAdmin credentials

After changing `.env`, restart the containers:
```bash
docker compose down
docker compose up --build
```

## Troubleshooting

### Port Already in Use
If you see an error about ports being in use, modify the ports in `.env`:
```
POSTGRES_PORT=5433  # Change from 5432
FASTAPI_PORT=8001   # Change from 8000
PGADMIN_PORT=5051   # Change from 5050
```

### Permission Denied
If you get permission errors, prefix commands with `sudo`:
```bash
sudo docker compose up --build
```

Or add your user to the docker group (requires logout/login):
```bash
sudo usermod -aG docker $USER
```

### Container Won't Start
Check the logs:
```bash
docker compose logs [service-name]
```

### Clean Restart
Remove all containers and volumes:
```bash
docker compose down -v
docker compose up --build
```

## Next Steps

Once Docker is set up and running:
1. ✅ Verify FastAPI is accessible at http://localhost:8000
2. ✅ Verify pgAdmin is accessible at http://localhost:5050
3. ✅ Connect to PostgreSQL via pgAdmin
4. 🎯 You're ready to develop!
