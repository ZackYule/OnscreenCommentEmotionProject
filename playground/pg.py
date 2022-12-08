from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '28550310'
API_KEY = '2rf9CRp3orfk0TUxBIRo6hOS'
SECRET_KEY = 'sRMkj2002MBGMC31bbN3qgtZpiis5Twi'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

text="以前约过一个电子系妹子, 之前和妹子关系都挺好的 约出去一切也很正常, 直到不知怎么问起GPA.  我说我GPA不行, 只有多少多少. (大概略高于平均吧) 她哦了一声, 说她有多少多少(反正比我高很多, 她貌似是他们系前几名) 从此以后她再也没理过我.  "

result=client.sentimentClassify(text)

print(type(result))

print(result)