#! /usr/bin/env python
import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.common.by import By
import chromedriver_binary
import urllib.request
import pandas as pd
import sys
import time
import re
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

input_path = sys.argv[1] 
parameter = sys.argv[2]

output_path = 'output_1.txt'
output_path2 = 'output_2.txt'
output_file = 'output_1_1.txt'
output_file2 = 'output_3.txt'
summary_file = 'output_5.txt'
summary_file_tmp = 'output_5_1.txt'

output_path3 = 'test_deeploc.txt'
output_path3_1 = 'test_deeploc.txt.txt'
output_file3 = 'test_deeploc_file.txt'
output_file4 = 'test_targetp_file.txt'
summary_file2 = 'output_6.txt'

end_file = "tool_test.txt"

page_path = r"/html/body/div[2]/table[1]/tbody/tr[2]/td[3]/button"
page_path2 = r"/html/body/pre"

def readlines_file(file_name):
    # 行毎のリストを返す
    with open(file_name, 'r') as file:
        return file.readlines()

def save_file(file_name, text):
    with open(file_name, 'w') as file:
        file.write(text)

t1 = time.time() 

  # Chromeを準備
url = 'http://mitf.cbrc.jp/MitoFates/cgi-bin/top.cgi' 
driver.get(url)      # Mitofatesを開く
search = driver.find_element_by_name('query')          # HTML内で検索ボックス(name='query')を指定する
with open(input_path) as f:
    s = f.read()
    search.send_keys(s)             # 検索ワードを送信する
    organism_element = driver.find_element_by_name('organism')
    organism_select_element = Select(organism_element)
    if re.match(parameter,'fungi'):
        organism_select_element.select_by_value('fungi')
    elif re.match(parameter,'metazoa') or re.match(parameter,'Amoebozoa') or re.match(parameter,'other'):
        organism_select_element.select_by_value('metazoa')
    elif re.match(parameter,'plant') or re.match(parameter,'SAR') or re.match(parameter,'Euglena'):
        organism_select_element.select_by_value('plant')

    search.submit()                             # 解析を実行
    cur_url = driver.current_url
    
    driver.implicitly_wait(120)
    btn = driver.find_element_by_xpath(page_path)
    btn.click()

    driver.implicitly_wait(120)
    output_txt = driver.find_element_by_xpath(page_path2).text

    with open(output_path, 'w') as g:
        g.write(output_txt)

    t2 = time.time()

elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")
print("MitoFatesページロード完了")

if __name__ == '__main__':
    tag_name ='Sequence ID Probability of presequence Prediction Cleavage site (processing enzyme) Net charge Positions for TOM20 recognition motif (deliminated by comma) Position of amphypathic alpha-helix BHHPPP BPHBHH HBHHBb HBHHbB HHBHHB HHBPHB HHBPHH HHBPHP HHHBBH HHHBPH HHHHBB HHPBHH HPBHHP PHHBPH'
    
    with open(output_path) as f:
        body = f.read()
        before_1 = body.replace(tag_name,'')
        before_2 = re.sub("^\n","",before_1)
        before_3 = re.sub(" No mitochondrial presequence.*\n","\n",before_2)
        before_4 = re.sub("\tNo mitochondrial presequence.*\n","\n",before_3)
        before_5 = re.sub(" Possessing mitochondrial presequence.*\n","\n",before_4)
        before_6 = re.sub("\tPossessing mitochondrial presequence.*\n","\n",before_5)
        before_7 = re.sub("Possessing mitochondrial presequence.*$","",before_6)
        before_8 = re.sub("presequence\n\n","presequence\n",before_7)
        before_9 = re.sub(".* 0.","0.",before_8)
        before_10 = re.sub(".*\t0.","0.",before_9)
        before_11 = re.sub(".* 1.","1.",before_10)
        before_12 = re.sub(".*\t1.","1.",before_11)
        before_13 = before_12.replace("\n\n","\n")
        string = before_13[:-1].split("\n")

        with open(output_file, 'w') as g:
            for val in string:
                if float(val)>=0.5:
                    g.write("Possessing_mitochondrial_presequence"+"\n")
                    t3 = time.time()
                    elapsed_time = t3-t2
                    print(f"Mitofates処理時間：{elapsed_time}")
                else:
                    g.write("No_mitochondrial_presequence"+"\n")
                    t3 = time.time()
                    elapsed_time = t3-t2
                    print(f"Mitofates処理時間：{elapsed_time}")

url = 'http://crdd.osdd.net/raghava/marspred/submit.php' 
driver.get(url)      # MARSpredを開く

search = driver.find_element_by_name('seq')          # HTML内で検索ボックス(name='seq')を指定する
#search.send_keys('>test1[Homo Sapoens]\nMAAAAAAAAAASSASKHGGS\n>test2[Homo Sapoens]\nMSGHHAAASHAAHTR')             # 検索ワードを送信する
with open(input_path) as f:
    s = f.read()
    search.send_keys(s+"\n>")             # 検索ワードを送信する  
    search.submit()                             # 解析を実行
    time.sleep(10)
    cur_url = driver.current_url
    output_table = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/div/div/div/div/div/center/table").text

    with open(output_path2, 'w') as g:
        g.write(output_table)
        t4 = time.time()
        elapsed_time = t4-t3
        print("MARSpredページロード完了 "+f"経過時間：{elapsed_time}")
    driver.close()
    driver.quit()
    print("ページロード完了")

if __name__ == '__main__':
    before_str ='Sequence Name\nMARSpred Prediction\nMARSpred Score\n'
    after_str =''
    before_seq = '>.{9,10}'
    after_seq = ''
    before_words = ' AARS\n'
    after_words = ' AARS '
    before_delete = '\n\n'
    after_delete = '\n'

    with open(output_path2) as f:
        body = f.read()
        before_1 = re.sub(before_str, after_str, body, flags=re.DOTALL)
        before_2 = re.sub(before_seq, after_seq, before_1, flags=re.DOTALL)
        before_3 = re.sub(before_words, after_words, before_2, flags=re.DOTALL)
        before_4 = re.sub(before_delete, after_delete,before_3,flags=re.DOTALL)
        before_5 = re.sub("Mitochondrial AARS ","",before_4,flags=re.DOTALL)
        before_6 = re.sub("Cytosolic AARS ","",before_5,flags=re.DOTALL)
        string = before_6.split("\n")

        with open(output_file2, 'w') as g:
            for val in string:
                if float(val)>=0:
                    #g.write("Possessing_mitochondrial_presequence:"+val+"\n")
                    g.write("Mitochondrial AARS"+"\n")
                    t5 = time.time()
                    elapsed_time = t5-t4
                    print(f"MARSpred処理時間：{elapsed_time}")
                else:
                    #g.write("No_mitochondrial_presequence:"+val+"\n")
                    g.write("Cytosolic AARS"+"\n")
                    t5 = time.time()
                    elapsed_time = t5-t4
                    print(f"MARSpred処理時間：{elapsed_time}")
    
# 読み込んだファイルをlist型で受け取る
cal1 = readlines_file(output_file)
cal2 = readlines_file(output_file2)

# 改行や空白文字を削除
cal1 = list(map(lambda x: x.strip(), cal1))
cal2 = list(map(lambda x: x.strip(), cal2))

# タブ区切りで並べたリストを作成
lines = ["{0},{1}".format(line1, line2)+"\n" for line1, line2 in zip(cal1, cal2)]

save_file(summary_file, "".join(lines))

with open(summary_file,"r") as h:
    body = h.read()
    line = re.sub(" AARS .*\n","_AARS\n",body)
    with open(summary_file_tmp,"w") as k:
        k.write(line)

t6 = time.time()
elapsed_time = t6-t5
print(f"統合処理1回目の時間：{elapsed_time}")
print("web解析完了")

os.system("deeploc -f "+input_path+" -o "+output_path3)#subprocess.call(["deeploc -f "+input_path+" -o "+output_path_d])

if __name__ == '__main__':
    tag_name_dl ='ID\tLocation\tMembrane\tNucleus\tCytoplasm\tExtracellular\tMitochondrion\tCell_membrane\tEndoplasmic_reticulum\tPlastid\tGolgi_apparatus\tLysosome/Vacuole\tPeroxisome\n'
 
    with open(output_path3_1,"r") as f:
        body = f.read()
        before_1 = re.sub(tag_name_dl,"", body, flags=re.DOTALL)
        before_2 = re.sub("Mitochondrion\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Mitochondrion\n", before_1, flags=re.DOTALL)
        before_3 = re.sub("Cytoplasm\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Cytoplasm\n", before_2, flags=re.DOTALL)
        before_4 = re.sub("Nucleus\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Cytoplasm\n", before_3, flags=re.DOTALL)
        before_5 = re.sub("Endoplasmic_reticulum\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Plastid\n", before_4, flags=re.DOTALL)
        before_6 = re.sub("Cell_membrane\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Other\n", before_5, flags=re.DOTALL)
        before_7 = re.sub("Extracellular\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Other\n", before_6, flags=re.DOTALL)
        before_8 = re.sub("Golgi_apparatus\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Other\n", before_7, flags=re.DOTALL)
        before_9 = re.sub("Lysosome/Vacuole\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Other\n", before_8, flags=re.DOTALL)
        before_10 = re.sub("Peroxisome\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Other\n", before_9, flags=re.DOTALL)
        before_11 = re.sub("Plastid\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\t0.{1,5}\n","Plastid\n", before_10, flags=re.DOTALL)        
        before_12 = re.sub("\n.*\t","\n",before_11)
        before_13 = re.sub(".*\t","",before_12)
        
        with open(output_file3, 'w') as g:
            g.write(before_13)
            t7 = time.time()
            elapsed_time = t7-t6
            print(f"経過時間：{elapsed_time}"+" DeepLoc完了")

if re.match(parameter,'plant') or re.match(parameter,'SAR') or re.match(parameter,'Euglena'):
    os.system("targetp -fasta "+input_path+" org pl -format short") #subprocess.call(["targetp -fasta "+input_path+" org pl -format short"])
    t8 = time.time()
    elapsed_time5 = t8-t7
    print(f"経過時間：{elapsed_time5}"+" TargetP完了")

elif re.match(parameter,'fungi') or re.match(parameter,'metazoa') or re.match(parameter,'Amoebozoa') or re.match(parameter,'other'):
    os.system("targetp -fasta "+input_path+" org non-pl -format short")#subprocess.call(["targetp -fasta "+input_path+" org non-pl -format short"])
    t8 = time.time()
    elapsed_time5 = t8-t7
    print(f"経過時間：{elapsed_time5}"+" TargetP完了")

if __name__ == '__main__':
     
    with open("test_summary.targetp2","r") as f:
        body = f.read()
        before_1 = re.sub("# TargetP-2.0\tOrganism: Non-Plant\tTimestamp: \d{14}\n# ID\tPrediction\tnoTP\tSP\tmTP\tCS Position\n","",body)
        before_2 = re.sub("mTP\t.*\n","mTP\n",before_1)
        before_3 = re.sub("mTP\t.*","mTP",before_2)
        before_4 = re.sub("SP\t.*\n","SP\n",before_3)
        before_5 = re.sub("noTP\t.*\n","noTP\n",before_4)
        before_6 = re.sub("SP\t.*","SP",before_5)
        before_7 = re.sub("noTP\t.*","noTP",before_6)
        before_8 = re.sub(".*\t","",before_7)
        
        with open(output_file4, 'w') as g:
            g.write(before_8)
            t9 = time.time()
            elapsed_time = t9-t8
            print(f"経過時間：{elapsed_time}"+" TargetP完了")

cal3 = readlines_file(output_file3)
cal4 = readlines_file(output_file4)

# 改行や空白文字を削除
cal3 = list(map(lambda x: x.strip(), cal3))
cal4 = list(map(lambda x: x.strip(), cal4))

# タブ区切りで並べたリストを作成
lines = ["{0},{1}".format(line1, line2)+"\n" for line1, line2 in zip(cal3, cal4)]

save_file(summary_file2, "".join(lines))

cal5 = readlines_file(summary_file)
cal6 = readlines_file(summary_file2)

# 改行や空白文字を削除
cal5 = list(map(lambda x: x.strip(), cal5))
cal6 = list(map(lambda x: x.strip(), cal6))

# タブ区切りで並べたリストを作成
lines = ["{0},{1}".format(line1, line2)+"\n" for line1, line2 in zip(cal5, cal6)]

save_file(end_file, "".join(lines))

t10 = time.time()
elapsed_time = t10-t9
print(f"経過時間：{elapsed_time}"+" 解析完了")
