# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from myapi.models import *
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import logging
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
import socket
import json, requests
from django.http import HttpResponse
import time

log_date = datetime.now().strftime('%Y-%m-%d')
log_file = 'home/user/nFilterNew/log/Log_{0}'.format(log_date)
logging.basicConfig(filename=log_file + '.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Create your views here.

@api_view(['GET'])
def receive_sms_postpaid(request):
    logging.info("receive_sms_postpaid")
    user_ip = get_client_ip(request)
    logging.info("user_ip: " + str(user_ip))
    if request.method == 'GET':
        sms_from = request.query_params.get('sms_from', None)
        sms_text = request.query_params.get('sms_text', None)
        logging.info(sms_from)
        logging.info(sms_text)
        userMessage = UserMessage353()
        userMessage.sms_from = sms_from
        userMessage.sms_to = "353"
        userMessage.sms_text = sms_text
        userMessage.received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        userMessage.responded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = ""
        if sms_text.lower() == "help":
            userMessage.status = 1
            userMessage.sms_response = "Ta xaix dugaarynxaa suuliin 4 orong 353 dugaart ilgeene uu. Une:100T"
            res = sendSms(sms_from, "Ta xaix dugaarynxaa suuliin 4 orong 353 dugaart ilgeene uu. Une:100T")
            time.sleep(2.5)
            if res == "0: Accepted for delivery":
                sendSms(sms_from,
                        "Dugaaraa xadgaluulax bol songoson dugaaraa 353 dugaart ilgeej uurt oir bairlax uilchilgeenii salbaraas 3 cagyn dotor ochij avax bolomjtoi. Gmobile")
        elif len(sms_text) == 4 and sms_text.isnumeric():
            userMessage.status = 2
            res = buscarNumeros(sms_from, sms_text)
            userMessage.sms_response = res
        elif len(sms_text) == 8 and sms_text.isnumeric():
            socket_results = FilternumberBlockUnblock("block", "", sms_from, "", sms_text, user_ip)
            logging.info("socket_results block")
            logging.info(socket_results)
            if socket_results == "Success":
                userMessage.status = 3
                result = "Tany songoson " + str(sms_text) + " dugaar amjilttai xadgalagdlaa. Ta uurt oir bairlax uilchilgeenii salbaraas 3 cagyn dotor ochij avna uu. Gmobile"
            else:
                userMessage.status = 4
                result = "Uuchlaarai, uildel amjiltgui bolloo. Ta xaix dugaarynxaa suuliin 4 orong 353 dugaart ilgeene uu. Une:100T"
            userMessage.sms_response = result
        else:
            userMessage.status = 0
            result = "Uuchlaarai, Tany ilgeesen utga buruu baina. 353 dugaart Help gesen utgyg ilgeej medeelel avna uu. Une:100T"
            userMessage.sms_response = result
        userMessage.save()
        return HttpResponse(result)
    responseError = {
        "status": "unsuccessful",
        "message": "Not allowed request method"
    }
    return JsonResponse(responseError, status=status.HTTP_400_BAD_REQUEST)


def buscarNumeros(sms_from, last4Digit):
    logging.info("buscarNumeros")
    az = AziinDugaar.objects.all()
    numbers = []
    for a in range(len(az)):
        socket_results = FilternumberBlockUnblock("filter", "2", last4Digit, az[a].type, "", "")
        # logging.info("socket_results"+str(socket_results))
        if socket_results != "-1":
            socket_results = socket_results.split('|')
        else:
            socket_results = None
        logging.info("socket_results" + str(socket_results))
        if socket_results != None:
            for i in reversed(range(len(socket_results))):
                if ":" in socket_results[i]:
                    data = socket_results[i].split(":")
                    # if data[1] == az:
                    numbers.append(data[0])
    logging.info("numbers"+str(numbers))

    prepaid = []
    postpaid = []
    i = 0
    urt = 23
    j = 0
    while (j < len(numbers)):
        numero = numbers[j]
        numero = numero[0:4]
        if Prefix.objects.filter(is_active=1, prefix__contains=numero, category=7).exists() and numero != "9811":
            postpaid.append(json.loads(numbers[j]))
        if len(postpaid) >= 13:
            break
        j += 1

    pre_urt = urt - int(len(postpaid))
    while (i < len(numbers)):
        numero = numbers[i]
        numero = numero[0:4]
        if Prefix.objects.filter(is_active=1, prefix__contains=numero, category=2).exists() and numero != "9811":
            prepaid.append(json.loads(numbers[i]))
        if len(prepaid) >= pre_urt:
            break
        i += 1

    logging.info("prepaid"+str(prepaid))
    logging.info("postpaid"+str(postpaid))

    tamano = "1"
    if len(prepaid) == 0 and len(postpaid) == 0:
        result = "Uuchlaarai, Tany xaisan dugaar xudaldaand baixgui baina. Gmobile"
        tamano = "0"
    else:
        result = "Ta Uridchilsan tulburt: " + str(prepaid) +", Daraa tulburt: " + str(postpaid) + " dugaaruudaas songon avax bolomjtoi baina."

    res = sendSms(sms_from, result)
    logging.info("res")
    logging.info(res)
    time.sleep(2.5)
    if res == "0: Accepted for delivery" and tamano != "0":
        res1 = sendSms(sms_from,
                       "Tany songoson dugaaryg uur xereglegch avch bolzoshgui tul ta amjij www.gmobile.mn online salbar, uurt oir bairlax uilchilgeenii salbar, kiosk mashinaas avaarai.")
        logging.info("res1")
        logging.info(res1)
        time.sleep(2.5)
        if res1 == "0: Accepted for delivery":
            res2 = sendSms(sms_from,
                    "Dugaaraa xadgaluulax bol songoson dugaaraa 353 dugaart ilgeene uu. Tany dugaaryg 3 cag xadgalax bolomjtoi. Gmobile")
            logging.info("res2")
            logging.info(res2)
    return result


def FilternumberBlockUnblock(turul, search_type, number, az, user, user_ip):
    soc = socket.socket()
    soc.connect(('10.10.10.173', 8088))
    request_string = ""
    if turul == "filter":
        request_string = "0003ACC_QUERY:0|{0}|1000|{1}|{2}".format(search_type, number, az)
    elif turul == "block":
        request_string = "0003Block:{0}|{1}|0|{2}|0|353".format(user, "353-" + str(user.encode('utf-8')) + "-" + str(number), user_ip)
    logging.info("request_string")
    logging.info(request_string)
    soc.send(request_string)
    socket_results = soc.recv(2048)
    # logging.info(socket_results)
    soc.close()
    return socket_results


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def sendSms(number, smsText):
    url = "http://192.88.80.199/cgi-bin/sendsms?username=n_search&password=search*0223&from=353&to="+str(number)+"&text="+str(smsText)
    hariu = requests.get(url)
    return hariu.content
