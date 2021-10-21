FROM django:python3-onbuild

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN rm -rf venv
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

EXPOSE 8000
CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']