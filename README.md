This is our attempt at the SIH 2020 inter-college finals.

A simple webpage with the following features:

- A portal for the farmers to log in/signup.
- Predicts the soil contents based on the farmer's location.
- Suggests crops to the farmers based on the predicted soil contents and crop season.
- Suggests pesticides to the farmer based on the crop chosen.
- Sending weather updates to the farmer through SMS.
- A modest page for farmers to keep track of their loans.
- Scrapping tweets from agriculture-related Twitter accounts and displaying them on the webpage to ensure the farmer stays updated with agriculture-related news.

The web page was built with Flask and uses SQLite database to store the details of farmers and the list of pesticides. 'Website.py' consists of the code to run the website in localhost. The other python files uploaded serve to run the individual features of the website in a stand-alone manner. The datasets used ('soil.csv', 'monsoon.csv') are also uploaded.
