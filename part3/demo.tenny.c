#include <stdio.h>
int main(void){
float A;
float B;
float C;
float SUM;
float NUM;
float I;
A = 10;
B = 20;
printf("ADD:\n");
printf("%.2f\n", (float)(A+B));
printf("MINUS:\n");
printf("%.2f\n", (float)(A-B));
printf("ASTERISK:\n");
printf("%.2f\n", (float)(A*B));
printf("SLASH:\n");
printf("%.2f\n", (float)(A/B));
printf("-----------------------------------------\n");
printf("statements:\n");
printf("IF-ELSE:\n");
A = 20;
B = 30;
C = 0;
if(A>B){
printf("a>b IN IF\n");
}
else{
printf("a>b IN ELSE\n");
}
if(A>C){
printf("a>c IN IF\n");
}
else if(A<C){
printf("a>c IN ELSE\n");
}
printf("\n");
SUM = 0;
NUM = 100;
I = 0;
while(I<NUM){
SUM = SUM+I;
I = I+1;
}
printf("%.2f\n", (float)(SUM));
printf("-----------------------------------------\n");
printf("PRINT\n");
printf("Print\n");
printf("-----------------------------------------\n");
printf("COMMENT:\n");
printf("Not in comment\n");
printf("-----------------------------------------\n");
printf("EXTRA:\n");
printf("INVERSE:\n");
A = 2;
B = 5;
printf("!+:\n");
printf("%.2f\n", (float)(A-B));
printf("!-:\n");
printf("%.2f\n", (float)(A+B));
printf("!*:\n");
printf("%.2f\n", (float)(A/B));
printf("!/:\n");
printf("%.2f\n", (float)(A*B));
printf("\n");
A = 10;
B = 100;
C = 50;
if(A<=B){
printf("into !>\n");
}
if(A<B){
printf("into !>=\n");
}
if(B>=C){
printf("into !<\n");
}
if(B>=C){
printf("into !<=\n");
}
printf("\n");
printf("MULTILINE COMMENTS\n");
printf("Not in multiline comment\n");
printf("\n");
printf("Not in comment\n");
printf("-----------------------------------------\n");
printf("COMMENT:\n");
printf("Not in multiline comment\n");
printf("\n");
printf("Not in comment\n");
printf("-----------------------------------------\n");
printf("MAX_MIN\n");
printf("%d\n",10);
printf("%d\n",10);
printf("%d\n",30);
printf("\n");
printf("%d\n",40);
printf("%d\n",10);
printf("%d\n",20);
printf("-----------------------------------------\n");
printf("SORT\n");
printf("[10, 40, 305]\n");
printf("-----------------------------------------\n");
printf("POW\n");
printf("%.2f\n", (float)(5*5));
printf("%.2f\n", (float)(10*10));
printf("-----------------------------------------\n");
return 0;
}
