#include <stdio.h>
#include <string.h>
int B,G,n;
double wb,wg;
int main()
{
	char tmp[100];
	while(gets(tmp)!=NULL&&strcmp(tmp,"."))
	{
		sscanf(tmp,"%d %d %d %lf %lf",&B,&G,&n,&wb,&wg);
		int tmpb=0;
		for(int i=0;i<n;i++)
		{
			if(wb*B>=wg*G)
			{
				tmpb++,B--;
			}
			else G--;
		}
		printf("%d\n",tmpb);
	}
	return 0;
}
