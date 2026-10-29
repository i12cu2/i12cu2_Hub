#include <stdio.h>


int main(int argc, char *argv[])
{
    const int a= 10;
    int *p = (int *)&a;
    *p = 100;
    printf("*p = %d\n", *p);
    printf("a = %d\n", a);
    return 0;
}
