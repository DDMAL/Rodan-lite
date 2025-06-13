Generate an ERD from the code (although ugly):

````shell
python manage.py graph_models rodan > rodan_erd.dot
dot -Tpng rodan_erd.dot > rodan_erd.png
````
