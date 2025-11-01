FROM python:3.11-slim

# set working directory
WORKDIR /app

# copy the fastapi code
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose FastAPI port
EXPOSE 8000

# launch FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
