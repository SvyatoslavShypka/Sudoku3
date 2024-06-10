Docker file support
This project contains a Docker file named Dockerfile. 
In this file, the services could be defined like database version.

Please review the tags of the used images and set them to the same 
as you're running in production.

1. Zbuduj obraz Docker: W terminalu, w katalogu z Dockerfile, uruchom komendę:
docker build -t sudoku .

2. Uruchom kontener Docker: Po zbudowaniu obrazu, uruchom kontener używając komendy:
docker run sudoku
   
if you use web service you can access to your applicatio here:
http://localhost:5000
