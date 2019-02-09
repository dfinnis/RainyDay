# rainyday

When planning a cycle trip for the day, I want to find out what the weather is going to be like.
However, to do this I have to look up the weather at multiple locations along my route,
and estimate when I will be where, inevitably this is inefficient and inaccurate.

I built an automated weather forcast for a specified route.
It returns the weather every hour at the location I'll be along the route, easy!

## Approach

Using API requests its possible to first find the latitude and longitude for a given origin and destination.
Then yournavigation.org returns the route and travel time between origin and destination.
The travel time informs how many hourly 'stops', and so weather forecast API requests, are necessary.
The location along the route each hour can be found, then finaly the weather on location at the correct time.

![image of correct output](./images/Paris-Rouen.png)

![image of correct output2](./images/Evreux-Paris.png)
<br />

I protected against invalid city names:

![image of Invalid city name](./images/Invalidcityname.png)

I protected against problems associated with cycling across bodies of water:

![image of Paris-Toronto](./images/Paris-Toronto,acrosssea.png)

I also protected against problems associated with cycling too far in a day:

![image of Paris-Dubai](./images/Paris-Dubai,toofar.png)

## Usage

python3 rainyday.py

Specify origin and destination as prompted.

FYI: There are only 50 API requests per day available.

Ride safe and stay dry!
