FROM Python:3.8

WORKDIR /workspace

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8400

ENTRYPOINT [ "python3", "app.py" ]