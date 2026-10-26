FROM local-python-base:current
RUN curl -fsSL http://127.0.0.1:8044/install.sh | sh
COPY app/ /app/
WORKDIR /app
CMD ["python3", "report.py"]
