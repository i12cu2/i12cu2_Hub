#include <iostream>

using namespace std;
class TV;
class Remote
{
private:
    TV *p;
public:
    Remote(TV *p);
    void offOrOn(void);
    void upVolume(void);
    void downVolume(void);

    void upChannel(void);
    void downChannel(void);

    void showTv(void);

    void setChannel(int channel);
};
class TV
{
   friend void Remote::setChannel(int channel);
   enum{OFF, ON};
   enum{minVol, maxVol=10};
   enum{minChan, maxChan=25};
private:
    int state;
    int volume;
    int channel;
public:
    TV()
    {
        state = OFF;
        volume = minVol;
        channel = minChan;
    }
    void offOrOn(void);
    void upVolume(void);
    void downVolume(void);

    void upChannel(void);
    void downChannel(void);

    void showTv(void);

};


int main(int argc, char *argv[])
{
    //实例化一个电视机
    TV tv;
    Remote re(&tv);
    re.offOrOn();
    re.upVolume();
    re.upVolume();
    re.upVolume();
    re.setChannel(20);
    re.showTv();

    return 0;
}

void TV::offOrOn()
{
    state = (state==OFF?ON:OFF);
    return;
}

void TV::upVolume()
{
    if(volume == maxVol)
    {
        cout<<"音量已经最大了"<<endl;
        return;
    }
    volume++;
    return;
}

void TV::downVolume()
{
    if(volume == minVol)
    {
        cout<<"音量已经最小了"<<endl;
        return;
    }
    volume--;
    return;
}

void TV::upChannel()
{
    if(channel == maxChan)
    {
        cout<<"频道已经最大了"<<endl;
        return;
    }
    channel++;
    return;
}

void TV::downChannel()
{
    if(channel == minChan)
    {
        cout<<"频道已经最小了"<<endl;
        return;
    }
    channel--;
    return;
}

void TV::showTv()
{
    cout<<"当前电视机的状态:"<<(state==OFF?"关":"开")<<endl;
    cout<<"当前电视机的音量:"<<volume<<endl;
    cout<<"当前电视机的频道:"<<channel<<endl;
}

Remote::Remote(TV *p)
{
    this->p = p;
}

void Remote::offOrOn()
{
    p->offOrOn();
}

void Remote::upVolume()
{
    p->upVolume();
}

void Remote::downVolume()
{
    p->downVolume();
}

void Remote::upChannel()
{
    p->upChannel();
}

void Remote::downChannel()
{
    p->downChannel();
}

void Remote::showTv()
{
    p->showTv();
}

void Remote::setChannel(int channel)
{
    p->channel = channel;
}
