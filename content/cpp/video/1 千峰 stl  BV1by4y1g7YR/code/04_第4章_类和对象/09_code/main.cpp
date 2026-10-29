#include <iostream>
#include <string>
using namespace std;
#if 0
class Room
{
    friend void visiting01(Room &room);
private:
    string bedRoom;//卧室
public:
    string setingRoom;//客厅
public:
    Room(string bedRoom, string setingRoom)
    {
        this->bedRoom = bedRoom;
        this->setingRoom = setingRoom;
    }
};

//普通全局函数
void visiting01(Room &room)
{
    cout<<"访问了"<<room.setingRoom<<endl;
    cout<<"访问了"<<room.bedRoom<<endl;
}

int main(int argc, char *argv[])
{
    Room room("刘坤卧室","刘坤客厅");
    visiting01(room);
    return 0;
}
#endif
class Room;//向前声明 只能说明类名称
class goodGay
{
public:
    void visiting01(Room &room);
    void visiting02(Room &room);
};

class Room
{
    friend class goodGay;
private:
    string bedRoom;//卧室
public:
    string setingRoom;//客厅
public:
    Room(string bedRoom, string setingRoom)
    {
        this->bedRoom = bedRoom;
        this->setingRoom = setingRoom;
    }
};



int main(int argc, char *argv[])
{
    Room room("吴维的卧室","吴维的客厅");
    goodGay ob;
    ob.visiting01(room);
    ob.visiting02(room);
    return 0;
}

void goodGay::visiting01(Room &room)
{
    cout<<"翰文访问了"<<room.setingRoom<<endl;
    cout<<"翰文访问了"<<room.bedRoom<<endl;
}

void goodGay::visiting02(Room &room)
{
    cout<<"好基友张三访问了"<<room.setingRoom<<endl;
    cout<<"好基友张三访问了"<<room.bedRoom<<endl;
}
