COMPILANDO OS PROGRAMAS EM C
----------------------------

- No Ubuntu, é preciso instalar o OpenGL (nas máquinas da FEEC normalmente já está instalado):

sudo apt-get update
sudo apt-get install freeglut3-dev
Em seguida, o programa pode ser compilado e executado com:

gcc minimal.c -o minimal -lGL -lGLU -lglut -Wall
./minimal

- No macOS o OpenGL já vem instalado, e o programa pode ser compilado e executado com:

gcc minimal.c -o minimal -framework GLUT -framework OpenGL -Wall -Wno-deprecated-declarations
./minimal


EXECUTANDO OS PROGRAMAS EM PYTHON
---------------------------------
No Python é preciso instalar as bibliotecas do PyOpenGL, o que pode ser feito, independente do sistema, com:

pip install pyopengl

ou

sudo pip install pyopengl

Os exemplos acima são para o meu Ubuntu, para o meu macOS — para o seu, pode haver algumas variações: a pesquisa de fazer isso funcionar faz parte do trabalho, mas eu estimulo vocês a trocarem informações e ajuda no forum aqui do Moodle.
