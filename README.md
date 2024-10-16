This python script is an experimental callgrind (from valgrind) to html converter.


compiling source (e.g.):
* g++ -ggdb3 -fno-inline -O0 test.cpp

producing call data:
* valgrind --tool=callgrind --compress-strings=no --compress-pos=no ./a.out

generating results:
* ./process-callgrind.py callgrind.out.44211 > test.html


written by folkert van heusden <mail@vanheusden.com>
* licensed under the MIT license
