################################################################################
#				DOCKERFILE TO BUILD AN APACHE SERVER WITH 
#					    TIMETABLING APP INSTALLED
################################################################################

# The image will be based in the apache httpd image
FROM httpd:2.4
#COPY ./public-html/ /usr/local/apache2/htdocs/

# Install python3 
RUN apt update && apt install -y git wget make build-essential zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev libncurses5-dev  libncursesw5-dev \
	xz-utils tk-dev && \
	git clone https://github.com/BraulioV/TFG.git && \
	wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz && \
	tar xvf Python-3.6.1.tgz && rm Python-3.6.1.tgz && \
	wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.5.18.tar.gz && \
	tar xvfz 4.5.18.tar.gz && rm 4.5.18.tar.gz

WORKDIR Python-3.6.1

RUN ./configure --enable-shared && LD_RUN_PATH=/usr/local/lib make && make altinstall

# configure wsgi
WORKDIR ../mod_wsgi-4.5.18

RUN ./configure --with-python=/usr/local/bin/python3.6 && make install

# Change the workdir to the project's dir
WORKDIR ../TFG

# Install the python requeriments
RUN pip3.6 install -r requirements.txt

# Create database
WORKDIR djangoapp

RUN python3.6 manage.py makemigrations timetables && \
	python3.6 manage.py migrate && \
	python3.6 store_csv.py ../Dataset/classrooms.csv Classroom ../Dataset/subjects.csv Subjects ../Dataset/groups.csv Groups

# clean directories
WORKDIR ../..

RUN rm -rf Python-3.6.1 mod_wsgi-4.5.18

# configure WSGI in Apache
RUN echo "WSGIScriptAlias / /usr/local/apache2/TFG/djangoapp/djangoapp/wsgi.py" >> conf/httpd.conf && \
	echo "WSGIPythonPath /usr/local/apache2/TFG/djangoapp/" >> conf/httpd.conf && \
	echo "\n<Directory /usr/local/apache2/TFG/djangoapp/timetables>" >> conf/httpd.conf && \
	echo "<Files wsgi.py>" >> conf/httpd.conf && \
	echo "Require all granted" >> conf/httpd.conf && \
	echo "</Files>" >> conf/httpd.conf && \
	echo "</Directory>" >> conf/httpd.conf
