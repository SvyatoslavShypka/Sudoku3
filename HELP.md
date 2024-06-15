variant1
Setup script support:

1. Running the Setup Script
------------------------------------------
For Unix-based systems (Linux/Mac):
chmod +x setup.sh
./setup.sh
------------------------------------------
For Windows systems:
Double-click setup.bat or run it from the command line.
setup.bat
------------------------------------------

2. Running the Application
After setting up the environment using the above scripts:

------------------------------------------
Unix-based systems (Linux/Mac):
source venv/bin/activate
python game.py

------------------------------------------
Windows systems:
venv\Scripts\activate
python game.py


variant2
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

