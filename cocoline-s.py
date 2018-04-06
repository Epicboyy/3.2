# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse,timeit,data,atexit
from gtts import gTTS
from googletrans import Translator
botStart = time.time()
cl = LINE("LINE帳號","LINE密碼")
oepoll = OEPoll(cl)
settingsOpen = codecs.open("temp.json","r","utf-8")
settings = json.load(settingsOpen)
lineSettings = cl.getSettings()
clProfile = cl.getProfile()
clMID = cl.profile.mid
admin = ['u28d781fa3ba9783fd5144390352b0c24',clMID]
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']
msg_dict = {}
bl = [""]
def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def restartBot():
    print ("[ 訊息 ] 機器 重新啟動")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
def logError(text):
    cl.log("[ 錯誤 ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def helpmessage():
    helpMessage = """
╔═══════════
♥ ✿ CoCo指令表 ✿ ♥
    絕望の特製版
↪ 「Help」查看全部指令
↪ 「HelpInfo」查看狀態指令
↪ 「HelpBot」查看機器指令
↪ 「HelpGroup」查看機器指令
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpMessage
def helpmessageinfo():
    helpMessageInfo ="""
╔══[ 狀態指令 ]════════
↪ 「Rebot」重新啟動機器
↪ 「Runtime」查看機器運行時間
↪ 「Speed」查看機器速度
↪ 「Set」查看設定
↪ 「About」查看自己的狀態
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpMessageInfo
def helpmessagebot():
    helpMessageBot ="""
╔══[ 機器指令 ]════════
↪ 「Add On/Off」自動加入好友 打開/關閉
↪ 「Join On/Off」自動進入群組 打開/關閉
↪ 「Leave On/Off」自動離開副本 打開/關閉
↪ 「Reread On/Off」查看收回 打開/關閉
╚═〘 Credits By: ©CoCo™  〙
"""
    return helpMessageBot
def helpmessagegroup():
    helpMessageGroup ="""
╔══〘 群組指令 〙✪═══════
↪ 「Gowner」查看群組擁有者
↪ 「Gname」查看群組名稱
↪ 「GPicture」查看群組圖片網址
↪ 「O/Curl」打開/關閉群組網址
↪ 「Gb」查看群組成員
↪ 「Ginfo」查看群組狀態
↪ 「SetRead」設置已讀點
↪ 「LookRead」查看已讀的人
"""
    return helpMessageGroup
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if settings["autoAdd"] == True:
                cl.sendMessage(op.param1, "你好 {} 謝謝你加本機為好友 :D\n       本機為CoCo製作\n       line.me/ti/p/1MRX_Gjbmv".format(str(cl.getContact(op.param1).displayName)))
        if op.type == 13:
            if clMID in op.param3:
                if settings["autoJoin"] == True:
                    if op.param2 in admin:
                        cl.acceptGroupInvitation(op.param1)
        if op.type == 24:
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if msg.text is None:
                    pass
            if sender in admin:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'helpinfo':
                    helpMessageInfo = helpmessageinfo()
                    cl.sendMessage(to, str(helpMessageInfo))
                elif text.lower() == 'helpbot':
                    helpMessageBot = helpmessagebot()
                    cl.sendMessage(to, str(helpMessageBot))
                elif text.lower() == 'helpgroup':
                    helpMessageGroup = helpmessagegroup()
                    cl.sendMessage(to, str(helpMessageGroup))
                elif msg.text in ["SR","Setread"]:
                    cl.sendMessage(msg.to, "設置已讀點")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                    print ("設置已讀點")
                elif msg.text in ["LR","Lookread"]:
                    if msg.to in wait2['readPoint']:
                        print ("查詢已讀")
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "||已讀順序||%s\n\n%s\n[%s]" % (wait2['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "請輸入SR設置已讀點")
                elif text.lower() == 'speed':
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    curTime = time.time()
                    cl.sendMessage(to,'處理速度\n' + str1 + '秒')
                    rtime = time.time()
                    xtime = rtime - curTime
                    cl.sendMessage(to,'指令反應\n' + format(str(xtime)) + '秒')
                elif text.lower() == 'rebot':
                    cl.sendMessage(to, "重新啟動")
                    restartBot()
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "機器運行時間 {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner = "u28d781fa3ba9783fd5144390352b0c24"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        ret_ = "╔══[ 關於自己 ]"
                        ret_ += "\n╠ 名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 黑單 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠══[ 關於機器 ]"
                        ret_ += "\n╠ 版本 : 絕望の特製版"
                        ret_ += "\n╠ 作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ 未經許可禁止重製 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 設定 ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ 自動加入好友 ✅"
                        else: ret_ += "\n╠ 自動加入好友 ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠ 自動加入群組 ✅"
                        else: ret_ += "\n╠ 自動加入群組 ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠ 自動離開副本 ✅"
                        else: ret_ += "\n╠ 自動離開副本 ❌"
                        if settings["reread"] == True: ret_ += "\n╠ 查詢收回開啟 ✅"
                        else: ret_ += "\n╠ 查詢收回關閉 ❌"
                        ret_ += "\n╚══[ 設定 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'add on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動加入好友已開啟")
                elif text.lower() == 'add off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動加入好友已關閉")
                elif text.lower() == 'join on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "自動加入群組已開啟")
                elif text.lower() == 'join off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "自動加入群組已關閉")
                elif text.lower() == 'leave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "自動離開副本已開啟")
                elif text.lower() == 'leave off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "自動離開副本已關閉")
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    cl.sendMessage(to, "查詢收回開啟")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    cl.sendMessage(to, "查詢收回關閉")
                elif text.lower() == 'gowner':
                    group = cl.getGroup(to)
                    GS = group.creator.mid
                    cl.sendContact(to, GS)
                elif text.lower() == 'gpicture':
                    group = cl.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'gname':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to, "[群組名稱 : ]\n" + gid.name)
                elif text.lower() == 'gurl':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = cl.reissueGroupTicket(to)
                            cl.sendMessage(to, "[ 群組網址 ]\nhttps://cl.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            cl.sendMessage(to, "群組網址未開啟，請用Ourl先開啟".format(str(settings["keyCommand"])))
                elif text.lower() == 'ourl':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == False:
                            cl.sendMessage(to, "群組網址已開啟")
                        else:
                            G.preventedJoinByTicket = False
                            cl.updateGroup(G)
                            cl.sendMessage(to, "成功開啟群組網址")
                elif text.lower() == 'curl':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == True:
                            cl.sendMessage(to, "群組網址已關閉")
                        else:
                            G.preventedJoinByTicket = True
                            cl.updateGroup(G)
                            cl.sendMessage(to, "成功關閉群組網址")
                elif text.lower() == 'ginfo':
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "未找到"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "沒有"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 顯示名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組ＩＤ : {}".format(group.id)
                    ret_ += "\n╠ 群組作者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請數量 : {}".format(gPending)
                    ret_ += "\n╠ 群組網址 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╚══[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() == 'gb':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "╔══[ 成員列表 ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ 總共： {} ]".format(str(len(group.members)))
                        cl.sendMessage(to, str(ret_))
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if settings["reread"] == True:
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"] not in bl:
                            cl.sendMessage(at,"%s\n[收回了]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                            print ["收回訊息"]
                        del msg_dict[msg_id]
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            try:
                msg = op.message
                if settings["reread"] == True:
                    if msg.toType == 0:
                        cl.log("[%s]"%(msg._from)+msg.text)
                    else:
                        cl.log("[%s]"%(msg.to)+msg.text)
                    if msg.contentType == 0:
                        msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
                else:
                    pass
            except Exception as e:
                print(e)
        if op.type == 55:
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[•]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[•]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
