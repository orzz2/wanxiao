import time,json,requests,random,datetime
from campus import CampusCard

def main():
    #sectets字段录入

    
    #变变变
    print("start") 
    print(users) 
    users = input()
    print(users) 
    print("eend") 
    #定义变量
    success,failure=[],[]
    #sectets字段录入
    phone, password, sckey = [], [], []
    #多人循环录入
    # while True:  
    #     try:
    #
    #         users = input()
    #         info = users.split(',')
    #         phone.append(info[0])
    #         password.append(info[1])
    #         sckey.append(info[2])
    #
    #     except:
    #         break
    
    
    #数据检测
    print(AREASTR) 
    print(CUSTOMERID) 
    print(DEPTID) 
    print(EMERGENCYCONTACT) 
    print(MERGENCYPEOPLEPHONE)
    print(OWNPHONE)
    print(PHONENUM)
    print(SCKEY)
    print(STUNO)
    print(TEXT)
    print(USERID)
    print(USERS)
    print(USERNAME)
    #users="账号,密码,s酱"
    #users = input()
    print(users)
    info = users.split(',')
    #print(info)
    phone.append(info[0])
    print(phone[0])
    password.append(info[1])
    print(password[0])
    sckey.append(info[2])
    print(sckey[0])


    #提交打卡
    for index,value in enumerate(phone):
        print("开始尝试为用户%s打卡"%(value[-4:]))
        count = 0
        while (count <= 3):
            try:
                count +=1
                #campus = CampusCard(phone[index], password[index])
                campus = CampusCard(phone[0], password[0])
                print(campus)
                token = campus.user_info["sessionId"]
                userInfo=getUserInfo(token)
                response = checkIn(userInfo,token)
                strTime = getNowTime()
                if response.json()["msg"] == '成功':
                    success.append(value[-4:])
                    print(response.text)
                    msg = strTime + value[-4:]+"打卡成功"
                    if index == 0:
                        result=response
                    break
                else:
                    failure.append(value[-4:])
                    print(response.text)
                    msg =  strTime + value[-4:] + "打卡异常"
                    count = count + 1
                    if index == 0:
                        result=response
                    if count<=3:
                        print('%s打卡失败，开始第%d次重试...'%(value[-4:],count))
                    time.sleep(5)
            except AttributeError:
                print('%s获取信息失败，请检查密码！'%value[-4:])
                break
            except Exception as e:
                print(e.__class__)
                msg = "出现错误"
                failure.append(value[-4:])
                break
        print(msg)
        print("-----------------------")
    fail = sorted(set(failure),key=failure.index)
    title = "成功: %s 人,失败: %s 人"%(len(success),len(fail))
    # try:
    #     print('主用户开始微信推送...')
    #     wechatPush(title,sckey[0],success,fail,result)
    # except:
    #     print("微信推送出错！")

#时间函数
def getNowTime():
    cstTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    strTime = cstTime.strftime("%H:%M:%S ")
    return strTime

#打卡参数配置函数
def getUserJson(userInfo,token):
        a=time.time()
        bbb=int(round(a*1000)+28800000) 
        return   {
            "businessType": "epmpics",
            "method": "submitUpInfo",
            "jsonData": {
            "add": "false",
            "areaStr":areastr,
            "cardNo": "null",
            "customerid": customerid,
            "deptStr": {
                "deptid": deptid,
                "text": text
            },
            "phonenum": phonenum,
            "stuNo": stuno,
            "templateid": "pneumonia",
            "upTime": "null",
            "userid": userid,
            "username":username,
            "deptid": deptid,
            "updatainfo": [
                {
                    "propertyname": "wendu",
                    "value": "36.4"
                },
                {
                    "propertyname": "symptom",
                    "value": "无症状"
                },
                {
                    "propertyname": "jkzks",
                    "value": "正常"
                },
                {
                    "propertyname": "jtcy",
                    "value": "否"
                },
                {
                    "propertyname": "SFJCQZHYS",
                    "value": "否"
                },
                {
                    "propertyname": "sfddgr",
                    "value": "否"
                },
                {
                    "propertyname": "isTouch",
                    "value": "否"
                },
                {
                    "propertyname": "是否途径或逗留过疫情中，高风险地区？",
                    "value": ""
                },
                {
                    "propertyname": "isAlreadyInSchool",
                    "value": "没有"
                },
                {
                    "propertyname": "hsjc0511",
                    "value": "否"
                },
                {
                    "propertyname": "ownPhone",
                    "value": ownphone
                },
                {
                    "propertyname": "emergencyContact",
                    "value": emergencycontact
                },
                {
                    "propertyname": "mergencyPeoplePhone",
                    "value": mergencypeoplephone
                }
            ],
            "source": "app",
            "reportdate": bbb,
            "gpsType": 0,
            "token": token
        },
}

#信息获取函数
def getUserInfo(token):
    token={'token':token}
    sign_url = "https://reportedh5.17wanxiao.com/api/clock/school/getUserInfo"
    #提交打卡
    response = requests.post(sign_url, data=token)
    return response.json()['userInfo']

#打卡提交函数
def checkIn(userInfo,token):
    sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"
    jsons=getUserJson(userInfo,token)
    #提交打卡
    response = requests.post(sign_url, json=jsons)
    return response

#微信通知
def wechatPush(title,sckey,success,fail,result):    
    # strTime = getNowTime()
    timeArray = time.localtime(int(ttt/1000))
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    page = json.dumps(result.json(), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
    content = f"""
`{NowTime}` 
#### 打卡成功用户：
`{success}` 
#### 打卡失败用户:
`{fail}`
#### 主用户打卡信息:
```
{page}
```
        """
    data = {
            "text":title,
            "desp":content
    }
    scurl='https://sc.ftqq.com/'+sckey+'.send'
    try:
        req = requests.post(scurl,data = data)
        if req.json()["errmsg"] == 'success':
            print("Server酱推送服务成功")
        else:
            print("Server酱推送服务失败")
    except:
        print("微信推送参数错误")

if __name__ == '__main__':
    main()
