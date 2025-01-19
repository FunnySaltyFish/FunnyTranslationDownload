import requests
import datetime

def add_sponsor():
  text = """
  *洋
  加油
  2023-01-28 09:28:11
  万能膏
  加油[,!
  2023-02-09 12:10:04
  小孟
  加油
  2023年2月5日23:10:38
  666

  """
  datas = [
    {
      "name": "小孟",
      "message": "加油",
      "date": "2023-02-05 23:10:38",
      "money": 666
    },
  ]

  for data in datas:
    r=requests.post("https://api.funnysaltyfish.fun/trans/v1/sponsor/add",data, proxies={
      "http": "http://127.0.0.1:10809",
      "https": "http://127.0.0.1:10809"
    })
    print(r.text)

def update_apk():
  data = {
    "version_code":27,
    "version_name":"Beta",
  }
  files = {
    "apk":open("D:\\projects\\AppProjects\\Mine\\FunnyTranslation\\translate\\release\\translate-release.apk","rb")
  }
  
  header = {
    "Content-Type":"multipart/form-data;"
  }
  r=requests.post("https://api.funnysaltyfish.fun/trans/v1/app_update/add_new_version",headers=header,data=data,files=files)
  print(r.text)

# update_apk()
add_sponsor()
