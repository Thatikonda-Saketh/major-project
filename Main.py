from flask import Flask, render_template, request, redirect, url_for, session
import json
from web3 import Web3, HTTPProvider
import hashlib
from hashlib import sha256
import os
import datetime

app = Flask(__name__)

app.secret_key = 'welcome'
global uname, details

def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'FakeProduct.json' #FakeProduct contract code
    deployed_contract_address = '0x59FF698007D3fCC661B0d52b94B9456285c25D55' #hash address to access counter feit contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'adduser':
        details = contract.functions.getUserDetails().call()
    if contract_type == 'productdata':
        details = contract.functions.getProductDetails().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'FakeProduct.json' #FakeProduct contract file
    deployed_contract_address = '0x59FF698007D3fCC661B0d52b94B9456285c25D55' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.setUserDetails(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'productdata':
        details+=currentData
        msg = contract.functions.setProductDetails(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
   return render_template('Login.html', msg='')

@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():
   return render_template('AdminLogin.html', msg='')

@app.route('/AdminLoginAction', methods=['GET', 'POST'])
def AdminLoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        if user == "admin" and password == "admin":
            return render_template('AdminScreen.html', msg="Welcome "+user)
        else:
            return render_template('Login.html', msg="Invalid login details")

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    return render_template('Signup.html', msg='')

@app.route('/AccessData', methods=['GET', 'POST'])
def AccessData():
    return render_template('AccessData.html', msg='')

@app.route('/LoginAction', methods=['GET', 'POST'])
def LoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == user and array[1] == password:
                uname = user
                status = "success"
                break
        if status == "success":
            return render_template('UserScreen.html', msg="Welcome "+uname)
        else:
            return render_template('Login.html', msg="Invalid login details")

@app.route('/ViewProduct', methods=['GET', 'POST'])
def ViewProduct():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product ID', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details', 'Date & Time', 'Barcode Digital Signatures']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('productdata')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"
            output += "<td>"+font+array[5]+"</td>"
            output += "<td>"+font+array[6]+"</td>"
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewProduct.html', msg=output)         

@app.route('/ViewUsers', methods=['GET', 'POST'])
def ViewUsers():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Username', 'Password', 'Phone No', 'Email ID', 'Address']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"            
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewProduct.html', msg=output) 
        
        
@app.route('/SignupAction', methods=['GET', 'POST'])
def SignupAction():
    if request.method == 'POST':
        global details
        uname = request.form['t1']
        password = request.form['t2']
        phone = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == uname:
                status = uname+" Username already exists"
                break
        if status == "none":
            data = uname+"#"+password+"#"+phone+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"adduser")
            context = "User signup task completed"
            return render_template('Signup.html', msg=context)
        else:
            return render_template('Signup.html', msg=status)

@app.route('/Logout')
def Logout():
    return render_template('index.html', msg='')

@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProduct():
   return render_template('AddProduct.html', msg='')

@app.route('/AddProductAction', methods=['GET', 'POST'])
def AddProductAction():
    if request.method == 'POST':
        pid = request.form['t1']
        pname = request.form['t2']
        price = request.form['t3']
        manufacture = request.form['t4']
        company = request.form['t5']
        barcode = request.files['t6']
        contents = barcode.read()
        current_time = datetime.datetime.now() 
        digital_signature = sha256(contents).hexdigest();
        data = pid+"#"+pname+"#"+price+"#"+manufacture+"#"+company+"#"+str(current_time)+"#"+digital_signature+"\n"
        saveDataBlockChain(data,"productdata")
        context = "Product details added with id : "+pid+"<br/>Generated Digital Signatures : "+digital_signature
        return render_template('AddProduct.html', msg=context)
        
@app.route('/RetrieveData', methods=['GET', 'POST'])
def RetrieveData():
   return render_template('RetrieveData.html', msg='')


@app.route('/RetrieveDataAction', methods=['GET', 'POST'])
def RetrieveDataAction():
    if request.method == 'POST':
        pid = request.form['t1']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product ID', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details', 'Date & Time', 'Barcode Digital Signatures']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('productdata')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == pid:
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                output += "<td>"+font+array[6]+"</td>"
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewDetails.html', msg=output)  

@app.route('/AuthenticateScan', methods=['GET', 'POST'])
def AuthenticateScan():
   return render_template('AuthenticateScan.html', msg='')


@app.route('/AuthenticateScanAction', methods=['GET', 'POST'])
def AuthenticateScanAction():
    if request.method == 'POST':
        barcode = request.files['t1']
        contents = barcode.read()
        digital_signature = sha256(contents).hexdigest();
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product ID', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details', 'Date & Time', 'Barcode Digital Signatures']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('productdata')
        arr = details.split("\n")
        flag = 0
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[6] == digital_signature:
                flag = 1
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                output += "<td>"+font+array[6]+"</td>"
        if flag == 0:
            output += "<tr><td>Uploaded Product Barcode Authentication Failed</td></tr>"
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewDetails.html', msg=output)


if __name__ == '__main__':
    app.run()










