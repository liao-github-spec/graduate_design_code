import json
from py2neo import Graph, Node
import matplotlib.pyplot as plt

class MedicalGraph:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="lg789123")

    def create(self):
        with open('relationships.json', 'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)

        for data in load_dict:
            for relationships in data["relationships"]:
                # relationship属性
                relationship_id = relationships["relationship_id"]
                predicate = relationships["predicate"]
                synsets = relationships["synsets"]

                # object属性
                object_id = relationships["object"]["object_id"]
                # 不存在该属性就赋为空值
                if('name' in relationships['object'].keys()):
                    object_name = relationships["object"]["name"]
                else:
                    object_name = ""
                object_synsets = []
                for object_synset in relationships["object"]["synsets"]:
                    object_synsets.append(object_synset)

                # subject属性
                subject_id = relationships["subject"]["object_id"]
                # 不存在该属性就赋为空值
                if('name' in relationships['subject'].keys()):
                    subject_name = relationships["subject"]["name"]
                else:
                    subject_name = ""
                subject_synsets = []
                for subject_synset in relationships["subject"]["synsets"]:
                    subject_synsets.append(subject_synset)

                # 读入测试
                # print("======================")
                # print(relationship_id)
                # print("======================")
                # print(predicate)
                # print("======================")
                # print(synsets)
                # print("======================")
                # print(object_id)
                # print("======================")
                # print(object_name)
                # print("======================")
                # print(object_synsets)
                # print("======================")
                # print(subject_id)
                # print("======================")
                # print(subject_name)
                # print("======================")
                # print(subject_synsets)
                # print("======================")

                # 建立查询语句
                query1 = 'merge (object:Object{ object_id:"%s",name:"%s", synsets:"%s"})' % \
                         (object_id, object_name, object_synsets)
                query2 = 'merge (subject:Subject{ subject_id:"%s", name:"%s", synsets:"%s"})' % \
                         (subject_id, subject_name, subject_synsets)
                query3 = 'match (ob:%s),(sub:%s) where ob.name="%s" and sub.name="%s"' \
                         ' create (ob)-[rel:%s {predicate:"%s", relationship_id:"%s", synsets:"%s"}]->(sub)' \
                         % ("Object", "Subject", object_name, subject_name, "Relationship", predicate,
                            relationship_id, synsets)

                # 打印查询语句
                # print(query1)
                # print(query2)
                # print(query3)

                # 读入到neo4j中
                try:
                    self.g.run(query1)
                    self.g.run(query2)
                    self.g.run(query3)
                except Exception as e:
                    print(e)


    def drawCounts(self):
        with open('relationships.json', 'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)

        # 出现种类
        syn_rel = []
        pre_rel = []
        # 出现频率
        syn_rel_cnt = dict()
        pre_rel_cnt = dict()

        for data in load_dict:
            for relationships in data["relationships"]:
                # relationship属性
                predicate = relationships["predicate"]
                synsets = relationships["synsets"]

                # 统计relationship中的属性predicate和synsets的频率
                for synset in synsets:
                    # 统计出现种类
                    if synset not in syn_rel:
                        syn_rel.append(synset)
                    # 统计出现频率
                    if synset not in syn_rel_cnt.keys():
                        syn_rel_cnt[synset] = 1
                    else:
                        syn_rel_cnt[synset] = syn_rel_cnt[synset] + 1

                # 统计出现种类
                if predicate not in pre_rel:
                    pre_rel.append(predicate)
                # 统计出现频率
                if predicate not in pre_rel_cnt.keys():
                    pre_rel_cnt[predicate] = 1
                else:
                    pre_rel_cnt[predicate] = pre_rel_cnt[predicate] + 1

        # 打印种类和频率
        # print(pre_rel_cnt)
        # print(syn_rel_cnt)

        # 给数据排序
        # 排序predicate
        pre_sorted_all = sorted(pre_rel_cnt.items(), key=lambda x:x[1], reverse=True)
        pre_sorted_first100 = pre_sorted_all[:25]
        # 打印predicate排序结果
        # print(pre_sorted_first100)

        # 排序synsets
        syn_sorted_all = sorted(syn_rel_cnt.items(), key=lambda x: x[1], reverse=True)
        syn_sorted_first100 = syn_sorted_all[:25]
        # 打印synsets排序结果
        # print(syn_sorted_first100)

        # 绘制频率直方图
        # predicate直方图
        pre_x = []
        pre_y = []
        for pre in pre_sorted_first100:
            pre_x.append(pre[0])
            pre_y.append(pre[1])
        plt.barh(pre_x[0:25], pre_y[0:25])
        plt.show()
        # synsets直方图
        syn_x = []
        syn_y = []
        for syn in syn_sorted_first100:
            syn_x.append(syn[0])
            syn_y.append(syn[1])
        # 默认figsize=(6, 3),控制画布大小
        plt.figure(dpi=600, figsize=(12, 6))
        plt.xlabel('', fontdict={"family": "Times New Roman", "style": "italic"})
        plt.ylabel('', fontdict={"family": "Times New Roman", "style": "italic"})
        # plt.ylabel('出现次数', fontdict='Times New Roman')

        plt.barh(syn_x[0:25], syn_y[0:25])
        plt.savefig("t1.pdf", bbox_inches='tight')
        plt.show()


if __name__ == '__main__':

    handler = MedicalGraph()
    handler.drawCounts()
