# temp: to avoid ssl error
import urllib3
urllib3.disable_warnings()

import password_list
user = password_list.user
password = password_list.password

from O365 import Message
authenticiation = (user,password)
m = Message(auth=authenticiation)
m.setRecipients(user) ###
m.setSubject('test.')
m.setBody('test.')
m.sendMessage()
