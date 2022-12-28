FROM python:3.8.12-alpine3.15
ENV PYTHONUNBUFFERED 1
RUN mkdir APP
ADD . ./APP/
WORKDIR /APP/
RUN pip install -r requirements.txt
RUN bash -c "python manage.py makemigrations && python manage.py migrate"
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000