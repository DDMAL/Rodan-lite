It is also possible to work on Rodan-Client with this setup. Normally the Rodan-Client is transpiled, minified, and served from the Nginx container, but the Nginx container does not have node.js, npm or yarn installed. The Rodan-Client is built in the Rodan-Client container and by using multi-stage builds we just copy the finished files from the optional Rodan-Client image over to the Nginx image when it's finished building. To work on Rodan-Client, we spin up the optional `rodan-client` image and launch the development server on another port. This also gives the added bonus of having the original Rodan-Client and your new changes accessible for a side-by-side comparison if you need it.

## Step-by-step to run Rodan Client
1. Navigate to rodan. Add `rodan-main:ports` and `rodan-client:` to `docker-compose.yml` or `arm-compose.yml` (depends on you're using M1 or not). Your YAML file should look like this:
```
  rodan-main:
    env_file:
      - ./scripts/local.env
    ports:
      - "8000:8000"
...
  rodan-client:
    image: "ddmal/rodan-client:nightly"
    command: bash -c "tail -f /dev/null"
    ports:
      - "8080:9002"
    volumes:
      - "./rodan-client/code:/code"
volumes:
  resources:
```
2. Navigate to rodan. `make run`/`make run_arm` (remember to run `make build_arm` before `make run_arm` if you have not yet build an nginx-local container when running on an ARM machine)
3. Navigate to rodan. 
```
docker compose exec rodan-main /run/start
```
```
docker compose -f arm-compose.yml exec rodan-main /run/start
```
4. Navigate to rodan. 
```
docker compose exec celery /run/start-celery
```
```
docker compose -f arm-compose.yml exec celery /run/start-celery
```
5. Navigate to rodan.
```
docker compose exec py3-celery /run/start-celery
```
```
docker compose -f arm-compose.yml exec py3-celery /run/start-celery
```
6. 
```
docker compose exec rodan-client bash
```
```
docker compose -f arm-compose.yml exec rodan-client bash
```
to go to rodan-client container

7. Inside the container: 
```
cd /code; yarn install
```
8. Navigate to rodan-cleint: 
```
cp local-dev/COPYconfiguration code/configuration.json
```
9. Navigate to rodan-client: 
```
cp local-dev/CPCONFIGFILE code/src/js/configuration.js
```
10. Inside the container: 
```
cd /code/node_modules/.bin
```
11. Inside the container: 
```
yarn global add gulp
```
12. Inside the container: 
```
gulp
```
13. Go to `localhost:8080` on your browser

### Setup
- Rodan must be working to get started with client. Please refer to **"Working on Rodan"**.

- Go to the rodan-client directory and follow the instructions in the README file.

You can then visit http://localhost:8080
All changes to any javascript file will automatically rebuild the site, but changes to the HTML or CSS will not.
