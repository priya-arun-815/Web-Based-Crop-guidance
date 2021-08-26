from flask import Flask,render_template,flash,request
import numpy as np
import pandas as pd
import geocoder
import requests, json
import time
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError
import json
import tweepy
from datetime import date
import logging
import re
from sklearn.preprocessing import StandardScaler
global api

app=Flask(__name__)

ans=[]

@app.route('/crop')
def crop():
    userph=[[5.3]]
    usernx=[[53]]
    userpx=[[65]]
    userkx=[[89]]
    """from datetime import date
    today = date.today()
    d1 = int(today.strftime("%m"))
    if(d1>1 and d1<7):
        csvname="summer.csv"
        userrainx=[[108]]
        usertempx=[[32]]
        userhumx=[[75]]
    else:
        csvname="monsoon.csv"
        userrainx=[[130]]
        usertempx=[[20]]
        userhumx=[[80]]
    """
    csvname="monsoon.csv"
    userrainx=[[130]]
    usertempx=[[20]]
    userhumx=[[80]]
    data=pd.read_csv(csvname)
    data.drop(data.columns[data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    max_rows=len(data)
    Nx=data.iloc[:,1:2].values
    Px=data.iloc[:,2:3].values
    Kx=data.iloc[:,3:4].values
    min_tempx=data.iloc[:,4:5].values
    max_tempx=data.iloc[:,5:6].values
    min_humx=data.iloc[:,8:9].values
    max_humx=data.iloc[:,9:10].values
    min_rainx=data.iloc[:,6:7].values
    max_rainx=data.iloc[:,7:8].values

    from sklearn.preprocessing import StandardScaler

    sc1 = StandardScaler()
    sc2=StandardScaler()
    sc3=StandardScaler()
    sc4=StandardScaler()
    sc5=StandardScaler()
    sc6=StandardScaler()
    sc7=StandardScaler()
    sc8=StandardScaler()
    sc9=StandardScaler()

    Nx1=np.append(Nx,usernx)
    Nx1=Nx1.reshape(-1,1)
    Nx1=sc1.fit_transform(Nx1)
    Nx1=sc1.transform(Nx1)

    Px1=np.append(Px,userpx)
    Px1=Px1.reshape(-1,1)
    Px1=sc2.fit_transform(Px1)
    Px1=sc2.transform(Px1)

    Kx1=np.append(Kx,userkx)
    Kx1=Kx1.reshape(-1,1)
    Kx1=sc3.fit_transform(Kx1)
    Kx1=sc3.transform(Kx1)

    min_tempx1=np.append(min_tempx,usertempx)
    min_tempx1=min_tempx1.reshape(-1,1)
    min_tempx1 = sc4.fit_transform(min_tempx1)
    min_tempx1 = sc4.transform(min_tempx1)

    max_tempx1=np.append(max_tempx,usertempx)
    max_tempx1=max_tempx1.reshape(-1,1)
    max_tempx1 = sc5.fit_transform(max_tempx1)
    max_tempx1 = sc5.transform(max_tempx1)

    min_humx1=np.append(min_humx,userhumx)
    min_humx1=min_humx1.reshape(-1,1)
    min_humx1 = sc6.fit_transform(min_humx1)
    min_humx1 = sc6.transform(min_humx1)

    max_humx1=np.append(max_humx,userhumx)
    max_humx1=max_humx1.reshape(-1,1)
    max_humx1 = sc7.fit_transform(max_humx1)
    max_humx1 = sc7.transform(max_humx1)

    min_rainx1=np.append(min_rainx,userrainx)
    min_rainx1=min_rainx1.reshape(-1,1)
    min_rainx1 = sc8.fit_transform(min_rainx1)
    min_rainx1 = sc8.transform(min_rainx1)

    max_rainx1=np.append(max_rainx,userrainx)
    max_rainx1=max_rainx1.reshape(-1,1)
    max_rainx1 = sc9.fit_transform(max_rainx1)
    max_rainx1= sc9.transform(max_rainx1)


    error_row=[]
    for i in range(max_rows-1):
        error=float(pow((Nx1[i][0]-Nx1[max_rows][0]),2)+pow((Px1[i][0]-Px1[max_rows][0]),2)+pow((Kx1[i][0]-Kx1[max_rows][0]),2))
        error_row.append(error)

    for i in range(max_rows-1):
        if(userrainx[0][0]>=data['min_rain'][i] and userrainx[0][0]<=data['max_rain'][i]):
             error_row[i]+=0.0

        elif(userrainx[0][0]>data['max_rain'][i]):

            error_row[i]+=float(pow(max_rainx1[i][0]-max_rainx1[max_rows][0],2))
        elif(userrainx[0][0]<data['min_rain'][i]):

            error_row[i]+=float(pow(min_rainx1[i][0]-min_rainx1[max_rows][0],2) )

        if(userhumx[0][0]>=data['min_hum'][i] and userhumx[0][0]<=data['max_hum'][i]):
            error_row[i]+=0.0

        elif(userhumx[0][0]>data['max_hum'][i]):

            error_row[i]+=float(pow(max_humx1[i][0]-max_humx1[max_rows][0],2) )
        elif(userhumx[0][0]<data['min_hum'][i]):

             error_row[i]+=float(pow(min_humx1[i][0]-min_humx1[max_rows][0],2) )

        if(usertempx[0][0]>=data['min_temp'][i] and usertempx[0][0]<=data['max_temp'][i]):
            error_row[i]+=0.0


        elif(usertempx[0][0]>data['max_temp'][i]):

            error_row[i]+=float(pow(max_tempx1[i][0]-max_tempx1[max_rows][0],2) )
        elif(usertempx[0][0]<data['min_temp'][i]):
             error_row[i]+=float(pow(min_tempx1[i][0]-min_tempx1[max_rows][0],2))

    for i in range(max_rows-1):
        error_row[i]=0.5*(pow(error_row[i],0.5))


    q=[]
    q=error_row[:]
    q.sort()
    best=q[0]
    second_best=q[1]
    ans=[]
    pos1=error_row.index(best)
    pos2=error_row.index(second_best)
    for i in range(15):
        if(i==pos1 or i == pos2):
            ans.append((data['Crop'][i]))
    return render_template("show_crop.html", data=ans)


@app.route ('/weather')
def weather():
    api_key = 'c7d3a4f8990afb4408e75b2f232744d6'
    api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

    running = True
    flag=0
    red=0
    c=" "
    # Program loop
    while running and red==0:

        # Asks the user for the city or zip code to be queried
        while True:

            # Input validation

                # Passed the validation test
                red+=1
                city = "Chennai"
                if city.lower() == 'sf':
                    city = 'San Francisco, US'

                    # Appends the city to the api call
                api_call += '&q=' + city
                break



        # Stores the Json response
        json_data = requests.get(api_call).json()

        location_data = {
            'city': json_data['city']['name'],
            'country': json_data['city']['country']
        }

        #print('\n{city}, {country}'.format(**location_data))

        # The current date we are iterating through
        current_date = ''
        flag=0
        # Iterates through the array of dictionaries named list in json_data
        for item in json_data['list'] :
            flag+=1
            if(flag==1):
            # Time of the weather data received, partitioned into 3 hour blocks
                time = item['dt_txt']

            # Split the time into date and hour [2018-04-15 06:00:00]
                next_date, hour = time.split(' ')

            # Stores the current date and prints it once
                if current_date != next_date:
                    current_date = next_date
                    year, month, day = current_date.split('-')
                    date = {'y': year, 'm': month, 'd': day}
                    #print('\n{m}/{d}/{y}'.format(**date))

            # Grabs the first 2 integers from our HH:MM:SS string to get the hours
                hour = int(hour[:2])

            # Sets the AM (ante meridiem) or PM (post meridiem) period
                if hour < 12:
                    if hour == 0:
                        hour = 12
                    meridiem = 'AM'
                else:
                    if hour > 12:
                        hour -= 12
                    meridiem = 'PM'

            # Prints the hours [HH:MM AM/PM]
                #print('\n%i:00 %s' % (hour, meridiem))

            # Temperature is measured in Kelvin
                temperature = item['main']['temp']

            # Weather condition
                description = item['weather'][0]['description'],

            # Prints the description as well as the temperature in Celcius and Farenheit
                #print('Weather condition: %s' % description)
                #print('Celcius: {:.2f}'.format(temperature - 273.15))
                #print('Farenheit: %.2f' % (temperature * 9/5 - 459.67))
                b=description
                d=[]
                for a in range(0,len(b)):
                    c+="today's climate"+" : "+b[a]+"\ntemperature is {:.1f}".format(temperature - 273.15)
                    d.append(c)
                #print(c);
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=8939632343"
                headers = {
                'authorization':"Wbc2KH0nkwFvwkAlnGJiuwHUcAU83Qw7YvR9fhpWhQFqiY786XB7xYh6ZkCE",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
                #response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=8939632343".format(c), headers=headers)
                #print(response.text)

            elif(flag==9):
            # Time of the weather data received, partitioned into 3 hour blocks
                time = item['dt_txt']

            # Split the time into date and hour [2018-04-15 06:00:00]
                next_date, hour = time.split(' ')

            # Stores the current date and prints it once
                if current_date != next_date:
                    current_date = next_date
                    year, month, day = current_date.split('-')
                    date = {'y': year, 'm': month, 'd': day}
                    #print('\n{m}/{d}/{y}'.format(**date))

            # Grabs the first 2 integers from our HH:MM:SS string to get the hours
                hour = int(hour[:2])

            # Sets the AM (ante meridiem) or PM (post meridiem) period
                if hour < 12:
                    if hour == 0:
                        hour = 12
                    meridiem = 'AM'
                else:
                    if hour > 12:
                        hour -= 12
                    meridiem = 'PM'

            # Prints the hours [HH:MM AM/PM]
                #print('\n%i:00 %s' % (hour, meridiem))

            # Temperature is measured in Kelvin
                temperature = item['main']['temp']

            # Weather condition
                description = item['weather'][0]['description'],

            # Prints the description as well as the temperature in Celcius and Farenheit
                #print('Weather condition: %s' % description)
                #print('Celcius: {:.2f}'.format(temperature - 273.15))
                #print('Farenheit: %.2f' % (temperature * 9/5 - 459.67))
                b=description
                c=""
                for a in range(0,len(b)):
                    c+="\n"+"tomorrow's climate"+" : "+b[a]+"\ntemperature is {:.1f}".format(temperature - 273.15)
                    d.append(c)
                #print(c);
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=8939632343"
                headers = {
                'authorization':"Wbc2KH0nkwFvwkAlnGJiuwHUcAU83Qw7YvR9fhpWhQFqiY786XB7xYh6ZkCE",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
                #print(d)
                #response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=8939632343".format(c), headers=headers)
                #print(response.text)
            elif flag>11:
                break
        # Prints a calendar of the current month
           # "'calendar = calendar.month(int(year), int(month))'"
           # "'print('\n'+ calendar)'"

            #response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=8939632343".format(b), headers=headers)
        # Asks the user if he/she wants to exit
        response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=8939632343".format(c), headers=headers)
        return render_template("show_weather.html", data=d)


@app.route('/login')
def my_form2():
    return render_template('show_login.html')

@app.route('/login', methods=['POST'])
def my_form_post2():
    phoneno = request.form['text']
    password  = request.form['text1']
    ans=[]
    ans.append("you have logged in")
    return render_template("show_login.html",data=ans)


@app.route('/signup')
def my_form1():
    return render_template('show_signup.html')

@app.route('/signup', methods=['POST'])
def my_form_post1():
    name = request.form['text']
    age  = request.form['text1']
    phoneno = request.form['text2']
    password = request.form['text3']
    ans=[]
    ans.append("The details have been submitted to the database")
    return render_template("show_signup.html",data=ans)

@app.route('/loans')
def my_form():
    return render_template('show_loans.html')

@app.route('/loans', methods=['POST'])
def my_form_post():
    pr = request.form['text']
    p=int(pr)
    ra = request.form['text1']
    r=int(ra)
    print(r)
    ti = request.form['text2']
    t=int(ti)
    org = request.form['text3']
    ans=[]
    ans.append(org)
    ans.append(int(p * (pow((1 + r/ 100), t))/(t*12)))
    ans.append(p)
    ans.append(r)
    ans.append(t*12)
    return render_template('show_loans.html',data =ans)

app.secret_key=('hello')
@app.route('/tweets')
def tweets():
    consumer_key="5tlYTpVNtcxNR1tmPTcgMBC0j"
    consumer_secret="wVEX9My3v6340sHINjsJ2LVj6lmxxWPuo6KgALIMkUhlTu5lH4"
    access_token="1002549079774093313-fCET9YfrjgVJLe1gZy1n8O4mnArToO"
    access_token_secret="gNNGpKh7GBsQZYaguflQX5QXFSCER4mKyp5IVdOMcVKvE"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    if (api):
        print("Login Success")
    else:
        print("Failed")
    id_list=[1246396473983434752] #add the id's of twitter pages you want to get here. I randomly used trump and biden here.
    individual_tweet_list=[]  # the tweets of 1 particular ID or page is stored here and replaced
    # the tweets of 1 particular ID or page is stored here and replaced
    final_tweet_list=[]
    for i in range(len(id_list)):
        new_tweets=[]
        new_tweets = api.user_timeline(id= id_list[i],count=5,tweet_mode='extended') #count tell the number of most recent tweets you want
        for tweet in new_tweets:
            text=tweet.full_text.encode('utf-8')
            text = re.sub(r':', '', text)
            text = re.sub(r'[^\x00-\x7F]+',' ', text)
            final_tweet_list.append(text) # This is the final answer. It is a 2D list. First row contains the tweets of first user
        return render_template("show_tweets.html", data=final_tweet_list)


@app.route('/pesticide')
def Pesticide():
    answer=['banana','mustard']
    # answer=ans
    r=answer[0]
    b=""
    for ele in r:
       b+=ele

    c=""
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=8939632343"
    headers = {
    'authorization':"Wbc2KH0nkwFvwkAlnGJiuwHUcAU83Qw7YvR9fhpWhQFqiY786XB7xYh6ZkCE",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    if 'banana' in b:
        c+="the best pesticide for banana is : "+"Furadan 36(carbofuran)\n"
    #print(response.text)
    if 'coconut' in b:
        c+="the best pesticide for coconut is : "+"Monocrown(Monocrotophos)\n"
    if 'cotton' in b:
        c+="the best pesticide for cotton is : "+"Starthene(Acephate)\n"
    if 'garlic' in b:
        c+="the best pesticide for garlic is : "+"Hyquin(Quinalphos)\n"
    if 'gram' in b:
        c+="the best pesticide for gram is : "+"Suquin(Quinalphos)\n"
    if 'groundnut' in b:
        c+="the best pesticide for groundnut is : "+"Excaliber(Lamba cyhalothrin)\n"
    if 'maize' in b:
        c+="the best pesticide for maize is : "+"Metasystox-R(Oxydemeton methyl)\n"
    if 'mustard' in b:
        c+="the best pesticide for mustard is : "+"Thimet(Phorate)\n"
    if 'onion' in b:
        c+="the best pesticide for onion is : "+"Temidor Ceasefire(Fipronil)\n"
    if 'potato' in b:
        c+="the best pesticide for potato is : "+"Centric(Thiamethoxam)\n"
    if 'ragi' in b:
        c+="the best pesticide for ragi is : "+"Ridomil(Metalaxyl)\n"
    if 'rice' in b:
        c+="the best pesticide for rice is : "+"Marshal(Carbosurfan)\n"
    if 'sorghum' in b:
        c+="the best pesticide for sorghum is : "+"Cythion(Malathion)\n"
    if 'sugarcane' in b:
        c+="the best pesticide for sugarcane is : "+"Confidor 200 S.L(Imidachloprid)\n"
    if 'sunflower' in b:
        c+="the best pesticide for sunflower is : "+"Centric(Thiamethoxam)\n"
    if 'Turmeric' in b:
        c+="the best pesticide for turmeric is : "+"Aframe(Azoxystrobin and Difenoconazole\n"
    response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=8939632343".format(c), headers=headers)
    return render_template("show_pesticide.html", data=c)
if __name__ == '__main__':
    app.run(debug=True)

