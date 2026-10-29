#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <stdlib.h>
#include <time.h>
#include <deque>
using namespace std;
class Player
{
    friend void playGame(int index,vector<int> &v, map<int,Player> &m, vector<int> &v1);
private:
    int num;
    string name;
    float score[3];
public:
    Player(){}
    Player(int num, string name)
    {
        this->num = num;
        this->name = name;
    }
};
void createPlayer(vector<int> &v, map<int,Player> &m)
{
    int i=0;
    string seedName="ABCDEFGHIJKLMNOPQRSTUVWX";
    for(i=0; i<24; i++)
    {
        int num = 100;
        num = num+i;
        string tmpName = "选手";
        tmpName += seedName[i];

        v.push_back(num);
        m.insert(make_pair(num, Player(num,tmpName)));
    }
}
void playGame(int index,vector<int> &v, map<int,Player> &m, vector<int> &v1)
{
    //选手编号随机分组
    srand(time(NULL));
    random_shuffle(v.begin(), v.end());

    //每名选手比赛
    multimap<float, int, greater<float>> mul;//存放每组的分数--编号
    int count = 0;
    vector<int>::iterator it=v.begin();

    cout<<"---------第"<<index<<"轮比赛-----------"<<endl;
    for(;it!=v.end(); it++)
    {
        count++;
        //定义deque容器 存放评委打分
        deque<float> d;
        int i=0;
        for(i=0;i<10;i++)
        {
            d.push_back( (float)(rand()%41+60) );
        }
        //排序
        sort(d.begin(),d.end());
        //去掉最高、最低分
        d.pop_back();
        d.pop_front();
        //求平均分
        float avg = accumulate(d.begin(),d.end(), 0)/d.size();
        //将平均分 赋值给m中选手
        m[*it].score[index-1] = avg;
        mul.insert(make_pair(avg, *it));

        if(count%6 == 0)//刚好一组
        {
            //分析竞技名单
             cout<<"\t第"<<count/6<<"组的晋级名单:"<<endl;
            int i=0;
            multimap<float, int, greater<float>>::iterator mit=mul.begin();
            for(i=0;i<3;i++,mit++)
            {
                v1.push_back( (*mit).second);
                cout<<"\t\t"<<(*mit).second<<" "<<(*mit).first<<endl;
            }
            //打印当前组的得分情况
            cout<<"\t第"<<count/6<<"组的得分情况:"<<endl;
            mit=mul.begin();
            for(i=0;i<6;i++, mit++)
            {
                int num = (*mit).second;
                cout<<"\t\t"<<num<<" "<<m[num].name<<" "<<m[num].score[index-1]<<endl;
            }


            mul.clear();
        }

    }
}

int main(int argc, char *argv[])
{
    vector<int> v;//存放选手编号
    map<int,Player> m;//存放编号--选手信息

    //创建选手
    createPlayer(v, m);

    //比赛
    vector<int> v1;//存放晋级的编号
    playGame(1,v,m, v1);

    vector<int> v2;//存放晋级的编号
    playGame(2,v1,m, v2);

    vector<int> v3;//存放晋级的编号
    playGame(3,v2,m, v3);
    return 0;
}
