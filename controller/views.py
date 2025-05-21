# -*- coding: utf-8 -*-
from operator import concat
from tabnanny import check

import math
from rest_framework.decorators import api_view
from rest_framework.response import Response

import socket
import getpass
from django.shortcuts import render
from datetime import datetime

from .models import *

# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

import logging

log_date = datetime.now().strftime('%Y-%m-%d')
#log_file = 'home/bam/nFilterNew/Logs/Log_{0}'.format(log_date)
log_file = 'C:/Users/batuu/OneDrive/Documents/Self-employed/Projects/nFilterNew/Logs/Log_{0}'.format(log_date)
logging.basicConfig(filename=log_file + '.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


# -----------------------home page----------------------------

def index(request):
    logging.info("------------------------------------------------------------------------------------------------")
    return render(request, 'nuur.html')


def getprepix(request):
    logging.info("ДУГААРАА СОНГОЖ БУЙ ХЭСЭГ")
    numbertype = request.GET["numbertype"]
    logging.info(numbertype)
    az = request.GET['az']
    prepost = "prepaid"
    if numbertype == "7":
        prepost = "postpaid"
    numbertypetmp = numbertype
    if numbertype == "3":
        numbertypetmp = 2
    prefixes = list(PrefixOLD.objects.filter(is_active=1, category=numbertypetmp).order_by("prefix"))
    pre = []
    for i in range(0, len(prefixes)):
        pre.append(str(prefixes[i]))
    context = {"az": az, "numbertype": numbertype, "prefixes": pre, "prepost": prepost}
    return render(request, 'dugaarShuult.html', context)


def numberPrice(request):
    logging.info("ДУГААРЫН ҮНЭ")
    number = request.GET['number']
    numbertype = request.GET['numbertype']
    az = request.GET['az']
    selected_numbertype = NumberType.objects.get(id=numbertype)
    logging.info(selected_numbertype.price)
    aziinDugaar = AziinDugaar.objects.get(type=az)
    context = {"aziinDugaar": aziinDugaar, "selected_numbertype": selected_numbertype, "az": az, "number": number}
    return render(request, 'modalNumberPrice.html', context)


def registrDugaar(request):
    logging.info("РЕГИСТЕРИЙН ДУГААР")
    number = request.GET['number']
    numbertype = request.GET['numbertype']
    prepost = "prepaid"
    if numbertype == "7":
        prepost = "postpaid"
    az = request.GET['az']
    context = {"number": number, "prepost": prepost, "numbertype": numbertype, "az": az}
    return render(request, 'registr_oruulah.html', context)


def zahialga(request):
    logging.info("ДУГААРЫН ЗАХИАЛГА")
    number = request.GET['number']
    register = request.GET['register']
    prepost = request.GET['prepost']
    numbertype = request.GET['numbertype']
    az = request.GET['az']
    user_ip = get_client_ip(request)
    logging.info("user_ip: " + str(user_ip))
    socket_results = FilternumberBlockUnblock("block", "", number, "", register, user_ip)
    if socket_results == "Success":
        logging.info("Хадгалсан дугаар: "+str(number))
        context = {"try_again_url": "/nuur", "try_again": "OK",
                   "error1": "Таны сонгосон " + str(number) + " дугаар амжилттай хадгалагдлаа.",
                   "error2": "Та үйлчилгээний ажилтанд хандаж дугаараа авна уу."}
    else:
        logging.error('Уучлаарай, таны сонгосон ' + str(number) + ' дугаар захиалах боломжгүй байна. Line-1379')
        context = {"error1": "Уучлаарай, таны сонгосон " + str(number) + " дугаар захиалах боломжгүй байна.",
                   "try_again_url": "/" + prepost + "?numbertype=" + numbertype + "&az=" + az,
                   "try_again": "Дахин дугаар сонгох"}
    return render(request, 'timeout.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def FilternumberBlockUnblock(turul, search_type, number, az, user, user_ip):
    logging.info("FilternumberBlockUnblock")
    # logging.info(number)
    soc = socket.socket()
    soc.connect(('10.10.10.173', 8088))
    request_string = ""
    if turul == "filter":
        request_string = "0003ACC_QUERY:0|{0}|131|{1}|{2}".format(search_type, number, az)
        # request_string = "0003Block:{0}|{1}|0|{2}|0|DShuult".format("83120154", "shuult:" + str(user.encode('utf-8')),
        #                                                             user_ip)
    elif turul == "block":
        request_string = "0003Block:{0}|{1}|0|{2}|0|DShuult".format(number, "shuult-" + str(user.encode('utf-8')), user_ip)
        # request_string = "0003Block:{0}|{1}".format(number, user.encode('utf-8'))
    # else:
    #     request_string = "0003Unblock:{0}".format(number)
    # logging.info(request_string)
    soc.send(request_string)
    socket_results = soc.recv(2048)
    # logging.info(socket_results)
    soc.close()
    return socket_results


# --------------------------FILTER NUMBER ---------------------------
# dugaar shuult

@api_view(["GET"])
def getNumber(request):
    move = int(request.GET['move'])
    prefix = request.GET["prefix"]
    az = request.GET['az']
    numbertype = request.GET['numbertype']
    if numbertype == "3":
        numbertype = "2"
    # logging.info(prefix)

    first4 = prefix[0:4]
    last4 = prefix[4:8]

    # logging.info(prefix)

    ontsgoiDugaar = "engiin"

    if az != "6":
        if prefix == "DEAAAAAA":
            ontsgoiDugaar = "brilliant"
        if prefix == "DEABCCCC":
            ontsgoiDugaar = "alt1"
        if prefix == "DEAAAADE":
            ontsgoiDugaar = "alt2"
        if prefix == "DEAADEAA":
            ontsgoiDugaar = "alt3"
        if prefix == "DEAABBAA":
            ontsgoiDugaar = "alt4"
        if prefix == "DEBBAAAA":
            ontsgoiDugaar = "alt5"
        if prefix == "DEAAAABB":
            ontsgoiDugaar = "alt6"
        if prefix == "DExxABAB":
            ontsgoiDugaar = "mungu1"
        if prefix == "DExxABBA":
            ontsgoiDugaar = "mungu2"
        if prefix == "DExxAABB":
            ontsgoiDugaar = "mungu3"
        if prefix == "DEAAABBB":
            ontsgoiDugaar = "mungu4"
        if prefix == "DEABDEAB":
            ontsgoiDugaar = "mungu5"
        if prefix == "DEABABDE":
            ontsgoiDugaar = "mungu6"
        if prefix == "DExx000B":
            ontsgoiDugaar = "hurel1"
        if prefix == "DExxB000":
            ontsgoiDugaar = "hurel2"
        if prefix == "DEABABED":
            ontsgoiDugaar = "hurel3"
        if prefix == "DEABBAED":
            ontsgoiDugaar = "hurel4"
        last4 = "****"
    logging.info(ontsgoiDugaar)

    if ontsgoiDugaar == "engiin":
        prefixList = list(PrefixOLD.objects.filter(is_active=1, prefix__contains=prefix[0:2], category=numbertype).order_by("prefix"))
    else:
        prefixList = list(PrefixOLD.objects.filter(is_active=1, category=numbertype).order_by("prefix"))
    logging.info(prefixList)
    i = 0
    numbers = []

    if numbertype == "2":
        if prefix[2] == "*":
            if prefix[3] == "*":
                if ontsgoiDugaar == "engiin":
                    if (prefix[4:6] != "**" and prefix[6:8] == "**") or (prefix[4] == "*" and prefix[5:7] != "**" and prefix[7] == "*") or (prefix[4] != "*" and prefix[5:7] == "**" and prefix[7] != "*") \
                            or (prefix[4:6] == "**" and prefix[6:8] != "**") or (prefix[4] != "*" and prefix[5] == "*" and prefix[6] != "*" and prefix[7] == "*") \
                            or (prefix[4] == "*" and prefix[5] != "*" and prefix[6] == "*" and prefix[7] != "*") or (prefix[2:8] == "******"):
                        logging.info("hamgiin suuliin if")
                        first4 = str(prefixList[i].prefix)
                    else:
                        logging.info("hamgiin suuliin else")
                        first4 = first4
                else:
                    if ontsgoiDugaar != "engiin":
                        if az == "17" or az == "5" or az == "7" or az == "9":
                            first4 = str(prefixList[i].prefix)
            else:
                digit4 = []
                for j in range(0, len(prefixList)):
                    if str(prefixList[j].prefix)[3] == prefix[3]:
                        digit4.append(prefixList[j].prefix)
                first4 = str(digit4[i])
        if prefix[2] == "1" and prefix[3] == "*":
            first4 = str(prefixList[i].prefix)

    d = 0
    if ontsgoiDugaar != "engiin":
        while len(numbers) < 132:
            first4 = str(prefixList[d].prefix)
            # logging.info(first4)
            start = first4 + last4
            prefix = ''.join(str(k) for k in start)

            socket_results = FilternumberBlockUnblock("filter", "1", first4, az, "", "")
            if socket_results != "-1":
                socket_results = socket_results.split('|')
            else:
                socket_results = None
            if socket_results != None:
                for number in socket_results:
                    data = number.split(":")
                    if data[1] == az:
                        numbers.append(data[0])
            # logging.info(numbers)
            d += 1
            if d == len(prefixList):
                break
    else:
        logging.info(first4)
        logging.info(last4)
        start = first4 + last4
        prefix = ''.join(str(k) for k in start)

        socket_results = FilternumberBlockUnblock("filter", "3", prefix, az, "", "")
        if socket_results != "-1":
            socket_results = socket_results.split('|')
        else:
            socket_results = None
        if socket_results != None:
            for number in socket_results:
                data = number.split(":")
                # logging.info(data[1])
                if data[1] == az:
                    numbers.append(data[0])

    logging.info("numbers")
    logging.info(numbers)
    tmp = []
    i = 0
    while (i < len(numbers)):
        numero = numbers[i]
        numero = numero[0:4]
        # logging.info(numero)
        if PrefixOLD.objects.filter(is_active=1, prefix__contains=numero, category=numbertype).exists() and numero != "9811":
            tmp.append(numbers[i])
        i += 1
    logging.info("tmp")
    logging.info(tmp)
    numbers = tmp

    if 'movedown' in request.GET:
        # if socket_results != None:
        if len(numbers) > move + 24:
            numbers = numbers[move:move + 24]
            move = move + 24
        elif len(numbers) - move > 0:
            numbers = numbers[move:len(numbers)]
            move = move + 24
        elif len(numbers) == 0:
            move = 24
            numbers = None
        else:
            move = len(numbers) - 24
            # else:
            #   numbers = None
    else:
        # if socket_results != None:
        if len(numbers) != 0:
            if move > 24:
                numbers = numbers[move - 24:move + 23]
                move = move - 24
            elif move <= 24:
                numbers = numbers[0:24]
                move = 24
        else:
            numbers = None
            move = 24
            # else:
            #   numbers = None

    result = []
    data_number = dict()
    if numbers != None:
        for number in numbers:
            if checkNumber(number) == ontsgoiDugaar:
                # logging.info("match")
                data_number[str(number)] = number
    logging.info("data_number")
    logging.info(data_number)
    result.append(data_number)
    result.append(move)
    logging.info(result)
    # result.append(res)

    return Response(result)

def checkNumberOld(number):
    oron1 = number[0:1]
    oron2 = number[1:2]
    oron3 = number[2:3]
    oron4 = number[3:4]
    oron5 = number[4:5]
    oron6 = number[5:6]
    oron7 = number[6:7]
    oron8 = number[7:8]

    # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
    if (((oron3 != oron4) and (oron4 != oron5) and (oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)) or (
                        (oron3 != oron4) and (oron3 == oron5) and (oron4 != oron5) and (oron5 == oron6) and (
            oron6 == oron7) and (oron7 == oron8)) or (
                    (oron3 != oron4) and (oron4 == oron5) and (oron5 == oron6) and (oron6 == oron7) and (
        oron7 == oron8))):
        return "alt1"

    # silver shalgah DEABABDE, DExxAABB, DEABDEAB
    # DEABDEAB
    if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
        return "mungu1"
    # DEABABDE
    if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
        return "mungu2"
    # DExxAABB
    if (((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)) or (
                    (oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7) and (oron2 != oron5) and (
        oron2 != oron7))):
        return "mungu3"
    # hurel shalgah DExxABBA, DExxABAB
    # DExxABBA
    if ((oron1 != oron2) and (oron5 == oron8) and (oron6 == oron7)):
        return "hurel1"
    # DExxABAB
    if ((oron5 == oron7) and (oron6 == oron8)):
        return "hurel2"
    else:
        return "engiin"


def checkLast4(last4):
    oron5 = last4[0:1]
    oron6 = last4[1:2]
    oron7 = last4[2:3]
    oron8 = last4[3:4]

    if oron5 != "*" and oron6 != "*" and oron7 != "*" and oron8 != "*": # last4 != "****"
        # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
        if ((oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)):
            return "alt1"
        # silver shalgah DEABABDE, DExxAABB, DEABDEAB
        # DEABDEAB
        # if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
        #     return "mungu1"
        # # DEABABDE
        # if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
        #     return "mungu2"
        # DExxAABB
        if ((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)):
            return "mungu3"

        # hurel shalgah DExxABBA, DExxABAB
        # DExxABBA
        if ((oron5 == oron8) and (oron6 == oron7)):
            return "hurel1"
        # DExxABAB
        if ((oron5 == oron7) and (oron6 == oron8)):
            return "hurel2"
        else:
            return "engiin"
    else:
        return "engiin"

def checkNumber(number):
    oron1 = number[0:1]
    oron2 = number[1:2]
    oron3 = number[2:3]
    oron4 = number[3:4]
    oron5 = number[4:5]
    oron6 = number[5:6]
    oron7 = number[6:7]
    oron8 = number[7:8]

    # brilliant shalgah DEAAAAAA
    if ((oron3 == oron4) and (oron3 == oron5) and (oron3 == oron6) and (oron3 == oron7) and (oron3 == oron8) and
        (oron4 == oron5) and (oron4 == oron6) and (oron4 == oron7) and (oron4 == oron8) and
        (oron5 == oron6) and (oron5 == oron7) and (oron5 == oron8) and
        (oron6 == oron7) and (oron6 == oron8) and
        (oron7 == oron8)):
        return "brilliant"

    # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
    # DEABCCCC
    if (((oron3 != oron4)) and
        ((oron5 == oron6) and (oron5 == oron7) and (oron5 == oron8) and
         (oron6 == oron7) and (oron6 == oron8) and (oron7 == oron8))):
        return "alt1"
    # DEAAAADE
    if (((oron1 == oron7) and (oron2 == oron8)) and
            ((oron3 == oron4) and (oron3 == oron5) and (oron3 == oron6)) and
            ((oron4 == oron5) and (oron4 == oron6)) and ((oron5 == oron6))):
        return "alt2"
    # DEAADEAA
    if (((oron1 == oron5) and (oron2 == oron6)) and
            ((oron3 == oron4) and (oron3 == oron7) and (oron3 == oron8)) and
            ((oron4 == oron7) and (oron4 == oron8)) and ((oron7 == oron8))):
        return "alt3"
    # DEAABBAA
    if (((oron3 == oron4) and (oron3 == oron7) and (oron3 == oron8) and (oron4 == oron7) and (oron4 == oron8) and
         (oron7 == oron8)) and ((oron5 == oron6)) and
            ((oron5 != oron3) and (oron5 != oron4) and (oron5 != oron7) and (oron5 != oron8)) and
            ((oron6 != oron3) and (oron6 != oron4) and (oron6 != oron7) and (oron6 != oron8))):
        return "alt4"
    # DEBBAAAA
    if (((oron3 == oron4)) and ((oron3 != oron5) and (oron3 != oron6) and (oron3 != oron7) and (oron3 != oron8)) and
            ((oron4 != oron5) and (oron4 != oron6) and (oron4 != oron7) and (oron4 != oron8)) and
            ((oron5 == oron6) and (oron5 == oron7) and (oron5 == oron8)) and ((oron6 == oron7) and oron6 == oron8) and
            (oron7 == oron8)):
        return "alt5"
    # DEAAAABB
    if (((oron3 == oron4) and (oron3 == oron5) and (oron3 == oron6) and (oron4 == oron5) and (oron4 == oron6) and
         (oron5 == oron6)) and ((oron7 == oron8)) and ((oron7 != oron3) and (oron7 != oron4) and (oron7 != oron5) and
                                                       (oron7 != oron6) and (oron8 != oron3) and (oron8 != oron4) and
                                                       (oron8 != oron5) and (oron8 != oron6))):
        return "alt6"

    # if (((oron3 != oron4) and (oron4 != oron5) and (oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)) or (
    #                     (oron3 != oron4) and (oron3 == oron5) and (oron4 != oron5) and (oron5 == oron6) and (
    #         oron6 == oron7) and (oron7 == oron8)) or (
    #                 (oron3 != oron4) and (oron4 == oron5) and (oron5 == oron6) and (oron6 == oron7) and (
    #     oron7 == oron8))):
    #     return "alt1"

    # silver shalgah DEABABDE, DExxAABB, DEABDEAB
    # DExxABAB
    if (((oron5 == oron7) and (oron6 == oron8)) and
            ((oron5 != oron6) and (oron5 != oron8) and (oron6 != oron7) and (oron7 != oron8))):
        return "mungu1"
    # DExxABBA
    if (((oron5 == oron8) and (oron6 == oron7)) and
            ((oron5 != oron6) and (oron5 != oron7) and (oron6 != oron8) and (oron7 != oron8))):
        return "mungu2"
    # DExxAABB
    if (((oron5 == oron6) and (oron7 == oron8)) and
            ((oron5 != oron7) and (oron5 != oron8)) and ((oron6 != oron7) and (oron6 != oron8))):
        return "mungu3"
    # DEAAABBB
    if (((oron3 == oron4) and (oron3 == oron5) and (oron4 == oron5)) and
            ((oron6 == oron7) and (oron6 == oron8) and (oron7 == oron8)) and
            ((oron3 != oron6) and (oron3 != oron7) and (oron3 != oron8) and (oron4 != oron6) and (oron4 != oron7) and
             (oron4 != oron8)) and ((oron5 != oron6) and (oron5 != oron7) and (oron5 != oron8))):
        return "mungu4"
    # DEABDEAB
    if (((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)) and
            ((oron3 != oron4) and (oron3 != oron8) and (oron4 != oron7) and (oron7 != oron8))):
        return "mungu5"
    # DEABABDE
    if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and
            ((oron3 != oron4) and (oron3 != oron6) and (oron4 != oron5) and (oron5 != oron6))):
        return "mungu6"

    # # DEABDEAB
    # if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
    #     return "mungu1"
    # # DEABABDE
    # if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
    #     return "mungu2"
    # # DExxAABB
    # if (((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)) or (
    #                 (oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7) and (oron2 != oron5) and (
    #     oron2 != oron7))):
    #     return "mungu3"

    # hurel shalgah DExxABBA, DExxABAB
    #DExx000B
    if (((oron5 == "0") and (oron6 == "0") and (oron7 == "0")) and (oron8 != "0")):
        return "hurel1"
    # DExxB000
    if ((oron5 != "0") and ((oron6 == "0") and (oron7 == "0") and (oron8 == "0"))):
        return "hurel2"
    # DEABABED
    if (((oron1 == oron8) and (oron2 == oron7)) and ((oron3 == oron5) and (oron4 == oron6)) and
            ((oron3 != oron4) and (oron3 != oron6) and (oron4 != oron5) and (oron5 != oron6))):
        return "hurel3"
    # DEABBAED
    if (((oron1 == oron8) and (oron2 == oron7)) and ((oron3 == oron6) and (oron4 == oron5)) and
            ((oron3 != oron4) and (oron3 != oron5) and (oron4 != oron6) and (oron5 != oron6))):
        return "hurel4"

    # # DExxABBA
    # if ((oron1 != oron2) and (oron5 == oron8) and (oron6 == oron7)):
    #     return "hurel1"
    # # DExxABAB
    # if ((oron5 == oron7) and (oron6 == oron8)):
    #     return "hurel2"
    else:
        return "engiin"
