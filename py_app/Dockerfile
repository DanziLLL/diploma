FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./wait-for-it.sh", "mariadb:3306", "--", "python", "./main.py" ]
