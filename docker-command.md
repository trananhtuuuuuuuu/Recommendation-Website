# Create postgreSQL database docker container
```bash
docker run -d \
  --name postgres-db \
  -e POSTGRES_DB=rw-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123456 \
  -p 8386:5432 \
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  postgres:16
```

# Docker build image
```bash
```

# Docker compose  up
```
```

# Docker compose down


