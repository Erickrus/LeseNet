import os
import json
import getpass

from baidupcsapi import PCS

class BaiduYun:
    def __init__(self):
        print("BaiduYun")
        self.username = input("Username: ")
        print("initialize BaiduYun for %s " % self.username )
        print("you may need to recognize a photo and input the message code")
        self.password = getpass.getpass()
        self.pcs = PCS(self.username, self.password)
        
    def byte2json(self, content):
        content = str(content, 'utf-8')
        json_str = json.loads(content)
        return json_str

    def upload(self, localFilename, remoteDir):
        if self.exists(
            os.path.join(
                remoteDir,
                os.path.basename(localFilename) 
            )):
            # print("file exists")
            return
        f = open(localFilename, 'rb')
        content = f.read()
        f.close()
        try:
            ret = self.pcs.upload(remoteDir, content, os.path.basename(localFilename))
        except:
            print("\nfailed to upload %s" % localFilename )
            pass
       
    def mkdir(self, remoteDir):
        try:
            if not self.exists(remoteDir):
               self.pcs.mkdir(remoteDir)
        except:
            pass

    def exists(self, remoteFilename):
        res = False
        try:
            remoteDir = os.path.dirname(remoteFilename)
            filelist = self.byte2json(self.pcs.list_files(remoteDir).content)
            for item in filelist["list"]:
                # print(item["path"])
                if remoteFilename == item["path"]:
                    return True
        except:
            pass
        return res

    # 递归目录查询
    def list(self, remoteFilename, recursive=False):
        res = []
        remoteDir = os.path.dirname(remoteFilename)
        filelist = self.byte2json(self.pcs.list_files(remoteDir).content)
        for item in filelist["list"]:
            # print(item["path"])
            if item["isdir"] == 1:
                res.append(item["path"]+"/")
                if recursive:
                    res.extend(self.list(item["path"]+"/", recursive))
            else:
                res.append(item["path"])

        return res

