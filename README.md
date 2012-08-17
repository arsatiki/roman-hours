Roman Hours Bot
===============

This is a bot who tells the time according to Roman timekeeping.

Roman hours start from sunrise and end with sunset.
Both day and night are divided into 12 hours.
Unlike modern hours, their hours were longer during the summer and shorter during the winter.

The bot does not handle special cases very well, such as the sun not setting at all.
For example, it will break down in northern Finland.

Usage
-----

I am using the bot to provide the tweets of RomanHoursHKI.
If you'd like to do the same for your home town, follow these instructions.

Compile the bot with

    ./do.sh

Run it with

    ./sequence latitude longitude

Latitude is positive when going north and negative when going south.
Longitude is positive when going west and negative when going east.

You will need another tool to actually pipe the output into Twitter.
I use TTYtter.

(As an aside, I wrote this bot in C since I could not bear the idea of keeping a Python process running 24/7.
Then I attached my mean and lean C process into a Perl Twitter client...)


License
-------

Fully public domain, as long as my moral rights are respected.


Other people's work
-------------------

The photo of the Twitter bot is from http://www.freefoto.com/preview/11-22-1/Sun-Dial.

It is licensed via Creative Commons (http://creativecommons.org/licenses/by-nc-nd/3.0/)
