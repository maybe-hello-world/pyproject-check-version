FROM python:3-slim
RUN pip install --upgrade pip
RUN pip install requests tomli packaging

ENTRYPOINT ["python3", "./version_checker.py"]