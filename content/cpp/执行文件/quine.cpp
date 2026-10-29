// 自指魔术代码
#include <stdio.h>

#define CODE "\
#include <stdio.h>%c%c\
#define CODE %c%s%c%c\
int main() {%c\
    printf(CODE, 10, 10, 34, CODE, 34, 10, 10, 10, 10);%c\
        return 0;%c\
        }%c"

int main()
{
    printf(CODE, 10, 10, 34, CODE, 34, 10, 10, 10, 10);
    return 0;
}

/*
#include <iostream>

#define QUINE "#include <iostream>%c#define QUINE %c%s%c%cint main() {%c    printf(QUINE, 10, 34, QUINE, 34, 10, 10);%c    return 0;%c}%c"

int main() {
    printf(QUINE, 10, 34, QUINE, 34, 10, 10);
    return 0;
}
*/

/*
 * Quine 程序说明：
 * 这是一个 C 语言 Quine（自输出 / 自复制）程序。
 * 运行后不读取外部文件，而是打印出自己的完整源代码。
 *
 * 原理：
 *   - 用宏 CODE 保存源代码模板；
 *   - printf 使用 CODE 作为格式串，同时把 CODE 自身作为 %s 参数传入；
 *   - 10 表示 ASCII 换行 '\n'，34 表示 ASCII 双引号 '"'；
 *   - 通过格式化字符串把“代码”和“数据”统一起来，实现自我引用。
 *
 * 注释中的 C++ 版本：
 *   - 是一个类似尝试或草稿；
 *   - 参数与格式串不匹配，不能正确自输出；
 *   - 也混用了 <iostream> 和 printf。
 *
 * 用途与趣味：
 *   - 理论：自指、递归定理、可计算性、自复制自动机；
 *   - 教学：练习字符串转义、宏、格式化输出、程序即数据；
 *   - 安全：自复制是病毒 / 蠕虫的基础概念之一，但 Quine 本身通常无害；
 *   - 文化：Code Golf、多语言 Quine、Quine 链、自修改 Quine 等编程挑战。
 */