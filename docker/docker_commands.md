
## Docker

#### Build the Docker image
To **Build and image** run this command in a root directory
```bash
docker-compose build
```

To force rebuild:
```bash
docker-compose build --no-cache
```

#### Create and run a container
To create a container:
```bash
docker-compose up -d
```
If container doesn't exist -> docker creates and starts it.
If it already exists -> it just starts it.

To enter container:
```bash
docker-compose exec indomitus_rover_dev bash
```
You can enter one container from multiple terminals


To stop a container(it won't be deleted, just stopped):
```bash
docker-compose stop
```

To just start that containerdocker-compose start
```bash
docker-compose start
```

To delete:
```bash
docker-compose down
```
