#!/usr/bin/env python
# -*- coding: utf-8 -*-	

import os
from flask import Flask, request
import redis
import datetime
import datedelta
import calendar
import json
from flask_sslify import SSLify


ALL = "All"
NEC = "Necessities"
EDU = "Education"
LTS = "Saving"
PLY = "Play"
FFA = "Investment"
GIV = "Give"

ONCE = "Once"
DAILY = "Daily"
WEEKLY = "Weekly"
MONTHLY = "Monthly"
ANNUALLY = "Annually"

CURRENCY_VND = "VND"
CURRENCY_USD = "USD"

LANGUAGE_EN = "English"
LANGUAGE_VN = "Vietnamese"

TRANSACTION_TYPE_INCOME = "Income"
TRANSACTION_TYPE_EXPENSE = "Expense"

JAR_OPTION = {
    ALL:'all-option',
    NEC:'nec-option',
    EDU:'edu-option',
    LTS:'lts-option',
    PLY:'ply-option',
    FFA:'ffa-option',
    GIV:'giv-option'
}

REPEAT_TYPE = {
    ONCE:'once-type',
    DAILY:'daily-type',
    WEEKLY:'weekly-type',
    MONTHLY:'monthly-type',
    ANNUALLY:'annually-type'
}

app = Flask(__name__)
sslify = SSLify(app)


#VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
#CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
#r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
r = redis.Redis(host='redis-16798.c246.us-east-1-4.ec2.cloud.redislabs.com', port='16798', password='Cr6kdgmEUF1ZDbuaYr8lxWbneFHEQtDV')


@app.route('/')
def WelcomePage():
    
    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi - Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,6jars,app,money,method,management,cloud,native,application">
        <meta name="google-signin-client_id" content="955627858473-0arlet02drea1vfrn2rtndg6d430qdib.apps.googleusercontent.com">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->


    </head>
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    """

    end_html = "</body></html>"

    mid_html = """

    <style>

         html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

       #g-signin2 {
            width: 100%;
        }
                
        #g-signin2 > div {
            margin: 0 auto;
        }

     
        .bottom-label {
            display: block;
            margin-left: auto;
            margin-right: auto;
            height: 45px;
            text-align: center;
            bottom: 0;
            position: absolute;
            width: 100%;
            font-weight:300;
        }
       

        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        .image-center {
            position: absolute; 
            margin: auto; 
            top: 0; 
            left: 0; 
            right: 0; 
            bottom: 0;
        }


        .facebook-center {
            position: absolute; 
            margin: auto;
            text-align:center;
            top: calc(100% - 160px); 
            left: 0; 
            right: 0; 
        }

        .google-center {
            position: absolute;
            margin: auto;
            text-align:center;
            top: calc(100% - 110px);
            left: 0; 
            right: 0; 
        }
       
    </style>

    <div class="container">

        <div style="width:100%; height:100%">
            <img src="static/moneyoi.png" class="image-center" style="width:192px; height:192px;">
            
            <div class="google-center">
                <div id="g-signin2"></div>
            </div>

            <div class="facebook-center">
                <div 
                    class="fb-login-button" 
                    data-scope="public_profile,email"
                    data-width="254"
                    data-size="large" 
                    data-button-type="continue_with" 
                    data-auto-logout-link="false" 
                    data-use-continue-as="false" 
                    data-onlogin="checkLoginState();">
                </div>
            </div>
        </div>

    </div>

    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <div class="bottom-class">
        <label class="bottom-label">
            <p style="color: white;">
                &copy 2019 MoneyOi.
                <a href="https://moneyoi.io/blogs/moneyoi-quan-ly-6-hu-en/moneyoi-app-privacy-policy" style="color:white; text-decoration: underline;">Privacy Policy</a>
                <br>
                <span style="color:TURQUOISE">Powered by Heroku Application Platform</span>
            </p>
        </label>
    </div>


    <script>

        function addZero(i) {
            if (i < 10) {
                i = "0" + i;
            }
            return i;
        }

        var user_login = 'google';


        function onSignIn(googleUser) {

            user_login = 'google';

            var waiting = document.getElementById('waiting');
            waiting.style.display="block";

            var user_id = googleUser.getBasicProfile().getId();
            var user_email = googleUser.getBasicProfile().getEmail();
            
            var d = new Date();
            var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/HomePage/'+ user_id + '/' + today, true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

            xhr.onload = function() {
                document.open();
                document.write(xhr.responseText);
                document.close();

            };

            xhr.send('sender_id=WelcomePage'+'&user_email='+user_email+'&user_login='+user_login);

        }

        

        function onFailure(error) {
            console.log(error);
        }
            
        function renderButton() {
            gapi.signin2.render('g-signin2', {
                'scope': 'profile email',
                'width': 254,
                'longtitle': true,
                'theme': 'dark',
                'onsuccess': onSignIn,
                'onfailure': onFailure
            });
        }

        
        function statusChangeCallback(response) {
            
            // The response object is returned with a status field that lets the
            // app know the current login status of the person.
            // Full docs on the response object can be found in the documentation
            // for FB.getLoginStatus().

            user_login = 'facebook';

            if ((response.status === 'connected') && (user_login ==='facebook')) {
                // Logged into your app and Facebook.

                var user_id = response.authResponse.userID;
                
                var waiting = document.getElementById('waiting');
                waiting.style.display="block";

                var d = new Date();
                var today = d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());

                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/HomePage/'+ user_id + '/' + today, true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                        
                xhr.onload = function() {
                    document.open();
                    document.write(xhr.responseText);
                    document.close();

                };
        
                FB.api('/me', {fields: 'email'}, function(response) {   
                    xhr.send('sender_id=WelcomePage'+'&user_email='+response.email+'&user_login='+user_login);
                });

                
            } 
        }


        window.fbAsyncInit = function() {
            FB.init({
            appId      : '392841268177993',
            cookie     : true,
            xfbml      : true,
            version    : 'v6.0'
            });

            FB.getLoginStatus(function(response) {
                statusChangeCallback(response);
            });

        };

        (function(d, s, id){
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {return;}
            js = d.createElement(s); js.id = id;
            js.src = "https://connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));


        function checkLoginState() {
            FB.getLoginStatus(function(response) {
                statusChangeCallback(response);
            });
        }


    </script>

    <script src="https://apis.google.com/js/platform.js?onload=renderButton" async defer></script>

    <div id="fb-root"></div>
    <script async defer src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v5.0&appId=392841268177993&autoLogAppEvents=1"></script>
       

    """
    
    return begin_html + mid_html + end_html


@app.route('/HomePage/<user_id>/<today>', methods=['POST'])
def HomePage(user_id, today):
    

    pre_balance = 0
    nec_prebal = 0
    edu_prebal = 0
    lts_prebal = 0
    ply_prebal = 0
    ffa_prebal = 0
    giv_prebal = 0

    income_amt = 0
    expense_amt = 0
    balance_amt = income_amt - expense_amt + pre_balance

    nec_income = 0
    edu_income = 0
    lts_income = 0
    ply_income = 0
    ffa_income = 0
    giv_income = 0

    nec_expense = 0
    edu_expense = 0
    lts_expense = 0
    ply_expense = 0
    ffa_expense = 0
    giv_expense = 0

    nec_balance = nec_income - nec_expense + nec_prebal
    edu_balance = edu_income - edu_expense + edu_prebal
    lts_balance = lts_income - lts_expense + lts_prebal
    ply_balance = ply_income - ply_expense + ply_prebal
    ffa_balance = ffa_income - ffa_expense + ffa_prebal
    giv_balance = giv_income - giv_expense + giv_prebal
   
    nec_pct = 55
    edu_pct = 10
    lts_pct = 10
    ply_pct = 10
    ffa_pct = 10
    giv_pct = 5

    nec_progress = 0
    edu_progress = 0
    lts_progress = 0
    ply_progress = 0
    ffa_progress = 0
    giv_progress = 0

    nec_progress_color = "LIGHTGRAY"
    edu_progress_color = "LIGHTGRAY"
    lts_progress_color = "LIGHTGRAY"
    ply_progress_color = "LIGHTGRAY"
    ffa_progress_color = "LIGHTGRAY"
    giv_progress_color = "LIGHTGRAY"


    currency = CURRENCY_VND
    language = LANGUAGE_EN

    percentage = 0

    user_email = ''
    user_login = ''
 
    # Get current date for HomePage information
   
    dateString = today.split('-')
    currentDate = datetime.date(int(dateString[0]), int(dateString[1]), int(dateString[2]))
    current_date = dateString[0]+'-'+dateString[1]
    

    print "HomePage:today:"+today 
    print "HomePage:user_id:"+user_id 


    sender_id = request.form['sender_id']

    if (sender_id == 'WelcomePage'):
        user_email = request.form['user_email']
        user_login = request.form['user_login']

    # check whether if user_id exists or not
    if (r.hexists(user_id, "currency") == False): 
        print "HomePage:Account not exist"
        
        r.hmset(user_id,{
                'nec_pct':nec_pct,
                'edu_pct':edu_pct,
                'lts_pct':lts_pct,
                'ply_pct':ply_pct,
                'ffa_pct':ffa_pct,
                'giv_pct':giv_pct,
                'income_amt':income_amt,
                'expense_amt':expense_amt,
                'currency':currency,
                'nec_income':nec_income,
                'edu_income':edu_income,
                'lts_income':lts_income,
                'ply_income':ply_income,
                'ffa_income':ffa_income,
                'giv_income':giv_income,
                'nec_expense':nec_expense,
                'edu_expense':edu_expense,
                'lts_expense':lts_expense,
                'ply_expense':ply_expense,
                'ffa_expense':ffa_expense,
                'giv_expense':giv_expense,
                'nec_prebal':nec_prebal,
                'edu_prebal':edu_prebal,
                'lts_prebal':lts_prebal,
                'ply_prebal':ply_prebal,
                'ffa_prebal':ffa_prebal,
                'giv_prebal':giv_prebal,
                'pre_balance':pre_balance,
                'pre_date':current_date,
                'language':language,
                'user_email':user_email,
                'user_login':user_login
            })

    else:
        print "HomePage:Account exist"

        user_dict = r.hmget(user_id,
                            'income_amt',
                            'expense_amt',
                            'currency',
                            'nec_income',
                            'edu_income',
                            'lts_income',
                            'ply_income',
                            'ffa_income',
                            'giv_income',
                            'nec_expense',
                            'edu_expense',
                            'lts_expense',
                            'ply_expense',
                            'ffa_expense',
                            'giv_expense',
                            'nec_prebal',
                            'edu_prebal',
                            'lts_prebal',
                            'ply_prebal',
                            'ffa_prebal',
                            'giv_prebal',
                            'pre_balance',
                            'pre_date',
                            'language',
                            'user_email',
                            'user_login')

        language = user_dict[23]
        currency = user_dict[2]
        user_email = user_dict[24]
        user_login = user_dict[25]
        
        income_amt = int(float(user_dict[0]))
        expense_amt = int(float(user_dict[1]))

        nec_income = int(float(user_dict[3]))
        edu_income = int(float(user_dict[4]))
        lts_income = int(float(user_dict[5]))
        ply_income = int(float(user_dict[6]))
        ffa_income = int(float(user_dict[7]))
        giv_income = int(float(user_dict[8]))

        nec_expense = int(float(user_dict[9]))
        edu_expense = int(float(user_dict[10]))
        lts_expense = int(float(user_dict[11]))
        ply_expense = int(float(user_dict[12]))
        ffa_expense = int(float(user_dict[13]))
        giv_expense = int(float(user_dict[14]))

        nec_prebal = int(float(user_dict[15]))
        edu_prebal = int(float(user_dict[16]))
        lts_prebal = int(float(user_dict[17]))
        ply_prebal = int(float(user_dict[18]))
        ffa_prebal = int(float(user_dict[19]))
        giv_prebal = int(float(user_dict[20]))

        pre_balance = int(float(user_dict[21]))


        balance_amt = income_amt - expense_amt + pre_balance
        
        nec_balance = nec_income - nec_expense + nec_prebal
        edu_balance = edu_income - edu_expense + edu_prebal
        lts_balance = lts_income - lts_expense + lts_prebal
        ply_balance = ply_income - ply_expense + ply_prebal
        ffa_balance = ffa_income - ffa_expense + ffa_prebal
        giv_balance = giv_income - giv_expense + giv_prebal

        pre_date = user_dict[22]

        # if next month ?
        if (current_date != pre_date):
            print "HomePage:New month"
            #reset income/expense value, carry forward balance to next month
            income_amt = 0
            expense_amt = 0
            
            nec_income = 0
            edu_income = 0
            lts_income = 0
            ply_income = 0
            ffa_income = 0
            giv_income = 0

            nec_expense = 0
            edu_expense = 0
            lts_expense = 0
            ply_expense = 0
            ffa_expense = 0
            giv_expense = 0
            
            
            pre_balance = balance_amt
            nec_prebal = nec_balance
            edu_prebal = edu_balance
            lts_prebal = lts_balance
            ply_prebal = ply_balance
            ffa_prebal = ffa_balance
            giv_prebal = giv_balance

            #save to database
            r.hmset(user_id,{
                    'income_amt':income_amt,
                    'expense_amt':expense_amt,
                    'nec_income':nec_income,
                    'edu_income':edu_income,
                    'lts_income':lts_income,
                    'ply_income':ply_income,
                    'ffa_income':ffa_income,
                    'giv_income':giv_income,
                    'nec_expense':nec_expense,
                    'edu_expense':edu_expense,
                    'lts_expense':lts_expense,
                    'ply_expense':ply_expense,
                    'ffa_expense':ffa_expense,
                    'giv_expense':giv_expense,
                    'nec_prebal':nec_prebal,
                    'edu_prebal':edu_prebal,
                    'lts_prebal':lts_prebal,
                    'ply_prebal':ply_prebal,
                    'ffa_prebal':ffa_prebal,
                    'giv_prebal':giv_prebal,
                    'pre_balance':pre_balance,
                    'pre_date':current_date
                })

        # look for repeat transaction
        for key in r.hscan_iter(user_id, match='*repeat'):
            
            
            transactionID = key[0].replace('-repeat','')
            transactionValue = key[1]

            bRepeat = False

            key0 = key[0].split('-')
            key1 = key[1].split('-')

            repeat = key1[2]
            transaction_date = transactionDate = datetime.date(int(key0[0]), int(key0[1]), int(key0[2]))

            if (repeat == DAILY):
                while (transactionDate <= currentDate):
                    bRepeat = True
                    transaction_id = transactionID.replace(str(transaction_date),str(transactionDate))
                    transactionDate = transactionDate + datedelta.datedelta(days=1)
                    SaveTransactionPage(user_id, 'repeat', transaction_id, transactionValue)

            if (repeat == WEEKLY):
                while (transactionDate <= currentDate):
                    bRepeat = True
                    transaction_id = transactionID.replace(str(transaction_date),str(transactionDate))
                    transactionDate = transactionDate + datedelta.datedelta(days=7)
                    SaveTransactionPage(user_id, 'repeat', transaction_id, transactionValue)

            if (repeat == MONTHLY):
                while (transactionDate <= currentDate):
                    bRepeat = True
                    transaction_id = transactionID.replace(str(transaction_date),str(transactionDate))
                    transactionDate = transactionDate + datedelta.datedelta(months=1)
                    SaveTransactionPage(user_id, 'repeat', transaction_id, transactionValue)

            if (repeat == ANNUALLY):
                while (transactionDate <= currentDate):
                    bRepeat = True
                    transaction_id = transactionID.replace(str(transaction_date),str(transactionDate))
                    transactionDate = transactionDate + datedelta.datedelta(years=1)
                    SaveTransactionPage(user_id, 'repeat', transaction_id, transactionValue)

            if (bRepeat):
                transactionID = transactionID + '-repeat'
                r.hdel(user_id,transactionID)
                transaction_id = transactionID.replace(str(transaction_date),str(transactionDate))
                r.hset(user_id, transaction_id, transactionValue)   

        # calculate percentage for HomePage
        if (balance_amt > 0):
            percentage = int(float(balance_amt)/(balance_amt+expense_amt)*100)

        if (nec_balance > 0):
            nec_progress = int(float(nec_balance)/(nec_balance+nec_expense)*100)
            
            if (nec_progress >= 50):
                nec_progress_color = "TURQUOISE"
            elif (nec_progress >= 20):
                nec_progress_color = "GOLD"
            else:
                nec_progress_color = "TOMATO"       

        if (edu_balance > 0):
            edu_progress = int(float(edu_balance)/(edu_balance+edu_expense)*100)

            if (edu_progress >= 50):
                edu_progress_color = "TURQUOISE"
            elif (edu_progress >= 20):
                edu_progress_color = "GOLD"
            else:
                edu_progress_color = "TOMATO"
 

        if (lts_balance > 0):
            lts_progress = int(float(lts_balance)/(lts_balance+lts_expense)*100)

            if (lts_progress >= 50):
                lts_progress_color = "TURQUOISE"
            elif (lts_progress >= 20):
                lts_progress_color = "GOLD"
            else:
                lts_progress_color = "TOMATO"
 

        if (ply_balance > 0):
            ply_progress = int(float(ply_balance)/(ply_balance+ply_expense)*100)

            if (ply_progress >= 50):
                ply_progress_color = "TURQUOISE"
            elif (ply_progress >= 20):
                ply_progress_color = "GOLD"
            else:
                ply_progress_color = "TOMATO"
 

        if (ffa_balance > 0):
            ffa_progress = int(float(ffa_balance)/(ffa_balance+ffa_expense)*100)

            if (ffa_progress >= 50):
                ffa_progress_color = "TURQUOISE"
            elif (ffa_progress >= 20):
                ffa_progress_color = "GOLD"
            else:
                ffa_progress_color = "TOMATO"
 

        if (giv_balance > 0):
            giv_progress = int(float(giv_balance)/(giv_balance+giv_expense)*100)

            if (giv_progress >= 50):
                giv_progress_color = "TURQUOISE"
            elif (giv_progress >= 20):
                giv_progress_color = "GOLD"
            else:
                giv_progress_color = "TOMATO"
 
    
    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)

    #load currency json file
    with open('static/currency.json') as f:
        currency_data = json.load(f)
  

    title_caption=language_data[language]['dashboard_page']['title_caption'].encode('utf-8')
    nec_caption=language_data[language]['dashboard_page']['nec_caption'].encode('utf-8')
    edu_caption=language_data[language]['dashboard_page']['edu_caption'].encode('utf-8')
    lts_caption=language_data[language]['dashboard_page']['lts_caption'].encode('utf-8')
    ply_caption=language_data[language]['dashboard_page']['ply_caption'].encode('utf-8')
    ffa_caption=language_data[language]['dashboard_page']['ffa_caption'].encode('utf-8')
    giv_caption=language_data[language]['dashboard_page']['giv_caption'].encode('utf-8')
    balance_caption=language_data[language]['dashboard_page']['balance_caption'].encode('utf-8')
    income_caption=language_data[language]['dashboard_page']['income_caption'].encode('utf-8')
    expense_caption=language_data[language]['dashboard_page']['expense_caption'].encode('utf-8')

    for i in range(0,len(currency_data['currency'])):
        currency_code = currency_data['currency'][i]['currency_code']
        if (currency == currency_code):
            currency_sign = currency_data['currency'][i]['currency_sign']
            break
    
    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <meta name="format-detection" content="telephone=no">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>


    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    addZero = """
        function addZero(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }
    """

    if (user_login == 'google'):

        signOut_function = """
        function signOut() {

            document.location.href = "https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=https://moneyoi.herokuapp.com";

        };
        """
    elif (user_login == 'facebook'):
        signOut_function = """
        function signOut() {
            
            FB.logout(function(response) {
                // Logout and redirect to the home page

                document.location.href = "https://moneyoi.herokuapp.com";
                    
            });
           
        };
        """

    facebook_init = """
    window.fbAsyncInit = function() {
        FB.init({
            appId      : '392841268177993',
            cookie     : true,
            xfbml      : true,
            version    : 'v3.2'
        });

    };

    """

    jarFunction = """
    function jarFunction(user_id, historyType) {
        hisFunction(user_id, historyType)
    };
    """

 
    pieFunction = """
    function pieFunction(user_id, reportType) {

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var d = new Date();
        year = d.getFullYear();
        month = addZero(d.getMonth()+1);
        reportDate = year+'-'+month
        url = '/ReportPage/' + user_id + '/' + reportType + '/' + reportDate;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                

        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send();

    };
    """

    hisFunction = """

    function hisFunction(user_id, historyType) {
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var d = new Date();
        year = d.getFullYear();
        month = addZero(d.getMonth()+1);
        historyDate = year+'-'+month
        url = '/HistoryPage/' + user_id + '/' + historyType + '/' + historyDate;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send();

    };
    """

    cogFunction = """
    function cogFunction(user_id) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/SettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send();

    };
    """


    addTransaction = """
    function addTransaction(user_id, transactionType, jarOption, date) {

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/TransactionPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send("transactionType="+transactionType+"&jarOption="+jarOption+"&date="+date);

 
    }
    """

    doughnut_chart = """

        var expense_amt = document.getElementById("expense").value;
        var balance_amt = document.getElementById("balance").value;

        var percentage =  parseInt(document.getElementById('percentage').textContent);

        window.chartColors = {
	        lightgray: 'rgb(211, 211, 211)',
	        darkslategray: 'rgb(47, 79, 79)',
	        tomato: 'rgb(255, 99, 71)',
	        gold: 'rgb(255, 215, 0)',
            turquoise: 'rgb(64, 224, 208)'
        };

        var color = window.chartColors.turquoise;

        if (percentage >= 50) {
            color = window.chartColors.turquoise;
        } else {
            if (percentage >= 20) {
                color = window.chartColors.gold;
            } else {
                color = window.chartColors.tomato;
            }
            
        }

        // 100% percentage
        if (balance_amt == 0) {
            expense_amt = 1;
            balance_amt = 0;
        }

        var config = {
			type: 'doughnut',
			data: {
				datasets: [{
                    label:['Expense','Balance'],
					data: [expense_amt, balance_amt],
					backgroundColor: [window.chartColors.lightgray, color],
                    borderColor:[window.chartColors.darkslategray, window.chartColors.darkslategray],
				}],
				
			},
			options: {
                cutoutPercentage: 70,
				tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            return data.datasets[tooltipItem.datasetIndex].label[tooltipItem.index];
                        }
                    }
                },
			}
		};

		var ctx = document.getElementById('myChart')
		new Chart(ctx, config);
        
    """

    percentage_width = """
        
        var element =  document.getElementById('percentage');
        var percentage = element.textContent;

        var per = parseInt(percentage);

        if (per == 100) {
            element.setAttribute("style", "position: absolute; display: block; text-align:center; padding-left:25px; padding-top:35px; font-weight:300;");
        } else {
            if (per < 10) {
                element.setAttribute("style", "position: absolute; display: block; text-align:center; padding-left:32px; padding-top:35px; font-weight:300;");

            }
            else {
                element.setAttribute("style", "position: absolute; display: block; text-align:center; padding-left:28px; padding-top:35px; font-weight:300;");

            }
        };

    """    


    six_jars_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            padding-bottom: 4em;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }


        input[type="button"] {
            display: none;
        }
        
        .sixjars-label-class {
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            cursor: pointer;
            padding: 6px 0px;
            width: 100%;
            height: 35px;
            font-weight:400;
        }

        .sixjars-label-class:active {
            color: DARKSLATEGRAY;
            border: 1px solid LIGHTGRAY;
        }

        .balance-label-class {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 100px;
        }


        .income-expense-label {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 70px;

        }

        
        .menu-label {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 10px 0px;
            width: 100%;
            height: 50px;
            text-align: center;
        }


        .bottom-label {
            display: block;
            margin-left: auto;
            margin-right: auto;
            height: 45px;
            text-align: center;
            bottom: 0;
            position: absolute;
            width: 100%;
            font-weight:300;
        }

       
        .minus-button-label {
            color: TURQUOISE;
            cursor: pointer;
            display: block;
            text-align: center;
        }


        .minus-button-label:active {
            color: LIGHTGRAY;
        }

        .menu-button-label {
            display: block;
            color: LIGHTGRAY;
            cursor: pointer;
        }

        
        .menu-button-label:active {
            color: TURQUOISE;
        }
        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            padding-top: 50%;
            position:absolute;
            background: rgba(0, 0, 0, 0.3)
        }

        .progress-class {
            background-color:LIGHTGRAY;
            height:2px;
            width:100px;
        }
        

    """


    mid_html = """
    
    <style>
        /*------ six jars style ---------*/
        {six_jars_style}
    </style>


    <div class="container">

        <div class="col-sx-12" style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>
  

        <div class="sixjars-class">

            <input id="nec-submit" type="button" onclick="jarFunction('{user_id}','Necessities')">
            <input id="edu-submit" type="button" onclick="jarFunction('{user_id}','Education')"> 
            <input id="lts-submit" type="button" onclick="jarFunction('{user_id}','Saving')"> 
            <input id="ply-submit" type="button" onclick="jarFunction('{user_id}','Play')"> 
            <input id="ffa-submit" type="button" onclick="jarFunction('{user_id}','Investment')"> 
            <input id="giv-submit" type="button" onclick="jarFunction('{user_id}','Give')"> 


            <label for="nec-submit" class="sixjars-label-class">
                <div class="col-xs-6" style="padding-left:7px">
                    <p class="text-left" style="font-weight:300;"><img src="/static/nec.png" style="width:24px;height:24px;">&nbsp {nec_caption}</p>
                </div>
                <div class="col-xs-6">
                    <p class="text-right" style="color:white;">{nec_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                    <div class="progress-class" style="position:absolute; top: 20px; right:15px;">
                        <div id="nec-progress" style="background-color:{nec_progress_color}; height:100%; width:{nec_progress}%"></div>
                    </div>
                </div>
            </label>


            <label for="edu-submit" class="sixjars-label-class">
                <div class="col-xs-6" style="padding-left:7px">
                    <p class="text-left" style="font-weight:300;"><img src="/static/edu.png" style="width:24px;height:24px;">&nbsp {edu_caption}</p>
                </div>
                <div class="col-xs-6">
                    <p class="text-right" style="color:white;">{edu_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                    <div class="progress-class" style="position:absolute; top: 20px; right:15px;">
                        <div id="edu-progress" style="background-color:{edu_progress_color}; height:100%; width:{edu_progress}%"></div>
                    </div>
                </div>
            </label>


            <label for="lts-submit" class="sixjars-label-class">
                <div class="col-xs-6" style="padding-left:7px">
                    <p class="text-left" style="font-weight:300;"><img src="/static/lts.png" style="width:24px;height:24px;">&nbsp {lts_caption}</p>
                </div>
                <div class="col-xs-6">
                    <p class="text-right" style="color:white;">{lts_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                    <div class="progress-class" style="position:absolute; top: 20px; right:15px;">
                        <div id="lts-progress" style="background-color:{lts_progress_color}; height:100%; width:{lts_progress}%"></div>
                    </div>
                </div>
            </label>


            <label for="ply-submit" class="sixjars-label-class">
                <div class="col-xs-6" style="padding-left:7px">
                    <p class="text-left" style="font-weight:300;"><img src="/static/ply.png" style="width:24px;height:24px;">&nbsp {ply_caption}</p>
                </div>
                <div class="col-xs-6">
                    <p class="text-right" style="color:white;">{ply_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                    <div class="progress-class" style="position:absolute; top: 20px; right:15px;">
                        <div id="ply-progress" style="background-color:{ply_progress_color}; height:100%; width:{ply_progress}%"></div>
                    </div>
                </div>
            </label>
            
            <label for="ffa-submit" class="sixjars-label-class">
                <div class="col-xs-6" style="padding-left:7px">
                    <p class="text-left" style="font-weight:300;"><img src="/static/ffa.png" style="width:24px;height:24px;">&nbsp {ffa_caption}</p>
                </div>
                <div class="col-xs-6">
                    <p class="text-right" style="color:white;">{ffa_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                    <div class="progress-class" style="position:absolute; top: 20px; right:15px;">
                        <div id="ffa-progress" style="background-color:{ffa_progress_color}; height:100%; width:{ffa_progress}%"></div>
                    </div>
                </div>
            </label>


            <label for="giv-submit" class="sixjars-label-class">
                <div class="col-xs-6" style="padding-left:7px">
                    <p class="text-left" style="font-weight:300;"><img src="/static/giv.png" style="width:24px;height:24px;">&nbsp {giv_caption}</p>
                </div>
                <div class="col-xs-6">
                    <p class="text-right" style="color:white;">{giv_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                    <div class="progress-class" style="position:absolute; top: 20px; right:15px;">
                        <div id="giv-progress" style="background-color:{giv_progress_color}; height:100%; width:{giv_progress}%"></div>
                    </div>
                </div>
            </label>

        </div>

        <div class="balance-class">
            <label class="balance-label-class">
                <div class="col-xs-3" style="display:block; text-align:center; padding-left:10px">
                    <div class="text-center" style="display: block; margin: 0 auto; width: 80px; height: 80px">
                        <p id="percentage" class="text-center">{percentage}%</p>
                        <canvas id="myChart" style="width:100%; height:100%"></canvas> 
                    </div>
                </div>
                <div class="col-xs-9" style="padding-top:10px;">
                    <p class="text-left" style="font-weight:300;">{balance_caption} ({currency_sign})</p>
                    <p class="text-left" style="font-weight:300; font-size:xx-large; color:white;">{balance_amt}</p>
                    <li id="balance" value="{balance_amt2}" style="display:none"></li>
                </div>
            </label>
        </div>

        <div class="income-expense">
            <label class="income-expense-label">
                <div class="col-xs-5" style="padding: 0;">
                    <input id="income-submit" type="button" onclick=addTransaction('{user_id}','new-income','jarOption','date')>
                    <label for="income-submit" class="income-button-label" style="cursor:pointer; width:100%; padding-left:18px;">
                        <p class="text-left" style="font-weight:300;">{income_caption} &nbsp <i class="fa fa-plus" style="color:LIME"></i></p>
                        <p class="text-left" style="color:white; font-weight:400;">{income_amt} {currency_sign}</p>
                        <li id="income" value="{income_amt2}" style="display:none"></li>
                    </label>
                </div>
                <div class="col-xs-2" style="padding: 0">
                    <input id="minus-submit" type="button" onclick="addTransaction('{user_id}','new-expense','jarOption','date')">
                    <label for="minus-submit" class="minus-button-label">
                        <p ><i class="fa fa-minus-circle fa-4x"></i></p>
                    </label>
                </div>
                <div class="col-xs-5" style="padding: 0">
                    <input id="expense-submit" type="button" onclick="addTransaction('{user_id}','new-expense','jarOption','date')">
                    <label for="expense-submit" class="expense-button-label" style="cursor:pointer; width:100%; padding-right:18px;">
                        <p class="text-right" style="font-weight:300;"> <i class="fa fa-minus" style="color:TOMATO"></i>&nbsp {expense_caption}</p>
                        <p class="text-right" style="color:white; font-weight:400;">{expense_amt} {currency_sign}</p>
                        <li id="expense" value="{expense_amt2}" style="display:none"></li>
                    </label>
                </div>
            </label>
        </div>

        <div class="menu-class">
            <label class="menu-label">
                <div class="col-xs-3">
                    <input id="home-submit" type="button">
                    <label for="home-submit" class="menu-button-label">
                        <i class="fa fa-home fa-2x" style="color:TURQUOISE"></i>
                    </label>
                </div>
                <div class="col-xs-3">
                    <input id="history-submit" type="button" onclick="hisFunction('{user_id}','All')">
                    <label for="history-submit" class="menu-button-label">
                        <i class="fa fa-history fa-2x"></i>
                    </label>
                </div>
                <div class="col-xs-3">
                    <input id="pie-submit" type="button" onclick="pieFunction('{user_id}','All')">
                    <label for="pie-submit" class="menu-button-label">
                        <i class="fa fa-pie-chart fa-2x"></i>
                    </label>
                </div>
                <div class="col-xs-3">
                    <input id="cog-submit" type="button" onclick="cogFunction('{user_id}')">
                    <label for="cog-submit" class="menu-button-label">
                        <i class="fa fa-cog fa-2x"></i>
                    </label>
                </div>
            </label>

        </div>
	
        <script>
            {facebook_init}
            {addZero}
            {doughnut_chart}
            {signOut_function}
            {addTransaction}
            {jarFunction}
            {percentage_width}
            {pieFunction}
            {hisFunction}
            {cogFunction}

        </script>

        <div id="fb-root"></div>
        <script async defer src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v3.2&appId=392841268177993&autoLogAppEvents=1"></script>
       
    </div>


    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <div class="bottom-class">
        <label class="bottom-label">
            <p style="color: white;">
                Signed in as {user_email}
                <br> <a href="javascript:void(0)" onclick="signOut();" style="color:TURQUOISE">Sign out</a>
            </p>
        </label>
    </div>
   
    """.format(user_id=user_id,
                signOut_function=signOut_function,
                nec_balance="{:,}".format(nec_balance),
                edu_balance="{:,}".format(edu_balance),
                lts_balance="{:,}".format(lts_balance),
                ply_balance="{:,}".format(ply_balance),
                ffa_balance="{:,}".format(ffa_balance),
                giv_balance="{:,}".format(giv_balance),
                six_jars_style=six_jars_style,
                balance_amt="{:,}".format(balance_amt),
                addZero=addZero,
                doughnut_chart=doughnut_chart,
                percentage=percentage,
                percentage_width=percentage_width,
                income_amt="{:,}".format(income_amt),
                expense_amt="{:,}".format(expense_amt),
                income_amt2=income_amt,
                expense_amt2=expense_amt,
                balance_amt2=balance_amt,
                addTransaction=addTransaction,
                jarFunction=jarFunction,
                pieFunction=pieFunction,
                hisFunction=hisFunction,
                cogFunction=cogFunction,
                nec_progress=nec_progress,
                edu_progress=edu_progress,
                lts_progress=lts_progress,
                ply_progress=ply_progress,
                ffa_progress=ffa_progress,
                giv_progress=giv_progress,
                nec_progress_color=nec_progress_color,
                edu_progress_color=edu_progress_color,
                lts_progress_color=lts_progress_color,
                ply_progress_color=ply_progress_color,
                ffa_progress_color=ffa_progress_color,
                giv_progress_color=giv_progress_color,
                currency_sign=currency_sign,
                title_caption=title_caption,
                nec_caption=nec_caption,
                edu_caption=edu_caption,
                lts_caption=lts_caption,
                ply_caption=ply_caption,
                ffa_caption=ffa_caption,
                giv_caption=giv_caption,
                balance_caption=balance_caption,
                income_caption=income_caption,
                expense_caption=expense_caption,
                user_email=user_email,
                facebook_init=facebook_init)
    
    return begin_html + mid_html + end_html


@app.route('/TransactionPage/<user_id>', methods=['POST'])
def TransactionPage(user_id):
    
    transactionType = request.form['transactionType']

    print "TransactionPage:user_id:"+user_id
    print "TransactionPage:transactionType:"+transactionType


    initValue = """
        var d = new Date();
        var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());
        document.getElementById('theDate').value = today;
        document.getElementById('amount-input').focus();
    """
    jarOption = ""
    date = ""

    user_dict = r.hmget(user_id,
                        'currency',
                        'nec_income',
                        'edu_income',
                        'lts_income',
                        'ply_income',
                        'ffa_income',
                        'giv_income',
                        'nec_expense',
                        'edu_expense',
                        'lts_expense',
                        'ply_expense',
                        'ffa_expense',
                        'giv_expense',
                        'nec_prebal',
                        'edu_prebal',
                        'lts_prebal',
                        'ply_prebal',
                        'ffa_prebal',
                        'giv_prebal',
                        'language')

    currency = user_dict[0]
    language = user_dict[19]

    
    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)
    
    #load currency json file
    with open('static/currency.json') as f:
        currency_data = json.load(f)


    title_caption=language_data[language]['transaction_page']['title_caption']
    all_caption=language_data[language]['transaction_page']['all_caption']
    nec_caption=language_data[language]['transaction_page']['nec_caption']
    edu_caption=language_data[language]['transaction_page']['edu_caption']
    lts_caption=language_data[language]['transaction_page']['lts_caption']
    ply_caption=language_data[language]['transaction_page']['ply_caption']
    ffa_caption=language_data[language]['transaction_page']['ffa_caption']
    giv_caption=language_data[language]['transaction_page']['giv_caption']
    income_caption=language_data[language]['transaction_page']['income_caption']
    expense_caption=language_data[language]['transaction_page']['expense_caption']
    amount_title_caption=language_data[language]['transaction_page']['amount_title_caption']
    amount_caption=language_data[language]['transaction_page']['amount_caption']
    once_caption=language_data[language]['transaction_page']['once_caption']
    daily_caption=language_data[language]['transaction_page']['daily_caption']
    weekly_caption=language_data[language]['transaction_page']['weekly_caption']
    monthly_caption=language_data[language]['transaction_page']['monthly_caption']
    annually_caption=language_data[language]['transaction_page']['annually_caption']
    description_caption=language_data[language]['transaction_page']['description_caption']
    msg_successful_caption=language_data[language]['transaction_page']['msg_successful_caption']
    msg_amount_caption=language_data[language]['transaction_page']['msg_amount_caption']
    msg_over_caption=language_data[language]['transaction_page']['msg_over_caption']
    save_caption=language_data[language]['transaction_page']['save_caption']
    back_caption=language_data[language]['transaction_page']['back_caption']


    for i in range(0,len(currency_data['currency'])):
        currency_code = currency_data['currency'][i]['currency_code']
        if (currency == currency_code):
            currency_sign = currency_data['currency'][i]['currency_sign']
            break

    nec_income = int(float(user_dict[1]))
    edu_income = int(float(user_dict[2]))
    lts_income = int(float(user_dict[3]))
    ply_income = int(float(user_dict[4]))
    ffa_income = int(float(user_dict[5]))
    giv_income = int(float(user_dict[6]))

    nec_expense = int(float(user_dict[7]))
    edu_expense = int(float(user_dict[8]))
    lts_expense = int(float(user_dict[9]))
    ply_expense = int(float(user_dict[10]))
    ffa_expense = int(float(user_dict[11]))
    giv_expense = int(float(user_dict[12]))

    nec_prebal = int(float(user_dict[13]))
    edu_prebal = int(float(user_dict[14]))
    lts_prebal = int(float(user_dict[15]))
    ply_prebal = int(float(user_dict[16]))
    ffa_prebal = int(float(user_dict[17]))
    giv_prebal = int(float(user_dict[18]))

    nec_balance = nec_income - nec_expense + nec_prebal
    edu_balance = edu_income - edu_expense + edu_prebal
    lts_balance = lts_income - lts_expense + lts_prebal
    ply_balance = ply_income - ply_expense + ply_prebal
    ffa_balance = ffa_income - ffa_expense + ffa_prebal
    giv_balance = giv_income - giv_expense + giv_prebal
    
    transactionID = ""
    transactionValue = ""

    #default TransactionPage is "new-income" transactionType
    if (transactionType == "new-expense"):
        
        initValue = """
            var sign_symbol = document.getElementById('sign-symbol');       
            sign_symbol.setAttribute("class", "fa fa-minus");
            sign_symbol.style.color = "TOMATO";

            document.getElementById('expense-option').selected = "selected";

            document.getElementById('amount-input').focus();

            document.getElementById('nec-option').selected = "selected";

            var d = new Date();         
            var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());
            document.getElementById('theDate').value = today;

            document.getElementById('all-option').disabled = "disabled";
            
        """
    else:
        if ((transactionType == "update") or (transactionType == "recurring-update")):
            transactionID = request.form['transactionID']
            transactionValue = request.form['transactionValue'].replace("#","&")
            jarOption = request.form['jarOption']
            date = request.form['date']


            print "TransactionPage:transactionID:"+transactionID
            print "TransactionPage:transactionValue:"+transactionValue.encode('utf-8')
            print "TransactionPage:jarOption:"+jarOption
            print "TransactionPage:date:"+date

            key = transactionID.split('-')
            value = transactionValue.split('-')
            
            year = key[0]
            month = key[1]
            day = key[2]
         
            theDate = year+'-'+month+'-'+day

            ttype = value[0]
            jar = value[1]
            repeat = value[2]
            description = value[3]

            amount = "{:,}".format(int(float(value[4])))
            
            if (ttype=="Income"):
                sign_symbol = "fa fa-plus"
                color = "LIME"
                ttype_option="income-option"
                all_option = ""
            else:
                sign_symbol = "fa fa-minus"
                color = "TOMATO"
                ttype_option="expense-option"
                all_option = """
                    document.getElementById('all-option').disabled = 'disabled'
                """

            jar_option = JAR_OPTION[jar]
            repeat_type = REPEAT_TYPE[repeat]
            
            initValue = all_option + u"""
                var sign_symbol = document.getElementById('sign-symbol');       
                sign_symbol.setAttribute("class", "{sign_symbol}");
                sign_symbol.style.color = "{color}";

                document.getElementById('{ttype_option}').selected = "selected";

                var amount_input = document.getElementById('amount-input');
                amount_input.value = '{amount}';
                amount_input.focus();
             
                document.getElementById('{jar_option}').selected = "selected";


                document.getElementById('theDate').value = '{theDate}';

                document.getElementById('{repeat_type}').selected = "selected";

                document.getElementById('desc-input').value = '{description}';

            """.format(sign_symbol=sign_symbol,
                        color=color,
                        ttype_option=ttype_option,
                        amount=amount,
                        jar_option=jar_option,
                        theDate=theDate,
                        repeat_type=repeat_type,
                        description=description)            
        # report/history-new-income & report/history-new-expense transactionType
        elif (transactionType != 'new-income'):
            jarOption = request.form['jarOption']
            date = request.form['date']

            print "TransactionPage:jarOption:"+jarOption
            print "TransactionPage:date:"+date

            jar_option = JAR_OPTION[jarOption]

            if ((transactionType=="history-new-income") or (transactionType=="report-new-income")):
                sign_symbol = "fa fa-plus"
                color = "LIME"
                ttype_option="income-option"
                all_option = ""
            else:
                sign_symbol = "fa fa-minus"
                color = "TOMATO"
                ttype_option="expense-option"
                all_option = """
                    document.getElementById('all-option').disabled = 'disabled'
                """

                if ((transactionType == 'report-new-expense') and (jarOption == ALL)):
                    jar_option = JAR_OPTION[NEC]


            initValue = all_option + """
                var sign_symbol = document.getElementById('sign-symbol');       
                sign_symbol.setAttribute("class", "{sign_symbol}");
                sign_symbol.style.color = "{color}";

                document.getElementById('{ttype_option}').selected = "selected";

                document.getElementById('amount-input').focus();
                
                document.getElementById('{jar_option}').selected = "selected";

                
                var d = new Date();         
                var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());
                document.getElementById('theDate').value = today;

            """.format(sign_symbol=sign_symbol,
                        color=color,
                        ttype_option=ttype_option,
                        jar_option=jar_option) 

    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    #handle float amount
    format_amount_input = r"""
    document.getElementById('amount-input').addEventListener('input', function(event) {

        value_b = event.target.value.replace(/[^\d.]+/gi, '');

        event.target.value = (parseInt(value_b) || '').toLocaleString('en-US');

    });         
    """


    addZero = """
        function addZero(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }
    """

    selectTransaction = """
    function selectTransaction() {
        var transaction = document.getElementById('transaction-type');
        var sign_symbol = document.getElementById('sign-symbol');
        var all_option = document.getElementById('all-option');
        var nec_option = document.getElementById('nec-option');

        
        if (transaction.value == "Income") {
            sign_symbol.setAttribute("class", "fa fa-plus");
            sign_symbol.style.color = "LIME";
            all_option.removeAttribute("disabled");
            all_option.selected = "selected";
        } else {
            sign_symbol.setAttribute("class", "fa fa-minus");
            sign_symbol.style.color = "TOMATO";
            nec_option.selected = "selected";
            all_option.disabled = "disabled";

        }
         
    };
    """

    save = """

    function save(user_id, transactionType, transactionID, transactionValue, jarOption, date, nec_balance, edu_balance, lts_balance, ply_balance, ffa_balance, giv_balance) {


        var theDate = document.getElementById("theDate").value;
        var type = document.getElementById("transaction-type").value;
        var jar = document.getElementById('jar-type').value;
        var repeat = document.getElementById('repeat-type').value;
        var desc = document.getElementById('desc-input').value;
        var amount = document.getElementById('amount-input').value.replace(/,/g,'');
        var error_msg =document.getElementById('error-msg');
        var info_msg =document.getElementById('info-msg');
        var msg =document.getElementById('msg-label');
        var time = new Date();
        var msg_successful_label=document.getElementById('msg-successful-label');
        var msg_amount_label=document.getElementById('msg-amount-label');
        var msg_over_label=document.getElementById('msg-over-label');

        if (desc == "") {
            desc = type;
        } else {
            desc = desc.replace(/&/g,'#');
            desc = desc.replace(/-/g,'_');
        }

        if (amount == "") {
            msg.style.color="gold";
            msg.setAttribute("class", "fa fa-warning");
            msg.textContent = msg_amount_label.textContent;
            msg.style.display = "block";

            return;
        } 
        
        // only applicable for expense transaction
        if (type == 'Expense') {
            // update transaction
            if ((transactionType == 'update') || (transactionType == 'recurring-update')) {
                transactionValue = transactionValue.replace(/&/g,'#');
                old_transaction_value = transactionValue.split('-');
                old_amount = parseFloat(old_transaction_value[4]);
                old_jar = old_transaction_value[1];

                // same jar
                if (jar == old_jar) {

                    if (((jar == 'Necessities') && (parseFloat(amount) > (parseFloat(nec_balance)+old_amount))) ||
                        ((jar == 'Education') && (parseFloat(amount) > (parseFloat(edu_balance)+old_amount))) ||
                        ((jar == 'Saving') && (parseFloat(amount) > (parseFloat(lts_balance)+old_amount))) ||
                        ((jar == 'Play') && (parseFloat(amount) > (parseFloat(ply_balance)+old_amount))) ||
                        ((jar == 'Investment') && (parseFloat(amount) > (parseFloat(ffa_balance)+old_amount))) ||
                        ((jar == 'Give') && (parseFloat(amount) > (parseFloat(giv_balance)+old_amount)))) {

                        msg.style.color="gold";
                        msg.setAttribute("class", "fa fa-warning");
                        msg.textContent = msg_over_label.textContent;
                        msg.style.display = "block";

                        return;
                    }

                }
                // change jar
                else {
                    if (((jar == 'Necessities') && (parseFloat(amount) > parseFloat(nec_balance))) ||
                        ((jar == 'Education') && (parseFloat(amount) > parseFloat(edu_balance))) ||
                        ((jar == 'Saving') && (parseFloat(amount) > parseFloat(lts_balance))) ||
                        ((jar == 'Play') && (parseFloat(amount) > parseFloat(ply_balance))) ||
                        ((jar == 'Investment') && (parseFloat(amount) > parseFloat(ffa_balance))) ||
                        ((jar == 'Give') && (parseFloat(amount) > parseFloat(giv_balance)))) {

                        msg.style.color="gold";
                        msg.setAttribute("class", "fa fa-warning");
                        msg.textContent = msg_over_label.textContent;
                        msg.style.display = "block";

                        return;
                    }
                }

            } 
            // new transaction
            else {
                if (((jar == 'Necessities') && (parseFloat(amount) > parseFloat(nec_balance))) ||
                    ((jar == 'Education') && (parseFloat(amount) > parseFloat(edu_balance))) ||
                    ((jar == 'Saving') && (parseFloat(amount) > parseFloat(lts_balance))) ||
                    ((jar == 'Play') && (parseFloat(amount) > parseFloat(ply_balance))) ||
                    ((jar == 'Investment') && (parseFloat(amount) > parseFloat(ffa_balance))) ||
                    ((jar == 'Give') && (parseFloat(amount) > parseFloat(giv_balance)))) {

                    msg.style.color="gold";
                    msg.setAttribute("class", "fa fa-warning");
                    msg.textContent = msg_over_label.textContent;
                    msg.style.display = "block";

                    return;
                }
            }
        }
        
        
        // ready to save transaction

        var newTransactionID = theDate+'-'+addZero(time.getHours())+'-'+addZero(time.getMinutes())+'-'+addZero(time.getSeconds());
        var newTransactionValue = type+'-'+jar+'-'+repeat+'-'+desc+'-'+amount;
                
        if (transactionType == 'recurring-update') {
            newTransactionID = newTransactionID + '-repeat'
        }

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        if ((transactionType == 'update') || (transactionType == 'recurring-update')) {

            old_transaction_id = transactionID.split('-');
            old_date = old_transaction_id[0]+'-'+old_transaction_id[1]+'-'+old_transaction_id[2];

            if (theDate == old_date) {
                newTransactionID = transactionID;
            }

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/UpdateTransactionPage/'+user_id, true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                        
            xhr.onload = function() {
                document.open();
                document.write(xhr.responseText);
                document.close();
            };

            xhr.send("transactionType="+transactionType+"&oldTransactionID="+transactionID+"&oldTransactionValue="+transactionValue+
                    "&newTransactionID="+newTransactionID+"&newTransactionValue="+newTransactionValue+
                    "&jarOption="+jarOption+"&date="+date);
                    
        }
        else {
            var xhr = new XMLHttpRequest();

            xhr.open('POST', '/SaveTransactionPage/' + user_id + '/add/transactionID/transactionValue', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                        
            xhr.onload = function() {
                msg.style.color="lime";
                msg.setAttribute("class", "fa fa-info-circle");
                msg.textContent = msg_successful_label.textContent;
                msg.style.display = "block";

                waiting.style.display="none";

            };

            xhr.send("transactionID="+newTransactionID+"&transactionValue="+newTransactionValue);
        }
        
            
    };
    """

    back = """
    function back(user_id, transactionType, jarOption, date) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var d = new Date();
        var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());

        url = '/HomePage/'+ user_id + '/' + today;

        if ((transactionType == 'update') || 
            (transactionType == 'history-new-income') || 
            (transactionType == 'history-new-expense')) {

            url = '/HistoryPage/' + user_id + '/' + jarOption + '/' + date;

        } else if ((transactionType == 'report-new-income') || 
                    (transactionType == 'report-new-expense')) {

            url = '/ReportPage/' + user_id + '/' + jarOption + '/' + date;

        } else if (transactionType == 'recurring-update') {
            url = '/RecurringTransactionPage/' + user_id;
        }
            

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };

        xhr.send('sender_id=TransactionPage');
 
    };
    """
    

    addtransaction_style = """


        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

    
        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }

        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

    """

    mid_html = u"""
    
    <style>
        /*------ addtransaction style ---------*/
        {addtransaction_style}
    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        <div class="transaction-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <label style="font-weight: 300; border: 1px solid DARKSLATEGRAY; height:35px; width: 100%; padding-left: 15px; padding-top:7px">
                    <i id ="sign-symbol" class="fa fa-plus" style="color:LIME"></i>&nbsp
                    <select id="transaction-type" onchange="selectTransaction()" style="cursor:pointer; width: calc(100% - 20px); background-color: SLATEGRAY; border:none; outline:none; -webkit-appearance: none;">
                        <option id='income-option' value='Income'>{income_caption}</option>
                        <option id='expense-option' value='Expense'>{expense_caption}</option>
                    </select>

                    <i id ="sign-symbol" class="fa fa-angle-down" style="position:absolute; top:10px; right:15px"></i>

                </label>
            </div>
            
        </div>


        <div class="amount-class" style="height:75px; color: LIGHTGRAY;">
            
            <div class="col-xs-9" style="height:100%; padding: 0;">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:70px; width: 100%; padding-left: 15px; padding-top:10px">
                    {amount_title_caption}
                    <input id="amount-input" type="text" maxlength="15" placeholder="{amount_caption}" style="font-size: x-large; width:100%; padding:0; color:white; background-color: DARKSLATEGRAY; border:none; outline:none; -webkit-appearance: none;">
                </label>
        
            </div>

            <div class="col-xs-3" style="height:100%; padding: 0;">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:70px; width: 100%; padding-top: 30px; text-align:right; padding-right:15px">
                    <font style="border-radius: 10px; background-color:SLATEGRAY; color:LIME; font-size:x-large">&nbsp {currency_sign} &nbsp</font>
                </label>
            </div>

            
        </div>

        <div class="jars-class" style="height:45px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:40px; width: 100%; padding-left: 15px; padding-top:10px">
                    <i class="fa fa-flask"></i>&nbsp
                    <select id="jar-type" style="cursor:pointer; width: calc(100% - 25px); background-color: DARKSLATEGRAY; border:none; outline:none; -webkit-appearance: none;">
                        <option id='all-option' value='All'>{all_caption}</option>
                        <option id='nec-option' value='Necessities'>{nec_caption}</option>
                        <option id='edu-option' value='Education'>{edu_caption}</option>
                        <option id='lts-option' value='Saving'>{lts_caption}</option>
                        <option id='ply-option' value='Play'>{ply_caption}</option>
                        <option id='ffa-option' value='Investment'>{ffa_caption}</option>
                        <option id='giv-option' value='Give'>{giv_caption}</option>
                    </select>

                    <i class="fa fa-angle-down" style="position:absolute; top:12px; right:15px"></i>

                </label>
            </div>
            
        </div>

        <div class="date-class" style="height:45px; color: LIGHTGRAY;">
            
            <div class="col-xs-8" style="height:100%; padding: 0">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:40px; width: 100%; padding-left: 15px; padding-top:7px">
                    <i class="fa fa-calendar"></i>&nbsp
                    <input type="date" id="theDate" style="cursor:pointer; width: calc(100% - 25px); background-color: DARKSLATEGRAY; border:none; outline:none; -webkit-appearance: none;">
                </label>

            </div>

            <div class="col-xs-4" style="height:100%; padding: 0">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:40px; width: 100%; padding-top:9px">
                    <select id="repeat-type" style="direction:rtl; padding-right:30px; cursor:pointer; width: 100%; background-color: DARKSLATEGRAY; border:none; outline:none; -webkit-appearance: none;">
                        <option id="once-type" value='Once'>{once_caption}</option>
                        <option id="daily-type" value='Daily'>{daily_caption}</option>
                        <option id="weekly-type" value='Weekly'>{weekly_caption}</option>
                        <option id="monthly-type" value='Monthly'>{monthly_caption}</option>
                        <option id="annually-type" value='Annually'>{annually_caption}</option>
                    </select>
                    <i id class="fa fa-angle-down" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
            
        </div>

        <div class="desc-class" style="height:45px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:40px; width: 100%; padding-left: 15px; padding-top:10px">
                    <i class="fa fa-pencil"></i>&nbsp
                    
                    <input id="desc-input" type="text" placeholder="{description_caption}" style="width:90%; padding:0; color:white; background-color: DARKSLATEGRAY; border:none; outline:none; -webkit-appearance: none;">

                </label>
            </div>
            
        </div>

        <p></p>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="save" type="button" onclick="save('{user_id}', '{transactionType}', '{transactionID}', '{transactionValue}', '{jarOption}', '{date}', '{nec_balance}', '{edu_balance}', '{lts_balance}', '{ply_balance}', '{ffa_balance}', '{giv_balance}')"> 
                <label class="save-class" for="save">
                    <i class="fa fa-floppy-o" style="color:LIME"></i>&nbsp {save_caption}
                </label>
            </div>
            
        </div>
    
        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}','{transactionType}','{jarOption}','{date}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>


    </div>           

    <p></p>
         

    <div class="msg-class">           
        <label id="msg-label" style="text-align:center; display:none;"><i class="fa fa-info-circle"></i></label>
        <label id="msg-successful-label" style="display:none;">&nbsp {msg_successful_caption}</label>
        <label id="msg-amount-label" style="display:none">&nbsp {msg_amount_caption}</label>
        <label id="msg-over-label" style="display:none">&nbsp {msg_over_caption}</label>
    </div>


    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>


    <script>
        {addZero}
        {selectTransaction}
        {format_amount_input}
        {save}
        {back}
        {initValue}
    </script>
    
    """.format(user_id=user_id,
                addtransaction_style=addtransaction_style,
                format_amount_input=format_amount_input,
                addZero=addZero,
                selectTransaction=selectTransaction,
                save=save,
                back=back,
                initValue=initValue,
                nec_balance=nec_balance,
                edu_balance=edu_balance,
                lts_balance=lts_balance,
                ply_balance=ply_balance,
                ffa_balance=ffa_balance,
                giv_balance=giv_balance,
                transactionType=transactionType,
                jarOption=jarOption,
                date=date,
                transactionID=transactionID,  
                transactionValue=transactionValue,
                currency_sign=currency_sign,
                title_caption=title_caption,
                expense_caption=expense_caption,
                income_caption=income_caption,
                amount_title_caption=amount_title_caption,
                amount_caption=amount_caption,
                all_caption=all_caption,
                nec_caption=nec_caption,
                edu_caption=edu_caption,
                lts_caption=lts_caption,
                ply_caption=ply_caption,
                ffa_caption=ffa_caption,
                giv_caption=giv_caption,
                once_caption=once_caption,
                daily_caption=daily_caption,
                weekly_caption=weekly_caption,
                monthly_caption=monthly_caption,
                annually_caption=annually_caption,
                description_caption=description_caption,
                msg_successful_caption=msg_successful_caption,
                msg_amount_caption=msg_amount_caption,
                msg_over_caption=msg_over_caption,
                save_caption=save_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/HistoryPage/<user_id>/<historyType>/<historyDate>', methods=['POST'])
def HistoryPage(user_id, historyType, historyDate):
    
    print "HistoryPage:user_id:"+user_id
    print "HistoryPage:historyType:"+historyType
    print "HistoryPage:historyDate:"+historyDate


    table_begin = """
        <table>
    """
    table_end = """
        </table>
    """

    table_body = ""


    income_amt = 0
    expense_amt = 0
    balance_amt = 0


    nec_amount = 0
    edu_amount = 0
    lts_amount = 0
    ply_amount = 0
    ffa_amount = 0
    giv_amount = 0

    progress_color= "LIGHTGRAY"
    progress = 0
    jar_url = ""

    user_dict = r.hmget(user_id,
                        'nec_income',
                        'edu_income',
                        'lts_income',
                        'ply_income',
                        'ffa_income',
                        'giv_income',
                        'nec_expense',
                        'edu_expense',
                        'lts_expense',
                        'ply_expense',
                        'ffa_expense',
                        'giv_expense',
                        'nec_prebal',
                        'edu_prebal',
                        'lts_prebal',
                        'ply_prebal',
                        'ffa_prebal',
                        'giv_prebal',
                        'currency',
                        'language')

    
    currency = user_dict[18]
    language = user_dict[19]

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)
    
    #load currency json file
    with open('static/currency.json') as f:
        currency_data = json.load(f)

    title_caption=language_data[language]['history_page']['title_caption'].encode('utf-8')
    all_caption=language_data[language]['history_page']['all_caption'].encode('utf-8')
    nec_caption=language_data[language]['history_page']['nec_caption'].encode('utf-8')
    edu_caption=language_data[language]['history_page']['edu_caption'].encode('utf-8')
    lts_caption=language_data[language]['history_page']['lts_caption'].encode('utf-8')
    ply_caption=language_data[language]['history_page']['ply_caption'].encode('utf-8')
    ffa_caption=language_data[language]['history_page']['ffa_caption'].encode('utf-8')
    giv_caption=language_data[language]['history_page']['giv_caption'].encode('utf-8')
    balance_caption=language_data[language]['history_page']['balance_caption'].encode('utf-8')
    income_caption=language_data[language]['history_page']['income_caption'].encode('utf-8')
    expense_caption=language_data[language]['history_page']['expense_caption'].encode('utf-8')
    back_caption=language_data[language]['history_page']['back_caption'].encode('utf-8')

    for i in range(0,len(currency_data['currency'])):
        currency_code = currency_data['currency'][i]['currency_code']
        if (currency == currency_code):
            currency_sign = currency_data['currency'][i]['currency_sign']
            break

    nec_income = int(float(user_dict[0]))
    edu_income = int(float(user_dict[1]))
    lts_income = int(float(user_dict[2]))
    ply_income = int(float(user_dict[3]))
    ffa_income = int(float(user_dict[4]))
    giv_income = int(float(user_dict[5]))

    nec_expense = int(float(user_dict[6]))
    edu_expense = int(float(user_dict[7]))
    lts_expense = int(float(user_dict[8]))
    ply_expense = int(float(user_dict[9]))
    ffa_expense = int(float(user_dict[10]))
    giv_expense = int(float(user_dict[11]))

    nec_prebal = int(float(user_dict[12]))
    edu_prebal = int(float(user_dict[13]))
    lts_prebal = int(float(user_dict[14]))
    ply_prebal = int(float(user_dict[15]))
    ffa_prebal = int(float(user_dict[16]))
    giv_prebal = int(float(user_dict[17]))
        
    nec_balance = nec_income - nec_expense + nec_prebal
    edu_balance = edu_income - edu_expense + edu_prebal
    lts_balance = lts_income - lts_expense + lts_prebal
    ply_balance = ply_income - ply_expense + ply_prebal
    ffa_balance = ffa_income - ffa_expense + ffa_prebal
    giv_balance = giv_income - giv_expense + giv_prebal

    if (historyType != ALL):

        table_padding = "385px"

        if (historyType == NEC):

            title = nec_caption

            income_amt = "{:,}".format(nec_income)
            expense_amt = "{:,}".format(nec_expense)
            balance_amt = "{:,}".format(nec_balance)

            jar_url = "/static/nec.png"

            if (nec_balance > 0):
                progress = int(float(nec_balance)/(nec_balance+nec_expense)*100)

        if (historyType == EDU):

            title = edu_caption

            income_amt = "{:,}".format(edu_income)
            expense_amt = "{:,}".format(edu_expense)
            balance_amt = "{:,}".format(edu_balance)

            jar_url = "/static/edu.png"  

            if (edu_balance > 0):
                progress = int(float(edu_balance)/(edu_balance+edu_expense)*100)

        if (historyType == LTS):

            title = lts_caption

            income_amt = "{:,}".format(lts_income)
            expense_amt = "{:,}".format(lts_expense)
            balance_amt = "{:,}".format(lts_balance)

            jar_url = "/static/lts.png"

            if (lts_balance > 0):
                progress = int(float(lts_balance)/(lts_balance+lts_expense)*100)

        if (historyType == PLY):

            title = ply_caption

            income_amt = "{:,}".format(ply_income)
            expense_amt = "{:,}".format(ply_expense)
            balance_amt = "{:,}".format(ply_balance)

            jar_url = "/static/ply.png" 

            if (ply_balance > 0):
                progress = int(float(ply_balance)/(ply_balance+ply_expense)*100)

        if (historyType == FFA):

            title = ffa_caption

            income_amt = "{:,}".format(ffa_income)
            expense_amt = "{:,}".format(ffa_expense)
            balance_amt = "{:,}".format(ffa_balance)

            jar_url = "/static/ffa.png" 

            if (ffa_balance > 0):
                progress = int(float(ffa_balance)/(ffa_balance+ffa_expense)*100)

        if (historyType == GIV):

            title = giv_caption

            income_amt = "{:,}".format(giv_income)
            expense_amt = "{:,}".format(giv_expense)
            balance_amt = "{:,}".format(giv_balance)

            jar_url = "/static/giv.png" 

            if (giv_balance > 0):
                progress = int(float(giv_balance)/(giv_balance+giv_expense)*100)

        if (progress >= 50):
            progress_color = "TURQUOISE"
        elif (progress >= 20):
            progress_color = "GOLD"
        else:
            progress_color = "TOMATO"   

    else:
        table_padding = "210px"
        title = title_caption


    for key in sorted(r.hscan_iter(user_id, match=historyDate+'*'), reverse=True):

        transactionID = key[0]
        transactionValue = key[1].replace("&","#")

        key0 = key[0].split('-')
        key1 = key[1].split('-')
        

        year = key0[0]
        month = key0[1]
        day = key0[2]
      

        transactionType = key1[0]
        jar = key1[1]
        repeat = key1[2]
        description = key1[3]

        #skip repeat transaction
        if ('repeat' in transactionID):
            continue

        #skip break-out transaction
        if ((historyType == ALL) and (len(key0) == 7)):
            continue

        #filter transaction by jar
        if ((historyType != ALL) and (historyType != jar)):
            continue

        if (jar == ALL):
            user_dict1 = r.hmget(user_id,
                                transactionID+'-'+NEC,
                                transactionID+'-'+EDU,
                                transactionID+'-'+LTS,
                                transactionID+'-'+PLY,
                                transactionID+'-'+FFA,
                                transactionID+'-'+GIV)

            nec_amount = user_dict1[0].split('-')[4]
            edu_amount = user_dict1[1].split('-')[4]
            lts_amount = user_dict1[2].split('-')[4]
            ply_amount = user_dict1[3].split('-')[4]
            ffa_amount = user_dict1[4].split('-')[4]
            giv_amount = user_dict1[5].split('-')[4]


        trash_symbol = """
            <i class="fa fa-trash-o">
        """
        
        editTransaction_function = """
            editTransaction('{user_id}','update','{transactionID}','{transactionValue}','{historyType}','{historyDate}')
        """.format(user_id=user_id,
                    transactionID=transactionID,
                    transactionValue=transactionValue,
                    historyType=historyType,
                    historyDate=historyDate)

        deleteTransaction_function = """
            deleteTransaction('{user_id}','delete','{transactionID}','{transactionValue}','{historyType}','{historyDate}',
            '{nec_balance}','{edu_balance}','{lts_balance}','{ply_balance}','{ffa_balance}','{giv_balance}',
            '{nec_amount}','{edu_amount}','{lts_amount}','{ply_amount}','{ffa_amount}','{giv_amount}')
        """.format(user_id=user_id,
                    transactionID=transactionID,
                    transactionValue=transactionValue,
                    historyType=historyType,
                    historyDate=historyDate,
                    nec_balance=nec_balance,
                    edu_balance=edu_balance,
                    lts_balance=lts_balance,
                    ply_balance=ply_balance,
                    ffa_balance=ffa_balance,
                    giv_balance=giv_balance,
                    nec_amount=nec_amount,
                    edu_amount=edu_amount,
                    lts_amount=lts_amount,
                    ply_amount=ply_amount,
                    ffa_amount=ffa_amount,
                    giv_amount=giv_amount)

        if (len(key0) == 7):
            editTransaction_function=""
            deleteTransaction_function=""
            trash_symbol=""

        amount = "{:,}".format(int(float(key1[4])))

        if (jar == ALL):
            jar_caption = all_caption
        
        if (jar == NEC):
            jar_caption = nec_caption
        
        if (jar == EDU):
            jar_caption = edu_caption

        if (jar == LTS):
            jar_caption = lts_caption

        if (jar == PLY):
            jar_caption = ply_caption

        if (jar == FFA):
            jar_caption = ffa_caption

        if (jar == GIV):
            jar_caption = giv_caption

        if (transactionType == "Income"):
            sign_symbol = """<i class="fa fa-plus" style="color:LIME"></i>"""
            color = "color:LIME"
            sign = "+"
        else:
            sign_symbol = """<i class="fa fa-minus" style="color:TOMATO"></i>"""
            color = "color:white"
            sign = "-"

        if (repeat != ONCE):
            repeat_symbol = """<i class="fa fa-refresh" style="color:TURQUOISE"></i>"""
        else:
            repeat_symbol = "<br>"

        
        date = day+'/'+month+'/'+year


        table_body = table_body + """
            <tr style="cursor:pointer;">
                <td>{sign_symbol}<br>{repeat_symbol}</td>
                <td id="cel1" onclick="{editTransaction_function}"><span style="color:white">{jar_caption}</span><br><span style="font-size:small; font-weight:300; color:LIGHTGRAY">{description}</span></td>
                <td id="cel2" onclick="{editTransaction_function}" style="padding-right:5px; text-align:right; {color}">{sign}{amount} {currency_sign}<br><span style="font-size:small; font-weight:300; color:LIGHTGRAY">{date}</span></td>
                <td id="cel3" style="text-align:right; color:white" onclick="{deleteTransaction_function}">{trash_symbol}</td>
            </tr>
        """.format(sign_symbol=sign_symbol,
                    repeat_symbol=repeat_symbol,
                    jar_caption=jar_caption,
                    description=description, 
                    sign=sign,
                    amount=amount,
                    date=date,
                    color=color,
                    editTransaction_function=editTransaction_function,
                    deleteTransaction_function=deleteTransaction_function,
                    trash_symbol=trash_symbol,
                    currency_sign=currency_sign)

    table = table_begin + table_body + table_end        

    addZero = """
        function addZero(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }
    """

    deleteTransaction = """
    function deleteTransaction(user_id, transactionType, transactionID, transactionValue, jarOption, date,
                                nec_balance, edu_balance, lts_balance, ply_balance, ffa_balance, giv_balance,
                                nec_amount, edu_amount, lts_amount, ply_amount, ffa_amount, giv_amount) {

        if (confirm("Are you sure to delete this transaction ?")) {

            value = transactionValue.split('-');
            ttype = value[0];
            jar = value[1]
            amount = value[4];


            if (((jar == 'Necessities') && (parseFloat(amount) > parseFloat(nec_balance)) ||
                (jar == 'Education') && (parseFloat(amount) > parseFloat(edu_balance)) ||
                (jar == 'Saving') && (parseFloat(amount) > parseFloat(lts_balance)) ||
                (jar == 'Play') && (parseFloat(amount) > parseFloat(ply_balance)) ||
                (jar == 'Investment') && (parseFloat(amount) > parseFloat(ffa_balance)) ||
                (jar == 'Give') && (parseFloat(amount) > parseFloat(giv_balance)) ||
                (jar == 'All') && ((parseFloat(nec_amount) > parseFloat(nec_balance)) || 
                (parseFloat(edu_amount) > parseFloat(edu_balance)) || 
                (parseFloat(lts_amount) > parseFloat(lts_balance)) || 
                (parseFloat(ply_amount) > parseFloat(ply_balance)) || 
                (parseFloat(ffa_amount) > parseFloat(ffa_balance)) || 
                (parseFloat(giv_amount) > parseFloat(giv_balance)))) && (ttype == 'Income')) {
                    
                alert('Could not delete this transaction');
                return;

            }

            var waiting = document.getElementById('waiting');
            waiting.style.display="block";


            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/DeleteTransactionPage/'+ user_id +'/delete/transactionID/transactionValue/jarOption/date', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    
            xhr.onload = function() {
                document.open();
                document.write(xhr.responseText);
                document.close();
            };
    
            xhr.send("transactionType="+transactionType+"&transactionID="+transactionID+"&transactionValue="+transactionValue+
                    "&jarOption="+jarOption+"&date="+date);
        }
        
    }
    """

    editTransaction = """
    function editTransaction(user_id, transactionType, transactionID, transactionValue, jarOption, date) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/TransactionPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send("transactionType="+transactionType+"&transactionID="+transactionID+"&transactionValue="+transactionValue+
                "&jarOption="+jarOption+"&date="+date);

    };
    """

    back = """
    function back(user_id) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var d = new Date();
        var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/HomePage/'+ user_id + '/' + today, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send("sender_id=HistoryPage");
    };
    """

    monthChange = """
    function monthChange(user_id, historyType) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";
        
        var historyDate = document.getElementById('theDate').value;
    
        url = '/HistoryPage/' + user_id + '/' + historyType + '/' + historyDate;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {

            document.open();
            document.write(xhr.responseText);
            document.close();

        };
 
        xhr.send();
      
    };
    """

    mozilla_detect = """
    if(navigator.userAgent.toLowerCase().indexOf('firefox') > -1) {
        document.getElementById('theDate').readOnly="true";
    }
    """

    select_jar = """
    function selectJar(user_id, historyType, historyDate) {
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/SelectJarPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=HistoryPage'+'&jar='+historyType+'&date='+historyDate);
    }
    """

    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    history_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        table {
            width: 100%;
        }

        td {
            border-bottom: 1px solid DARKSLATEGRAY;
            padding-top:10px;
            padding-bottom:10px;

        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .balance-label-class {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 100px;
        }


        .income-expense-label {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 70px;

        }

        .minus-button-label {
            color: TURQUOISE;
            cursor: pointer;
            display: block;
            text-align: center;
        }


        .minus-button-label:active {
            color: LIGHTGRAY;
        }

        .progress-class {
            background-color:LIGHTGRAY;
            height:3px;
            width:100%;
        }

    """

    additional_html = """
    <div class="balance-class">
        <label class="balance-label-class">
            <div class="col-xs-3" style="display:block; text-align:center; padding-top:20px; padding-left:15px; padding-right:0">
                <p class="text-center"><img src="{jar_url}" style="cursor:pointer;width:40px;height:40px;" onclick="selectJar('{user_id}','{historyType}','{historyDate}')"></p>
                <p class="text-center" style="background-color:blue">
                    <div class="progress-class">
                        <div style="background-color:{progress_color}; height:100%; width:{progress}%"></div>
                    </div>
                </p>
            </div>
            <div class="col-xs-9" style="padding-top:10px;">
                <p class="text-left" style="font-weight:300;">{balance_caption} ({currency_sign})</p>
                <p class="text-left" style="font-weight:300; font-size:xx-large; color:white;">{balance_amt}</p>
            </div>
        </label>
    </div>

    <div class="income-expense">
        <label class="income-expense-label">
            <div class="col-xs-5" style="padding: 0;">
                <input id="income-submit" type="button" onclick=addTransaction('{user_id}','history-new-income','{historyType}','{historyDate}')>
                <label for="income-submit" class="income-button-label" style="cursor:pointer; width:100%; padding-left:18px;">
                    <p class="text-left" style="font-weight:300;">{income_caption} &nbsp <i class="fa fa-plus" style="color:LIME"></i></p>
                    <p class="text-left" style="color:white; font-weight:400;">{income_amt} {currency_sign}</p>
                </label>
            </div>
            <div class="col-xs-2" style="padding: 0">
                <input id="minus-submit" type="button" onclick="addTransaction('{user_id}','history-new-expense','{historyType}','{historyDate}')">
                <label for="minus-submit" class="minus-button-label">
                    <p ><i class="fa fa-minus-circle fa-4x"></i></p>
                </label>
            </div>
            <div class="col-xs-5" style="padding: 0">
                <input id="expense-submit" type="button" onclick="addTransaction('{user_id}','history-new-expense','{historyType}','{historyDate}')">
                <label for="expense-submit" class="expense-button-label" style="cursor:pointer; width:100%; padding-right:18px;">
                    <p class="text-right" style="font-weight:300;"> <i class="fa fa-minus" style="color:TOMATO"></i>&nbsp {expense_caption}</p>
                    <p class="text-right" style="color:white; font-weight:400;">{expense_amt} {currency_sign}</p>
                </label>
            </div>
        </label>
    </div>

    <script>
        {select_jar}
    </script>

    """.format(user_id=user_id,
                balance_amt=balance_amt,
                income_amt=income_amt,
                expense_amt=expense_amt,
                historyType=historyType,
                historyDate=historyDate,
                progress_color=progress_color,
                progress=progress,
                jar_url=jar_url,
                select_jar=select_jar,
                currency_sign=currency_sign,
                balance_caption=balance_caption,
                income_caption=income_caption,
                expense_caption=expense_caption)

    if (historyType == ALL):
        additional_html = ""

    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {history_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title}</p>
            </h4>
        </div>

        <div class="date-class" style="height:45px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:40px; width: 100%; padding-left: 15px; padding-top:7px">
                    <i class="fa fa-calendar"></i>&nbsp
                    <input type="month" id="theDate" onchange="monthChange('{user_id}','{historyType}')" style="cursor:pointer; width: calc(100% - 25px); background-color: DARKSLATEGRAY; border:none; outline:none; -webkit-appearance: none;">
                    <i id class="fa fa-angle-down" style="position:absolute; top:12px; right:15px"></i>
                </label>

            </div>
            
        </div>

        <div class="history-table-class" id="history-table" style="height:calc(100vh - {table_padding}); min-height:calc(630px - {table_padding}); overflow:auto; -webkit-overflow-scrolling: touch">
            {table}
        </div>

        {additional_html}

        <p></p>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     

    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {addZero}
        {back}
        {monthChange}
        {editTransaction}
        {deleteTransaction}
        {mozilla_detect}
        document.getElementById('theDate').value = '{historyDate}';
    </script>      


    """.format(user_id=user_id,
                history_style=history_style,
                table=table,
                addZero=addZero,
                back=back, 
                monthChange=monthChange,
                historyType=historyType,
                historyDate=historyDate, 
                editTransaction=editTransaction,
                deleteTransaction=deleteTransaction,
                additional_html=additional_html,
                table_padding=table_padding,
                title=title,
                mozilla_detect=mozilla_detect,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/ReportPage/<user_id>/<reportType>/<reportDate>', methods=['POST'])
def ReportPage(user_id, reportType, reportDate):
    
    print "ReportPage:user_id:"+user_id
    print "ReportPage:reportType:"+reportType
    print "ReportPage:reportDate:"+reportDate

    income_amt = 0
    expense_amt = 0
    balance_amt = 0

    progress_color= "LIGHTGRAY"
    progress = 0
    jar_url = ""

    user_dict = r.hmget(user_id,
                        'nec_income',
                        'edu_income',
                        'lts_income',
                        'ply_income',
                        'ffa_income',
                        'giv_income',
                        'nec_expense',
                        'edu_expense',
                        'lts_expense',
                        'ply_expense',
                        'ffa_expense',
                        'giv_expense',
                        'nec_prebal',
                        'edu_prebal',
                        'lts_prebal',
                        'ply_prebal',
                        'ffa_prebal',
                        'giv_prebal',
                        'currency',
                        'income_amt',
                        'expense_amt',
                        'pre_balance',
                        'language')

    currency = user_dict[18]
    language = user_dict[22]

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)

    #load currency json file
    with open('static/currency.json') as f:
        currency_data = json.load(f)

    title_caption=language_data[language]['report_page']['title_caption'].encode('utf-8')
    week_caption=language_data[language]['report_page']['week_caption'].encode('utf-8')
    balance_caption=language_data[language]['report_page']['balance_caption'].encode('utf-8')
    income_caption=language_data[language]['report_page']['income_caption'].encode('utf-8')
    expense_caption=language_data[language]['report_page']['expense_caption'].encode('utf-8')
    back_caption=language_data[language]['report_page']['back_caption'].encode('utf-8')

    for i in range(0,len(currency_data['currency'])):
        currency_code = currency_data['currency'][i]['currency_code']
        if (currency == currency_code):
            currency_sign = currency_data['currency'][i]['currency_sign']
            break

    income_amt = int(float(user_dict[19]))
    expense_amt = int(float(user_dict[20]))
    pre_balance = int(float(user_dict[21]))

    nec_income = int(float(user_dict[0]))
    edu_income = int(float(user_dict[1]))
    lts_income = int(float(user_dict[2]))
    ply_income = int(float(user_dict[3]))
    ffa_income = int(float(user_dict[4]))
    giv_income = int(float(user_dict[5]))

    nec_expense = int(float(user_dict[6]))
    edu_expense = int(float(user_dict[7]))
    lts_expense = int(float(user_dict[8]))
    ply_expense = int(float(user_dict[9]))
    ffa_expense = int(float(user_dict[10]))
    giv_expense = int(float(user_dict[11]))

    nec_prebal = int(float(user_dict[12]))
    edu_prebal = int(float(user_dict[13]))
    lts_prebal = int(float(user_dict[14]))
    ply_prebal = int(float(user_dict[15]))
    ffa_prebal = int(float(user_dict[16]))
    giv_prebal = int(float(user_dict[17]))
        

    balance_amt = income_amt - expense_amt + pre_balance

    nec_balance = nec_income - nec_expense + nec_prebal
    edu_balance = edu_income - edu_expense + edu_prebal
    lts_balance = lts_income - lts_expense + lts_prebal
    ply_balance = ply_income - ply_expense + ply_prebal
    ffa_balance = ffa_income - ffa_expense + ffa_prebal
    giv_balance = giv_income - giv_expense + giv_prebal

    
    if (reportType == ALL):

        if (balance_amt > 0):
             progress = int(float(balance_amt)/(balance_amt+expense_amt)*100)

        income_amt = "{:,}".format(income_amt)
        expense_amt = "{:,}".format(expense_amt)
        balance_amt = "{:,}".format(balance_amt)

        jar_url = "/static/all.png"

        
    if (reportType == NEC):

        income_amt = "{:,}".format(nec_income)
        expense_amt = "{:,}".format(nec_expense)
        balance_amt = "{:,}".format(nec_balance)

        jar_url = "/static/nec.png"

        if (nec_balance > 0):
             progress = int(float(nec_balance)/(nec_balance+nec_expense)*100)

    if (reportType == EDU):

        income_amt = "{:,}".format(edu_income)
        expense_amt = "{:,}".format(edu_expense)
        balance_amt = "{:,}".format(edu_balance)

        jar_url = "/static/edu.png"  

        if (edu_balance > 0):
            progress = int(float(edu_balance)/(edu_balance+edu_expense)*100)

    if (reportType == LTS):

        income_amt = "{:,}".format(lts_income)
        expense_amt = "{:,}".format(lts_expense)
        balance_amt = "{:,}".format(lts_balance)

        jar_url = "/static/lts.png"

        if (lts_balance > 0):
            progress = int(float(lts_balance)/(lts_balance+lts_expense)*100)

    if (reportType == PLY):

        income_amt = "{:,}".format(ply_income)
        expense_amt = "{:,}".format(ply_expense)
        balance_amt = "{:,}".format(ply_balance)

        jar_url = "/static/ply.png" 

        if (ply_balance > 0):
            progress = int(float(ply_balance)/(ply_balance+ply_expense)*100)

    if (reportType == FFA):

        income_amt = "{:,}".format(ffa_income)
        expense_amt = "{:,}".format(ffa_expense)
        balance_amt = "{:,}".format(ffa_balance)

        jar_url = "/static/ffa.png" 

        if (ffa_balance > 0):
            progress = int(float(ffa_balance)/(ffa_balance+ffa_expense)*100)

    if (reportType == GIV):

        income_amt = "{:,}".format(giv_income)
        expense_amt = "{:,}".format(giv_expense)
        balance_amt = "{:,}".format(giv_balance)

        jar_url = "/static/giv.png" 

        if (giv_balance > 0):
            progress = int(float(giv_balance)/(giv_balance+giv_expense)*100)



    if (progress >= 50):
        progress_color = "TURQUOISE"
    elif (progress >= 20):
        progress_color = "GOLD"
    else:
        progress_color = "TOMATO" 


    week_income_amt = [0,0,0,0]
    week_expense_amt = [0,0,0,0]

    for key in r.hscan_iter(user_id, match=reportDate+'*'):
        key0 = key[0].split('-')
        key1 = key[1].split('-')

        ttype = key1[0]
        jar = key1[1]
        day = int(key0[2])

        #skip repeat & break-out transactions
        if ((reportType == ALL) and (len(key0) == 7)):
            continue

        #filer transactions by jar
        if ((reportType != ALL) and (reportType != jar)):
            continue


        amount = int(float(key1[4]))

        if (day <= 7 ):
            x = 0
        elif (day <= 14):
            x = 1
        elif (day <= 21):
            x = 2
        else:
            x = 3

        if (ttype == TRANSACTION_TYPE_INCOME):
            week_income_amt[x] = week_income_amt[x] + amount
        else:
            week_expense_amt[x] = week_expense_amt[x] + amount
        

    bar_chart = """

        var week1_income_amt = document.getElementById("week1_income_amt").value;
        var week1_expense_amt = document.getElementById("week1_expense_amt").value;

        var week2_income_amt = document.getElementById("week2_income_amt").value;
        var week2_expense_amt = document.getElementById("week2_expense_amt").value;

        var week3_income_amt = document.getElementById("week3_income_amt").value;
        var week3_expense_amt = document.getElementById("week3_expense_amt").value;

        var week4_income_amt = document.getElementById("week4_income_amt").value;
        var week4_expense_amt = document.getElementById("week4_expense_amt").value;

        var week_label=document.getElementById('week-label');

        var income_label=document.getElementById('income-label');
        var expense_label=document.getElementById('expense-label');

        week1 = week_label.textContent + ' 1'
        week2 = week_label.textContent + ' 2'
        week3 = week_label.textContent + ' 3'
        week4 = week_label.textContent + ' 4'

        window.chartColors = {
	        lime: 'rgb(0, 255, 0)',
	        tomato: 'rgb(255, 99, 71)'
        };

        Chart.defaults.global.defaultFontColor = "white";
        var color = Chart.helpers.color;

        var barChartData = {
			labels: [week1, week2, week3, week4],
			datasets: [{
				label: income_label.textContent,
				backgroundColor: color(window.chartColors.lime).alpha(0.5).rgbString(),
				borderColor: window.chartColors.lime,
				borderWidth: 1,
				data: [week1_income_amt,week2_income_amt,week3_income_amt,week4_income_amt]
			}, {
				label: expense_label.textContent,
				backgroundColor: color(window.chartColors.tomato).alpha(0.5).rgbString(),
				borderColor: window.chartColors.tomato,
				borderWidth: 1,
				data: [week1_expense_amt,week2_expense_amt,week3_expense_amt,week4_expense_amt]
			}]

		};

		var ctx = document.getElementById('myChart');
		new Chart(ctx, {
			type: 'bar',
			data: barChartData,
			options: {
                maintainAspectRatio: false,
                tooltips: {
                    callbacks: {
                        label: function (tooltipItem, data) {
                            var tooltipLabel = data.datasets[tooltipItem.datasetIndex].label;
                            var tooltipValue = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                            return tooltipLabel+': '+tooltipValue.toLocaleString();
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            callback: function(value, index, values) {
                                return value.toLocaleString();
                            }
                        }
                    }]
                }
			}
		});

    """

    addZero = """
        function addZero(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }
    """


    back = """
    function back(user_id) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var d = new Date();
        var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/HomePage/'+user_id+'/'+today, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send("sender_id=ReportPage");
    };
    """

    monthChange = """
    function monthChange(user_id, reportType) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";
        
        var reportDate = document.getElementById('theDate').value;
    
        url = '/ReportPage/' + user_id + '/' + reportType + '/' + reportDate;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {

            document.open();
            document.write(xhr.responseText);
            document.close();

        };
 
        xhr.send();
      
    };
    """

    mozilla_detect = """
    if(navigator.userAgent.toLowerCase().indexOf('firefox') > -1) {
        document.getElementById('theDate').readOnly="true";
    }
    """

    select_jar = """
    function selectJar(user_id, reportType, reportDate) {
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/SelectJarPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=ReportPage'+'&jar='+reportType+'&date='+reportDate);
    }
    """


    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">
        
        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->

        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    report_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        table {
            width: 100%;
        }

        td {
            border-bottom: 1px solid DARKSLATEGRAY;
            padding-top:10px;
            padding-bottom:10px;

        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .balance-label-class {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 100px;
        }


        .income-expense-label {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 70px;

        }

        .minus-button-label {
            color: TURQUOISE;
            cursor: pointer;
            display: block;
            text-align: center;
        }


        .minus-button-label:active {
            color: LIGHTGRAY;
        }

        .progress-class {
            background-color:LIGHTGRAY;
            height:3px;
            width:100%;
        }

        .report-class {
            position: relative;
            height:calc(100vh - 385px);
            width:100%; 
            min-height:245px;
        }

    """

    
    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {report_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        <div class="date-class" style="height:45px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <label style="font-weight: 300; background-color:DARKSLATEGRAY; height:40px; width: 100%; padding-left: 15px; padding-top:7px">
                    <i class="fa fa-calendar"></i>&nbsp
                    <input type="month" id="theDate" onchange="monthChange('{user_id}','{reportType}')" style="cursor:pointer; width: calc(100% - 25px); background-color: DARKSLATEGRAY; border:none; outline:none; -webkit-appearance: none;">
                    <i id class="fa fa-angle-down" style="position:absolute; top:12px; right:15px"></i>
                </label>

            </div>
            
        </div>

        <div class="report-class">
            <canvas id="myChart"></canvas>
            <label id="week-label" style="display:none">{week_caption}</label>
            <label id="income-label" style="display:none">{income_caption}</label>
            <label id="expense-label" style="display:none">{expense_caption}</label>
            <li id="week1_income_amt" value="{week1_income_amt}" style="display:none"></li>
            <li id="week1_expense_amt" value="{week1_expense_amt}" style="display:none"></li>
            <li id="week2_income_amt" value="{week2_income_amt}" style="display:none"></li>
            <li id="week2_expense_amt" value="{week2_expense_amt}" style="display:none"></li>
            <li id="week3_income_amt" value="{week3_income_amt}" style="display:none"></li>
            <li id="week3_expense_amt" value="{week3_expense_amt}" style="display:none"></li>
            <li id="week4_income_amt" value="{week4_income_amt}" style="display:none"></li>
            <li id="week4_expense_amt" value="{week4_expense_amt}" style="display:none"></li>
         </div>

        <div class="balance-class">
            <label class="balance-label-class">
                <div class="col-xs-3" style="display:block; text-align:center; padding-top:20px; padding-left:15px; padding-right:0">
                    <p class="text-center"><img src="{jar_url}" style="cursor:pointer; width:40px;height:40px;" onclick="selectJar('{user_id}','{reportType}','{reportDate}')"></p>
                    <p class="text-center" style="background-color:blue">
                        <div class="progress-class">
                            <div style="background-color:{progress_color}; height:100%; width:{progress}%"></div>
                        </div>
                    </p>
                </div>
                <div class="col-xs-9" style="padding-top:10px;">
                    <p class="text-left" style="font-weight:300;">{balance_caption} ({currency_sign})</p>
                    <p class="text-left" style="font-weight:300; font-size:xx-large; color:white;">{balance_amt}</p>
                </div>
            </label>
        </div>

        <div class="income-expense">
            <label class="income-expense-label">
                <div class="col-xs-5" style="padding: 0;">
                    <input id="income-submit" type="button" onclick=addTransaction('{user_id}','report-new-income','{reportType}','{reportDate}')>
                    <label for="income-submit" class="income-button-label" style="cursor:pointer; width:100%; padding-left:18px;">
                        <p class="text-left" style="font-weight:300;">{income_caption} &nbsp <i class="fa fa-plus" style="color:LIME"></i></p>
                        <p class="text-left" style="color:white; font-weight:400;">{income_amt} {currency_sign}</p>
                    </label>
                </div>
                <div class="col-xs-2" style="padding: 0">
                    <input id="minus-submit" type="button" onclick="addTransaction('{user_id}','report-new-expense','{reportType}','{reportDate}')">
                    <label for="minus-submit" class="minus-button-label">
                        <p ><i class="fa fa-minus-circle fa-4x"></i></p>
                    </label>
                </div>
                <div class="col-xs-5" style="padding: 0">
                    <input id="expense-submit" type="button" onclick="addTransaction('{user_id}','report-new-expense','{reportType}','{reportDate}')">
                    <label for="expense-submit" class="expense-button-label" style="cursor:pointer; width:100%; padding-right:18px;">
                        <p class="text-right" style="font-weight:300;"> <i class="fa fa-minus" style="color:TOMATO"></i>&nbsp {expense_caption}</p>
                        <p class="text-right" style="color:white; font-weight:400;">{expense_amt} {currency_sign}</p>
                    </label>
                </div>
            </label>
        </div>

        <p></p>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     

    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {addZero}
        {back}
        {monthChange}
        {bar_chart}
        {mozilla_detect}
        {select_jar}
        document.getElementById('theDate').value = '{reportDate}';
    </script>      


    """.format(user_id=user_id,
                report_style=report_style,
                addZero=addZero,
                back=back, 
                monthChange=monthChange,
                reportType=reportType,
                reportDate=reportDate,
                balance_amt=balance_amt,
                income_amt=income_amt,
                expense_amt=expense_amt,
                progress_color=progress_color,
                progress=progress,
                jar_url=jar_url,
                bar_chart=bar_chart,
                week1_income_amt=week_income_amt[0],
                week1_expense_amt=week_expense_amt[0],
                week2_income_amt=week_income_amt[1],
                week2_expense_amt=week_expense_amt[1],
                week3_income_amt=week_income_amt[2],
                week3_expense_amt=week_expense_amt[2],
                week4_income_amt=week_income_amt[3],
                week4_expense_amt=week_expense_amt[3],
                mozilla_detect=mozilla_detect,
                select_jar=select_jar,
                currency_sign=currency_sign,
                title_caption=title_caption,
                week_caption=week_caption,
                income_caption=income_caption,
                expense_caption=expense_caption,
                balance_caption=balance_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/SettingPage/<user_id>', methods=['POST'])
def SettingPage(user_id):
    

    print "SettingPage:user_id:"+user_id

    language = r.hget(user_id,'language')

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)


    title_caption=language_data[language]['settings_page']['title_caption'].encode('utf-8')
    general_setting_caption=language_data[language]['settings_page']['general_setting_caption'].encode('utf-8')
    jar_setting_caption=language_data[language]['settings_page']['jar_setting_caption'].encode('utf-8')
    recurring_transaction_caption=language_data[language]['settings_page']['recurring_transaction_caption'].encode('utf-8')
    guide_caption=language_data[language]['settings_page']['guide_caption'].encode('utf-8')
    fanpage_caption=language_data[language]['settings_page']['fanpage_caption'].encode('utf-8')
    feedback_caption=language_data[language]['settings_page']['feedback_caption'].encode('utf-8')
    back_caption=language_data[language]['settings_page']['back_caption'].encode('utf-8')
    version_caption=language_data[language]['general_setting_page']['version_caption'].encode('utf-8')


    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">
        
        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"


    general_setting = """
    function general_setting(user_id) {
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/GeneralSettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send();
    }
    """

    jars_setting = """
    function jars_setting(user_id) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/JarSettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send();
    }
    """

    recurring_transaction = """
    function recurring_transaction(user_id) {


        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/RecurringTransactionPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send();
    }
    """

    guide = """
    function guide() {
        
        document.location.href = "https://moneyoi.io";

    }
    """

    addZero = """
        function addZero(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }
    """

    back = """

    function back(user_id) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var d = new Date();
        var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/HomePage/'+user_id+'/'+today, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };

        xhr.send("sender_id=SettingPage");
 
    };
    """

    feedback = """
    function feedback(version) {
        
        document.location.href = "mailto:support@moneyoi.io?subject=[MoneyOi CNA - "+version+"]";
    }
    """

    fanpage = """
    function fanpage() {

        document.location.href = "https://www.facebook.com/MoneyOiApp";

    }
    """
 
    setting_style = """


        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

    
        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        .general-class {
            text-align: left; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:40px; width: 100%; 
            padding-left:15px;
            padding-top:10px;
            cursor: pointer;
        }

        .general-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .back-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }

        .back-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

    """

    mid_html = """
    
    <style>
        /*------ addtransaction style ---------*/
        {setting_style}
    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="general-setting" type="button" onclick="general_setting('{user_id}')"> 
                <label class="general-class" for="general-setting">
                    <i class="fa fa-th" style="color:LIGHTGRAY;"></i>&nbsp {general_setting_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
            
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="jars-setting" type="button" onclick="jars_setting('{user_id}')"> 
                <label class="general-class" for="jars-setting">
                    <i class="fa fa-flask" style="color:LIGHTGRAY;"></i>&nbsp {jar_setting_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="recurring-transaction" type="button" onclick="recurring_transaction('{user_id}')"> 
                <label class="general-class" for="recurring-transaction">
                    <i class="fa fa-refresh" style="color:LIGHTGRAY;"></i>&nbsp {recurring_transaction_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="guide" type="button" onclick="guide()"> 
                <label class="general-class" for="guide">
                    <i class="fa fa-question-circle-o" style="color:LIGHTGRAY;"></i>&nbsp {guide_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
        </div>

        <p></p>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="fanpage" type="button" onclick="fanpage()"> 
                <label class="general-class" for="fanpage">
                    <i class="fa fa-facebook-official" style="color:LIGHTGRAY;"></i>&nbsp {fanpage_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="feedback" type="button" onclick="feedback('{version_caption}')"> 
                <label class="general-class" for="feedback">
                    <i class="fa fa-envelope-o" style="color:LIGHTGRAY;"></i>&nbsp {feedback_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
        </div>

        <p></p>

      
        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="back-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>


    </div>           

  
    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>


    <script>
        {addZero}
        {general_setting}
        {jars_setting}
        {recurring_transaction}
        {guide}
        {back}
        {feedback}
        {fanpage}
    </script>
    
    """.format(user_id=user_id,
                setting_style=setting_style,
                addZero=addZero,
                general_setting=general_setting,
                jars_setting=jars_setting,
                recurring_transaction=recurring_transaction,
                guide=guide,
                back=back,
                feedback=feedback,
                fanpage=fanpage,
                title_caption=title_caption,
                general_setting_caption=general_setting_caption,
                jar_setting_caption=jar_setting_caption,
                recurring_transaction_caption=recurring_transaction_caption,
                guide_caption=guide_caption,
                fanpage_caption=fanpage_caption,
                feedback_caption=feedback_caption,
                back_caption=back_caption,
                version_caption=version_caption)

    
    return begin_html + mid_html + end_html


@app.route('/SaveTransactionPage/<user_id>/<transactionType>/<transactionID>/<transactionValue>', methods=['POST'])
def SaveTransactionPage(user_id, transactionType, transactionID, transactionValue):
    

    if (transactionType == "add"):
        transactionID = request.form['transactionID']
        transactionValue = request.form['transactionValue'].replace("#","&")

    print "SaveTransactionPage:user_id:"+user_id
    print "SaveTransactionPage:transactionType:"+transactionType
    print "SaveTransactionPage:transactionID:"+transactionID

    if (transactionType == "repeat"):
        #string already encoded oto utf-8, no need to encode
        print "SaveTransactionPage:transactionValue:"+transactionValue
    else:
        print "SaveTransactionPage:transactionValue:"+transactionValue.encode('utf-8')



    value = transactionValue.split('-')

    transaction_type = value[0]
    transaction_jar = value[1]
    transaction_repeat = value[2]
    transaction_desc = value[3]

    transaction_id_nec = transactionID + '-' + NEC
    transaction_id_edu = transactionID + '-' + EDU
    transaction_id_lts = transactionID + '-' + LTS
    transaction_id_ply = transactionID + '-' + PLY
    transaction_id_ffa = transactionID + '-' + FFA
    transaction_id_giv = transactionID + '-' + GIV
    
    break_out = False

    user_dict = r.hmget(user_id,
                        'nec_pct',
                        'edu_pct',
                        'lts_pct',
                        'ply_pct',
                        'ffa_pct',
                        'giv_pct',
                        'income_amt',
                        'expense_amt',
                        'currency',
                        'nec_income',
                        'edu_income',
                        'lts_income',
                        'ply_income',
                        'ffa_income',
                        'giv_income',
                        'nec_expense',
                        'edu_expense',
                        'lts_expense',
                        'ply_expense',
                        'ffa_expense',
                        'giv_expense')


    nec_pct = int(float(user_dict[0]))
    edu_pct = int(float(user_dict[1]))
    lts_pct = int(float(user_dict[2]))
    ply_pct = int(float(user_dict[3]))
    ffa_pct = int(float(user_dict[4]))
    giv_pct = int(float(user_dict[5]))


    if (transactionType == "delete"):
        transaction_amount = int(float(value[4])) * (-1)
    else:
        transaction_amount = int(float(value[4]))

    nec_income = int(float(user_dict[9]))
    edu_income = int(float(user_dict[10]))
    lts_income = int(float(user_dict[11]))
    ply_income = int(float(user_dict[12]))
    ffa_income = int(float(user_dict[13]))
    giv_income = int(float(user_dict[14]))

    nec_expense = int(float(user_dict[15]))
    edu_expense = int(float(user_dict[16]))
    lts_expense = int(float(user_dict[17]))
    ply_expense = int(float(user_dict[18]))
    ffa_expense = int(float(user_dict[19]))
    giv_expense = int(float(user_dict[20]))

    income_amt = int(float(user_dict[6]))
    expense_amt = int(float(user_dict[7]))

    nec_value = int(transaction_amount*nec_pct/100)
    edu_value = int(transaction_amount*edu_pct/100)
    lts_value = int(transaction_amount*lts_pct/100)
    ply_value = int(transaction_amount*ply_pct/100)
    ffa_value = int(transaction_amount*ffa_pct/100)
    giv_value = int(transaction_amount*giv_pct/100)


    if (transaction_type == TRANSACTION_TYPE_EXPENSE):

        expense_amt = expense_amt + transaction_amount

        if (transaction_jar == NEC):
            nec_expense = nec_expense + transaction_amount

        if (transaction_jar == EDU):
            edu_expense = edu_expense + transaction_amount

        if (transaction_jar == LTS):
            lts_expense = lts_expense + transaction_amount

        if (transaction_jar == PLY):
            ply_expense = ply_expense + transaction_amount

        if (transaction_jar == FFA):
            ffa_expense = ffa_expense + transaction_amount

        if (transaction_jar == GIV):
            giv_expense = giv_expense + transaction_amount
    else:
        income_amt = income_amt + transaction_amount

        if (transaction_jar == ALL):

            transaction_value_nec = transaction_type + '-' + NEC + '-' + transaction_repeat + '-' + transaction_desc + '-' + str(nec_value)
            transaction_value_edu = transaction_type + '-' + EDU + '-' + transaction_repeat + '-' + transaction_desc + '-' + str(edu_value)
            transaction_value_lts = transaction_type + '-' + LTS + '-' + transaction_repeat + '-' + transaction_desc + '-' + str(lts_value)
            transaction_value_ply = transaction_type + '-' + PLY + '-' + transaction_repeat + '-' + transaction_desc + '-' + str(ply_value)
            transaction_value_ffa = transaction_type + '-' + FFA + '-' + transaction_repeat + '-' + transaction_desc + '-' + str(ffa_value)
            transaction_value_giv = transaction_type + '-' + GIV + '-' + transaction_repeat + '-' + transaction_desc + '-' + str(giv_value)

            nec_income = nec_income + nec_value
            edu_income = edu_income + edu_value
            lts_income = lts_income + lts_value
            ply_income = ply_income + ply_value
            ffa_income = ffa_income + ffa_value
            giv_income = giv_income + giv_value

            break_out = True


        if (transaction_jar == NEC):
            nec_income = nec_income + transaction_amount

        if (transaction_jar == EDU):
            edu_income = edu_income + transaction_amount


        if (transaction_jar == LTS):
            lts_income = lts_income + transaction_amount


        if (transaction_jar == PLY):
            ply_income = ply_income + transaction_amount


        if (transaction_jar == FFA):
            ffa_income = ffa_income + transaction_amount


        if (transaction_jar == GIV):
            giv_income = giv_income + transaction_amount


    if (transactionType == "recurring-delete"):
        r.hdel(user_id, transactionID)
    elif (transactionType == "delete"):
        
        # delete single transaction
        r.hdel(user_id, transactionID)

        # delete break-out transaction
        if (transaction_jar == ALL):
            r.hdel(user_id, transaction_id_nec)
            r.hdel(user_id, transaction_id_edu)
            r.hdel(user_id, transaction_id_lts)
            r.hdel(user_id, transaction_id_ply)
            r.hdel(user_id, transaction_id_ffa)
            r.hdel(user_id, transaction_id_giv)

        # delete recurring transaction
        if (transaction_repeat != ONCE):

            key = transactionID.split('-')

            transaction_date = transactionDate = datetime.date(int(key[0]), int(key[1]), int(key[2]))

            if (transaction_repeat == DAILY):
                transactionDate = transactionDate + datedelta.datedelta(days=1)

            if (transaction_repeat == WEEKLY):
                transactionDate = transactionDate + datedelta.datedelta(days=7)

            if (transaction_repeat == MONTHLY):
                transactionDate = transactionDate + datedelta.datedelta(months=1)

            if (transaction_repeat == ANNUALLY):
                transactionDate = transactionDate + datedelta.datedelta(years=1)

            transaction_id = transactionID.replace(str(transaction_date),str(transactionDate))

            r.hdel(user_id, transaction_id+'-repeat')

        # re-calculate amount after deleting transaction
        r.hmset(user_id,{
                'income_amt':income_amt,
                'expense_amt':expense_amt,
                'nec_income':nec_income,
                'edu_income':edu_income,
                'lts_income':lts_income,
                'ply_income':ply_income,
                'ffa_income':ffa_income,
                'giv_income':giv_income,
                'nec_expense':nec_expense,
                'edu_expense':edu_expense,
                'lts_expense':lts_expense,
                'ply_expense':ply_expense,
                'ffa_expense':ffa_expense,
                'giv_expense':giv_expense
            })
    # add and update
    else:
        if (transactionType == 'recurring-update'):
            r.hset(user_id, transactionID, transactionValue)
        # add, update, repeat
        else:
            r.hmset(user_id,{
                    'income_amt':income_amt,
                    'expense_amt':expense_amt,
                    'nec_income':nec_income,
                    'edu_income':edu_income,
                    'lts_income':lts_income,
                    'ply_income':ply_income,
                    'ffa_income':ffa_income,
                    'giv_income':giv_income,
                    'nec_expense':nec_expense,
                    'edu_expense':edu_expense,
                    'lts_expense':lts_expense,
                    'ply_expense':ply_expense,
                    'ffa_expense':ffa_expense,
                    'giv_expense':giv_expense,
                    transactionID:transactionValue
                })

            if ((transaction_repeat != ONCE) and (transactionType != 'repeat')):

                key = transactionID.split('-')

                transaction_date = transactionDate = datetime.date(int(key[0]), int(key[1]), int(key[2]))

                if (transaction_repeat == DAILY):
                    transactionDate = transactionDate + datedelta.datedelta(days=1)

                if (transaction_repeat == WEEKLY):
                    transactionDate = transactionDate + datedelta.datedelta(days=7)

                if (transaction_repeat == MONTHLY):
                    transactionDate = transactionDate + datedelta.datedelta(months=1)

                if (transaction_repeat == ANNUALLY):
                    transactionDate = transactionDate + datedelta.datedelta(years=1)

                transaction_id = transactionID.replace(str(transaction_date),str(transactionDate))

                r.hset(user_id, transaction_id+'-repeat',transactionValue)

            if (break_out):
                r.hmset(user_id,{
                    transaction_id_nec:transaction_value_nec,
                    transaction_id_edu:transaction_value_edu,
                    transaction_id_lts:transaction_value_lts,
                    transaction_id_ply:transaction_value_ply,
                    transaction_id_ffa:transaction_value_ffa,
                    transaction_id_giv:transaction_value_giv
                })
        

    return ""


@app.route('/DeleteTransactionPage/<user_id>/<transactionType>/<transactionID>/<transactionValue>/<jarOption>/<date>', methods=['POST'])
def DeleteTransactionPage(user_id, transactionType, transactionID, transactionValue, jarOption, date):

    
    if (transactionType == 'delete'):
        transactionID = request.form['transactionID']
        transactionValue = request.form['transactionValue'].replace("#","&")
        jarOption = request.form['jarOption']
        date = request.form['date']
    elif (transactionType == 'recurring-delete'):
        transactionID = request.form['transactionID']
        transactionValue = request.form['transactionValue'].replace("#","&")

    
    print "DeleteTransactionPage:user_id:"+user_id
    print "DeleteTransactionPage:transactionType:"+transactionType
    print "DeleteTransactionPage:transactionID:"+transactionID
    print "DeleteTransactionPage:transactionValue:"+transactionValue.encode('utf-8')
    print "DeleteTransactionPage:jarOption:"+jarOption
    print "DeleteTransactionPage:date:"+date

    if ((transactionType == 'recurring-delete') or (transactionType == 'recurring-update')):
        SaveTransactionPage(user_id, 'recurring-delete', transactionID, transactionValue)
    else:
        SaveTransactionPage(user_id, 'delete', transactionID, transactionValue)

    if (transactionType == "delete"):
        return HistoryPage(user_id, jarOption, date)
    elif (transactionType == "recurring-delete"):
        return RecurringTransactionPage(user_id)
    else:
        return ""


@app.route('/UpdateTransactionPage/<user_id>', methods=['POST'])
def UpdateTransactionPage(user_id):


    transactionType = request.form['transactionType']
    oldTransactionID = request.form['oldTransactionID']
    oldTransactionValue = request.form['oldTransactionValue'].replace("#","&")
    newTransactionID = request.form['newTransactionID']
    newTransactionValue = request.form['newTransactionValue'].replace("#","&")
    jarOption = request.form['jarOption']
    date = request.form['date']
    
    print "UpdateTransactionPage:user_id:"+user_id
    print "UpdateTransactionPage:transactionType:"+transactionType
    print "UpdateTransactionPage:oldTransactionID:"+oldTransactionID
    print "UpdateTransactionPage:oldTransactionValue:"+oldTransactionValue.encode('utf-8')
    print "UpdateTransactionPage:newTransactionID:"+newTransactionID
    print "UpdateTransactionPage:newTransactionValue:"+newTransactionValue.encode('utf-8')

    DeleteTransactionPage(user_id, transactionType, oldTransactionID, oldTransactionValue, jarOption, date)

    SaveTransactionPage(user_id, transactionType, newTransactionID, newTransactionValue)

    if (transactionType == "update"):
        return HistoryPage(user_id, jarOption, date)
    else:
        return RecurringTransactionPage(user_id)


@app.route('/RecurringTransactionPage/<user_id>', methods=['POST'])
def RecurringTransactionPage(user_id):
    
    print "RecurringTransactionPage:user_id:"+user_id

    table_begin = """
        <table>
    """
    table_end = """
        </table>
    """

    table_body = ""



    user_dict = r.hmget(user_id,
                        'currency',
                        'language')
    
    currency = user_dict[0]
    language = user_dict[1]


    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)

    #load currency json file
    with open('static/currency.json') as f:
        currency_data = json.load(f)

    title_caption=language_data[language]['recurring_transaction_page']['title_caption'].encode('utf-8')
    all_caption=language_data[language]['history_page']['all_caption'].encode('utf-8')
    nec_caption=language_data[language]['history_page']['nec_caption'].encode('utf-8')
    edu_caption=language_data[language]['history_page']['edu_caption'].encode('utf-8')
    lts_caption=language_data[language]['history_page']['lts_caption'].encode('utf-8')
    ply_caption=language_data[language]['history_page']['ply_caption'].encode('utf-8')
    ffa_caption=language_data[language]['history_page']['ffa_caption'].encode('utf-8')
    giv_caption=language_data[language]['history_page']['giv_caption'].encode('utf-8')
    back_caption=language_data[language]['recurring_transaction_page']['back_caption'].encode('utf-8')


    for i in range(0,len(currency_data['currency'])):
        currency_code = currency_data['currency'][i]['currency_code']
        if (currency == currency_code):
            currency_sign = currency_data['currency'][i]['currency_sign']
            break

    for key in sorted(r.hscan_iter(user_id, match='*repeat'), reverse=False):

        transactionID = key[0]
        transactionValue = key[1].replace("&","#")


        key0 = key[0].split('-')
        key1 = key[1].split('-')
        

        year = key0[0]
        month = key0[1]
        day = key0[2]
      

        transactionType = key1[0]
        jar = key1[1]
        repeat = key1[2]
        description = key1[3]


        editTransaction_function = """
            editTransaction('{user_id}','recurring-update','{transactionID}','{transactionValue}')
        """.format(user_id=user_id,
                    transactionID=transactionID,
                    transactionValue=transactionValue)

        deleteTransaction_function = """
            deleteTransaction('{user_id}','recurring-delete','{transactionID}','{transactionValue}')
        """.format(user_id=user_id,
                    transactionID=transactionID,
                    transactionValue=transactionValue)

    
        amount = "{:,}".format(int(float(key1[4])))

        if (jar == ALL):
            jar_caption = all_caption
        
        if (jar == NEC):
            jar_caption = nec_caption
        
        if (jar == EDU):
            jar_caption = edu_caption

        if (jar == LTS):
            jar_caption = lts_caption

        if (jar == PLY):
            jar_caption = ply_caption

        if (jar == FFA):
            jar_caption = ffa_caption

        if (jar == GIV):
            jar_caption = giv_caption


        if (transactionType == "Income"):
            sign_symbol = """<i class="fa fa-plus" style="color:LIME"></i>"""
            color = "color:LIME"
            sign = "+"
        else:
            sign_symbol = """<i class="fa fa-minus" style="color:TOMATO"></i>"""
            color = "color:white"
            sign = "-"

        if (repeat != ONCE):
            repeat_symbol = """<i class="fa fa-refresh" style="color:TURQUOISE"></i>"""
        else:
            repeat_symbol = "<br>"

        
        date = day+'/'+month+'/'+year


        table_body = table_body + """
            <tr style="cursor:pointer;">
                <td>{sign_symbol}<br>{repeat_symbol}</td>
                <td id="cel1" onclick="{editTransaction_function}"><span style="color:white">{jar_caption}</span><br><span style="font-size:small; font-weight:300; color:LIGHTGRAY">{description}</span></td>
                <td id="cel2" onclick="{editTransaction_function}" style="padding-right:5px; text-align:right; {color}">{sign}{amount} {currency_sign}<br><span style="font-size:small; font-weight:300; color:LIGHTGRAY">{date}</span></td>
                <td id="cel3" style="text-align:right; color:white" onclick="{deleteTransaction_function}"><i class="fa fa-trash-o"></i></td>
            </tr>
        """.format(sign_symbol=sign_symbol,
                    repeat_symbol=repeat_symbol,
                    jar_caption=jar_caption,
                    description=description, 
                    sign=sign,
                    amount=amount,
                    date=date,
                    color=color,
                    editTransaction_function=editTransaction_function,
                    deleteTransaction_function=deleteTransaction_function,
                    currency_sign=currency_sign)

    table = table_begin + table_body + table_end        

   
    deleteTransaction = """
    function deleteTransaction(user_id, transactionType, transactionID, transactionValue) {

        if (confirm("Are you sure to delete this transaction ?")) {

    
            var waiting = document.getElementById('waiting');
            waiting.style.display="block";


            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/DeleteTransactionPage/'+ user_id + '/recurring-delete/transactionID/transactionValue/jarOption/date', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    
            xhr.onload = function() {
                document.open();
                document.write(xhr.responseText);
                document.close();
            };
    
            xhr.send("transactionType="+transactionType+"&transactionID="+transactionID+"&transactionValue="+transactionValue);
        }
        
    }
    """

    editTransaction = """
    function editTransaction(user_id, transactionType, transactionID, transactionValue) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/TransactionPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send("transactionType="+transactionType+"&transactionID="+transactionID+"&transactionValue="+transactionValue+
                "&jarOption=jarOption"+"&date=date");

    };
    """

    back = """
    function back(user_id) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/SettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=RecurringTransactionPage');
    };
    """


    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    history_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        table {
            width: 100%;
        }

        td {
            border-bottom: 1px solid DARKSLATEGRAY;
            padding-top:10px;
            padding-bottom:10px;

        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .balance-label-class {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 100px;
        }


        .income-expense-label {
            background-color: DARKSLATEGRAY;
            border: 1px solid DARKSLATEGRAY;
            color: LIGHTGRAY;
            display: block;
            padding: 6px 0px;
            width: 100%;
            height: 70px;

        }

        .minus-button-label {
            color: TURQUOISE;
            cursor: pointer;
            display: block;
            text-align: center;
        }


        .minus-button-label:active {
            color: LIGHTGRAY;
        }

        .progress-class {
            background-color:LIGHTGRAY;
            height:3px;
            width:100%;
        }

    """

    

    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {history_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>


        <div class="history-table-class" id="history-table" style="height:calc(100vh - 165px); min-height:465px; overflow:auto; -webkit-overflow-scrolling: touch">
            {table}
        </div>

        <p></p>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     

    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {back}
        {editTransaction}
        {deleteTransaction}
    </script>      


    """.format(user_id=user_id,
                history_style=history_style,
                table=table,
                back=back, 
                editTransaction=editTransaction,
                deleteTransaction=deleteTransaction,
                title_caption=title_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/JarSettingPage/<user_id>', methods=['POST'])
def JarSettingPage(user_id):
    
    print "JarSettingPage:user_id:"+user_id

    user_dict = r.hmget(user_id,
                        'nec_pct',
                        'edu_pct',
                        'lts_pct',
                        'ply_pct',
                        'ffa_pct',
                        'giv_pct',
                        'language')

    language = user_dict[6]

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)


    title_caption=language_data[language]['jar_setting_page']['title_caption'].encode('utf-8')
    total_caption=language_data[language]['jar_setting_page']['total_caption'].encode('utf-8')
    nec_caption=language_data[language]['jar_setting_page']['nec_caption'].encode('utf-8')
    edu_caption=language_data[language]['jar_setting_page']['edu_caption'].encode('utf-8')
    lts_caption=language_data[language]['jar_setting_page']['lts_caption'].encode('utf-8')
    ply_caption=language_data[language]['jar_setting_page']['ply_caption'].encode('utf-8')
    ffa_caption=language_data[language]['jar_setting_page']['ffa_caption'].encode('utf-8')
    giv_caption=language_data[language]['jar_setting_page']['giv_caption'].encode('utf-8')
    save_caption=language_data[language]['jar_setting_page']['save_caption'].encode('utf-8')
    back_caption=language_data[language]['jar_setting_page']['back_caption'].encode('utf-8')

    nec_pct = int(user_dict[0])
    edu_pct = int(user_dict[1])
    lts_pct = int(user_dict[2])
    ply_pct = int(user_dict[3])
    ffa_pct = int(user_dict[4])
    giv_pct = int(user_dict[5])

    total_pct = nec_pct + edu_pct + lts_pct + ply_pct + ffa_pct + giv_pct

    pie_chart = """


        var nec_pct = document.getElementById("nec_pct").value;
        var edu_pct = document.getElementById("edu_pct").value;
        var lts_pct = document.getElementById("lts_pct").value;
        var ply_pct = document.getElementById("ply_pct").value;
        var ffa_pct = document.getElementById("ffa_pct").value;
        var giv_pct = document.getElementById("giv_pct").value;

        var nec_jar = document.getElementById("nec-jar").innerHTML;
        var edu_jar = document.getElementById("edu-jar").innerHTML;
        var lts_jar = document.getElementById("lts-jar").innerHTML;
        var ply_jar = document.getElementById("ply-jar").innerHTML;
        var ffa_jar = document.getElementById("ffa-jar").innerHTML;
        var giv_jar = document.getElementById("giv-jar").innerHTML;


        Chart.defaults.global.defaultFontColor = "white";
        var color = Chart.helpers.color;

        window.chartColors = {
            crimson: 'rgb(220, 20, 60)',
            dodgerblue: 'rgb(30, 144, 255)',
            orange: 'rgb(255, 165, 0)',
            orchid: 'rgb(218, 112, 214)',
	        lime: 'rgb(0, 255, 0)',
	        hotpink: 'rgb(255, 105, 180)'
        };

        var pieChartData = {
			labels: [nec_jar, edu_jar, lts_jar, ply_jar, ffa_jar, giv_jar],
			datasets: [{
                borderWidth:1,
                data: [nec_pct, edu_pct, lts_pct, ply_pct, ffa_pct, giv_pct],
                backgroundColor:[
                    window.chartColors.crimson, 
                    window.chartColors.dodgerblue,
                    window.chartColors.orange,
                    window.chartColors.orchid,
                    window.chartColors.lime,
                    window.chartColors.hotpink
                ]
            }]
		};

		var ctx = document.getElementById('myChart');
		new Chart(ctx, {
			type: 'doughnut',
			data: pieChartData,
			options: {
                maintainAspectRatio: false,
				responsive: true,
                legend: {
                    display: false
                }
			}
		});

    """


    jarPercentageChange = """
    function jarPercentageChange(jar, change) {

        var jarPct = "";

        switch(jar) {
        case 'Necessities':
            jarPct = document.getElementById("nec-pct");
            break;
        case 'Education':
            jarPct = document.getElementById("edu-pct");
            break;
        case 'Saving':
            jarPct = document.getElementById("lts-pct");
            break;
        case 'Play':
            jarPct = document.getElementById("ply-pct");
            break;
        case 'Investment':
            jarPct = document.getElementById("ffa-pct");
            break;
        case 'Give':
            jarPct = document.getElementById("giv-pct");
            break;
       
        }

        var jar_pct = parseInt(jarPct.innerHTML);

        var totalPct = document.getElementById("total-pct");
        var total_pct = parseInt(totalPct.innerHTML);

        if (change == 'decrease') {
            if (jar_pct > 0) {
                jar_pct--;
                total_pct--;
            }
        } else {
            if (jar_pct < 100) {
                jar_pct++;
                total_pct++;
            }
        }


        jarPct.innerHTML = jar_pct + "%";

        if (total_pct != 100) {
            totalPct.style.color="TOMATO";
        } else {
            totalPct.style.color="WHITE";
        }

        totalPct.innerHTML = total_pct + "%";

       
    }
    """




    back = """
    function back(user_id) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/SettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=JarSettingPage');
    };
    """

    save = """

    function save(user_id) {

        var nec_pct = parseInt(document.getElementById("nec-pct").innerHTML);
        var edu_pct = parseInt(document.getElementById("edu-pct").innerHTML);
        var lts_pct = parseInt(document.getElementById("lts-pct").innerHTML);
        var ply_pct = parseInt(document.getElementById("ply-pct").innerHTML);
        var ffa_pct = parseInt(document.getElementById("ffa-pct").innerHTML);
        var giv_pct = parseInt(document.getElementById("giv-pct").innerHTML);
        var msg = document.getElementById('msg-label');

        total_pct = nec_pct+edu_pct+lts_pct+ply_pct+ffa_pct+giv_pct;

        if (total_pct != 100) {
            msg.style.color="gold";
            msg.style.display="block";
            return;
        }

   
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/SaveJarSettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    
        xhr.onload = function() {
            back(user_id);
        };
    
        xhr.send("nec_pct="+nec_pct+"&edu_pct="+edu_pct+"&lts_pct="+lts_pct
            +"&ply_pct="+ply_pct+"&ffa_pct="+ffa_pct+"&giv_pct="+giv_pct);

    };
    """

    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/emn178/chartjs-plugin-labels/src/chartjs-plugin-labels.js"></script>


    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    report_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .report-class {
            position: relative;
            width:100%; 
            height:210px;
        }

        .sixjars-label-class {
            display: block;
            color: LIGHTGRAY;
            width: 100%;
            height: 35px;
            font-weight:400;
            padding: 6px 0px;
        }

        .menu-button-label {
            position: absolute;
            color: LIGHTGRAY;
            cursor: pointer;
        }

        
        .menu-button-label:active {
            color: TURQUOISE;
        }

        .pecentage-class {
            border-radius: 5px; 
            position: absolute; 
            top:2px; 
            right: 45px; 
            padding-top:3px; 
            text-align:center; 
            width:40px; 
            height:25px; 
            background-color:SLATEGRAY; 
            color:LIME;
        }

    """

    
    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {report_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        <div class="report-class">
            <canvas id="myChart" style="width:100%; height:100%"></canvas>
            <li id="nec_pct" value="{nec_pct}" style="display:none"></li>
            <li id="edu_pct" value="{edu_pct}" style="display:none"></li>
            <li id="lts_pct" value="{lts_pct}" style="display:none"></li>
            <li id="ply_pct" value="{ply_pct}" style="display:none"></li>
            <li id="ffa_pct" value="{ffa_pct}" style="display:none"></li>
            <li id="giv_pct" value="{giv_pct}" style="display:none"></li>
            <label style="position:absolute; color:white; font-weight:400; top:195px; right:5px">{total_caption} &nbsp<span id="total-pct">{total_pct}%</span></label>

         </div>

        <p></p>

        <div class="sixjars-class" style="background-color:DARKSLATEGRAY">

            <input id="nec-inc-submit" type="button" onclick="jarPercentageChange('Necessities','increase')"> 
            <input id="nec-dec-submit" type="button" onclick="jarPercentageChange('Necessities','decrease')"> 
            <input id="edu-inc-submit" type="button" onclick="jarPercentageChange('Education','increase')"> 
            <input id="edu-dec-submit" type="button" onclick="jarPercentageChange('Education','decrease')"> 
            <input id="lts-inc-submit" type="button" onclick="jarPercentageChange('Saving','increase')"> 
            <input id="lts-dec-submit" type="button" onclick="jarPercentageChange('Saving','decrease')"> 
            <input id="ply-inc-submit" type="button" onclick="jarPercentageChange('Play','increase')"> 
            <input id="ply-dec-submit" type="button" onclick="jarPercentageChange('Play','decrease')"> 
            <input id="ffa-inc-submit" type="button" onclick="jarPercentageChange('Investment','increase')"> 
            <input id="ffa-dec-submit" type="button" onclick="jarPercentageChange('Investment','decrease')"> 
            <input id="giv-inc-submit" type="button" onclick="jarPercentageChange('Give','increase')"> 
            <input id="giv-dec-submit" type="button" onclick="jarPercentageChange('Give','decrease')"> 

            <label class="sixjars-label-class">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/nec.png" style="width:24px;height:24px;">&nbsp<span id="nec-jar">{nec_caption}</span></p>
                </div>
                
                <div class="col-xs-6" style="padding:0px; color:white">
                   
                    <label for="nec-dec-submit" class="menu-button-label" style="right: 95px;">
                        <i class="fa fa-minus-circle fa-2x"></i>
                    </label>

                    <label class="pecentage-class" id="nec-pct">{nec_pct}%</label>
                    
                    <label for="nec-inc-submit" class="menu-button-label" style="right: 10px;">
                        <i class="fa fa-plus-circle fa-2x"></i>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/edu.png" style="width:24px;height:24px;">&nbsp<span id="edu-jar">{edu_caption}</span></p>
                </div>
                
                <div class="col-xs-6" style="padding:0px; color:white">
                   
                    <label for="edu-dec-submit" class="menu-button-label" style="right: 95px;">
                        <i class="fa fa-minus-circle fa-2x"></i>
                    </label>

                    <label class="pecentage-class" id="edu-pct">{edu_pct}%</label>
                    
                    <label for="edu-inc-submit" class="menu-button-label" style="right: 10px;">
                        <i class="fa fa-plus-circle fa-2x"></i>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/lts.png" style="width:24px;height:24px;">&nbsp<span id="lts-jar">{lts_caption}</span></p>
                </div>
                
                <div class="col-xs-6" style="padding:0px; color:white">
                   
                    <label for="lts-dec-submit" class="menu-button-label" style="right: 95px;">
                        <i class="fa fa-minus-circle fa-2x"></i>
                    </label>

                    <label class="pecentage-class" id="lts-pct">{lts_pct}%</label>
                    
                    <label for="lts-inc-submit" class="menu-button-label" style="right: 10px;">
                        <i class="fa fa-plus-circle fa-2x"></i>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/ply.png" style="width:24px;height:24px;">&nbsp<span id="ply-jar">{ply_caption}</span></p>
                </div>
                
                <div class="col-xs-6" style="padding:0px; color:white">
                   
                    <label for="ply-dec-submit" class="menu-button-label" style="right: 95px;">
                        <i class="fa fa-minus-circle fa-2x"></i>
                    </label>

                    <label class="pecentage-class" id="ply-pct">{ply_pct}%</label>
                    
                    <label for="ply-inc-submit" class="menu-button-label" style="right: 10px;">
                        <i class="fa fa-plus-circle fa-2x"></i>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/ffa.png" style="width:24px;height:24px;">&nbsp<span id="ffa-jar">{ffa_caption}</span></p>
                </div>
                
                <div class="col-xs-6" style="padding:0px; color:white">
                   
                    <label for="ffa-dec-submit" class="menu-button-label" style="right: 95px;">
                        <i class="fa fa-minus-circle fa-2x"></i>
                    </label>

                    <label class="pecentage-class" id="ffa-pct">{ffa_pct}%</label>
                    
                    <label for="ffa-inc-submit" class="menu-button-label" style="right: 10px;">
                        <i class="fa fa-plus-circle fa-2x"></i>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/giv.png" style="width:24px;height:24px;">&nbsp<span id="giv-jar">{giv_caption}</span></p>
                </div>
                
                <div class="col-xs-6" style="padding:0px; color:white">
                   
                    <label for="giv-dec-submit" class="menu-button-label" style="right: 95px;">
                        <i class="fa fa-minus-circle fa-2x"></i>
                    </label>

                    <label class="pecentage-class" id="giv-pct">{giv_pct}%</label>
                    
                    <label for="giv-inc-submit" class="menu-button-label" style="right: 10px;">
                        <i class="fa fa-plus-circle fa-2x"></i>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

        </div>
      
        <p></p>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="save" type="button" onclick="save('{user_id}')"> 
                <label class="save-class" for="save">
                    <i class="fa fa-floppy-o" style="color:LIME"></i>&nbsp {save_caption}
                </label>
            </div>
            
        </div>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     

    <div class="msg-class">           
        <label id="msg-label" style="text-align:center; display:none; font-weight:400"><i class="fa fa-warning"></i> Total percentage must be 100%</label>
    </div>

    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {back}
        {save}
        {jarPercentageChange}
        {pie_chart}
    </script>      


    """.format(user_id=user_id,
                report_style=report_style,
                back=back,
                save=save,
                jarPercentageChange=jarPercentageChange,
                pie_chart=pie_chart,
                nec_pct=nec_pct,
                edu_pct=edu_pct,
                lts_pct=lts_pct,
                ply_pct=ply_pct,
                ffa_pct=ffa_pct,
                giv_pct=giv_pct,
                total_pct=total_pct,
                title_caption=title_caption,
                total_caption=total_caption,
                nec_caption=nec_caption,
                edu_caption=edu_caption,
                lts_caption=lts_caption,
                ply_caption=ply_caption,
                ffa_caption=ffa_caption,
                giv_caption=giv_caption,
                save_caption=save_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/SaveJarSettingPage/<user_id>', methods=['POST'])
def SaveJarSettingPage(user_id):
    

    nec_pct = request.form['nec_pct']
    edu_pct = request.form['edu_pct']
    lts_pct = request.form['lts_pct']
    ply_pct = request.form['ply_pct']
    ffa_pct = request.form['ffa_pct']
    giv_pct = request.form['giv_pct']



    print "SaveJarsSetting:user_id:"+user_id
    print "SaveJarsSetting:nec_pct:"+nec_pct
    print "SaveJarsSetting:edu_pct:"+edu_pct
    print "SaveJarsSetting:lts_pct:"+lts_pct
    print "SaveJarsSetting:ply_pct:"+ply_pct
    print "SaveJarsSetting:ffa_pct:"+ffa_pct
    print "SaveJarsSetting:giv_pct:"+giv_pct

    r.hmset(user_id,{
            'nec_pct':nec_pct,
            'edu_pct':edu_pct,
            'lts_pct':lts_pct,
            'ply_pct':ply_pct,
            'ffa_pct':ffa_pct,
            'giv_pct':giv_pct
        })
    

    return ""


@app.route('/GeneralSettingPage/<user_id>', methods=['POST'])
def GeneralSettingPage(user_id):
    
    print "GeneralSettingPage:user_id:"+user_id

    language = r.hget(user_id,'language')

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)


    title_caption=language_data[language]['general_setting_page']['title_caption'].encode('utf-8')
    language_caption=language_data[language]['general_setting_page']['language_caption'].encode('utf-8')
    currency_caption=language_data[language]['general_setting_page']['currency_caption'].encode('utf-8')
    factory_reset_caption=language_data[language]['general_setting_page']['factory_reset_caption'].encode('utf-8')
    version_caption=language_data[language]['general_setting_page']['version_caption'].encode('utf-8')
    back_caption=language_data[language]['general_setting_page']['back_caption'].encode('utf-8')

    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">
        

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">


        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"


    language_setting = """
    function language_setting(user_id) {
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/LanguageSettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };

        xhr.send();
    }
    """

    currency_setting = """
    function currency_setting(user_id) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/CurrencySettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };

        xhr.send();

    }
    """

    factory_reset = """
    function factory_reset(user_id) {

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/FactoryResetPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };

        xhr.send();

        
    }
    """


    back = """

    function back(user_id) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/SettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };

        xhr.send('sender_id=GeneralSettingPage');
 
    };
    """

 
    setting_style = """


        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

    
        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        .general-class {
            text-align: left; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:40px; width: 100%; 
            padding-left:15px;
            padding-top:10px;
            cursor: pointer;
        }

        .general-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .back-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }

        .back-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .version-class {
            text-align: left; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:40px; width: 100%; 
            padding-left:15px;
            padding-top:10px;
        }

    """

    mid_html = """
    
    <style>
        /*------ addtranaction style ---------*/
        {setting_style}
    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="language-setting" type="button" onclick="language_setting('{user_id}')"> 
                <label class="general-class" for="language-setting">
                    <i class="fa fa-globe" style="color:LIGHTGRAY;"></i>&nbsp {language_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
            
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="currency-setting" type="button" onclick="currency_setting('{user_id}')"> 
                <label class="general-class" for="currency-setting">
                    <i class="fa fa-usd" style="color:LIGHTGRAY;"></i>&nbsp {currency_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="factory-reset" type="button" onclick="factory_reset('{user_id}')"> 
                <label class="general-class" for="factory-reset">
                    <i class="fa fa-refresh" style="color:LIGHTGRAY;"></i>&nbsp {factory_reset_caption}
                    <i class="fa fa-angle-right" style="position:absolute; top:12px; right:15px"></i>
                </label>
            </div>
        </div>

        <div class="button-class" style="height:45px; color: LIGHTGRAY;">
            <div class="col-xs-12" style="height:100%; padding: 0">
                <label class="version-class">
                    <i class="fa fa-info-circle" style="color:LIGHTGRAY;"></i>&nbsp {version_caption}
                </label>
            </div>
        </div>

        <p></p>

      
        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="back-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>


    </div>           

  
    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>


    <script>
        {language_setting}
        {currency_setting}
        {factory_reset}
        {back}
    </script>
    
    """.format(user_id=user_id,
                setting_style=setting_style,
                language_setting=language_setting,
                currency_setting=currency_setting,
                factory_reset=factory_reset,
                back=back,
                title_caption=title_caption,
                language_caption=language_caption,
                currency_caption=currency_caption,
                factory_reset_caption=factory_reset_caption,
                version_caption=version_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/LanguageSettingPage/<user_id>', methods=['POST'])
def LanguageSettingPage(user_id):
    
    language = r.hget(user_id,'language')

    print "LanguageSettingPage:user_id"+user_id
    print "LanguageSettingPage:"+language

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)

    title_caption=language_data[language]['language_page']['title_caption'].encode('utf-8')
    save_caption=language_data[language]['language_page']['save_caption'].encode('utf-8')
    back_caption=language_data[language]['language_page']['back_caption'].encode('utf-8')


    initValue = """
    function initValue(language) {
        var radioButtons = document.getElementsByName("language");
        for (var x = 0; x < radioButtons.length; x ++) {

            if (radioButtons[x].value == language) {
                radioButtons[x].checked = "checked"
            }

        }
    }
    """

    back = """
    function back(user_id) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/GeneralSettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=LanguageSettingPage');
    };
    """

    save = """

    function save(user_id) {
        
        var radioButtons = document.getElementsByName("language");
        for (var x = 0; x < radioButtons.length; x ++) {
            if (radioButtons[x].checked) {

                var waiting = document.getElementById('waiting');
                waiting.style.display="block";

                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/SaveLanguagePage/'+user_id, true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                        
                xhr.onload = function() {
                    back(user_id);
                };
        
                xhr.send('language='+radioButtons[x].value);
            }
        }

    };
    """



    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    report_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .report-class {
            position: relative;
            width:100%; 
            height:210px;
        }

        .sixjars-label-class {
            display: block;
            color: LIGHTGRAY;
            width: 100%;
            height: 35px;
            font-weight:400;
            padding: 6px 0px;
        }

        

        /* The radio-container */
        .radio-container {
            display: block;
            position: absolute;
            top:5px;
            right:27px;
            cursor: pointer;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }

        /* Hide the browser's default radio button */
        .radio-container input {
            position: absolute;
            opacity: 0;
            cursor: pointer;
        }

        /* Create a custom radio button */
        .checkmark {
            position: absolute;
            top: 0;
            left: 0;
            height: 18px;
            width: 18px;
            background-color: LIGHTGRAY;
            border-radius: 50%;
        }

       
        /* Create the indicator (the dot/circle - hidden when not checked) */
        .checkmark:after {
            content: "";
            position: absolute;
            display: none;
        }

        /* Show the indicator (dot/circle) when checked */
        .radio-container input:checked ~ .checkmark:after {
            display: block;
        }

        /* Style the checkmark/indicator */
        .radio-container .checkmark:after {
            left: 5px;
            top: 2px;
            width: 8px;
            height: 14px;
            border: solid DARKSLATEGRAY;
            border-width: 0 3px 3px 0;
            -webkit-transform: rotate(45deg);
            -ms-transform: rotate(45deg);
            transform: rotate(45deg);
        }

    """

    
    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {report_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        
        <div class="sixjars-class" style="background-color:DARKSLATEGRAY">


            <label class="sixjars-label-class">
                <div class="col-xs-10" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/vietnam.png" style="width:24px;height:24px;">&nbsp Tiếng Việt (Vietnamese) </p>
                </div>
                
                <div class="col-xs-2">
                    <label class="radio-container">
                        <input type="radio" name="language" value="Vietnamese">
                        <span class="checkmark"></span>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class">
                <div class="col-xs-10" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/usa.png" style="width:24px;height:24px;">&nbsp English (US/UK)</p>
                </div>
                
                <div class="col-xs-2" style="padding-top:5px;">   
                    <label class="radio-container">
                        <input type="radio" name="language" value="English">
                        <span class="checkmark"></span>
                    </label>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

        </div>
      
        <p></p>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="save" type="button" onclick="save('{user_id}')"> 
                <label class="save-class" for="save">
                    <i class="fa fa-floppy-o" style="color:LIME"></i>&nbsp {save_caption}
                </label>
            </div>
            
        </div>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     


    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {back}
        {save}
        {initValue}

        initValue('{language}');
    </script>      


    """.format(user_id=user_id,
                report_style=report_style,
                back=back,
                save=save,
                initValue=initValue,
                language=language,
                title_caption=title_caption,
                save_caption=save_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/SaveLanguagePage/<user_id>', methods=['POST'])
def SaveLanguagePage(user_id):
    
    language = request.form['language']
   
    print "SaveLanguagePage:user_id"+user_id
    print "SaveLanguagePage:"+language
    
    r.hset(user_id, 'language', language) 

    return ""


@app.route('/CurrencySettingPage/<user_id>', methods=['POST'])
def CurrencySettingPage(user_id):
    
    print "CurrencySettingPage:user_id:"+user_id

    table_begin = """
        <table>
    """
    table_end = """
        </table>
    """

    table_body = ""

    checked = ""

    user_dict = r.hmget(user_id,
                        'currency',
                        'language')
    
    currency = user_dict[0]
    language = user_dict[1]

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)

    #load currency json file
    with open('static/currency.json') as f:
        currency_data = json.load(f)

    title_caption=language_data[language]['currency_page']['title_caption'].encode('utf-8')
    save_caption=language_data[language]['currency_page']['save_caption'].encode('utf-8')
    back_caption=language_data[language]['currency_page']['back_caption'].encode('utf-8')

    for i in range(0,len(currency_data['currency'])):

        currency_icon = currency_data['currency'][i]['currency_icon']
        currency_name = currency_data['currency'][i]['currency_name']
        currency_code = currency_data['currency'][i]['currency_code']
        currency_sign = currency_data['currency'][i]['currency_sign']

        if (currency == currency_code):
            checked = "checked"
        else:
            checked = ""
            
        table_body = table_body + """
            <tr>
                <td id="cell1" style="text-align:center"><img src="{currency_icon}" style="width:32px;height:32px;"></td>
                <td id="cell2"><span style="color:white">{currency_name}</span><br><span style="font-size:small; font-weight:300; color:LIGHTGRAY">{currency_code} ({currency_sign})</span></td>
                <td id="cell3">
                    <label class="radio-container">
                        <input type="radio" name="currency" {checked} value="{currency_code}">
                        <span class="checkmark"></span>
                    </label>
                </td>
            </tr>
        """.format(currency_icon=currency_icon,
                    currency_name=currency_name,
                    currency_code=currency_code,
                    currency_sign=currency_sign,
                    checked=checked)


    table = table_begin + table_body + table_end        

    
    back = """
    function back(user_id) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";


        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/GeneralSettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=CurrencySettingPage');
    };
    """

    save = """

    function save(user_id) {
        
        var radioButtons = document.getElementsByName("currency");
        for (var x = 0; x < radioButtons.length; x ++) {
            if (radioButtons[x].checked) {

                var waiting = document.getElementById('waiting');
                waiting.style.display="block";

                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/SaveCurrencyPage/'+user_id, true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                        
                xhr.onload = function() {
                    back(user_id);
                };
        
                xhr.send('currency='+radioButtons[x].value);
            }
        }

    };
    """
    
    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    history_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        table {
            width: 100%;
        }

        td {
            border-bottom: 1px solid DARKSLATEGRAY;
            padding-top:10px;
            padding-bottom:10px;

        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

       

        /* The radio-container */
        .radio-container {
            display: block;
            position: relative;
            padding-right: 18px;
            padding-bottom: 15px;
            cursor: pointer;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }

        /* Hide the browser's default radio button */
        .radio-container input {
            position: absolute;
            opacity: 0;
            cursor: pointer;
        }

        /* Create a custom radio button */
        .checkmark {
            position: absolute;
            top: 0;
            left: 0;
            height: 18px;
            width: 18px;
            background-color: LIGHTGRAY;
            border-radius: 50%;
        }

       
        /* Create the indicator (the dot/circle - hidden when not checked) */
        .checkmark:after {
            content: "";
            position: absolute;
            display: none;
        }

        /* When the radio button is checked, add a blue background */
        .radio-container input:checked ~ .checkmark {
            background-color: DARKSLATEGRAY;
        }

        /* Show the indicator (dot/circle) when checked */
        .radio-container input:checked ~ .checkmark:after {
            display: block;
        }

        /* Style the checkmark/indicator */
        .radio-container .checkmark:after {
            left: 5px;
            top: 2px;
            width: 8px;
            height: 14px;
            border: solid LIGHTGRAY;
            border-width: 0 3px 3px 0;
            -webkit-transform: rotate(45deg);
            -ms-transform: rotate(45deg);
            transform: rotate(45deg);
        }

    """

    

    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {history_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

       
        <div class="history-table-class" id="history-table" style="height:calc(100vh - 205px); min-height:425px; overflow:auto; -webkit-overflow-scrolling: touch">
            {table}
        </div>

        <p></p>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="save" type="button" onclick="save('{user_id}')"> 
                <label class="save-class" for="save">
                    <i class="fa fa-floppy-o" style="color:LIME"></i>&nbsp {save_caption}
                </label>
            </div>
            
        </div>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     

    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {back}
        {save}
    </script>      


    """.format(user_id=user_id,
                history_style=history_style,
                table=table,
                back=back,
                save=save,
                title_caption=title_caption,
                save_caption=save_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/SaveCurrencyPage/<user_id>', methods=['POST'])
def SaveCurrencyPage(user_id):
    
    currency = request.form['currency']
   
    print "SaveCurrencyPage:user_id"+user_id
    print "SaveCurrencyPage:"+currency
    
    r.hset(user_id, 'currency', currency) 

    return ""


@app.route('/FactoryResetPage/<user_id>', methods=['POST'])
def FactoryResetPage(user_id):
    
    print "FactoryResetPage:user_id:"+user_id

    user_dict = r.hmget(user_id,
                            'language',
                            'user_email',
                            'user_login')

    language = user_dict[0]
    user_email = user_dict[1]
    user_login = user_dict[2]

    #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)

    title_caption=language_data[language]['factory_reset_page']['title_caption'].encode('utf-8')
    note_caption=language_data[language]['factory_reset_page']['note_caption'].encode('utf-8')
    step1_caption=language_data[language]['factory_reset_page']['step1_caption'].encode('utf-8')
    step2_caption=language_data[language]['factory_reset_page']['step2_caption'].encode('utf-8')
    reset_caption=language_data[language]['factory_reset_page']['reset_caption'].encode('utf-8')
    back_caption=language_data[language]['factory_reset_page']['back_caption'].encode('utf-8')


    back = """
    function back(user_id) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/GeneralSettingPage/'+user_id, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=FactoryResetPage');
    };
    """

    back2 = """
    function back2(user_id, user_email, user_login) {
        

        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var d = new Date();
        var today =d.getFullYear()+'-'+addZero(d.getMonth()+1)+'-'+addZero(d.getDate());

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/HomePage/'+user_id+'/'+today, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send('sender_id=WelcomePage'+'&user_email='+user_email+'&user_login='+user_login);
    };
    """

    reset = """

    function reset(user_id, user_email, user_login) {
        
        var confirm = document.getElementById('confirm');

        if (confirm.value.toUpperCase() == "CONFIRM") {
            var waiting = document.getElementById('waiting');
            waiting.style.display="block";


            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/ResetConfirmPage/'+user_id, true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    
            xhr.onload = function() {
                back2(user_id, user_email, user_login);
            };
    
            xhr.send();
        }


    };
    """
    
    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    history_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        
        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        
        
    """

    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {history_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        <div>
            <label style="color: orange; font-weight:400">{note_caption}</label>
        </div>
       
        <br>

        <div>
            <label style="color: white; font-weight:300">{step1_caption}</label>
            <input type="text" id="confirm" style="color: white; text-transform:uppercase; border: 1px solid tomato; width:100%; height: 35px; background-color:SLATEGRAY; -webkit-appearance: none;">
        </div>

        <br>
      
        <div>
            <label style="color: white; font-weight:300">{step2_caption}</label>
        </div>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="reset" type="button" onclick="reset('{user_id}','{user_email}','{user_login}')"> 
                <label class="save-class" for="reset">
                    <i class="fa fa-refresh" style="color:LIME"></i>&nbsp {reset_caption}
                </label>
            </div>
            
        </div>

        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{user_id}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     

    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {back}
        {back2}
        {reset}
    </script>      


    """.format(user_id=user_id,
                user_email=user_email,
                user_login=user_login,
                history_style=history_style,
                back=back,
                back2=back2,
                reset=reset,
                title_caption=title_caption,
                note_caption=note_caption,
                step1_caption=step1_caption,
                step2_caption=step2_caption,
                reset_caption=reset_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


@app.route('/ResetConfirmPage/<user_id>', methods=['POST'])
def ResetConfirmPage(user_id):
    
    print "ResetConfirmPage:user_id:"+user_id

    r.delete(user_id)
    
    return ""


@app.route('/SelectJarPage/<user_id>', methods=['POST'])
def SelectJarPage(user_id):
    
    sender_id = request.form['sender_id']
    jar = request.form['jar']
    date = request.form['date']
    
    print "SelectJarPage:user_id:"+user_id
    print "SelectJarPage:sender_id:"+sender_id
    print "SelectJarPage:jar:"+jar
    print "SelectJarPage:date:"+date
    
    user_dict = r.hmget(user_id,
                        'nec_income',
                        'edu_income',
                        'lts_income',
                        'ply_income',
                        'ffa_income',
                        'giv_income',
                        'nec_expense',
                        'edu_expense',
                        'lts_expense',
                        'ply_expense',
                        'ffa_expense',
                        'giv_expense',
                        'nec_prebal',
                        'edu_prebal',
                        'lts_prebal',
                        'ply_prebal',
                        'ffa_prebal',
                        'giv_prebal',
                        'currency',
                        'income_amt',
                        'expense_amt',
                        'pre_balance',
                        'language')

    currency = user_dict[18]
    language = user_dict[22]


   #load language json file
    with open('static/language.json') as f:
        language_data = json.load(f)

    #load currency json file
    with open('static/currency.json') as f:
        currency_data = json.load(f)


    title_caption=language_data[language]['select_jar_page']['title_caption'].encode('utf-8')
    all_caption=language_data[language]['select_jar_page']['all_caption'].encode('utf-8')
    nec_caption=language_data[language]['select_jar_page']['nec_caption'].encode('utf-8')
    edu_caption=language_data[language]['select_jar_page']['edu_caption'].encode('utf-8')
    lts_caption=language_data[language]['select_jar_page']['lts_caption'].encode('utf-8')
    ply_caption=language_data[language]['select_jar_page']['ply_caption'].encode('utf-8')
    ffa_caption=language_data[language]['select_jar_page']['ffa_caption'].encode('utf-8')
    giv_caption=language_data[language]['select_jar_page']['giv_caption'].encode('utf-8')
    back_caption=language_data[language]['select_jar_page']['back_caption'].encode('utf-8')

    for i in range(0,len(currency_data['currency'])):
        currency_code = currency_data['currency'][i]['currency_code']
        if (currency == currency_code):
            currency_sign = currency_data['currency'][i]['currency_sign']
            break

    income_amt = int(float(user_dict[19]))
    expense_amt = int(float(user_dict[20]))
    pre_balance = int(float(user_dict[21]))

    nec_income = int(float(user_dict[0]))
    edu_income = int(float(user_dict[1]))
    lts_income = int(float(user_dict[2]))
    ply_income = int(float(user_dict[3]))
    ffa_income = int(float(user_dict[4]))
    giv_income = int(float(user_dict[5]))

    nec_expense = int(float(user_dict[6]))
    edu_expense = int(float(user_dict[7]))
    lts_expense = int(float(user_dict[8]))
    ply_expense = int(float(user_dict[9]))
    ffa_expense = int(float(user_dict[10]))
    giv_expense = int(float(user_dict[11]))

    nec_prebal = int(float(user_dict[12]))
    edu_prebal = int(float(user_dict[13]))
    lts_prebal = int(float(user_dict[14]))
    ply_prebal = int(float(user_dict[15]))
    ffa_prebal = int(float(user_dict[16]))
    giv_prebal = int(float(user_dict[17]))
        

    balance_amt = income_amt - expense_amt + pre_balance

    nec_balance = nec_income - nec_expense + nec_prebal
    edu_balance = edu_income - edu_expense + edu_prebal
    lts_balance = lts_income - lts_expense + lts_prebal
    ply_balance = ply_income - ply_expense + ply_prebal
    ffa_balance = ffa_income - ffa_expense + ffa_prebal
    giv_balance = giv_income - giv_expense + giv_prebal

    back = """
    function back(sender_id,user_id,jar,date) {
        
        var waiting = document.getElementById('waiting');
        waiting.style.display="block";

        var url = '/ReportPage/'+user_id+'/'+jar+'/'+date

        if (sender_id == 'HistoryPage') {
            url = '/HistoryPage/'+user_id+'/'+jar+'/'+date
        }

        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                
        xhr.onload = function() {
            document.open();
            document.write(xhr.responseText);
            document.close();
        };
 
        xhr.send("sender_id=SelectJarPage");
    };
    """

    jarFunction = """
    function jarFunction(sender_id,user_id,jar,date) {
        back(sender_id,user_id,jar,date);
    };
    """
    

    begin_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MoneyOi</title>
        <meta charset="utf-8">
        <meta name="description" content="MoneyOi Cloud Native Application">
        <meta name="author" content="moneyoi.herokuapp.com">
        <meta name="keywords" content="moneyoi,free,6,six,jar,jars,app,money,method,management,cloud,native,application">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700">

        <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <link rel="apple-touch-icon" sizes="57x57" href="/static/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/static/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/static/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/static/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/static/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/static/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/static/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/static/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192" href="/static/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/static/ms-icon-144x144.png">
        <meta name="msapplication-square70x70logo" content="/static/ms-icon-70x70.png">
        <meta name="msapplication-square150x150logo" content="/static/ms-icon-150x150.png">
        <meta name="msapplication-square310x310logo" content="/static/ms-icon-310x310.png">

        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <![endif]-->
  	

    </head>
    
    <body style="font-family:Roboto; background-color:SLATEGRAY" ontouchstart="">
    
    """

    end_html = "</body></html>"

    
    report_style = """

        html {
            height: 100%;
        }

        body {
            position: relative;
            min-height: 100%;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }

        input[type="button"] {
            display: none;
        }

        
        .waiting-class {
            display:none;
            margin: auto;
            text-align: center;
            width:100%;
            height:100%;
            top:0;
            position:absolute;
            padding-top: 50%;
            background: rgba(0, 0, 0, 0.3)
        }

        .save-class {
            text-align: center; 
            font-weight: 300; 
            background-color: DARKSLATEGRAY; 
            height:35px; width: 100%; 
            padding-top:7px;
            cursor: pointer;
        }


        .save-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }

        .report-class {
            position: relative;
            width:100%; 
            height:210px;
        }

        .sixjars-label-class {
            display: block;
            color: LIGHTGRAY;
            width: 100%;
            height: 35px;
            font-weight:400;
            padding: 6px 0px;
            cursor:pointer;
        }

        .sixjars-label-class:active {
            color:DARKSLATEGRAY;
            background-color: LIGHTGRAY; 
        }


    """

    
    mid_html = """
    
    <style>
        /*------ history style ---------*/
        {report_style}

    </style>

    <div class="container">

        <div style="background-color:DARKSLATEGRAY">
    	    <h4>
                <p class="text-center" style="color:white;">{title_caption}</p>
            </h4>
        </div>

        <p></p>

        <div class="sixjars-class" style="background-color:DARKSLATEGRAY">


            <input id="all-submit" type="button" onclick="jarFunction('{sender_id}','{user_id}','All','{date}')">
            <input id="nec-submit" type="button" onclick="jarFunction('{sender_id}','{user_id}','Necessities','{date}')">
            <input id="edu-submit" type="button" onclick="jarFunction('{sender_id}','{user_id}','Education','{date}')">
            <input id="lts-submit" type="button" onclick="jarFunction('{sender_id}','{user_id}','Saving','{date}')">
            <input id="ply-submit" type="button" onclick="jarFunction('{sender_id}','{user_id}','Play','{date}')">
            <input id="ffa-submit" type="button" onclick="jarFunction('{sender_id}','{user_id}','Investment','{date}')">
            <input id="giv-submit" type="button" onclick="jarFunction('{sender_id}','{user_id}','Give','{date}')">

            <label class="sixjars-label-class" for="all-submit">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/all.png" style="width:24px;height:24px;">&nbsp {all_caption}</p>
                </div>
                
                <div class="col-xs-6" style="padding-top:4px;">
                    <p class="text-right" style="color:white;">{balance_amt} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class" for="nec-submit">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/nec.png" style="width:24px;height:24px;">&nbsp {nec_caption}</p>
                </div>
                
                <div class="col-xs-6" style="padding-top:4px;">
                    <p class="text-right" style="color:white;">{nec_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class" for="edu-submit">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/edu.png" style="width:24px;height:24px;">&nbsp {edu_caption}</p>
                </div>
                
                <div class="col-xs-6" style="padding-top:4px;">
                    <p class="text-right" style="color:white;">{edu_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class" for="lts-submit">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/lts.png" style="width:24px;height:24px;">&nbsp {lts_caption}</p>
                </div>
                
                <div class="col-xs-6" style="padding-top:4px;">
                    <p class="text-right" style="color:white;">{lts_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class" for="ply-submit">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/ply.png" style="width:24px;height:24px;">&nbsp {ply_caption}</p>
                </div>
                
                <div class="col-xs-6" style="padding-top:4px;">
                    <p class="text-right" style="color:white;">{ply_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class" for="ffa-submit">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/ffa.png" style="width:24px;height:24px;">&nbsp {ffa_caption}</p>
                </div>
                
                <div class="col-xs-6" style="padding-top:4px;">
                    <p class="text-right" style="color:white;">{ffa_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

            <label class="sixjars-label-class" for="giv-submit">
                <div class="col-xs-6" style="padding-top:2px; padding-left:7px; font-weight:300;">
                    <p class="text-left"><img src="/static/giv.png" style="width:24px;height:24px;">&nbsp {giv_caption}</p>
                </div>
                
                <div class="col-xs-6" style="padding-top:4px;">
                    <p class="text-right" style="color:white;">{giv_balance} {currency_sign} &nbsp <i class="fa fa-angle-right"></i></p>
                </div>
            </label>

            <div id="separator" style="background-color:SLATEGRAY; width:100%; height:1px;"></div>

        </div>
      
        <p></p>


        <div class="button-class" style="height:40px; color: LIGHTGRAY;">
            
            <div class="col-xs-12" style="height:100%; padding: 0">
                <input id="back" type="button" onclick="back('{sender_id}','{user_id}','{jar}','{date}')"> 
                <label class="save-class" for="back">
                    <i class="fa fa-angle-left" style="color:LIME;"></i>&nbsp {back_caption}
                </label>
            </div>
            
        </div>

    </div>     


    <div id="waiting" class="waiting-class">
        <i style="color:LIME" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
    </div>

    <script>
        {back}
        {jarFunction}
    </script>      

    """.format(user_id=user_id,
                report_style=report_style,
                back=back,
                jar=jar,
                date=date,
                sender_id=sender_id,
                balance_amt="{:,}".format(balance_amt),
                nec_balance="{:,}".format(nec_balance),
                edu_balance="{:,}".format(edu_balance),
                lts_balance="{:,}".format(lts_balance),
                ply_balance="{:,}".format(ply_balance),
                ffa_balance="{:,}".format(ffa_balance),
                giv_balance="{:,}".format(giv_balance),
                jarFunction=jarFunction,
                currency_sign=currency_sign,
                title_caption=title_caption,
                all_caption=all_caption,
                nec_caption=nec_caption,
                edu_caption=edu_caption,
                lts_caption=lts_caption,
                ply_caption=ply_caption,
                ffa_caption=ffa_caption,
                giv_caption=giv_caption,
                back_caption=back_caption)

    
    return begin_html + mid_html + end_html


if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))