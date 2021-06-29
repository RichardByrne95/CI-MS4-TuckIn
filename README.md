# TuckIn - Dublin

If code was directly copied and pasted from another source and left unchanged, then the link to the source will be above that code. However, if a source was referenced but significantly customised to the projects needs, then the link above the code will be preceded by 'Referenced...'.

### Food Images Source

#### Background Images

-   Homepage - https://unsplash.com/photos/JplMVRjzQVU

#### Ezio Pizza

Bufalina Pizza - Ezio Pizza = https://unsplash.com/photos/exSEmuA7R7k

#### McDoogle's

Quarter Kilo - https://www.pexels.com/photo/ham-and-bacon-burger-2983098/

#### Tomato King

-   MASSIVE Burger - https://www.pexels.com/photo/photo-of-burger-beside-fires-3616956/
-   MightyMeaty - https://www.pexels.com/photo/person-holding-a-double-patty-cheese-burger-3826273/
-   MiniMeaty - https://www.pexels.com/photo/close-up-photo-of-a-cheeseburger-1556698/
-   MiniMeaty Meal - https://www.pexels.com/photo/tomato-burger-and-fried-fries-1600727/
-   Cheez Burger - https://www.pexels.com/photo/close-up-photo-of-hamburger-1893557/
-   Classic Hamburger - https://www.pexels.com/photo/photo-of-burger-and-fries-3219547/
-   Classic Hamburger Meal - https://www.pexels.com/photo/plate-of-fries-and-burger-3219483/
-   Crispy Chicken Burger - https://www.pexels.com/photo/bread-food-dinner-lunch-6896379/
-   Classic Chicken Burger - https://www.pexels.com/photo/bread-food-dinner-lunch-7963144/
-   Bean Burger - https://www.pexels.com/photo/close-up-photo-of-burger-1639562/
-   Classic Chips - https://www.pexels.com/photo/fries-on-brown-table-2271110/
-   Onion Rings - https://pixabay.com/photos/food-restaurant-cafe-dining-dinner-3669928/
-   Fanta - https://pixabay.com/photos/aluminum-can-coca-cola-cylinder-87987/
-   Pepsi - https://pixabay.com/photos/pepsi-can-soda-cola-supermarket-5152332/

### Logo Images Sources

Tomato King logo was sourced from [Deviant Art](https://www.deviantart.com/greateronion/art/TomatoKing-163647925).
McDoogle's logo was created by the developer using [freelogodesign.org](https://www.freelogodesign.org/).
Ezio Pizza's logo was created by the developer using [freelogodesign.org](https://www.freelogodesign.org/).

### Django Secret Key Exposure

When starting off this project, I followed along with the course lectures to ensure that I had the project set up properly. In the course lecturers, however, the lecturer uploads the Django secret key to GitHub. I also did the same before realising what had happened. After contacting Student Care, they confirmed that removing 'settings.py' from GitHub in future commits and changing the Django secret key would be sufficient so as to not incur any penalties during grading.


### Google Maps Places API Autocomplete Limitations

While implementing the Autocomplete feature from Google's Maps API, I discovered that while you could restrict results to a specific country or between a set of co-ordinates, Google would [not allow you to restrict results to a specific city](https://issuetracker.google.com/issues/35822067). As a workaround, I tried using two pairs of co-ordinates that surrounded the entire county of Dublin. However, this proved unworkable as, firstly, since Dublin's boundaries do not form a quadrilateral, the co-ordinates that would create the boundary would include places outside of Dublin. Secondly, when setting a strict boundary in the Places API, you are restricted only to road and area names, with no house addresses being being selectable.

The most effective solution to this is to use a combination of Google's Maps APIs (Places, GeoCoding, Geolocation, Distance Matrix) in conjunction with one another to convert a given co-ordinate into standard address format, and to then to use the aforementioned services to check if that address is within Dublin. This method would provide extra validation of the inputted address through cross-checking it through multiple different Google services, leading to higher accuracy, better results and tighter security. If this were a commercial project, this would be the way in which I would solve this problem. However, as this is a college project and using these APIs together could easily incur hefty monthly costs, I chose to use the free Google Maps Places API as well as native form validation via HTML. The word 'Dublin' was also placed into 3 different places on the homepage (including the website logo) so that users would know before typing that the service is restricted to Dublin. 

The 'findPlaceFromQuery' method was used to find a place within the Google Maps Places' database using the selected autocomplete address. Then, if the address contained the string 'Dublin' or 'Baile Átha Cliath' (for Irish-speaking users), the form can be submitted. Otherwise, the submit button becomes disabled and an error message displays informing the user of the corrective action. While this method is more simple than the ideal method, it is effective and appropriate for the use case of this college project.

Biases were also used in the API settings, so that the API would search within Dublin first, but it ultimately searches all counties of Ireland if not enough results are found within Dublin.

### Django Math Filters

In order use multiplication and division in the Django templating language (without the result returning a rounded integer), [Django Math Filters](https://pypi.org/project/django-mathfilters/) was installed to allow this functionality. Specifically, it was required for the creation of the star ratings underneath each restaurant card in 'restaurants.html'.

### Custom Django Template Filters

Custom template filters were written to aid in the creation and rendering of the star rating system for restaurants.

Django's built in "json_script" template tag was used to [prevent code injection](https://adamj.eu/tech/2020/02/18/safely-including-data-for-javascript-in-a-django-template/) via some of Django's vulnerabilities.

### Delivery Time Timezone Issues

Upon starting the project, the 'TIME_ZONE' property in 'settings.py' was set to 'Europe/Dublin' to reflect the localised nature of the service. Each datetime object was also given the same time zone to make it an 'aware' datetime object. 

However, it was discovered upon saving an order after submission, that the 'Europe/Dublin' timezone was being interpreted as '+0025' instead of '+0100'. This was later found out to be caused by the datetime objects ['not working' with pytz](http://pytz.sourceforge.net/#localized-times-and-date-arithmetic) for many time zones. As such, the project and all datetime objects were reverted to UTC via Django's 'timezone.utc' class.

## Deployment

This project was deployed using Heroku and AWS, with a postgres database, via the following steps:

### Heroku Deployment

1.  A new app was created on Heroku for the project, with the region set as Europe.
2.  Once the app was created, the Heroku Postgres addon was installed in the Heroku resources tab.
3.  A backup of the database was created in a file called 'db.json' using the command 'python -m django dumpdata exclude auth.permission --exclude contenttypes > db.json' (this allows the database to be imported into the new Postgres database).
4.  dj_database_url was installed using pip in order to direct the database url to Heroku.
5.  psychopg2-binary was also installed using pip to facilitate the adaptation of the Postgres database by this Python application.
6.  dj_database_url was imported into the project's 'settings.py' and the default 'DATABASES' variable was replaced with "{'default': dj_database_url.parse()}".
7.  The Config Vars were revealed in the Heroku app's Settings tab and the database url was copied and pasted as a string into the brackets of the parse method from the previous step.
8.  The command 'python -m django loaddata db.json' was then used to load the database backup created in step 3 into the new Postgres database.
9.  As a new database was now being used, the project's migrations needed to be applied by using 'python manage.py migrate'.
10. An if statement was added to settings.py so that the application could detect whether it should be using the hosted database or the local development database.
11. Gunicorn was then installed via pip which acts as the webserver in this project.
12. A Procfile was created in the project's root in order to tell Heroku to create a web dyno and run Gunicorn to server our Django app.
13. 'heroku login' was used to login into the Heroku CLI.
14. In order to temporarily prevent Heroku from collecting the static files upon deployment, the command 'heroku config:set DISABLE_COLLECTSTATIC=1 --app=APP_NAME' was used.
15. The Heroku app hostname was added to ALLOWED_HOSTS in settings.py as 'HEROKU-APP-NAME.herokuapp.com'. 'localhost' and '127.0.0.1' were also added for local development.
16. A Heroku git remote was initialised using 'heroku git:remote -a HEROKU_APP_NAME'.
17. The project was then deployed to the Heroku master via 'git push heroku main'.
18. The application was set up to automatically deploy from GitHub via Heroku's deployment settings.
18. In settings.py, 'DEBUG' was set to be true only if an environment variable called 'DEVELOPMENT' was present.

### AWS S3 Bucket Setup

1.  A new AWS S3 bucket was created with the same name as the Heroku app for this application.
2.  During setup of the bucket, 'Block all public access' was disabled in order to allow users to access the static files.
3.  'Static website hosting' was enabled for the bucket via the bucket's properties, and 'Host a static website' was chosen with document values set as 'index.html' and 'error.html' respectively.
4.  Under the bucket's permissions, a JSON 'CORS' configuration was added to set up the required access between the Heroku app and the S3 bucket.
5.  A bucket policy was generated using the policy generator. The 'Principal' field was set to allow all principles using '*', and the action was set to 'Get object'. The ARN (Amazon Resource Number) was then copied from the bucket policy page and pasted into the policy generator. 
6.  Once generated, the policy was pasted into the policy editor. The 'Resource' key of the policy was edited by adding '/*' to the end of the ARN to allow access to all resources in this bucket.
7.  The Access Control List was edited to allow public access to 'List' the objects in the bucket.

### AWS Group and User Access Setup

1.  Next, a new group was created in IAM (Identity and Access Management) called 'manage-HEROKU-APP-NAME'.
2.  Once created, a new Access management policy was created from the Policies section in IAM, by importing the 'AmazonS3FullAccess' policy.
3. The policy's 'Resource' key was changed to a list containing two strings, one being the S3 bucket's ARN, and the other being the ARN with '/*' at the end. This allows access to both the bucket and the content of the bucket.
4. The policy was named 'HEROKU-APP-NAME-policy' and a brief description of the policy was added.
5. The policy was then attached to the group created a few steps ago.
6. Lastly, a user was created called 'HEROKU-APP-NAME-staticfiles-user', programmatic access was given, and then user was then added to the group.
7. Once the user was created, the .csv file was downloaded that contained the user's Access key and Secret Access key.

### Connecting Django to AWS

1.  'boto3' and 'django-storages' were installed using pip, and 'storages' was added to the project's installed apps.
2.  'USE_AWS' environment variable was added to Heroku, and if statement was added so that if it existed, the following variables were assigned:
    -   AWS_STORAGE_BUCKET_NAME = 'S3_BUCKET_NAME'
    -   AWS_S3_REGION_NAME = 'eu-west-1'
    -   AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    -   AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
3.  The relevant variables and values from the last step were added to Heroku, and the 'DISABLE_COLLECTSTATIC' variable was removed to allow Django to collect our static files and upload them to S3.
4.  In order to tell Django where our static files will be coming from in production, another variable was added in settings.py called 'AWS_S3_CUSTOM_DOMAIN' with a value of 'BUCKET-NAME.s3.amazonaws.com'.
5.  Next, in order to tell Django that we want to use S3 to store the static files whenever 'collectstatic' is run, a new file at the root level called 'custom_storages.py' was created.
6.  Inside this file, 'settings' was imported from 'django.conf' and 'S3Boto3Storage' was imported from 'storages.backends.s3boto3'.
7.  Then a StaticStorage class was created, which inherited the 'S3Boto3Storage' class. A 'location' property was added with a value of 'settings.STATICFILES_LOCATION'. A copy of this class was then pasted below and its names adjusted for the media storage.
8.  Back in settings.py the following variables and relevant values were created and assigned:
    -   STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    -   STATICFILES_LOCATION = 'static'
    -   DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    -   MEDIAFILES_LOCATION = 'media'
9.  In order to override and explicitly set the urls for static and media files, the following variables were created in settings.py:
    -   STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}'
    -   MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}'
10. A cache control section was added to 'setting.py' in order to improve performance for users by caching static files for a long time. This was done by addin the following variable:
    -   AWS_S3_OBJECT_PARAMETERS = {
            'Expires': 'Thu 31 Dec 2099 20:00:00 GMT',
            'CacheControl': 'max-age=94608000',
        }
11. In order to add media files to S3, a new folder was created in the S3 bucket called 'media' and the media files were uploaded to it.

## Roadmap

-   Use restaurant names instead of id numbers in restaurant url.
-   Allow users to change their email addresses
-   Ability to add multiple addresses to one account.
-   Add realtime updates of order status (cooking/on it's way etc.) to order confirmation page.
-   Add ability to add a note to the overall order for the restaurant.
-   Add ability to edit notes/additional details
-   Add flexible minimum order amount
-   Add restaurant accounts so that they can manage their inventory.
-   Allow restaurants delivery and collection times to be separate
-   Allow restaurant to have delivery intervals other that 15 minutes (done via adding delivery_interval option to model and setting interval to self.delivery_interval in class' functions)
-   Allow restaurant opening times to span over 2 days e.g. 13:00 - 02:00
-   Implement flexible minimum time before first available delivery slot as different restaurants prepare food at different speeds, and have different delivery schedules
-   Allow customers to pre-order with a restaurant if it's not open today
-   Add prompt to remove everything from order when food from another restaurant is in the bag
-   Allow the user to store a bag for each restaurant
-   Add choices to food modal e.g. select toppings
-   Add ability for restaurants to issue discount codes
-   Show previous orders on homepage for easy re-ordering.




Why underscores were used in html files instead of hyphens

Timezone for person marking this project. Some restaurants may not be open depending on what time of day the examiner is grading this project. Time is set to Dublin time.

After completing circa 75% of the project, I received feedback regarding my previous project stating that it would be useful to include more detail in my commit messages. I integrated this feedback into this project as soon as I received it by increasing the frequency at which I made commits. This allowed for lower-level and less-crucial functionality and changes to be documented.

For users, the user field was named 'customer' instead of 'user' to prevent confusion in the future, if user accounts for the restaurants themselves were to be set up to allow them to manage their menu.

Used https://webformatter.com/javascript for JavaScript formatting

Phone number purposely excluded from restaurant menu to encourage the user to order through tuckin. Phone number is provided on order confirmation page.

Used https://www.cookiepolicygenerator.com/ to generate cookie and privacy policies.
Cookies image - https://www.pexels.com/photo/cookies-on-square-white-ceramic-plate-890577/
Privacy Image - https://www.pexels.com/photo/camera-cctv-control-monitoring-274895/

Footer was removed from bag and checkout pages so as to minimise potential distractions that could prevent the user from completing an order.

f-strings were replaced with the .format method for Stripe's webhook handlers, as 500 errors were frequently occurring when using f-strings. Stripe also us the .format method in their example code in the [Stripe Docs](https://stripe.com/docs/webhooks/build).

The 'payment_intent.succeeded' webhook from Stripe kept failing due to being unable to get anything except the payment id from the intent (an Attribute error kept occurring, Stripe support recommended removing the code causing the issue). As each payment intent is unique, the decision was made to simply use the payment intent to search for the order in the webhook handler.

While jQuery was used for most of the JavaScript in the project, it was not used for the implementation of Google Autocomplete, in order to stick to Google's recommended practices.