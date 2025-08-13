# laughing-math
> A good collection of solutions of A&amp;C problems, especially for senior high school students struggling to handle math problem.
</br>
## 这个仓库是什么？
上次数学周测中（~~我没参加~~）,有下面这道题目，当同学问我时，我对着迷之114苦苦凝视：

```
7.已知6件不同的产品有2件次品，现对它们一一测试，直到找到所有2件次品为止，若至多测试4次就能找到所有2件次品，则不同的测试方法共有（）

A.114种         B.90种        C.106种        D.128种
```
（来自全品试卷选必3（一）第六章，答案是A）
难道你看第一眼，就能知道选哪个？所以我开发这个项目，就是为了给大家一个代码解，可能对学了选必下的同学有参考意义。
## 怎么用它？
在你的python代码中添加以下内容：
```
import lm
import builtin
lm.replace_builtins()
```
然后，你就可以使用一些千奇百怪的用法了：
```
# Example usage of the patched functions
print(int(5) ^ 10)  # 输出: [5, 6, 7, 8, 9, 10]
print(float(5.0) ^ 10.0)  # 输出: [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
print(~float(5.0))  # 输出: 120 (5的阶乘)
```
记住，代码的最后一行，要加上这个，不然会有意想不到的问题！！！
```
lm.restore_builtin()
```
## 警告
**不要在生产环境下使用此库**！！
更多用法，参见<a href="https://github.com/Jack-tendy-538/laughing-math/blob/main/teminology.md">技术文档</a>
