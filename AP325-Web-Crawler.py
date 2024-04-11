import requests
from bs4 import BeautifulSoup as BS

# 增加 http header user-agent 讓網站以為是正常的瀏覽使用者
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

# 輸出格式為 Markdown 的表格樣式
print('| Judge 題號 | 講義題號 | 題目名稱與連結 |')
print('| --------- | --------| ------------ |')

# 題目列表有 1 ~ 6 頁
for page in range(1,7):
    
    # 欲爬取的網頁網址
    url = f'https://judge.tcirc.tw/Problems?page={page}&&tabid=AP325'
    
    # 發出 HTTP GET request
    resp = requests.get(url, headers=headers)
    
    # 設定編碼為 utf-8
    resp.encoding = 'utf-8'
    
    # 解析原始碼
    soup = BS(resp.text,'html.parser')
    
    # 找尋所有題目
    problems = soup.find_all('a')
    
    # 遍歷每個題目提取重要的元素
    for problem in problems:
        
        # 過濾 只讀題目部分
        if 'ShowProblem' in problem['href']:
            
            # -- 預處理 --
            
            # 輸出確認是否為我們最終要的元素
            # print(problem)
            # <a href="./ShowProblem?problemid=d001" title="[Recursion]">例題 P-1-1. 合成函數(1)</a>
            
            # 去除空白
            problem_text = problem.text.strip()
            
            # 刪除前面的 例題 or 習題 文字 使格式統一
            if(problem_text[1] == '題'):
                problem_text = problem_text[3:]
                
            # 將題目編號與題目名稱以空白字元切割
            problem_text = problem_text.split(' ',1)
            
            # -- 提取元素 --
            
            # 取得題目編號 刪掉後面的 . 字元
            problem_number = problem_text[0][:-1]
            
            # 取得題目名稱
            problem_title = problem_text[1]
            
            # 取得題目連結 刪掉前面的 . 字元 
            problem_link = problem['href'][1:]
            
            # 取得 Judge 題號
            judge_number = problem['href'][-4:]
            
            # ----
            
            # 格式化輸出
            print(f"| {judge_number} | {problem_number} | [{problem_title}](https://judge.tcirc.tw{problem_link}) |")