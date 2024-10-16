compiling source (e.g.):
* g++ -ggdb3 -fno-inline -O0 test.cpp

producing call data:
* valgrind --tool=callgrind --compress-strings=no --compress-pos=no ./a.out

generating results:
* ./process-callgrind.py callgrind.out.44211 > test.html
