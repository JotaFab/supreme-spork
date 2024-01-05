# syntax=docker/dockerfile:1
FROM python:3.11.6-alpine3.18

WORKDIR /backend

COPY requeriments.txt /backend/requeriments.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requeriments.txt

COPY . /backend/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
