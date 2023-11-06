FROM ubi8/python-39
COPY . /opt/app-root/src
RUN pip install -r /opt/app-root/src/requirements.txt

CMD ["python", "pop-queue.py"]