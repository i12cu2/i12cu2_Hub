// 高校学籍管理系统.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
#include<iostream>
#include<fstream>
#include<iomanip>
#include<cstring>
using namespace std;



class Student			//个体类的定义
{
private:
	int number;			//编号(1001-9999)
	char name[20];		//姓名
	char sex[10];		//性别
	int math;			//数学成绩
	int chinese;		//语文成绩
	int language;		//外语成绩
	int sum;			//声明数学语文外语总分的属性
	Student* next;		//指向下一个同学的指针


public:
	int Getnumber()
	{
		return number;
	}



	char* Getname()
	{
		return name;
	}



	char* Getsex()
	{
		return sex;
	}



	int Getmath()
	{
		return math;
	}



	int Getchinese()
	{
		return chinese;
	}



	int Getlanguage()
	{
		return language;
	}



	int Getsum()
	{
		return Getmath() + Getchinese() + Getlanguage();
	}



	void Setnext(Student* n)
	{
		next = n;
	}



	Student* Getnext()
	{
		return next;
	}



	Student()
	{
		number = 0;
		strcpy(name, "");
		strcpy(sex, "");
		math = 0;
		chinese = 0;
		language = 0;
		sum = math + chinese + language;
		next = NULL;
	}



	Student(int m, char n[], char s[], int a, int b, int c)
	{
		number = m;
		strcpy(name, n);
		strcpy(sex, s);
		math = a;
		chinese = b;
		language = c;
		sum = math + chinese + language;
		next = NULL;
	}



	Student(int m, char n[], char s[], int a, int b, int c, Student* e)
	{
		number = m;
		strcpy(name, n);
		strcpy(sex, s);
		math = a;
		chinese = b;
		language = c;
		sum = math + chinese + language;
		next = e;
	}



	void Show_Student()
	{
		cout << "编号:" << number << endl
			<< "姓名:" << name << endl
			<< "性别:" << sex << endl
			<< "数学:" << math << endl
			<< "语文:" << chinese << endl
			<< "外语:" << language << endl
			<< "总分:" << sum << endl;
	}



};





class  Class				//班级类
{
public:
	Student* node;       //指向学表中结点的指针



	Class()					//类无参构造函数的定义
	{
		node = NULL;
	}



	Class(int m, char n[], char s[], int a, int b, int c)
	{
		node = new Student(m, n, s, a, b, c);
	}



	~Class()
	{
		Student* next = node;
		Student* p;
		while (next != NULL)
		{
			p = next;
			next = next->Getnext();
			delete p;
		}
		node = NULL;
	}



	void insert(int m, char n[], char s[], int a, int b, int c)
	{
		Student* p = node;
		if (p == NULL)
		{
			node = new Student(m, n, s, a, b, c);
		}
		else
		{
			while (p->Getnext() != NULL)
				p = p->Getnext();
			p->Setnext(new  Student(m, n, s, a, b, c, p->Getnext()));
		}
	}



	//1.读取同学的信息
	bool Load()
	{
		int number;
		char name[20];
		char sex[10];
		int math;
		int chinese;
		int language;
		ifstream readtxt("Student.txt", ios::in);
		while (readtxt.good())
			{
				readtxt >> number >> name >> sex >> math >> chinese >> language;
				if (!(readtxt.eof()))
				{
					insert(number, name, sex, math, chinese, language);
				}
			}
		readtxt.close();
		cout << endl << "已经将文本\"Student.txt\"中的信息加载到该系统当中" << endl;
		return true;
	}



	//2.存入同学的信息
	bool Add()
	{
		int number;
		Student* p = node;
		if (p == NULL)
		{
			cout << "目前该系统中无任何同学" << endl
				<< "请输入新添加同学的编号(1001-9999)";
			cin >> number;
			while ((1000 > number || number > 10000))
			{
				cout << "输入错误请重新尝试！！！" << endl;
				cin >> number;
			}
			input(number);
			return true;
		}
		else
		{
			if (p->Getnext() == NULL)
			{
				input(p->Getnumber() + 1);
			}
			else
			{
				while (p->Getnext() != NULL)
				{
					p = p->Getnext();
				}
				input(p->Getnumber() + 1);
			}
		}
		return true;
	}



	//2.存入同学各信息的属性
	void input(int number)
	{
		int a, b, c;
		int code;
		char n[20], s[10];
		cout << "已定义输入同学的编号(1001-9999)为" << number << endl;
		cout << "请输入该同学的姓名" << endl;
		cin >> n;
		cout << "请输入该同学的性别男(1)/女(2))" << endl;
		cin >> code;
		while (!(code == 1 || code == 2))
		{
			cout << "输入有误,请重新输入该同学的性别男(1)/女(2)!!!" << endl;
			cin >> code;
		}
		if (code == 1)
		{
			strcpy(s, "男");
		}
		else if (code == 2)
		{
			strcpy(s, "女");
		}
		cout << "请输入该同学的数学成绩(0-100)" << endl;
		cin >> a;
		while (a < 0 || a>100)
		{
			cout << "输入有误,请重新输入该同学的数学成绩(0-100)!!!" << endl;
			cin >> a;
		}
		cout << "请输入该同学的语文成绩(0-100)" << endl;
		cin >> b;
		while (b < 0 || b>100)
		{
			cout << "输入有误,请重新输入该同学的语文成绩(0-100)!!!" << endl;
			cin >> b;
		}
		cout << "请输入该同学的外语成绩(0-100)" << endl;
		cin >> c;
		while (c < 0 || c>100)
		{
			cout << "输入有误,请重新输入该同学的外语成绩(0-100)!!!" << endl;
			cin >> c;
		}
		cout << "已将该同学的信息存入系统" << endl
			<< "恭喜" << n << "加入我们!!!" << endl
			<< "以下是他的信息:" << endl
			<< "编号:" << number << endl
			<< "姓名:" << n << endl
			<< "性别:" << s << endl
			<< "数学:" << a << endl
			<< "语文:" << b << endl
			<< "外语:" << c << endl
			<< "总分:" << a + b + c << endl;
		insert(number, n, s, a, b, c);
	}



	//3.删除同学的信息
	bool Deleteperson()     //删除同学的信息
	{
		int i;
		Student* ahead = node;
		Student* follow = ahead;
		cout << "请输入删除目标同学的信息的编号:";
		cin >> i;
		if (ahead == NULL)
		{
			cout << "此系统目前无任何人信息!";
			return false;
		}
		else  if (ahead->Getnumber() == i)
		{
			node = node->Getnext();
			cout << "编号为" << i << "的同学的信息被系统删除了!!!" << endl;
			delete ahead;
			return true;
		}
		else
		{
			ahead = ahead->Getnext();
			while (ahead != NULL)
			{
				if (ahead->Getnumber() == i)
				{
					follow->Setnext(ahead->Getnext());
					cout << "编号为" << i << "的同学的信息已被删除\n";
					delete ahead;
					return true;
				}
				follow = ahead;
				ahead = ahead->Getnext();
			}
			cout << "不存在此编号的同学,删除失败,请重新尝试!!!" << endl;
			return false;
		}
	}



	//4.6.以编号检索同学的信息并且输出
	bool Findnum()
	{
		int number;
		Student* ahead = node;
		Student* follow = ahead;
		cout << "请输入需要检索同学信息的编号:" << endl;
		cin >> number;
		if (ahead == NULL)
		{
			cout << "此系统目前无任何人信息!" << endl;
			return false;
		}
		else
		{
			while (ahead != NULL)
			{
				if (ahead->Getnumber() == number)
				{
					ahead->Show_Student();
					return true;
				}
				else
				{
					follow = ahead;
					ahead = ahead->Getnext();
				}
			}
			cout << "查无此人!!!" << endl;
			return false;
		}
	}



	//5.6.以姓名检索同学的信息并且输出
	bool Findname()
	{
		char name[20];
		Student* ahead = node;
		Student* follow = ahead;
		cout << "请输入需要检索同学信息的姓名:";
		cin >> name;
		if (ahead == NULL)
		{
			cout << "此系统目前无任何人信息!" << endl;
			return false;
		}
		else
		{
			while (ahead != NULL)
			{
				if (strcmp(ahead->Getname(), name) == 0)
				{
					ahead->Show_Student();
					return true;
				}
				else
				{
					follow = ahead;
					ahead = ahead->Getnext();
				}
			}
			cout << "查无此人!!!" << endl;
			return false;
		}
	}




	//7.显示系统中记录的所有同学的信息
	void  Show_all()
	{
		Student* ahead = node;
		cout << setw(8) << "编号" << setw(8) << "姓名" << setw(8) << "性别"
			<< setw(8) << "数学" << setw(8) << "语文" << setw(8) << "外语"
			<< setw(8) << "总分" << endl;
		while (ahead != NULL)
		{
			cout << setw(8) << ahead->Getnumber() << setw(8) << ahead->Getname() << setw(8) << ahead->Getsex()
				<< setw(8) << ahead->Getmath() << setw(8) << ahead->Getchinese() << setw(8) << ahead->Getlanguage()
				<< setw(8) << ahead->Getsum() << endl;
			ahead = ahead->Getnext();
		}
	}



	//8.显示每个同学在班上的排名
	bool Findrank()
	{
		int n = 1;
		Student* ahead = node;
		Student* follow = ahead;
		Student* end = ahead;
		if (ahead == NULL)
		{
			cout << "此系统目前无任何人信息!" << endl;
			return false;
		}
		else
		{
			cout << "接下来将显示每个同学在班上的排名:" << endl
				<< setw(8) << "编号" << setw(8) << "姓名" << setw(8) << "性别"
				<< setw(8) << "数学" << setw(8) << "语文" << setw(8) << "外语"
				<< setw(8) << "总分" << setw(8) << "排名" << endl;
			while (ahead != NULL)
			{
				cout << setw(8) << ahead->Getnumber() << setw(8) << ahead->Getname() << setw(8) << ahead->Getsex()
					<< setw(8) << ahead->Getmath() << setw(8) << ahead->Getchinese() << setw(8) << ahead->Getlanguage()
					<< setw(8) << ahead->Getsum();
				while (follow != NULL)
				{
					if (ahead->Getsum() < follow->Getsum())
					{
						n++;
					}
					follow = follow->Getnext();
				}
				cout << setw(8) << n << endl;
				ahead = ahead->Getnext();
				n = 1;
				follow = end;
			}
		}
		return true;
	}



	//8.显示以编号检索同学的排名
	bool Findnum_rank()
	{
		int n = 1, sum = -1;
		int number;
		cout << "请输入需要检索同学信息的编号:" << endl;
		cin >> number;
		Student* ahead = node;
		Student* follow = ahead;
		Student* end = ahead;
		while (ahead != NULL)
		{
			if (ahead->Getnumber() == number)
			{
				sum = ahead->Getsum();
			}
			else
			{
				follow = ahead;
				ahead = ahead->Getnext();
			}
		}
		if (sum == -1)
		{
			cout << "查无此人!!!" << endl;
			return false;
		}
		ahead = end;
		while (ahead != NULL)
		{
			if (ahead->Getsum() > sum)
				n++;
		}
		cout << "排名:" << n << endl;
		return true;
	}



	//8.显示以姓名检索同学的排名
	bool Findname_rank()
	{
		int n = 1, sum = -1;
		char name[20];
		cout << "请输入需要检索同学信息的姓名:" << endl;
		cin >> name;
		Student* ahead = node;
		Student* follow = ahead;
		Student* end = ahead;
		while (ahead != NULL)
		{
			if (strcmp(ahead->Getname(), name) == 0)
			{
				sum = ahead->Getsum();
			}
			else
			{
				follow = ahead;
				ahead = ahead->Getnext();
			}
		}
		if (sum == -1)
		{
			cout << "查无此人!!!" << endl;
			return false;
		}
		ahead = end;
		while (ahead != NULL)
		{
			if (ahead->Getsum() > sum)
				n++;
		}
		cout << "排名:" << n << endl;
		return true;
	}



	//9.统计存入的各科成绩和及格率
	void Count()
	{
		char i;
		int math = 0, chinese = 0, language = 0;
		int hang_math = 0, hang_chinese = 0, hang_language = 0;
		int person = 0;
		Student* ahead = node;
		Student* follow = ahead;
		if (ahead == NULL)
		{
			cout << "此系统目前无任何人信息!" << endl;
		}
		else
		{
			cout << "  ***********************************************" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *           1.统计存入学生的各科成绩			 *" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *           2.统计存入学生的及格率		     *" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *************************************************" << '\n'
				<< "请您选择上面的选项：" << endl;
			cin >> i;
			cout << "请稍后！" << endl;
			while (ahead != NULL)
			{
				cout << "已经载入" <<ahead->Getname()<<"同学的数据!"<< endl;
				person++;
				if (ahead->Getmath() < 60)hang_math++;
				if (ahead->Getchinese() < 60)hang_chinese++;
				if (ahead->Getlanguage() < 60)hang_language++;
				math = math + ahead->Getmath();
				chinese = chinese + ahead->Getchinese();
				language = language + ahead->Getlanguage();
				ahead=ahead->Getnext() ;

			}
			ahead = follow;

			if (i == '1')
			{
				cout << "  ***********************************************" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *           1.统计存入学生的各科成绩			 *" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *           2.统计存入学生的数学成绩			 *" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *           3.统计存入学生的语文成绩			 *" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *           4.统计存入学生的外语成绩		     *" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *************************************************" << '\n'
					<< "请您选择上面的选项：" << endl;

				cin >> i;
				if (i == '1')
					//输出各科成绩
				{
					cout << "数学平均分为:" << math / person << endl
						<< "语文平均分为:" << chinese / person << endl
						<< "外语平均分为:" << language / person << endl;
				}
				else if (i == '2')		//输出数学成绩
				{
					cout << "数学平均分为:" << math / person << endl;
				}
				else if (i == '3')		//输出语文成绩
				{
					cout << "语文平均分为:" << chinese / person << endl;
				}
				else if (i == '4')		//输出外语成绩
				{
					cout << "外语平均分为:" << language / person << endl;
				}
				else
				{
					cout << "输入失败！！" << endl;
				}
			}

			else if (i == '2')
			{
				if (hang_math == 0)
				{
					cout << "恭喜!目前数学暂无挂科!及格率是100%!!!" << endl;
				}
				else
				{
					cout << "统计存入学生的数学及格率:" << (person - hang_math) / person << endl;
				}


				if (hang_chinese == 0)
				{
					cout << "恭喜!目前语文暂无挂科!及格率是100%!!!" << endl;
				}
				else
				{
					cout << "统计存入学生的语文及格率:" << (person - hang_chinese) / person << endl;
				}


				if (hang_language == 0)
				{
					cout << "恭喜!目前外语暂无挂科!及格率是100%!!!" << endl;
				}
				else
				{
					cout << "统计存入学生的外语及格率:" << (person - hang_language) / person << endl;
				}
			}
			else
			{

				cout << "输入失败！！" << endl;
			}
		}
	}




	//10.保存系统中同学的信息	
	bool Save()
	{
		remove("Student.txt");
		ofstream fout("Student.txt", ios::out);
		Student* p = node;
		if (!p)
		{
			return false;
		}
		else
		{
			while (p)
			{
				fout << p->Getnumber() << "\t" << p->Getname() << "\t" << p->Getsex() << "\t" << p->Getmath() << "\t"
					<< p->Getchinese() << "\t" << p->Getlanguage() << "\t" << endl;
				p = p->Getnext();
			}
		}
		fout.close();
		cout << "保存数据已经完成" << endl;
		return true;
	}



};




int main()
{
	char code;
	Class This_class;
	while (1)
	{
		cout << "*********************************************" << endl
			<< "欢迎访问高校学籍管理系统!!!" << endl << endl
			<< "目前系统含有以下功能:" << endl << endl
			<< "1）读取同学的信息" << endl
			<< "2）存入同学的信息" << endl
			<< "3）删除同学的信息及警告" << endl
			<< "4）以编号检索同学的信息" << endl
			<< "5）以姓名检索同学的信息" << endl
			<< "6）显示检索目标同学的结果" << endl
			<< "7）统计存入的每个学生总成绩" << endl
			<< "8）显示每个同学在班上的排名" << endl
			<< "9）统计存入的各科成绩和及格率" << endl
			<< "q）保存系统中同学的信息(补充功能)" << endl
			<< "请输入以上数字实现对应功能,或任意键退出" << endl
			<< "*********************************************" << endl;


		cin >> code;
		if (code == '1')
		{
			cout << "您正在使用(读取同学的信息)功能" << endl;
			This_class.Load();
			cout << "完成此功能,返回主交互界面" << endl;
		}
		else if (code == '2')
		{
			cout << "您正在使用(存入同学的信息)功能" << endl;
			This_class.Add();
			cout << "完成此功能,返回主交互界面" << endl;
		}
		else if (code == '3')
		{
			cout << "您正在使用(删除同学的信息)功能" << endl
				<< "警告!!!您正在尝试删除同学的信息" << endl
				<< "请输入\"n\"确认删除操作" << endl;
			cin >> code;
			if (code == 'n')
			{
				cout << "您已再次确认使用(删除同学的信息)功能" << endl;
				This_class.Deleteperson();
				cout << "完成此功能,返回主交互界面" << endl;
			}
			else
			{
				cout << "已撤销删除操作,返回主交互界面" << endl;
			}
		}
		else if (code == '4')
		{
			cout << "您正在使用(以编号检索同学的信息)功能" << endl;
			if (This_class.Findnum())
			{
				cout << "完成此功能,返回主交互界面" << endl;
			}
			else
			{
				cout << "该功能未完成,请重新尝试!!!" << endl
					<< "返回主交互界面" << endl;
			}
		}
		else if (code == '5')
		{
			cout << "您正在使用(以姓名检索同学的信息)功能" << endl;
			if (This_class.Findname())
			{
				cout << "完成此功能,返回主交互界面" << endl;
			}
			else
			{
				cout << "该功能未完成,请重新尝试!!!" << endl
					<< "返回主交互界面" << endl;
			}
		}
		else if (code == '6')
		{
			cout << "您正在使用(显示检索目标同学的结果)功能" << endl
				<< "  ***********************************************" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *           1.编号							 *" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *           2.姓名							 *" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *************************************************" << '\n'
				<< "请您选择上面的选项：" << endl;
			cin >> code;

			if (code == '1')
			{
				if (This_class.Findnum())
				{
					cout << "完成此功能,返回主交互界面" << endl;
				}
				else
				{
					cout << "该功能未完成,请重新尝试!!!" << endl
						<< "返回主交互界面" << endl;
				}
			}
			else if (code == '2')
			{

				cout << "您正在使用(以姓名检索同学的信息)功能" << endl;
				if (This_class.Findname())
				{
					cout << "完成此功能,返回主交互界面" << endl;
				}
				else
				{
					cout << "该功能未完成,请重新尝试!!!" << endl
						<< "返回主交互界面" << endl;
				}
			}
			else
			{
				cout << "输入有误,返回系统界面" << endl;
			}
		}
		else if (code == '7')
		{
			cout << "您正在使用(统计存入的每个同学总成绩)功能" << endl;
			This_class.Show_all();
			cout << "完成此功能,返回主交互界面" << endl;
		}
		else if (code == '8')
		{
			cout << "您正在使用(显示每个同学在班上的排名)功能" << endl
				<< "  ***********************************************" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *           1.全部同学的排名					 *" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *           2.指定同学的排名					 *" << '\n'
				<< "  *                                              *" << '\n'
				<< "  *************************************************" << '\n'
				<< "请您选择上面的选项：" << endl;
			cin >> code;
			if (code == '1')
			{
				This_class.Findrank();
			}
			else if (code == '2')
			{
				cout << "您正在使用(显示每个同学在班上的排名)功能" << endl
					<< "  ***********************************************" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *           1.检索编号的排名					 *" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *           2.检索姓名的排名					 *" << '\n'
					<< "  *                                              *" << '\n'
					<< "  *************************************************" << '\n'
					<< "请您选择上面的选项：" << endl;
				cin >> code;
				if (code == '1')
				{
					This_class.Findnum_rank();
				}
				else if (code == '2')
				{
					This_class.Findname_rank();
				}
				else
				{
					cout << "输入错误" << endl;
				}
			}
			else
			{
				cout << "输入错误" << endl;
			}
			cout << "完成此功能,返回主交互界面" << endl;
		}
		else if (code == '9')
		{
			cout << "您正在使用(统计存入的各科成绩和及格率)功能" << endl;
			This_class.Count();
			cout << "完成此功能,返回主交互界面" << endl;
		}
		else if (code == 'q')
		{
			cout << "您正在使用(保存系统中同学的信息)功能" << endl;
			This_class.Save();
			cout << "完成此功能,返回主交互界面" << endl;
		}
		else break;
	}
	return 0;
}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
