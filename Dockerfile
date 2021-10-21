FROM python:3.8.10

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN rm -rf venv
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt --no-cache-dir

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]