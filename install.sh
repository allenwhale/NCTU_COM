sudo apt-get install python3 python3-pip build-essential
sudo apt-get install postgresql postgresql-server-dev-all
sudo pip3 install tornado msgpack-python psycopg2
sudo su postgres
createuser root -i -d -r -l -s
echo "ALTER ROLE root WITH PASSWORD 'root';" | psql
echo "CREATE DATABASE nctu_com;" | psql
psql -d nctu_com < psql
