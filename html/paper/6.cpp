#include <stdio.h>
#include <stack>
#include <string.h>
using namespace std;
char in[1000010];
char s[1000010];
struct node{
	char c;
	node *L,*R,*P;
	node(char _c=0){c=_c,P=L=R=NULL;}
};
void print(node *tr){
	if(!tr)return;
	printf("%c",tr->c);
	print(tr->L);
	print(tr->R);
}
int d[30];
double p;
double dfs(node *tr){
	if(tr->c=='1')return 1.0;
	if(tr->c=='0')return 0.0;
	d[tr->c-'a']=1;
	double res=0.0;
	res+=p*dfs(tr->L);
	d[tr->c-'a']=0;
	res+=(1.0-p)*dfs(tr->R);
	return res;	
}
int main(){
	while(gets(in)&&strcmp(in,"0 0")){
		memset(d,-1,sizeof(d));
		sscanf(in,"%lf %s",&p,s);
		int len=strlen(s);
		node *root;
		stack<node*>st;
		for(int i=0;i<len;i++){
			if(s[i]==',')continue;
			if(s[i]==')'){
				node *a=st.top();st.pop();
				node *b=st.top();st.pop();
				node *c=st.top();st.pop();
				c->L=b;c->R=a;
				st.push(c);
			}else if(s[i]=='('){
				//st.push(NULL);
			}else{
				st.push(new node(s[i]));
			}
		}
		root=st.top();
		printf("%lf\n",dfs(root));
	}
}
