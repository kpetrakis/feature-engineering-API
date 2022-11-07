# pull the docker image
FROM python:3.10.8-slim

WORKDIR /app

# install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy 
COPY . .
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
# without host 0.0.0.0 i get ERR_SOCKET_NOT_CONNECTED
