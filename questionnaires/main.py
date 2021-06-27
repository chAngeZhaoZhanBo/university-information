# encoding = utf-8
import os
import csv


QUESTIONAIRE = ["宿舍是上床下桌吗？", "教室和宿舍有没有空调？", "有独立卫浴吗？没有独立浴室的话，澡堂离宿舍多远？", "有早自习、晚自习吗？", "有晨跑吗？",
                 "每学期跑步打卡的要求是多少公里，可以骑车吗？", "寒暑假放多久，每年小学期有多长？", "学校允许点外卖吗，取外卖的地方离宿舍楼多远？", "学校交通便利吗，有地铁吗，在市区吗，不在的话进城要多久？",
                 "宿舍楼有洗衣机吗？", "校园网怎么样？", "每天断电断网吗，几点开始断？", "食堂价格贵吗，会吃出异物吗？", "洗澡热水供应时间？", "校园内可以骑电瓶车吗，电池在哪能充电？",
                 "宿舍限电情况？", "通宵自习有去处吗？", "大一能带电脑吗？", "学校里面用什么卡，饭堂怎样消费？", "学校会给学生发银行卡吗？", "学校的超市怎么样？", "学校的收发快递政策怎么样？",
                 "学校里面的共享单车数目与种类如何？", "现阶段学校的门禁情况如何？", "宿舍晚上查寝吗，封寝吗，晚归能回去吗？"]

WHETHER_SHARE_MAIL_CSV_COL = 2
MAIL_CSV_COL = 3
WHETHER_MAKE_MAIL_PUBLIC_CSV_COL = 4
SCHOOL_NAME_CSV_COL = 5
REAL_QUESTION_START_CSV_COL = 6
MORE_THING_TO_SAY_CSV_COL = REAL_QUESTION_START_CSV_COL + len(QUESTIONAIRE)

SCHOOL_NAME_LINE = 0
DATA_SRC_LINE = 1
REAL_QUESTION_START_LINE = 2
MORE_THING_TO_SAY_LINE = 2 + len(QUESTIONAIRE)
TOTAL_DOC_LINE_CNT = len(QUESTIONAIRE) + 3      # school_name + data_src + questions + more_thing_to_say

def IsAnonymous(row):
    return int(row[WHETHER_SHARE_MAIL_CSV_COL]) == 2 or float(row[WHETHER_MAKE_MAIL_PUBLIC_CSV_COL]) == 2.0 or str(row[MAIL_CSV_COL]) == ''



with open('results_desensitized.csv', 'r', encoding="gb18030") as csv_file:
    csv_reader = csv.reader(csv_file)
    school_to_result = dict()
    next(csv_reader)  # here we skip the first line
    for row in csv_reader:
        school_name = row[SCHOOL_NAME_CSV_COL]
        try:
            school_result = school_to_result[school_name]
            if IsAnonymous(row):
                school_result[DATA_SRC_LINE].append(" + 匿名数据")
            else:
                school_result[DATA_SRC_LINE].append(f" + 来自 {row[MAIL_CSV_COL]} 的数据")
        except KeyError:
            school_result = [list() for _ in range(TOTAL_DOC_LINE_CNT)]
            school_result[SCHOOL_NAME_LINE] = [f"# {school_name}\n\n"]
            school_to_result[school_name] = school_result
            if IsAnonymous(row):
                school_result[DATA_SRC_LINE].append("> 匿名数据")
            else:
                school_result[DATA_SRC_LINE].append(f"> 来自 {row[MAIL_CSV_COL]} 的数据")


        for csv_index in range(REAL_QUESTION_START_CSV_COL, REAL_QUESTION_START_CSV_COL + len(QUESTIONAIRE)):
            question_index = csv_index - REAL_QUESTION_START_CSV_COL
            result_index = question_index + REAL_QUESTION_START_LINE
            if len(school_result[result_index]) == 0:
                school_result[result_index].append(f"\n\n## Q: {QUESTIONAIRE[question_index]}")
            school_result[result_index].append(f"\n\n- A{len(school_result[result_index])}: {row[csv_index]}")

        
        if row[MORE_THING_TO_SAY_CSV_COL] != '':
            if len(school_result[MORE_THING_TO_SAY_LINE]) == 0:
                school_result[MORE_THING_TO_SAY_LINE].append("\n\n# 关于学校的评价")
            school_result[MORE_THING_TO_SAY_LINE].append("\n\n***")
            school_result[MORE_THING_TO_SAY_LINE].append(f"\n\n{row[MORE_THING_TO_SAY_CSV_COL]}")

    with open("README.md", 'w', encoding="utf-8") as output_readme_file:
        readme_template_file = open("README_template.md", 'r', encoding="utf-8")
        output_readme_file.write(readme_template_file.read())
        readme_template_file.close()
        readme_school_link_list = []
        try:
            os.mkdir("universities")
        except FileExistsError:
            pass
        for school_name, school_result in school_to_result.items():
            school_name = school_name.replace(' ', '').replace('/', '')
            with open(f"universities/{school_name}.md", 'w', encoding="utf-8") as output_item_file:
                for school_line in school_result:
                    output_item_file.write("".join(school_line))
                    output_item_file.write("")
            readme_school_link_list.append(f"\n\n[{school_name}](./universities/{school_name}.md)")
        readme_school_link_list.sort()
        output_readme_file.write("".join(readme_school_link_list))
