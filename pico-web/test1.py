from RequestParser import RequestParser

method = ""
full_url = ""
url = ""
query_string = ""
protocol = ""
headers = {}
query_params = {}
post_data = {}
boundary = False
content = []


rawRequestData = 'POST /api HTTP/1.1\r\nHost: 192.168.1.250:3030\r\nContent-Type: application/json;charset=UTF-8\r\nOrigin: http://192.168.1.250:3030\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nAccept: */*\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.138 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.1.250:3030/\r\nContent-Length: 30\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n'


rawRequestData2 = 'POST /api HTTP/1.1\r\nHost: 192.168.1.250:3030\r\nConnection: keep-alive\r\nContent-Length: 30\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\r\nContent-Type: application/json;charset=UTF-8\r\nAccept: */*\r\nOrigin: http://192.168.1.250:3030\r\nReferer: http://192.168.1.250:3030/\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: MicrosoftApplicationsTelemetryDeviceId=7b5b2885-6e87-4150-85e6-ae7b513d7d9d; MicrosoftApplicationsTelemetryFirstLaunchTime=2024-02-03T14:58:34.911Z\r\n\r\n{"action":"turnInternalLedOn"}'

print("************ Raw Request Data Begin **************")
print(rawRequestData)
print("************ Raw Request Data End **************")

print("************ Raw Request Data 2 Begin **************")
print(rawRequestData2)
print("************ Raw Request Data 2 End **************")


request = RequestParser(rawRequestData)