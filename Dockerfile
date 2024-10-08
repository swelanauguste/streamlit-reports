FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app


# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc


RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501
CMD ["streamlit","run","app.py"]