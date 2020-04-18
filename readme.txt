1. prerequisite: 
   1) install selenium:
   pip install selenium
   2) download chromedriver 
   https://chromedriver.storage.googleapis.com/index.html

   You need to match driver to the chrome browser version on your system.


2. run ./pangbot.py -h to get help, you can add additional parameters 
   if you want SMS notification.

3. When bot notices there is an slot, music will be played and bot will stop,
   go to the brower page immediately and secure the slot. After done, end bot.

4. The first run (and occasionally) amazon will ask you to fill captcha and 
   2-factor auth, just do it and restart the bot.
