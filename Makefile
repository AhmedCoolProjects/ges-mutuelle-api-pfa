dev2:
	uvicorn --port 5000 --host 127.0.0.1 main:app --reload
dev:
	uvicorn main:app --reload
freeze:
	pip3 freeze > requirements.txt
install:
	pip3 install -r requirements.txt