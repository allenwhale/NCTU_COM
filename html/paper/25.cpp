#include <stdio.h>
#include <vector>
using namespace std;
long long int f[1010];
int main(){
	f[1]=1;
	f[2]=2;
	long long int sum=2;
	for(int i=3;i<=1000;i++){
		f[i]=(1+2*f[i-2]+f[i-1])%1000000009;
		sum+=f[i];
	}
	int N;
	while(~scanf("%d",&N)&&N){
		printf("%lld\n",f[N]);
	}
	return 0;
}
