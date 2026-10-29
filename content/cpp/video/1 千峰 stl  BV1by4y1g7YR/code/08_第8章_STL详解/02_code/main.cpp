#include <iostream>
#include <deque>
using namespace std;
void printfDequeInt(deque<int> &d)
{
    deque<int>::iterator it;
    for(it=d.begin(); it!=d.end();it++)
    {
        cout<<*it<<" ";
    }
    cout<<endl;
}

void test01()
{
    deque<int> d1;
    d1.push_back(1);
    d1.push_back(2);
    d1.push_back(3);
    d1.push_front(4);
    d1.push_front(5);
    d1.push_front(6);
    printfDequeInt(d1);//6 5 4 1 2 3

    cout<<"大小:"<<d1.size()<<endl;
    d1.pop_front();
    printfDequeInt(d1);//5 4 1 2 3
    d1.pop_back();
    printfDequeInt(d1);//5 4 1 2
    d1.insert(d1.begin()+1,3, 100);
    printfDequeInt(d1);//5 100 100 100 4 1 2
}

#include<vector>
class Player
{
public:
    string name;
    float score;
public:
    Player(){}
    Player(string name,float score=0.0f)
    {
        this->name = name;
        this->score=score;
    }
};
void createPlayer(vector<Player> &v)
{
    string seedName = "ABCDE";
    int i=0;
    for(i=0;i<5;i++)
    {
        string tmpName = "选手";
        tmpName+=seedName[i];

        v.push_back(Player(tmpName));
    }
}
#include<stdlib.h>
#include<time.h>
#include<algorithm>
void playGame(vector<Player> &v)
{
    //设置随机数 种子
    srand(time(NULL));
    //每名选手都要参加
    vector<Player>::iterator it;
    for(it=v.begin(); it!=v.end();it++)
    {
        //10个评委打分
        deque<float> d;
        int i=0;
        for(i=0;i<10;i++)
        {
            d.push_back(rand()%41+60);
        }

        // 对d容器排序
        sort(d.begin(),d.end());

        //去掉最高分
        d.pop_back();
        //去掉最低分
        d.pop_front();

        //求总分数
        (*it).score = accumulate(d.begin(),d.end(), 0)/d.size();
    }
}
void showScore(vector<Player> &v)
{
    vector<Player>::iterator it;
    for(it=v.begin(); it!=v.end();it++)
    {
        cout<<(*it).name<<"所得分数:"<<(*it).score<<endl;
    }
}
void test02()
{
    //创建5名选手 放入vector容器中
    vector<Player> v;
    createPlayer(v);

    //开始比赛
    playGame(v);

    //公布成绩
    showScore(v);
}

int main(int argc, char *argv[])
{
    test02();
    return 0;
}
