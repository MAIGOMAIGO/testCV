import requests

# name : (filename,filedata,MIMETYPE TypeName/subTypeName)
video = {
    'driveNum':('','1','text/plain;charset=UTF-8'),
    'camNum':('','0','text/plain;charset=UTF-8'),
    'video': ('cam0stream1.ts', open('cam0stream1.ts','rb'),'video/mp2t')
    }

response = requests.post('http://172.16.100.27:8000/', files=video)
print(response)