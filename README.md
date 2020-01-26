# Alfred Plus Code

This is an [Alfred](https://www.alfredapp.com/) workflow to convert [Plus Codes](https://plus.codes/) to their corresponding Lat/Lng coordindates. 

Google claims Plus Codes are convertable to lat/lng offline, but this is only true for the long form of the Plus Codes (e.g. `9C3XGW4F+5V`). On Maps short Plus Codes are used to display places wich need an reference point (e.g. `GW4F+5V, London`). To convert this short code you need to lookup the lat/lng coordinates of `London` to determine the lat/lng coordinates of the Plus Code. For this you need some sort of (online) API, which will probably require a key.

This workflow converts the given short Plus Code into it's corresponding long form as well as the lat/lng coordinates.

It querries `https://plus.code` for this and needs to be online.

## Dependencies

- Chrome needs to be installed
- [ChromeDriver](https://chromedriver.chromium.org/) (path to executable need to be set in workflow settings) 
- Python 3.x (set path in Script filter)
- [Selenium](https://selenium-python.readthedocs.io/installation.html) (needs to be installed for the used Python environment!)