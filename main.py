from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# 가장최근 추첨회수를 구한다.
url = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin'
with urlopen(url) as doc:
    html = BeautifulSoup(doc,'lxml')
    descrip = html.find('meta',id='desc')
    s = int(descrip.attrs['content'].split(" ")[1].replace('회',''))

# 데이터를 획득하여 pandas에 DataFrame 으로 만든다.
xlsfile = 'https://www.dhlottery.co.kr/gameResult.do?method=allWinExel&gubun=byWin&nowPage=1&drwNoStart=1&drwNoEnd={}'.format(s)
df = pd.DataFrame(pd.read_html(xlsfile,skiprows=2,index_col=1)[0])
df.drop(columns=[0,2,3,4,5,6,7,8,9,10,11,12],inplace=True)
df.sort_index(ascending=False)
df.columns = ['1','2','3','4','5','6','7']

# dict 타입변수에 각 숫자별로 발생빈도를 카운드한다.
stats = {}
for idx, row in df.iterrows() :
    for i in range(1,7) :
        if stats.get(str(row[i])) == None :
            stats[str(row[i])] = 1
        else :
            stats[str(row[i])] = stats[str(row[i])] + 1

# 발생빈도를 소트한다.
maxvalues = list(stats.values())
maxvalues.sort()
# print(stats)

# 발생빈도가 높은 번호를 List에 담아서 출력한다. 발생빈도 상위 10개정도만 대상으로함
rtlist = list()
for x in stats :
    if  stats[x] in maxvalues[-10:-1] :
        rtlist.append(x)

# print(rtlist)

for x in rtlist :
    if  x in stats.keys() :
        print('{} : {}'.format(x,stats[x]))
