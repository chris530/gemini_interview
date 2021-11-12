FROM python:3.9-bullseye
RUN mkdir -p /opt/gemini
WORKDIR /opt/gemini
COPY app.py /opt/gemini/
COPY requirements.txt /opt/gemini/
RUN pip install -r requirements.txt
RUN chmod +rx /opt/gemini/app.py
ENTRYPOINT ["/opt/gemini/app.py"]
