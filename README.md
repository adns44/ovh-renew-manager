# OVH renew manager

## Purpose of this program

You can manage your services renewal on OVHcloud with this cript.

Motivation was that some of the addons of my services with autorenew was stick in manual state and the provider sent me renewal warnings. [Issue described on LET](https://lowendtalk.com/discussion/191096/how-to-fix-ovhs-broken-renewal-system-since-they-don-t-give-a-shit#latest). However it is hard to find which addons stuck in manual state so this script helps you to set same state on the server and the corresponding addons.

## Usage

Download or clone the repo, and CD into the directory.

Install Python3 on your system.

Install the requirements with
```
python3 -m pip install -r requirements.txt
```

Set up API access. Go to [this link](https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*) and optain data. Set the proper expiration. As it is an one-time run script, it might be a good idea to set a short expiration period.

Copy the data out and create an `.env` file (yes, the filename is this, starts with a period and env and hidden).
Fill the file out
```
OVH_ENDPOINT='ovh-eu'
OVH_APPLICATION_KEY='XXX'
OVH_APPLICATION_SECRET='XXX'
OVH_CONSUMER_KEY='XXX'
```

> Change endpoint if neccessary.

If done run the script.
```
python3 set-renew.py
```

And follow on-screen instructions.

## Remakrs

No responsibility taken, use at your own risk!

OVHcloud, OVH API, OVH services and other related stuff are part of OVHcloud.

The project based on [OVHcloud Python wrapper](https://github.com/ovh/python-ovh).