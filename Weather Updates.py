import requests
import calendar

#api key must got from the website
api_key = 'YOUR KEY'
#api for getting weather description
api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

running = True
flag=0
red=0
c=" "

while running and red==0:

    # Enter city name
    while True:
        
            # Proves that input is valid
            red+=1
            city = input('Please input the city name: ')
            if city.lower() == 'sf':
                city = 'San Francisco, US'
           
                # Name of city is used for api
            api_call += '&q=' + city
            break
               
           
   
    # Stores the Json response
    json_data = requests.get(api_call).json()

    location_data = {
        'city': json_data['city']['name'],
        'country': json_data['city']['country']
    }

    print('\n{city}, {country}'.format(**location_data))

    # The current date we are iterating through
    current_date = ''
    flag=0
    # Iterates through the array of dictionaries named list in json_data
    for item in json_data['list'] :
        flag+=1
        if(flag==1):
        # Time separated into 3 hours
            time = item['dt_txt']
   
        # Split time into date and hour 
            next_date, hour = time.split(' ')
       
        # Stores and prints the date
            if current_date != next_date:
                current_date = next_date
                year, month, day = current_date.split('-')
                date = {'y': year, 'm': month, 'd': day}
                print('\n{m}/{d}/{y}'.format(**date))
       
        # Slicing is done to get HH:MM:SS format 
            hour = int(hour[:2])

        # Decides AM or PM 
            if hour < 12:
                if hour == 0:
                    hour = 12
                meridiem = 'AM'
            else:
                if hour > 12:
                    hour -= 12
                meridiem = 'PM'

        # Prints the time
            print('\n%i:00 %s' % (hour, meridiem))

        # Temperature in Kelvin
            temperature = item['main']['temp']

        # Weather condition or description
            description = item['weather'][0]['description'],

        # Prints the whole information of temp in celsius and weather for today at 09:00
            print('Weather condition: %s' % description)
            print('Celcius: {:.2f}'.format(temperature - 273.15))
            print('Farenheit: %.2f' % (temperature * 9/5 - 459.67))
            b=description
           
            for a in range(0,len(b)):
                c+="TODAY'S climate"+"\n"+b[a]+"\ntemperature is {:.1f}".format(temperature - 273.15)
                #c is the string containing the description  
            #The api used for sending messages
            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=YOUR NUMBER" #Enter the number to which the message must be sent
            headers = {
            'authorization':"YOUR AUTHORIZATION",       #The authorization must be got from fast2sms website
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
            

        elif(flag==9):
        # Time separated into 3 hours
            time = item['dt_txt']
   
        # Split into date and hour
            next_date, hour = time.split(' ')
       
        # Stores and prints the date
            if current_date != next_date:
                current_date = next_date
                year, month, day = current_date.split('-')
                date = {'y': year, 'm': month, 'd': day}
                print('\n{m}/{d}/{y}'.format(**date))
       
        # Slicing is done to get HH:MM:SS format
            hour = int(hour[:2])

        # Decides AM or PM
            if hour < 12:
                if hour == 0:
                    hour = 12
                meridiem = 'AM'
            else:
                if hour > 12:
                    hour -= 12
                meridiem = 'PM'

        # Prints the time
            print('\n%i:00 %s' % (hour, meridiem))

        # Temperature in Kelvin
            temperature = item['main']['temp']

        # Weather condition or description
            description = item['weather'][0]['description'],

        # Prints the whole information of temp in celsius and weather for tomorrow at 09:00
            print('Weather condition: %s' % description)
            print('Celcius: {:.2f}'.format(temperature - 273.15))
            print('Farenheit: %.2f' % (temperature * 9/5 - 459.67))
            b=description
           
            for a in range(0,len(b)):
                c+="\n"+"TOMORROW'S climate"+"\n"+b[a]+"\ntemperature is {:.1f}".format(temperature - 273.15)
                #c is the string containing the description
            #the api used for sending messages
            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=FSTSMS&message=",b,"&language=english&route=p&numbers=YOUR NUMBER" #Enter the number to which the message must be sent
            headers = {
            'authorization':"YOUR AUTHORIZATION",   #The authorization must be got from fast2sms website
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }

        elif flag>11:
            break
#The message informing the weather description for two days is sent to the number in the position of YOUR NUMBER
        
response = requests.request("POST", url, data="sender_id=FSTSMS&message={}&language=english&route=p&numbers=YOUR NUMBER".format(c), headers=headers)
