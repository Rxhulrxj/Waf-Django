from collections import Counter
from typing_extensions import final
from unittest import result
from urllib.parse import urlparse
from random import sample
import requests.exceptions
import requests
import argparse
# import operator
import sys
import time
from . import views
def mainfun(Url,posts,types,useragents):
    url = Url
    post = posts
    type =types
    useragent = useragents
    print ("  URL: ", url)
    base_url = "bla"
    param_list = {}
    proxies = {}
    sum_req_succ = 0
    sum_req_succ = 0
    des = 0
    headers = {}
    final_res = ""
    response=[]
    up_down=""
    net_issue=""

    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


    if (len(url) - (len(domain) - 1)) == 0:
        url = domain
    # #Headers
    if useragent:
        headers['user-agent'] = useragent
    else:
        headers['user-agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"

    #upordown
    try:
        r = requests.get(domain, proxies=proxies, headers=headers, allow_redirects=False, timeout=20)
        # r.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print ("\r\nTarget appears to be down!!\r\n")
        up_down="Site appears to be down!!"
        sys.exit()
    #upordown

    #Header-cheking
    header_changed = 0
    req_header = requests.get(url,headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
    req_header_attack = requests.get(url, params={'test': '%00'}, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
    if req_header_attack.status_code == req_header.status_code:

        if req_header.headers.get('Content-Length'):
            len_req_header = int(len(''.join(req_header.headers.values()))) - int(len(req_header.headers.get('Content-Length')))
        else:
            len_req_header = int(len(''.join(req_header.headers.values())))

        if req_header_attack.headers.get('Content-Length'):
            len_req_header_attack = int(len(''.join(req_header_attack.headers.values()))) - int(len(req_header_attack.headers.get('Content-Length')))
        else:
            len_req_header_attack = int(len(''.join(req_header_attack.headers.values())))

        if len_req_header != len_req_header_attack :
            print ("\r\n\tThe server header is different when an attack is detected.\r\n")
            header_changed = 1
    #Header-cheking




    if not post:
        if "?" in url:
            des = 1
            urls = url.split("&")
            c = len(urls)
            part_1 = urls[0].split("?")
            base_url = part_1[0]
            del urls[0]
        else:
            urls = url.split("/")
            base_url = domain
            del urls[0:3]


    if post:
        paramp = post.split("&")


    def parameters_equal (arg):
        s_arg=arg.split("=")
        param_list[s_arg[0]] = s_arg[1]
        return;

    def parameters_slash (arg,param_count):
        param_list["param_"+str(param_count)] = arg
        return;

    if not post:
        if des == 1:
            parameters_equal(part_1[1])
            for url in urls:
                parameters_equal(url)
        else:
            param_count = 1
            for url in urls:
                parameters_slash(url, param_count)
                param_count = param_count + 1


    if post:
        for param in paramp:
            parameters_equal(param)


    payloads = {}
    def file2dic (filename):
        f = open(filename, 'r')
        for line in f:
            param_split = line.rpartition('@')
            payloads[param_split[0]] = param_split[2]
    #PayloadstoDic
    if type == "xss":
        file2dic ('C:/projects/Firewall_Django_project/firewall_app/payloads/XSS_Payloads.csv')
    elif type == "sql":
        file2dic ('C:/projects/Firewall_Django_project/firewall_app/payloads/SQLi_Payloads.csv')
    elif type == "others":
        file2dic ('C:/projects/Firewall_Django_project/firewall_app/payloads/other_Payloads.csv')
    elif type == "all":
        file2dic ('C:/projects/Firewall_Django_project/firewall_app/payloads/XSS_Payloads.csv')
        file2dic ('C:/projects/Firewall_Django_project/firewall_app/payloads/SQLi_Payloads.csv')
        file2dic ('C:/projects/Firewall_Django_project/firewall_app/payloads/other_Payloads.csv')

    #PayloadstoDic

    for name_m, value_m in param_list.items():
        print ("\r\n<Parameter Name> " , name_m , "\r\n")

        params = {}
        rs = []
        q = ""
        c = 0
        trycount = 0
        succ = 0
        fai = 0

        for payload, string in payloads.items():
            c = c + 1
            # if args.delay:
            #     time.sleep(args.delay)
            name_m = str(name_m)
            value_m = str(value_m)
            if (payload[:1] == "\'") or (payload[:1] == "\""):
                param_list[name_m] = value_m+payload
            else:
                param_list[name_m] = value_m+"\" "+payload




            #Send-Request
            for i in range(3):
                try:
                    if post:
                        req = requests.post(url, data=param_list, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
                    else:
                        if des == 1:
                            req = requests.get(base_url, params=param_list, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
                        else:
                            base_url = domain
                            base_url = base_url + '/'.join(param_list.values())
                            req = requests.get(base_url, headers=headers, proxies=proxies, allow_redirects=False, timeout=10)
                            base_url = domain
                    r.raise_for_status()
                    if (str(req.status_code)[0] == "2") or (str(req.status_code)[0] == "1") or (req.status_code == 404):


                        if req.headers.get('Content-Length'):
                            len_req = int(len(''.join(req.headers.values())) - int(len(req.headers.get('Content-Length'))))
                        else:
                            len_req = 1

                        if not ((req.status_code == req_header_attack.status_code) and (len_req == len_req_header_attack) and (header_changed == 1)):
                            string = string[:-1]
                            print (" ✔ [", string, "][", payload,"] --> "  , "<successful> Response Status: "+str(req.status_code)+"\n\r", end="")
                            succ = succ + 1
                        else:
                            print ("   [", payload,"] --> "  , "<Failed> Response Status: "+str(req.status_code)+" *Header changed!\n\r", end="")
                            fai = fai + 1    
                    else:
                        print ("   [", payload,"] --> "  , "<Failed> Response Status: "+str(req.status_code)+"\n\r", end="")
                        fai = fai + 1           

                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                    print (" Retrying ... [ ", payload, " ]")
                    trycount = trycount + 1
                    continue
                else:
                    break    
            else:
                print (" Skipping ... [ ", payload, " ]")
                continue

            rs.append(req.status_code) 
            if trycount > 150:
                print ("\r\nSorry dude!, Check your internet connection or it appears you have been blocked!!!!!\r\nYou can use delay for the next try.")
                net_issue="Sorry, Check your internet connection or it appears you have been blocked!!"   
                sys.exit()         
            #Send-Request
            param_list[name_m] = value_m


        #Summary
        print ("   [ done ]")


        sum_req_succ = rs.count(200) + rs.count(404)
        print ("\r\n Summary \"" , name_m , "\":\r\n\r\n")
        sum_req_fai = rs.count(500) + rs.count(403) + rs.count(301) + rs.count(400) + rs.count(503) + rs.count(302)


        print ("   *Number of Requests: ", c, "\n\r\n\r", end="")
        count_err = Counter(rs)
        print ("       http response code = quantity")
        for err, err_count in count_err.items():
            print ("      ",err, " = ", err_count, "\r\n")
        print ("      + Successful:", succ, "\n\r", end="")
        print ("      x Failed:", fai, "\n\r", end="")
        print ("      - No response:", c - (fai+succ), "\n\r\n\r\n\r", end="")
        x = c - (fai+succ) 
        #Summary


    sum_req_succ = sum_req_succ / len(param_list)
    sum_req_fai = sum_req_fai / len(param_list)
    
    if sum_req_succ >=100:
        print ("\n\r\n\r   Your Website is Strong!!!!!!\n\r")
        final_res = "Your Website is Strong"
    if sum_req_fai >=100:
        print ("\n\r\n\r   Bad Security Measures Detected\n\r")
        final_res ="Bad Security Measures Detected"
    return final_res,up_down,net_issue,succ,fai,x,c
# if __name__ == '__main__':
#     main()