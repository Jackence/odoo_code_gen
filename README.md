# odoo_code_gen
用于生成odoo 中一些简单的初始化。

--------------------------------------------


说明：
本文件夹用于生成odoo 中的简要数据，可以自动生成一些简单代码：

包括但不限于：
模型中字段的初始化
XML的初始化


excel 中包含的文件簿：
字段名，form视图，tree视图，权限，search视图，初始化数据，其他初始化，验证
---------------------------------------------------------------------

###### 字段名页签
A1 输入模型名英文，
A列其他字段，写入字段中文名称
B列其他字段，写入字段英文名称
C列写入字段类型，做的是字段类型校验，
D列写入该字段是否后台必输
E列写入该字段是否只读
F列写入是否是双语字段
H1写入form视图是否需要消息界面
J1写入该模型所在的模块

注：字段的定义的翻译已经编写







###### form视图页签
第二行分别表示form视图是否可以编辑，删除，创建，是否包含有效按钮，doc_number之类的是否需要单列，是否需要form视图，是否可以复制

第四行表示form视图中的左边字段，可选值为字段名页签中定义的值

第六行表示form视图中的右边字段，可选值为字段名页签中定义的值



###### tree视图页签
第二行分别表示tree视图是否可以编辑，删除，创建，是否需要form视图，是否可以复制



###### 权限页签
第二行及后面行都是群组的权限的生成

A列需要填写群组xml_id
B列填写该群组的模块
C,D,E,F分别是赋予的权限



###### search视图页签
F1表示的是是否需要search视图，
第二行到第十二行，是搜索部分的字段，
第十四到第二十六行，是筛选部分的字段


###### 初始化数据页签
初始化数据页签是对该模型的数据进行初始化
ACE列输入模型中的字段
BDF列输入初始化的值



###### 其他初始化页签
其他初始化页签是对其他可初始化数据的初始化，包含菜单，快码，序列，记录规则，审批流等
此部分内容不稳定，需要查看使用。



第2，3行是用户组的初始化
B1填写是否需要初始化用户组
A列填写用户组（英文名），
B列填写所属模块，
C列填写权限分类，
D列填写备注（英文名）。


第5-9行是初始化菜单
A列填写菜单英文名
B列填写序号


B10填写是否需要初始化快码
第11-22是初始化快码


B23填写是否需要初始化序列
第24-29填写初始化序列的值
A列填写初始化英文，
B列填写简写，
C列填写前缀，
D列填写需要，
E列填写是否按年，
F列填写是否按月。




B30填写是否需要初始化记录规则（还未写）
第31-35填写记录规则的值


B36填写是否需要初始化审批流
工作流自动生成。初始化了一个开始和一个结束节点。


