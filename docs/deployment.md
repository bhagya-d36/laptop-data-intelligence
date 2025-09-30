# Deployment Guide

This guide covers deploying the Laptop Assistant platform to production environments.

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured
- SSL certificates (for HTTPS)
- DeepSeek API key
- Server with at least 2GB RAM and 2 CPU cores

## Quick Deployment

### 1. Clone and Configure
```bash
git clone <your-repository-url>
cd ai-engineer-assessment

# Copy production environment file
cp backend/env.production backend/.env

# Edit .env with your production values
nano backend/.env
```

### 2. Deploy with Docker Compose
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Verify Deployment
```bash
# Check API health
curl http://your-domain.com/api/v1/health

# Check frontend
curl http://your-domain.com
```

## Production Configuration

### Environment Variables

#### Required Variables
```bash
DEEPSEEK_API_KEY=sk-your-production-api-key
ENVIRONMENT=production
DEBUG=False
```

#### Optional Variables
```bash
# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/laptop_assistant

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
```

### SSL Configuration

#### Generate SSL Certificates
```bash
# Using Let's Encrypt
certbot certonly --standalone -d yourdomain.com

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/key.pem
```

#### Update Nginx Configuration
Uncomment the HTTPS server block in `nginx.conf` and update the SSL paths.

## Scaling and Performance

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
    environment:
      - REDIS_URL=redis://redis:6379/0
```

### Load Balancing
```yaml
# Add load balancer service
  loadbalancer:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

### Caching Strategy
```python
# Enable Redis caching (if implemented)
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend

# FastAPICache.init(RedisBackend(), prefix="laptop-cache")
```

## Monitoring and Logging

### Health Checks
```bash
# API health
curl http://yourdomain.com/api/v1/health

# Frontend health
curl http://yourdomain.com/health

# Database health (if applicable)
curl http://yourdomain.com/api/v1/health/db
```

### Log Management
```bash
# View application logs
docker-compose logs -f backend

# View nginx logs
docker-compose logs -f nginx

# Log rotation
logrotate /etc/logrotate.d/laptop-intelligence
```

### Metrics Collection
```python
# Prometheus metrics (if implemented)
# from prometheus_client import Counter, Histogram, generate_latest

# REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
# REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# @app.get('/metrics')
# def metrics():
#     return generate_latest()
```

## Security Hardening

### Network Security
```bash
# Firewall rules
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

### Application Security
```python
# Rate limiting (if implemented)
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address

# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Input validation (using Pydantic)
from pydantic import BaseModel, Field

class LaptopSearchRequest(BaseModel):
    query: str = Field(..., max_length=100)
    brand: str = Field(None, regex="^(hp|lenovo|dell)$")
```

### Data Protection
```bash
# Encrypt sensitive data
openssl enc -aes-256-cbc -salt -in data.csv -out data.csv.enc

# Secure file permissions
chmod 600 backend/.env
chmod 644 data/processed/laptop_info_cleaned.csv
```

## Backup and Recovery

### Data Backup
```bash
# Backup data files
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup database (if applicable)
pg_dump laptop_assistant > backup-$(date +%Y%m%d).sql

# Upload to cloud storage
aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://your-backup-bucket/
```

### Disaster Recovery
```bash
# Restore from backup
tar -xzf backup-20240101.tar.gz

# Restore database
psql laptop_assistant < backup-20240101.sql

# Restart services
docker-compose restart
```

## Maintenance

### Regular Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade
npm update

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Performance Optimization
```python
# Database indexing (if using database)
# CREATE INDEX idx_laptop_brand ON laptops(brand);
# CREATE INDEX idx_laptop_price ON laptops(price);

# Query optimization (current CSV-based approach)
def get_laptops_optimized():
    # Current implementation uses pandas for CSV data
    # Future database implementation would use SQLAlchemy
    return data_service.get_all_laptops()
```

### Monitoring Alerts
```yaml
# Prometheus alert rules
groups:
- name: laptop_intelligence
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: High error rate detected
```

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
docker-compose logs backend

# Check resource usage
docker stats

# Restart services
docker-compose restart
```

#### High Memory Usage
```bash
# Monitor memory usage
docker stats

# Optimize worker count
# Reduce uvicorn workers in start.sh
```

#### Database Connection Issues
```bash
# Check database status
docker-compose ps postgres

# Test connection
docker-compose exec backend python -c "import psycopg2; print('DB OK')"
```

### Performance Issues

#### Slow API Responses
```bash
# Enable profiling (if implemented)
# export FASTAPI_PROFILING=True

# Check slow queries
# Review data service performance
```

#### Frontend Loading Issues
```bash
# Check nginx configuration
nginx -t

# Verify static file serving
curl -I http://yourdomain.com/static/js/main.js
```

## Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Domain name configured
- [ ] Firewall rules set
- [ ] Monitoring configured
- [ ] Backup strategy implemented
- [ ] Health checks working
- [ ] Performance benchmarks met
- [ ] Security scan completed
- [ ] Documentation updated

## Support

For production support:
- Check application logs first
- Review monitoring dashboards
- Test API endpoints
- Verify database connectivity
- Check external service status (DeepSeek API)

## Scaling Beyond Single Server

### Multi-Server Deployment
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.role == worker
  
  frontend:
    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == worker
  
  nginx:
    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == manager
```

### Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: laptop-assistant-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: laptop-assistant-backend
  template:
    metadata:
      labels:
        app: laptop-assistant-backend
    spec:
      containers:
      - name: backend
        image: laptop-assistant-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEEPSEEK_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: deepseek-api-key
```

This deployment guide provides comprehensive instructions for deploying the Laptop Assistant platform to production environments with proper security, monitoring, and scaling considerations.
