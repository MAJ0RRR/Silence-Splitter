FROM python

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get install -y ffmpeg make autoconf automake libtool sox espeak-ng libavcodec-extra

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]