# coding:utf-8

import re
import xlwt
import xlrd

data_sheet = xlrd.open_workbook('model_cost4.xlsx')


# 阅读字段文件簿，生成字段，视图和初始化的数据


def normalize(name):
    return name[:1].upper() + name[1:].lower()


# 模型名
table0 = data_sheet.sheets()[0]

model = table0.cell(0, 0).value.lower()

record = table0.cell(0, 7).value

temp_model = model.split('.')

# 输出import
import_module = """
# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError,RedirectWarning
"""

cls_name = ''.join(map(normalize, temp_model))
class_name = "class " + cls_name + "(models.Model):"

model_name = "    _name = '" + str(model) + "'"

all_des = ' '.join(map(normalize, temp_model))

model_desc = "    _description = '" + all_des + "'"

# 行列数
nrows = table0.nrows

# #data 结构（中文，英文，字段类型，是否必输,是否只读,translate，是否记录变化）


# 输出导入
print(import_module)
# 输出类
print(class_name)
# 输出模型名
print(model_name)
# 输出描述
print(model_desc)

if record:
    print("    _inherit = 'mail.thread'")
field_list_dict = {}
eng_ch_dict = {}

for i in range(1, nrows):
    data = table0.row_values(i)
    attr = ''
    data_temp = data[1].replace(' ', '_').replace('.', '')
    data_temp_field = data_temp.lower()
    # 字符替换，是many2one字段，加id,是one2many,many2many字段，加ids
    field_type = data[2]
    if field_type == 'Many2one':
        data_temp_field += '_id'
    if field_type == 'Many2many' or field_type == 'One2many':
        data_temp_field += '_ids'
    if data[3]:
        attr += ', required = True'
    if data[4]:
        attr += ' ,readonly = True'
    if data[5]:
        attr += ', translate = True'
    if record:
        attr += ", track_visibility = 'onchange'"
    field_line = "    " + data_temp_field + " = fields." + field_type + '(string = "' + data[1] + '"' + attr + ')'
    field_list_dict[data[1]] = data_temp_field
    # print (field_list_dict)
    eng_ch_dict[data[1]] = data[0]
    new_dict = {v: k for k, v in eng_ch_dict.items()}

    print(field_line)
print('\n\n\n')

print("---------------------------以上是字段定义部分--------------------------")

# 阅读视图文件簿，生成视图部分的
table1 = data_sheet.sheets()[1]

view_model = model.replace('.', '_')
form_view_id = "view_" + view_model + "_form"
form_view_name = model + '.form'
tree_view_name = model + '.tree'
search_view_name = model + '.search'
table6 = data_sheet.sheets()[6]

# form 视图：
form_editable_ex = table1.row_values(1)
# print (form_editable_ex)
if form_editable_ex[5]:
    form_view_edit = '<form'
    namelist = ''

    if not form_editable_ex[0]:
        form_view_edit += ' edit="0"'
    if not form_editable_ex[1]:
        form_view_edit += ' delete="0"'
    if not form_editable_ex[2]:
        form_view_edit += ' create="0"'
    if form_editable_ex[3]:
        buttonx = """<div class="oe_button_box" name="button_box">
	                            <button name="toggle_active" type="object" class="oe_stat_button" icon="fa-archive">
	                                <field name="active" widget="boolean_button" options='{"terminology": "archive"}'/>
	                            </button>
	                        </div>"""
    else:
        buttonx = """"""
    if form_editable_ex[4]:
        namelist = """<div class="oe_title">
	                            <label for="name" class="oe_edit_only"/>
	                            <h1>
	                                <field name="name" class="oe_inline"/>
	                            </h1>
	                        </div>"""

    left_show = """"""
    right_show = """"""

    left_filed = []

    right_filed = []

    # 对字段进行转换
    if table1.nrows >= 3:
        left_filed = table1.row_values(3)

    if table1.nrows >= 5:
        right_filed = table1.row_values(3)
    if left_filed:
        for left_i in left_filed:
            if left_i:
                left_i = field_list_dict[new_dict[left_i]]
                if '_id' in left_i:
                    left_show += """<field name='""" + left_i + """' options="{'no_create_edit':True,'no_create':True,'no_open':1}"/>"""
                else:
                    left_show += """<field name='""" + left_i + """'/>"""
    if right_filed:
        for right_i in right_filed:
            if right_i:
                right_i = field_list_dict[new_dict[right_i]]
                if '_id' in right_i:
                    left_show += """<field name='""" + right_i + """' options="{'no_create_edit':True,'no_create':True,'no_open':1}"/>"""
                else:
                    right_show += """<field name='""" + right_i + """'/>"""

    record_view = """"""
    work_form_1 = work_form_2 = ''''''
    if table6.cell(34, 1).value:
        workflow_value = table6.cell(34, 1).value
        if workflow_value:
            work_form_1 = '''                    <header>
		                        <button name="action_submit" string="Submit" type="object"
		                                attrs="{'invisible':[('state','!=','created')]}" class="oe_highlight"/>
		                        <button name="action_to_draft" string="Set to Draft" type="object"
		                                attrs="{'invisible':['|',('state','!=','rejected'),('is_creator','=',False)]}"
		                                class="oe_highlight"/>
		                        <button name="action_cancel" string="Cancel" type="object"
		                                attrs="{'invisible':['|',('state','not in',('created','rejected','approved')),('is_creator','=',False)]}"
		                                class="oe_link"
		                                confirm="The order will be voided permanently if cancelled, are you sure?"/>
		                        <button name="action_withdraw" type="object" string="Withdraw"
		                                attrs="{'invisible':['|',('has_withdraw','=',False),('state','!=','submitted')]}"
		                                class="oe_highlight"/>
		                        <button name="action_approve_wizard" string="Approve" type="object"
		                                attrs="{'invisible': ['|','|',('approve_task_id', '=', False),('has_approve','=',False),('state','not in',('submitted','approving'))]}"
		                                class="oe_highlight"/>
		                        <button name="action_reject_wizard" type="object" string="Reject"
		                                attrs="{'invisible': ['|','|',('approve_task_id', '=', False),('has_reject','=',False),('state','not in',('submitted','approving'))]}"
		                                class="oe_highlight"/>
		                        <button name="action_transfer_wizard" type="object" string="Transfer"
		                                attrs="{'invisible': ['|','|',('approve_task_id', '=', False),('has_transfer','=',False),('state','not in',('submitted','approving'))]}"
		                                class="oe_highlight"/>
		                        <button name="action_return_wizard" type="object" string="Return"
		                                attrs="{'invisible': ['|','|',('approve_task_id', '=', False),('has_return','=',False),('state','not in',('submitted','approving'))]}"
		                                class="oe_highlight"/>
		                        <button name="action_complete" string="Complete" type="object"
		                                attrs="{'invisible':[('state','!=','processing')]}" class="oe_highlight"/>
		                        <field name="state" widget="statusbar"
		                               statusbar_visible="created,submitted,approving,approved"/>
		                    </header>
		
		                        '''
            work_form_2 = '''
		    <field name="is_creator" invisible="1"/>
		                        <field name="has_approve" invisible="1"/>
		                        <field name="has_reject" invisible="1"/>
		                        <field name="has_transfer" invisible="1"/>
		                        <field name="has_return" invisible="1"/>
		                        <field name="has_withdraw" invisible="1"/>
		                        <field name="approve_task_id" invisible="1"/>
		                        <field name="display_type" invisible="1"/>
		    '''

    if record:
        record_view = """<div class="oe_chatter">
	                        <field name="message_ids" widget="mail_thread"/>
	                    </div>"""

    form_view = """

	<record id='""" + form_view_id + """' model="ir.ui.view" >
	            <field name="name">""" + form_view_name + """</field>
	            <field name="model">""" + model + """</field>
	            <field name="arch" type="xml">""" + form_view_edit + """>""" + work_form_1 + """
	                    <sheet>
	                        """ + work_form_2 + buttonx + namelist + """
	                            <group>
	                                <group>
	                                   """ + left_show + """
	                                </group>
	                                <group>
	                                    """ + right_show + """
	                                </group>
	                            </group>

	                    </sheet>""" + record_view + """

	                </form>
	            </field>
	        </record>
    """

    print('-----以上是form 视图-----')

else:
    form_view = ''''''
# 以上部分是form视图




table2 = data_sheet.sheets()[2]

# 视图是否可编辑
filed_tree_editable = table2.row_values(1)
filed_tree = 0
if filed_tree_editable[4]:
    filed_tree = table2.row_values(2)

# 排序部分，待完善
# filed_tree_order = table2.row_values(3) 

# filed_tree_order_desc = table2.row_values(4) 


tree_view_id = "view_" + view_model + "_tree"

tree_show_con = ''
if filed_tree:
    for filed_t in filed_tree:
        if filed_t:
            filed_t = field_list_dict[new_dict[filed_t]]
            tree_show_con += """<field name='""" + filed_t + """'/>"""

tree_view_edit = ''
if not filed_tree_editable[0]:
    tree_view_edit += ' edit="0"'
if not filed_tree_editable[1]:
    tree_view_edit += ' delete="0"'
if not filed_tree_editable[2]:
    tree_view_edit += ' create="0"'
if not filed_tree_editable[3]:
    tree_view_edit += ' duplicate="0"'

tree_view = """

<record id='""" + tree_view_id + """' model="ir.ui.view" >
            <field name="name">""" + tree_view_name + """</field>
            <field name="model">""" + model + """</field>
            <field name="arch" type="xml">
            <tree""" + tree_view_edit + """>""" + tree_show_con + """</tree>
            </field>
        </record>"""
#
# # 以上视图是tree视图
#
if not filed_tree_editable[4]:
    tree_view = """"""

table3 = data_sheet.sheets()[3]

# 搜索部分
if not table3.cell(1, 5).value:
    search_view = """"""
else:
    search_view_id = "view_" + view_model + "_search"
    search_show_con = ''
    # print (eng_ch_dict)
    # print (field_list_dict)
    # print (new_dict)
    search_part = """"""
    for search in range(2, 12):
        if table3.row_values(search):
            fileld_x1 = table3.row_values(search)[0]
            if fileld_x1:
                search_ = """<field string='""" + new_dict[fileld_x1] + """' name='""" + field_list_dict[
                    new_dict[fileld_x1]] + """' filter_domain="[('""" + field_list_dict[
                              new_dict[fileld_x1]] + """','ilike', self)]"/>"""
                search_part += search_
    filter_part = """"""
    for filter in range(13, 24):
        if table3.row_values(filter):
            filter__x1 = table3.row_values(filter)[0]
            if filter__x1:
                filter_ = """<filter name = '""" + field_list_dict[new_dict[filter__x1]] + """' string = '""" + \
                          new_dict[
                              filter__x1] + """' domain = "[('""" + field_list_dict[
                              new_dict[filter__x1]] + """','=','value')]" />"""
                filter_part += filter_
    group_part = """<group string="Group By">"""
    # for group in range(27, 35):
    #     if table3.row_values(group):
    #         group_x1 = table3.row_values(group)[0]
    #         if group_x1:
    #             group_ = """<filter name='""" + field_list_dict[new_dict[group_x1]] + """' string='""" + new_dict[
    #                 group_x1] + """"' domain="[]" context="{'group_by':'""" + field_list_dict[
    #                          new_dict[group_x1]] + """'}"/>"""
    #             filter_part += group_
    group_part += """</group>"""
    search_show_con += search_part + filter_part + group_part
    # print (search_show_con)





    #
    #
    #
    search_view = """
    <record id='""" + search_view_id + """' model="ir.ui.view" >
                <field name="name">""" + search_view_name + """</field>
                <field name="model">""" + model + """</field>
                <field name="arch" type="xml">
                <search>"""+search_show_con + """</search>
                </field>
            </record>"""
# print (search_view)
# 以上视图是search视图


# search_view = """"""
# action_view = """
# """
#
# menu_view = """
#
#
#
# """
#
# # 以上视图是action和menu视图
#
#
all_view_file_before = """
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
"""

all_view_file_end = """

    </data>
</odoo>
"""

action = """
"""

# # 暂时不做action，menu,和search部分内容
all_view_file = all_view_file_before + form_view + tree_view+search_view + all_view_file_end
#
print(all_view_file)
#
# print("-----------------以上是视图部分-----------------------------")
# # 阅读权限文件簿，生成权限文件
#
#
#
#
#
#
table4 = data_sheet.sheets()[4]
nrows4 = 5

ser = 'access_kthrp_budget_budget_adjustment_line_budget_accountant,kthrp.budget.budget.adjustment.line,model_kthrp_budget_budget_adjustment_line,kthrp_account.group_budget_accountant,1,1,1,1'
print('\n\n')
for x in range(1, nrows4):
    dax = table4.row_values(x)
    if dax:
        access_ser = 'access_' + view_model + '_' + dax[0].replace('group_',
                                                                   '') + ',' + model + ',model_' + view_model + ',' + \
                     dax[1] + '.' + dax[0] + ',' + str(int(dax[2])) + ',' + str(int(dax[3])) + ',' + str(
            int(dax[4])) + ',' + str(int(dax[5]))
        print(access_ser)

# # 以上是权限文件

print('\n\n\n')
print('---------------以上是权限文件-------------')
#
table5 = data_sheet.sheets()[5]
#
nrows5 = table5.nrows

print('''<!-- 初始化数据-->\n\n\n''')
# if nrows5 > 1:
#     for xi in range(1, nrows5):
#         init_data = """"""
#         record_id = 'data_model_' +view_model+ str(xi)
#         print("""<record id='""" + record_id + """'  model = '""" + model + """'>""")
#         data_len = table5.row_values(xi)
#         length = len(data_len)
#
#         for x in range(int(length / 2)):
#             filed_namex = field_list_dict[new_dict[data_len[x * 2]]]
#             init_data = """<field name = '""" + filed_namex + """'>""" + str((data_len[x * 2 + 1])) + """</field>"""
#             print(init_data)
#         print("""</record>""")

print('''------------以上是初始化数据------------\n\n''')

# #. module: kthrp_asset_maintenance
# #: model:ir.model,name:kthrp_asset_maintenance.model_kthrp_asset_maintenance_work_order_type
# msgid "Kthrp Asset Maintenance Work Order Type"
# msgstr "工作单单据类型"

module_name = table0.row_values(0)[9] if table0.row_values(0)[9] else 'kthrp_base'

# 模型名：
print("""#. module: """ + module_name)
print("""#: model:ir.model,name:""" + module_name + """.model_""" + view_model)
print("""msgid '""" + all_des + """'""")
print("""msgstr '模型名'""")

# 字段名：
print('\n')

# #. module: kthrp_asset_maintenance
# #: model:ir.model.fields,field_description:kthrp_asset_maintenance.field_kthrp_asset_maintenance_work_order_type_auto_assign
# msgid "Auto Assign"
# msgstr "自动分配"
for key in field_list_dict:
    print("""#. module: """ + module_name)
    print(
        """#: model:ir.model.fields,field_description:""" + module_name + '.field_' + view_model + '_' +
        field_list_dict[
            key])
    print("""msgid '""" + key + """'""")
    print("""msgstr '""" + eng_ch_dict[key] + """'""")
    print('\n')

print('-------------以上是字段翻译，模型名需要修改，视图翻译暂时没加----------\n\n\n')

print('-------以下是一些初始化数据，用户组，菜单，快码，序列，记录规则，审批流（开始和结束节点）-----')

print('---用户组初始化---')
"""
        <!--初始化用户组：资产申请处理-->
        <record id="group_apply_process_limit" model="res.groups">
            <field name="name">Asset Apply Process Limit</field>
            <field name="category_id" ref="kthrp_base.module_category_function_limit"/>
            <field name="classification">function_access</field>
            <field name="users" eval="[(4,ref('base.user_root'))]"/>
        </record>

"""

table6_row = table6.nrows

group_init = table6.cell(0, 1).value
if group_init:
    for row in range(1, 3):
        if table6.row_values[row]:
            group_name = table6.cell(row, 0).value.lower().replace(' ', '_')
            print('<record id ="' + group_name + '" model="res.groups"')
            print('<field name="name">' + table6.cell(row, 0).value + '</field>')
            print('<field name="category_id" ref="' + table6.cell(row, 1).value + '</field>')
            print('<field name="classification">' + table6.cell(row, 2).value + '</field>')
            print('<field name="comment">' + table6.cell(row, 3).value + '</field>')

'''

        <record id="action_kthrp_budget_budget_recruitment" model="ir.actions.act_window">
            <field name="name">Recruitments</field>
            <field name="res_model">kthrp.budget.recruitment</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="context">{'search_default_unprocessed':1}</field>
        </record>

        <menuitem id="menu_kthrp_budget_budget_recruitment"
                  name="Recruitments"
                  sequence="10"
                  parent="kthrp_budget.menu_kthrp_budget_budgeting"
                  action="action_kthrp_budget_budget_recruitment"
        />
'''
print('\n\n')
print('''<!-- 菜单数据需要填充-->\n\n\n''')
menu_init = table6.cell(4, 1).value
if menu_init:
    for row_menu in range(4, 9):
        if table6.cell(row_menu, 0).value:
            print('<menuitem id="menu_' + view_model + '_' + normalize(table6.cell(row_menu, 0).value).replace(' ',
                                                                                                               '_').replace(
                '.', '') + '"')
            print('name="' + table6.cell(row_menu, 0).value + '"')
            print('sequence="' + str(int(table6.cell(row_menu, 1).value)) + '"')
            print('parent=""')
            print('action=""')
            print('/>')
print('\n\n')
print('--------以下是快码内容----------')

look_up_value = table6.cell(9, 1).value
if look_up_value:
    temp_lookup_type = table6.cell(10, 0).value.lower().replace(' ', '_')
    type_id = 'type_' + temp_lookup_type
    print('<record model="kthrp.base.lookup.type"  id="' + type_id + '">')
    print("""<field name="code" eval="'""" + temp_lookup_type + """'"/>""")
    print("""<field name="name" eval="'""" + table6.cell(11, 0).value + """'"/></record>""")

    for row_menu in range(11, 22):
        if row_menu:
            temp_lookup_value = table6.cell(row_menu, 0).value.lower().replace(' ', '_')
            value_id = 'type_' + temp_lookup_value
            print('<record model="kthrp.base.lookup.value"  id="' + value_id + '">')
            print("""<field name="code" eval="'""" + temp_lookup_value + """'"/>""")
            print("""<field name="name" eval="'""" + table6.cell(row_menu, 0).value + """'"/>""")
            print("""<field name="lookup_type_id" ref="'""" + type_id + """'"/></record>""")

print('\n\n')
print('-----------以下是初始化序列的内容--------')
sequence_value = table6.cell(22, 1).value
if sequence_value:
    for sqx in range(23, 29):
        # print(table6.row_values(sqx))
        if table6.row_values(sqx)[0]:
            sequence_name = table6.cell(sqx, 0).value
            sequence_id = 'sequence_' + module_name + '_' + sequence_name.lower().replace(' ', '_')
            print('<record id="' + sequence_id + '"' + ' model="ir.sequence">')
            print('<field name="name">' + table6.cell(sqx, 0).value + '</field>')
            print('<field name="code">' + table6.cell(sqx, 1).value + '</field>')
            print('<field name="prefix">' + table6.cell(sqx, 2).value + '</field>')
            print('<field name="padding">' + str(int(table6.cell(sqx, 3).value)) + '</field>')
            print('<field name="number_per_year">' + str(
                table6.cell(sqx, 4).value.replace('Y', '1').replace('N', '0')) + '</field>')
            print('<field name="number_per_month">' + str(
                table6.cell(sqx, 5).value.replace('Y', '1').replace('N', '0')) + '</field>')
            # print('<field name="note">' + str(table6.cell(sqx, 6).value) + '</field>')
            # print('<field name="company_id">' + str(int(table6.cell(sqx, 7).value)) + '</field>')
            print('</record>\n')
print('\n\n')
print('--------------以下是审批流-------')

workflow_value = table6.cell(34, 1).value
if workflow_value:
    workflow_model_id = 'workflow_model_' + module_name + '_' + view_model
    workflow__id1 = 'workflow_' + module_name + '_' + view_model
    workflow__id_start = workflow__id1 + '_line_start'
    workflow__id_end = workflow__id1 + '_line_end'
    print(' <record id="' + workflow_model_id + '" model="' + model + '">')
    print('<field name="name">' + all_des + '</field>')
    print("""<field name="model_id" eval=" ref('""" + module_name + '.model_' + view_model + """')"/>""")
    print('</record>\n')
    print('''<record id="''' + workflow__id1 + '''" model="kthrp.base.workflow">''')
    print('''<field name="name">''' + all_des + '''</field>''')
    print("""<field name="wkf_model_id" eval=" ref('""" + module_name + '.model_' + view_model + """')"/>""")
    print('''<field name="sequence" eval="11"/>
        <field name="is_init" eval="True"/>
        <field name="withdraw" eval="True"/>
    </record>\n''')
    print('''<record id="''' + workflow__id_start + '''" model="kthrp.base.workflow.line">''')
    print(
        """<field name="name">Workflow Start</field>        <field name="model_id" eval="ref('""" + workflow__id1 + """')"/>""")

    print('''        <field name="sequence" eval="10"/>
        <field name="approver_type" eval="False"/>
        <field name="node_type">start</field>
    </record>\n''')
    print('''<record id="''' + workflow__id_end + '''" model="kthrp.base.workflow.line">''')
    print(
        """<field name="name">Workflow End</field> <field name="name">Workflow End</field>        <field name="model_id" eval="ref('""" + workflow__id1 + """')"/>""")
    print(
        """<field name="sequence" eval="100"/>        <field name="approver_type" eval="False"/>        <field name="node_type">end</field>    </record>\n""")

    print('------感谢使用，欢迎提出改进意见-------\n\n')
