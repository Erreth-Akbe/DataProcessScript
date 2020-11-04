#include<bits/stdc++.h>
#define ll long long
using namespace std;
const int MAXN = 400;
int main()
{
	char buf[MAXN];
	int tot = 0;
	freopen("cardsort","w",stdout);
	while(~scanf("%s",buf))
	{
		if (tot)
		{
			printf(",");
		}
		tot++;
		printf("\'%s\'",buf);
	}
	return 0;
}

