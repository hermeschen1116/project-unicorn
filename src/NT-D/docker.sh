docker build -t nt-d . --compress --force-rm --no-cache
docker run -it --rm --name nt-d -p 8080:8080 -p 8081:8081 -p 8082:8082 nt-d
