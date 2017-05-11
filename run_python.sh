docker run --name data-python --link data-mysql:mysql --rm -it -v ~/proj/data-practice:/app python:3.4 bash
