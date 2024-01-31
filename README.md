# espn-fantasy-api-connector
program for connecting to the espn fantasy api and downloading relevant information

## installation
### create a .env file
In the root folder, create a file called `.env'.  This file stores secret information that you wouldn't want to share in a version control system like GitHub.
The .env file requires three fields so that the application can authenticate with the ESPN API. Your .env file should read:

```
ESPN_API_URL="https://fantasy.espn.com/apis/v3/games/ffl/seasons/<ENTER SEASON NUMBER HERE>/segments/0/leagues/<ENTER LEAGUE_ID HERE>"
swid="<your SWID Cookie>"
espn_s2=<your ESPN_S2 Cookie>  
```

#### ESPN_API_URL 
The URL is going to depend on your league number and season you want to specify. Your league number is in the url of your fantasy league when you use the espn website. When you are looking at your league in a browser it should have a parameter in the url that says `&leagueId=<your league id number>`

#### SWID & espn_s2 cookies
Follow the instructions at this [website](https://cran.r-project.org/web/packages/ffscrapr/vignettes/espn_authentication.html) for how to get the SWID and espn_s2 cookies for your authentication to the ESPN API.

### create a virtual environment
To create a clean working environment, from the command line at the root project folder, type in
`python -m venv venv`

Once you type that in, activating the virtual environment will depend on whether you are using a mac/unix or windows machine:
For mac/unix, type: `source .venv/bin/activate`
For windows, type: `.venv\Scripts\activate.bat`

You should now see a `(venv)` in your command line to the left of your prompt`

### install packages from requirements.txt file
To install the packages this application needs to run into our new, clean virtual environment, type:
`pip install -r requirements.txt`

## running the program
Once you are set up, you can run the program. Type `python main.py` at the root directory in the command line.  
The program will likely run very quickly and you should now see an output .csv file in the `./output` folder!
