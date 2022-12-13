### README.md 👋
# 6u4rd
[![Awesome Badges](https://img.shields.io/badge/badges-awesome-green.svg)](https://github.com/Xeroxxhah/6u4rd)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
![Contribution](https://img.shields.io/badge/Contributions-Welcome-<brightgreen>)
[![Active](http://img.shields.io/badge/Status-Active-green.svg)](https://github.com/Xeroxxhah)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![releases](https://img.shields.io/github/release/Xeroxxhah/6u4rd.svg)](https://github.com/Xeroxxhah/6u4rd/releases)

Your backdoor for your device. It is a simple utility when it is up and running; you get an email every hour with a unique link. You are presented with a hideous dashboard; you can control your device using this dashboard.

Don't ask me why i did it (._.).

# Installation & Usage:


# Follow these steps: 
- 1st: ```git clone https://github.com/Xeroxxhah/6u4rd.git```
- 2nd: ```cd 6u4rd```
- 3rd: ```pip install -r requirements.txt```
- 4th: ```Setup Dummy Account (Gmail)```
- 5th: ```Get ngrok token```
- 5th  ```python3 6u4rd.py```



### Get ngrok token
- Sign up for [ngrok](https://ngrok.com/).
- copy "ngrok config add-authtoken <token>"


### Setting up a Dummy email account
- Create a new dummy gmail account.
- Follow these steps: [App Password Guide](https://support.google.com/mail/answer/185833?hl=en)


### Setting up as Schedule Task
- Open Schedule Task.
- Create a Basic task.
- Name the task (6u4rd).
- On Trigger click on "when i log on".
- Action: Start a program.
- Browse for web.pyw script.
- check the properties check box.
- in properties check to run with highiest privs and also check the hidden check box.
- Under condition tab uncheck only AC power check box.
- Create another task for mailer.pyw with same settings.



### Usage
- Once downloaded and setup correctly you will receive receive a ngrok link to your mail from your dummy account.
- Open the link and press "visit site".
- you'll be presented with default apache page, press p or press ubuntu icon (for android) and a login field will appear.
- you can make is disappear by pressing h.
- Default password is ```pass```, but if you changed the password enter password.
- You'll be presented with an ugly dashboard.
- Enjoy...


### Features
- Shutdown your device
- Lock your device 
- Take screenshot
- Channge password ofyour device
- webshell
- geo information
- More features coming

### Bug report
Found any bug!
Report it to me at xeroxxhah@pm.me
or open an [issue](https://github.com/Xeroxxhah/6u4rd/issues)

### TODO:
Add more features.

### Contributions:
All contributions are welcomed.fork this repo,improve it and [pull requests](https://github.com/Xeroxxhah/6u4rd/pulls)
### License
Distributed under GPLV3.0
