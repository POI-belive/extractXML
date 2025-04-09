import xml.etree.ElementTree as ET
import csv
from io import StringIO
from os import write



#从XML当中提取弹幕
def extract_xml(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        return [d.text for d in root.findall('d') if d.text]
    except ET.ParseError as e:
        print(f"XML解析错误: {e}")
        return []

#将弹幕写入CSV文件
def save_csv(text_list,csv_file_path):
    with open(csv_file_path,'w',newline='',encoding='GBK') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(["序号","弹幕内容"])  #表头
        for idx,text in enumerate(text_list,1):
            writer.writerow([idx,text])

if __name__ == '__main__':
    xml_file_path = "D://pythonFile//del_xml//test.xml"
    csv_file_path="D://pythonFile//del_xml//danmu.csv"

    text_list=extract_xml(xml_file_path)
    save_csv(text_list,csv_file_path)

    print(extract_xml(xml_file_path))