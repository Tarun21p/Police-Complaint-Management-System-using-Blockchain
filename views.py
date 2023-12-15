from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider
import ipfsApi
import os
from django.core.files.storage import FileSystemStorage
import pickle
from datetime import date
import pyaes, pbkdf2, binascii, os, secrets
import base64
import urllib, mimetypes
from django.http import HttpResponse

global details, username
details=''
global contract

api = ipfsApi.Client(host='http://127.0.0.1', port=5001)

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Police.json' #Police contract code
    deployed_contract_address = '0x94A6E788d45B2c830B0E5703B4C552d444beC84c' #hash address to access Police contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'addusers':
        details = contract.functions.getUsers().call()
    if contract_type == 'complaints':
        details = contract.functions.getComplaints().call()
    if contract_type == 'investigations':
        details = contract.functions.getInvestigation().call()    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Police.json' #Police contract file
    deployed_contract_address = '0x94A6E788d45B2c830B0E5703B4C552d444beC84c' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'addusers':
        details+=currentData
        msg = contract.functions.addUsers(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'complaints':
        details+=currentData
        msg = contract.functions.addComplaints(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'investigations':
        details+=currentData
        msg = contract.functions.addInvestigation(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def PoliceLogin(request):
    if request.method == 'GET':
       return render(request, 'PoliceLogin.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})    
    
def AddNewPolice(request):
    if request.method == 'GET':
       return render(request, 'AddNewPolice.html', {})

def AddFir(request):
    if request.method == 'GET':
       return render(request, 'AddFir.html', {})

def getKey(): #generating key with PBKDF2 for AES
    password = "s3cr3t*c0d3"
    passwordSalt = '76895'
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key

def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

def UpdateInvestigations(request):
    if request.method == 'GET':
        global username
        output = '<tr><td><font size="" color="black">Complaint&nbsp;ID</font></td><td><select name="t1">'
        readDetails("complaints")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            output+='<option value="'+arr[0]+'">'+arr[0]+'</option>'
        output += "</select></td></tr>"    
        context= {'data1': output}        
        return render(request, 'UpdateInvestigations.html', context)     

def UpdateInvestigationsAction(request):
    if request.method == 'POST':
        global username
        today = date.today()
        complaint = request.POST.get('t1', False)
        investigation = request.POST.get('t2', False)
        today = date.today()
        data = complaint+"#"+username+"#"+investigation+"#"+str(today)+"#\n"
        saveDataBlockChain(data,"investigations")
        output = "Investigation Details Submitted Under Complaint No : "+str(complaint)
        context= {'data': output}
        return render(request, 'UserScreen.html', context)

def ViewInvestigations(request):
    if request.method == 'GET':
        global username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Complaint No</font></th>'
        output+='<th><font size=3 color=black>Complaint Details</font></th>'
        output+='<th><font size=3 color=black>Complainer Name</font></th>'
        output+='<th><font size=3 color=black>Complainer Contact No</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Criminal Name</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Case Type</font></th>'
        output+='<th><font size=3 color=black>Station Details</font></th>'
        output+='<th><font size=3 color=black>IPFS Storage Hashcode</font></th>'
        output+='<th><font size=3 color=black>Document Name</font></th>'
        output+='<th><font size=3 color=black>Complaint Date</font></th>'
        output+='<th><font size=3 color=black>Inspector Name</font></th>'
        output+='<th><font size=3 color=black>Investigation Details</font></th>'
        output+='<th><font size=3 color=black>Download Documents</font></th></tr>'
        readDetails("investigations")
        investigations = details.split("\n")
        readDetails("complaints")
        rows = details.split("\n")        
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[3]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[4]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[5]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[6]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[7]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[8]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[9]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[10]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[11]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[12]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[13]+'</font></td>'
            invest = ""
            for k in range(len(investigations)):
                ar = investigations[k].split("#")
                if ar[0] == arr[0]:
                    invest += ar[2]+"\n"
            output+='<td><font size=3 color=black>'+invest+'</font></td>'        
            output+='<td><a href=\'DownloadAction?file='+arr[0]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"          
        context= {'data': output}        
        return render(request, 'UserScreen.html', context)   



def ViewReports(request):
    if request.method == 'GET':
        global username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Complaint No</font></th>'
        output+='<th><font size=3 color=black>Complaint Details</font></th>'
        output+='<th><font size=3 color=black>Complainer Name</font></th>'
        output+='<th><font size=3 color=black>Complainer Contact No</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Criminal Name</font></th>'
        output+='<th><font size=3 color=black>Contact No</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Case Type</font></th>'
        output+='<th><font size=3 color=black>Station Details</font></th>'
        output+='<th><font size=3 color=black>IPFS Storage Hashcode</font></th>'
        output+='<th><font size=3 color=black>Document Name</font></th>'
        output+='<th><font size=3 color=black>Complaint Date</font></th>'
        output+='<th><font size=3 color=black>Inspector Name</font></th>'
        output+='<th><font size=3 color=black>Investigation Details</font></th>'
        output+='<th><font size=3 color=black>Download Documents</font></th></tr>'
        readDetails("investigations")
        investigations = details.split("\n")
        readDetails("complaints")
        rows = details.split("\n")        
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[3]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[4]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[5]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[6]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[7]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[8]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[9]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[10]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[11]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[12]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[13]+'</font></td>'
            invest = ""
            for k in range(len(investigations)):
                ar = investigations[k].split("#")
                if ar[0] == arr[0]:
                    invest += ar[2]+"\n"
            output+='<td><font size=3 color=black>'+invest+'</font></td>'        
            output+='<td><a href=\'DownloadAction?file='+arr[0]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"          
        context= {'data': output}        
        return render(request, 'AdminScreen.html', context)


def AddFirAction(request):
    if request.method == 'POST':
        global username
        today = date.today()
        complaint = request.POST.get('t1', False)
        complainer_name = request.POST.get('t2', False)
        complainer_contact = request.POST.get('t3', False)
        complainer_address = request.POST.get('t4', False)
        criminal_name = request.POST.get('t5', False)
        criminal_contact = request.POST.get('t6', False)
        criminal_address = request.POST.get('t7', False)
        case_type = request.POST.get('t8', False)
        station = request.POST.get('t9', False)
        filedata = request.FILES['t10'].read()
        filename = request.FILES['t10'].name
        filedata = encrypt(filedata)
        complaint_id = 0
        readDetails("complaints")
        rows = details.split("\n")
        if len(rows) == 0:
            complaint_id = 1
        else:
            complaint_id = len(rows)
        filedata = pickle.dumps(filedata)
        hashcode = api.add_pyobj(filedata)
        data = str(complaint_id)+"#"+complaint+"#"+complainer_name+"#"+complainer_contact+"#"+complainer_address+"#"+criminal_name+"#"+criminal_contact+"#"
        data += criminal_address+"#"+case_type+"#"+station+"#"+hashcode+"#"+filename+"#"+str(today)+"#"+username+"\n"
        saveDataBlockChain(data,"complaints")
        output = "Complaint Details saved in Blockchain with IPFS storage hashcode : "+hashcode+"<br/>Complaint No : "+str(complaint_id)
        context= {'data': output}
        return render(request, 'UserScreen.html', context)
        
def DownloadAction(request):
    if request.method == 'GET':
        global username
        complaint = request.GET['file']
        fileName = ""
        hashcode = ""
        readDetails("complaints")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == complaint:
                fileName = arr[11]
                hashcode = arr[10]
                break
        content = api.get_pyobj(hashcode)
        content = pickle.loads(content)
        content = decrypt(content)
        response = HttpResponse(content,content_type="application/octet-stream")
        response['Content-Disposition'] = "attachment; filename=%s" % fileName
        return response


def ViewPolice(request):
    if request.method == 'GET':
        global username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Username</font></th>'
        output+='<th><font size=3 color=black>Passwor</font></th>'
        output+='<th><font size=3 color=black>Police Station Contact No</font></th>'
        output+='<th><font size=3 color=black>E-Mail ID</font></th>'
        output+='<th><font size=3 color=black>Address</font></th></tr>'
        readDetails("addusers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[3]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[4]+'</font></td></tr>'
        output += "</table><br/><br/><br/><br/>"        
        context= {'data': output}        
        return render(request, 'AdminScreen.html', context)     

def AddNewPoliceAction(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        record = 'none'
        readDetails("addusers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[1] == username:
                record = "exists"
                break
        if record == 'none':
            data = username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"addusers")
            context= {'data':'Signup process completed and record saved in Blockchain'}
            return render(request, 'AddNewPolice.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'AddNewPolice.html', context)
        
def PoliceLoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        readDetails("addusers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username and arr[1] == password:
                status = 'success'
                break
        if status == 'success':
            context= {'data':"Welcome "+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'PoliceLogin.html', context)            


        
def AdminLoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context= {'data':"Welcome "+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'AdminLogin.html', context)            

        



        
            
