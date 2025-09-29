FROM python:2.7.12

WORKDIR /app

COPY requirements_fiscal.txt requirements_fiscal.txt
RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements_fiscal.txt  

COPY . .

EXPOSE 12000

CMD ["python", "server.py"]   