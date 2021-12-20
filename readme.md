# Twitch Raid Campaign Reward Claimer

This tool was hastily cobbled together during Rare's Sea of Thieves Festival of giving event in December, 2021. Rare ran a 72 hour stream event where they would sporatically raid or host Sea of Thieves streamers. If you tuned into one of these raided or hosted streams for 15 minutes, you could claim a drop reward.

This tool runs on python, and leverages the selenium browser automation and testing framework to tune into the appropriate twitch channel with the Microsoft Edge web browser. It then looks for raids or hosting changes on the select channel, and responds by watching the raided or hosted stream for 20 minutes before returning to the main stream. No personal data is saved.

This solution includes a browser extension, [Automatic Drops & Twitch Channel Points](https://chrome.google.com/webstore/detail/automatic-drops-twitch-ch/kfhgpagdjjoieckminnmigmpeclkdmjm/related?hl=en), that automatically claims earned twitch points and rewards. Definitely worth checking out if you use Twitch often!

## How To Run

1. [Install python](https://www.microsoft.com/store/productId/9P7QFQMJRFP7) if you haven't already.
2. [Download the source code zip file](https://github.com/Frosthaven/twitch-raid-campaign-reward-claimer/archive/refs/heads/main.zip) and extract it whereever you want.
3. Double click `run.bat` to start the automation. It will automatically install needed dependencies.
4. Wait for the login prompt on twitch to appear and then login.
5. That's it! Mute the tab if you want. You may not want to minimize it, though, in case twitch decides to stop counting watch time.

## Extra Customizations

If any other broadcaster runs a similar event in the future, you can open `index.py` in a text editor and alter the values below to your needs:

```py
# CONFIG ***********************************************************************
#*******************************************************************************

main_channel = 'https://twitch.tv/seaofthieves'
watch_time_minutes = 20
```

## Known Issues

-   Python is not my primary language, and this had to be done under the pressure of speed when the event launched. Bugs may occur, though the tool ran smoothly for this event.
-   Using msedgedriver under selenium, an edge taskbar entry will be pinned after use. It is safe to unpin this until a fix can be found.
