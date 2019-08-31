#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#define MAXLENGTH 2187

bool inArray(char word[], char words[][8]);

int main(void)
{
	srand(time(NULL)); //seed random int generator
	char *telwords[10][3] = {{"","",""}, {"","",""}, {"A","B","C"}, {"D","E","F"},{"G","H","I"},{"J","K","L"},{"M","N","O"},{"P","R","S"},{"T","U","V"},{"W","X","Y"}};
	char words[MAXLENGTH][8]; //collection of words
	int head, tail; //two halves of phone number
	bool valid = true; //to know if a number contains 0s and 1s
	char numberStr[8]; //store phone number string
	
	int k;
	for(k = 0; k < MAXLENGTH; ++k) //init words array
	{
		strcpy(words[k],"");
	}
	
  printf("%s\n","******* USER AGENT GENERATOR ***********\nPhone numbers will be used as a seed for the generator.\nAvoid entering 1's and 0's");
	printf("%s","Enter Phone Number (XXX-XXXX): ");
	scanf("%d-%d", &head, &tail);
	sprintf(numberStr, "%d%d", head, tail); //combine 2 halves
	
	char *s = &numberStr[0]; //number char pointer for extracting individual chars	
 	
	for(; *s != '\0'; s++)
	{
		if ((int)(*s-'0') < 2) //convert char to int and check if any is 0 or 1
		{
			valid = false;
			break;
		}
	}
	
	s = &numberStr[0]; 	
	if (!valid)
		puts("The phone number cannot contain 0's or 1's");
	else
	{
		int i, j; //loop counter variables
		char word[8] = ""; //current gen word
		int num = 1; //number of gen words
		char * c; //temp storage for randomly selected letter
		while (num < MAXLENGTH+1)
		{
			for(j = 0; j < 7,*s != '\0'; ++j,++s)
			{
				c = telwords[(int)(*s - '0')][rand() % 3];
				strcat(word, c);
			}
			
			if (inArray(word, words)) //if gen word is not unique, do not increment num and try to get a unique gen word
			{
				s = &numberStr[0];
				strcpy(word,"");
				continue;
			}
			else
			{
				strcat(words[num-1], word);
				s = &numberStr[0];
				strcpy(word,"");				
				num += 1;
			}
		}
		
		//output unique gen words (2,187) to file named after the phone number
		FILE *wPtr;
		char title[20];
		sprintf(title, "USER_GEN_%s.txt", numberStr);
		if ((wPtr = fopen(title, "w")) == NULL)
			printf("\"%s\" could not be created/opened.",title);
		else
		{
			for(j = 0; j < MAXLENGTH; ++j)
				fprintf(wPtr, "%s\n",words[j]);
			fclose(wPtr);
			printf("Generated user-agents outputted to \"%s\"",title);
		}
	}
}

bool inArray(char word[], char words[][8])
{
	int i;
	for(i = 0; i < MAXLENGTH; ++i)
	{
		if (strcmp(word, words[i]) == 0)
			return true;
	}
	return false;
}
