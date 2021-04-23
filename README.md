# TuckIn - Dublin

If code was directly copied and pasted from another source and left unchanged, then the link to the source will be above that code. However, if a source was referenced but customised to the projects needs, then the link above the code will be preceded by 'Referenced...'.

#### Food Images Source

Bufalina Pizza - Ezio Pizza = https://unsplash.com/photos/exSEmuA7R7k
https://www.kaggle.com/kmader/food41

#### Logo Images Sources

Tomato King logo was sourced from [Deviant Art](https://www.deviantart.com/greateronion/art/TomatoKing-163647925).
McDoogle's logo was created by the developer using [freelogodesign.org](https://www.freelogodesign.org/)

### Django Secret Key Exposure

When starting off this project, I followed along with the course lectures to ensure that I had the project set up properly. In the course lecturers, however, the lecturer uploads the Django secret key to GitHub. I also did the same before realising what had happened. After contacting Student Care, they confirmed that removing 'settings.py' from GitHub in future commits and changing the Django secret key would be sufficient so as to not incur any penalties during grading.


### Google Maps Places API Autocomplete Incomplete

While implementing the Autocomplete feature from Google's Maps API, I discovered that while you could restrict results to a specific country or between a set of co-ordinates, Google would [not allow you to restrict results to a specific city](https://issuetracker.google.com/issues/35822067). As a workaround, I tried using two pairs of co-ordinates that surrounded the entire county of Dublin. However, this proved unworkable as, firstly, since Dublin's boundaries do not form a quadrilateral, the co-ordinates that would create the boundary would include places outside of Dublin. Secondly, when setting a strict boundary in the Places API, you are restricted only to road and area names, with no house addresses being being selectable.

The most effective solution to this is to use a combination of Google's Maps APIs (Places, GeoCoding, Geolocation, Distance Matrix) in conjunction with one another to convert a given co-ordinate into standard address format, and to then check if that address is within Dublin. If this were a commercial project, this would be the way in which I would solve this problem. However, as this is a college project and using these APIs would incur hefty monthly costs, I chose to use the free Google Maps Places API and implement form validation via HTML, as well as inserting 'Dublin' into 3 different places on the homepage (including the website logo) so that users would know before typing that the service is restricted to Dublin. Biases were also used in the API settings, so that the API would search within Dublin first, but it ultimately searches all counties in Ireland if no results are found within Dublin.

### Django Math Filters

In order use multiplication and division in the Django templating language (without the result returning a rounded integer), [Django Math Filters](https://pypi.org/project/django-mathfilters/) was installed to allow this functionality. Specifically, it was required for the creation of the star ratings underneath each restaurant card in 'restaurants.html'.

### Custom Django Template Filters

Custom template filters were written to aid in the creation and rendering of the star rating system for restaurants.

Django's built in "|json_script" template tag was used to [prevent code injection](https://adamj.eu/tech/2020/02/18/safely-including-data-for-javascript-in-a-django-template/) via some of Django's vulnerabilities.

## Roadmap

-   Use restaurant names instead of id numbers in restaurant url.
-   Ability to add multiple addresses to one account.








Why underscores were used in html files instead of hyphens

Timezone for person marking this project. Some restaurants may not be open depending on what time of day the examiner is grading this project. Time is set to Dublin time.