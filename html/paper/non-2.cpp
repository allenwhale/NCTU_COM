#include <stdio.h>
#include <algorithm>
#include <string.h>
using namespace std;
int s[1010];
bool dp[50010];
int main(){
	int N,L,R;
	while(~scanf("%d",&N)&&N){
		scanf("%d %d",&L,&R);
		for(int i=0;i<N;i++)
			scanf("%d",&s[i]);
		memset(dp,false,sizeof(dp));
		dp[0]=true;
		for(int i=0;i<N;i++){
			for(int j=50000;j>=s[i];j--){
				dp[j]|=dp[j-s[i]];
			}
		}
		bool ans=false;
		for(int i=L;i<=R&&!ans;i++){
			ans|=dp[i];
		}
		if(ans)puts("YES");
		else puts("NO");
	}
	return 0;
}
