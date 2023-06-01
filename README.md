#Cs50 Astrology Project
##Video Demo: https://drive.google.com/file/d/1yvmfVGhzfesEMDSX_JgzdFDfw01DuY85/view?usp=drivesdk

##Description


##Introduction
Astrology is a subject that initially caught my attention 3 years ago when I was going through an extremely dark period in life and a toxic relationship on the top. Suddenly, I met another girl and everything seemed absolutely perfect with her.(3 years down the linewe never even had a single arguement).
I considered astrology invalid, I was agnostic about it, but still leaned towards calling it a pseudoscience.
I just happened to check some readings of Indian vedic astrology about my relationships and bad periods and guess what it was perfectly
predicted that my relationship with my ex is'nt sustainable and that we will exhaust eachother.
It also predicted my current relationship to be absolotely perfect with a score of 36/36. It perfectly said about my bad phase, I remember the starting lines "this will be the dark period of your life...." and I became a fan.
Later I saw some expert astrologers predict Donal Trump's win in 2016 despite the polls and they challeneged that something will turn the tide in the the end, I have seen astrologers perfectly predict coronavirus outbreak 3 months in advanced, Donald Trump's 2020 change of job and residence and loss of election and much more.
Since then, I have been living and breathing astrology every minute of my living life, my new major startup is based on astrology and I have also planned some researches to verify it on a scientific level.
So naturally, my cs50 project would be based on astrology and I have created an astrology website to end this course with full satisfaction.

##Database setup
I saw various methods to create sqlite databases. I downloaded an SQL background on my desktop and tried to link it with my VS code, I saw methods like SqlAlchemy but I had to concede that Cs50 database was the best and the most efficient. So I transfered all my work to cs50 VS code and later to old IDE.
I created the database using what I learnt in the last lecture of the flask when I tried practicing creating Froshims of Prof. David Malan. My database astro.db contains a table called users where all the registrants are stored along with their hashed passwords.

##Register route
I created "register.html" linked to "/register" route on the controller. GET route renders the register template. "SignUp" link on the login page is linked to the GET route of the /register route.
In register.html you need to enter the email as your username, password and then confirm the password for security. Username is of type email and will not accept non email formats and password will be hidden with dots since it's set to the type password.
POST route will first verify if you have entered the username, password, if you have confirmed the password and if the passwords and confirmed passwords match. If even one of conditions fail, an apolgy template is rendered with a message appropriate to the condition.
Once you have successfully registered successfuly, a success.html page will be rendered indicating you have been registered.
You will be sent an EMAIL CONFIRMATION of your registration. For email part, I tried to use the setup taught in Cs50, but it didn't work, so I saw many youtube tutorials and one with smtp database was the easiest and the most appealing. I also read some documentation on it and created the code in the POST route. I linked the app email with my gmail account and due to change in google's policy for unsecured apps, I created a seperate app password for the account which can only be accessed by this app.
Then your username will be stored in database along with your hashed password. For hashing, I took the reference from Cs50 Finance assignment and did it by importing werkzeug.

##Login route
Once you have registered successfully you will have to login. I practiced creating login routes multiple times using reference from cs50 finance. However I couldn't wrap my head around @login required function of cs50. So, i just manually added the lines "if not session.get("name"): return redirect("/login")" above every appropriate route that would direct the user to the internal tempplates. So if you enter /api or /advanced in the url without logging in, you will be redirected to the login page. I know this is not a perfect coding practice, but thats what my level of expertise allows right now.
GET route of the login page renders the login template. Once the information is entered in the form and submitted, it goes through the POST route.
In the POST route, for precaution, any session is cleared first, then the code verifies whether username and password have been entered. If not, you will be given an appropriate apology. Once this has been verified, system will check to see whether the user of the given name exists in the database using sqlite commands. Using the username provided in the form, we will extract a row from the sqlite database using SELECT function. If the length of the rows is not 1, means username doesn't exist. Len of rows cannot exceed 1 since that filter already has been added to the registered route.
Once the existence of the user is verified, we will have to user check_password_hash function imported from werkzeug since the password enetered by the user will not be in hash. Check_password_hash is designed to compare hashed and unhashed passwords.
If the passwords do not match, an apology is rendered. If they match, then a session is assigned to the user and the user is directed to the "/" route. Since session is not assigned, "/" route renders index.html.



##/ route
Once you login, you will be redirected to the  the index page. Index page contains some intro description to vedic astrology and a navbar with appropriate options. Main options are in the DROP DOWN menu.
Navbar has been imported from bootstrap. Drop down menu contains 3 options: One where you get readings of your nakshatra(sidereal constellation in which your moon was present at the time of your birth), second is where you will get some basic birth details, third where you get a detailed report of your vedic hororscope which is called kundli in Indian language.
I also wanted to add feature of downloading the template as a pdf and saw many online tutorials for the same by installing and importing pdfkit. But I found no way to import or install wkhtmltopdf which was additionally necessary for the code to work. So, I decided not to include that feature as of now.

##API setup
Given astrology required data related to position of planets and mathematical points in constellations, I had to use API to import some data and readings from external websites who provide the api service.
But I initially lacked any expertise in API which was not a part of cs50 course tutorials. By referring to finance helpers file of the cs50 staff, I got an initial idea but then i hired a tutor to teach me how to set it up.(Note: As a part of the academic honesty policy of the course, he didn't do my work, just taught me how to set it up).
He taught me to look at two things while setting up an API, end point and the parameters. After referring to various services, we found that prokerala.com provides the most accurate, convenient and detailed form of the API required by us.
I tested the API requests in my terminal which was returned in JSON format. prokerala.com provided two files, "client.py" which I wasn't supposed to touch and "test.py" had function run() with end points, to contact the API, import the data and store it. I was given this information by the prokerala staff. They also asked me to create another file which i named config.py where client ID and client secret are stored. This is imported in test.py as keys.
This was because they gave each account 5000 credits free every month and every API call would amount to 100 to 300 credits based on the size of data imported. Once free calls for the month were done, I had tp login with a new account, create new ID and secret key and use it in my app to avail free credits for testing on my app. So, having a seperate file for storing the ID and secret key is more convenient since it can be easily changed.
After posting the data to the terminal, my next challenge was to convert the json format API response to html format and display it in the template. After researching online, I came accross json2html function. I installed the json2html using pip install and used it to convert the API response to html format using the convert function of json2html. Once converted, I passed the data to birthdetails.html where the data is displayed in the html format.
Here the problem i came accross what that, when i would pass the data to birthdetails.html, it would display along with the table tags. I used to display the "message" passed with {{message}}. After researching a bit online, i got to know {{message | safe|}} would solve my problem where |safe ensures that the code is parsed.

##Personalized info display
For "Birth Details" and "Detailed Kundli info" options in the drop down menu, when we tested the API calls, test parameters were entered in the test.py file which remained constant. The biggest challenege in this project was at this point where I had to use the data entered by the user anc onver it into the format required by test.py file.
All 3 options in the dropdown menu render "details.html" through GET route where options of entering the birth details (year, month, day, time and place) are available. You may even set ayanamsha value that you would like. Ayanamsha is the astronomical precession of equinox where the constellations shift 1 degree backward every 72 years and complete a circle in 26,500 years. Since vedic astrology is based on constellations as opposed to western astrology which uses tropical zoodiac, Indian astrology uses the precession correection in every horoscope that's constructed.
I also had another challenge at this place whcih was to import the latitude, longitude and timezone of the birthplace entered by the user, and combine the timezone part with the datetime format which used the ISO8601 format.
These 4 lines of code where i converted the data to the required format, which i added in test.py provided by the api service took almost 2 wweeks of frustration and trials and errors.
For latitude and longitude part, I thought i might have to use the another API service, but most API services were either inefficient in documentation and demanded some form of payment. When i hired the tutor to show me how to import the API, he asked me to refer to "geonamescache" documentation and to import it. That was the best library which provided all sorts of info on the given place like latitude, longitude, population, timezone etc and with a stroke of luck i had come across the library which suited me most appropriately because no google search would point towards geonamescache. It's documentation too was fairly easy to test, took me a few days to wrap my head around it.

So, here I was in the middle of personalizing the results to the user by converting the parameters into variables.
path was initially not a variable, but i had 3 paths in my app and would have been impractical to create a seperate function for each path. So, after some research online on how to pass a string, i came3 accross a stack overflow thread on how to passs variables to the string. So after some testing I created a path variable in each of the 3 routes which stored the path to the endpoint required to generate the relevantg data and then in test.py I created a variable called url which had some string info of the url and also accepted the variable path imported from the controller using f"...{path}".
The result which imported and stored the api data already had a string of the path, but now i passed the url variable to it. This ensured, just one function would be able to call api for eevery route.

Coming to my biggest challenge of parameters, the parameters required by the run() function had to be in a particular format. So i had to create a seperate function below called coord(i randomly named it after coordinates since it also imported coordinates from geonamescache).
Function of coord was to import the data from geonamescache, users data from the controller and the path, convert the data into appropriate format and pass it to the run() function.
I imported the latitude, longitude and the timezone using geonamescache function. I tried to research a lot online about the task of splitting the date and time and combining those, but most online tutorials were about splitting columns. With some advice after asking around about the task, someone suggested me to check out the map function that usus split function to split the entered numbers.
using the same, i split the date at "-" and time at ":" into year, month, day, hours and minutes. This was done to pass them in the datetime function as variables to further use strftime function to format the datetime into required format.
finally, to combine it with timezone, I had to import pytz library acoording to the tutorial and then use timezone() function along with localize() in the documentation format to find the final_date_time.
Ideally they store the timezone value in a variable like east=timezone('Asia/Kolkata'). But here what went into timezone function itself was variable. this was imported from the timezone given by geonamescache.
Finally, inside the coord function, run function is called and where all the parameters are passed to the run function. run() function stores the data in result and returns the result.
This is again stored in another variable called result inside coord function.

In the controller, all 3 routes import the data from the user and call the coord function and coord function with the required parameters and coord function returns the data which is stored and converted from json to html.

##Nakshatra templates:
There was one more small challenge for me was to go beyond API and display something of our own too which i had planned from very start. Nakshatra means constellations. So I planned to access the name of the nakshatra from the api result, and access the names of created templates with the help of the name of the nakshatra in the API name.
So, i had to find a way to make render_template() function dynamic. So, using exact same method as used in passing the path variable in test.py file, i created another variable called templates and passed it to the render_template() which generated one of the 27 templates eachtime the api returns the nakshatra names in birth details end point.
Another, substantial challenge was to access the name of the nakshatra returned from the api calls. In /nakshatra route which is connected to "Your nakshatra readings" in the dropdown menu, i used the same path as that in /api which was to access the birth details.
When i researched onlin in found that accessing a particular piece of information in returned api json was a common problem and there were examples on how to extract the data from the json data. With some trial and errors, i was able to access the name of the nakshatra to pass  it into the templates variable to further pass it into the render_template() in /nakshatra route.

GET of the /nakshatra route is also connected to the details page and POST renders one of the 27 templates i created for each nakshatra.

The templates that i created had to have too much information content about the properties of the nakshatra which was impractical for me to write on my own. Being an astrology enthusiast, i knew that only some websites used original contant, rest 100s of others use common content.
So i got the astrology readings portion of the templates(which is not a part of the code) from the nakshatra descriptions of astrogle.com and ganeshaspeaks.com.
I used basic css to style each page either with a background image or background color.

#What i learnt
The amount of knowledge about computer science that i got from this course is invaluable, would be an insult to the course if i start describing it. But i learnt a value of being a programmer during my journey of completing the project and some last assignments. I learnt that no programmer can do everything from the top of the head as opposed to the other sciences. The better you are at efficiently breamking down task requirements and then researching the documentation related to to tasks, better a programmer you will become.
Thank you for providing this course for free to financially backward families like us as compared to US counterparts and thank you for such a an inavaluable experienc. Took me 1.5 years of on and off but consistent work to complete this course and I wanted to do this course since 2017 but suffered from mental health issues back then along wit priorities which made it impossible. Today as the time has come to finally submit this document, my feelings cannot be described in words. Thank you again,
Sincerely




















s