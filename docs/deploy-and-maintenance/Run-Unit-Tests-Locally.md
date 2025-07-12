* ### Setup Steps
1. Download docker image for CI jobs
```
docker pull ddmal/ci-jobs:django-v2.0.13
```
2. Start and detach a container using the image: 
```
docker run -itd -v <absolute path to rodan>/rodan-main/code:/code/Rodan ddmal/ci-jobs:django-v2.0.13
```
3. Go into the container: `docker ps` to get the container ID. 
```
docker exec -it <container ID> bash
```
to go into the container.

4. Inside the container: 
```
bash /run/prepare-ci.bash
```
5. Inside the container: 
```
DJANGO_DEBUG_MODE=True
```

### Start four tests
```
cd /code/Rodan; python manage.py test --no-input --pattern="test_*" rodan/test/
```
```
cd /code/Rodan; python manage.py test --no-input rodan.test.views.testIndividual_interactive
```
```
cd /code/Rodan; python manage.py test --no-input rodan.test.views.testIndividual_workflowrun
```
```
cd /code/Rodan; python manage.py test --no-input rodan.test.test_all_jobs
```
```
cd /code/Rodan; python manage.py test --no-input rodan.test.testIndividual_mimetype_identification
```