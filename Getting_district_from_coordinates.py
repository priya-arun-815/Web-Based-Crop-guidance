import geocoder
import reverse_geocoder as rg
import pprint


def reverseGeocode(coordinates):
    result = rg.search(coordinates) 
    # This prints the result district
    print(result[0]['name'])
 
# Driver function
if __name__=="__main__":
    g = geocoder.ip('me') #This line gets your address
    lat=g.latlng[0]
    long=g.latlng[1]
    coordinates =(lat,long)
    reverseGeocode(coordinates)  

