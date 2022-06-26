#include<stdio.h>

int main()
{
    volatile int a = 54, b = 12, c = 88;

    int i;
    for (i = 0; i < 5; ++i)
    {
        c += b + i;
    }

    int guess;
    printf("number: "); fflush(stdout);
    scanf("%d", &guess);

    int ans = a * b + 4 * c;
    if (ans == guess)
    {
        printf("WINNER!\n");
    }
    else
    {
        printf("NOPE :(\n");
    }
    return 0;
}
