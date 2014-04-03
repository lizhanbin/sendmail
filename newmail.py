#-*-coding:utf-8 -*-

import Tkinter
import smtplib

from email.mime.text import MIMEText
from ConfigParser import ConfigParser
import os
import tkFileDialog
import re

class Window:
    def __init__(self, root):
        Host = Tkinter.Label(root, text = 'service')
        Port = Tkinter.Label(root, text = 'port')
        User = Tkinter.Label(root, text = 'username')
        Passwd = Tkinter.Label(root, text = '[passwd')
        Subject = Tkinter.Label(root, text = 'subject')
        To = Tkinter.Label(root, text = 'receiver')
        MailFile = Tkinter.Button(root, text = 'liulan', command = self.MailFile)

        Host.place(x = 5, y = 5)
        Port.place(x = 200, y =5)
        User.place(x = 5, y = 30)
        Passwd.place(x = 200, y = 30)
        Subject.place(x = 5, y = 55)
        To.place(x = 5, y = 83)
        MailFile.place(x = 345, y = 80)

        self.entryHost = Tkinter.Entry(root)
        self.entryUser = Tkinter.Entry(root)
        self.entryPasswd = Tkinter.Entry(root, show = '*')
        self.entryTo = Tkinter.Entry(root, width = 40)
        self.entryPort = Tkinter.Entry(root)
        self.entrySub = Tkinter.Entry(root)

        config = ConfigParser()
        config.read('smtp.conf')
        Host = config.get('setting', 'Host')
        Port = config.get('setting', 'Port')
        User = config.get('setting', 'User')
        passwd = config.get('setting', 'Passwd')

        self.entryHost.insert(Tkinter.END, Host)
        self.entryPort.insert(Tkinter.END, Port)
        self.entryUser.insert(Tkinter.END, User)
        self.entryPasswd.insert(Tkinter.END, Passwd)

        self.entryHost.place(x = 50, y = 50)
        self.entryPort.place(x = 235, y = 5)
        self.entryUser.place(x = 50, y = 30)
        self.entryPasswd.place(x = 235, y = 30)
        self.entryTo.place(x = 50, y = 83)
        self.entrySub.place(x = 50, y = 55)

        self.mailSend = Tkinter.Button(root, text = 'start to send', width = 20, command = self.MailSend)
        self.help = Tkinter.Button(root, text = 'help', command = self.Help)
        self.mailSend.place(x = 430, y = 20)
        self.save.place(x = 430, y = 60)
        self.help.place(x = 520, y = 60)

        self.text = Tkinter.Text(root)
        self.text.place(y = 120)
    def MailFile(self):
        r = tkFileDialog.askopenfilename(title = 'open file', filetypes = [('txt','*.txt')])
        if r:
            self.entryTo.delete(0, Tkinter.END)
            self.entryTo.insert(Tkinter,END, r)

    def MailSend(self):
        host = self.entryHost.get()
        port = self.entryPort.get()
        user = self.entryUser.get()
        pw   = self.entryPasswd.get()
        fromaddr = user
        subject = self.entrySub.get()
        text = self.text.get(1.0, Tkinter.END)

        mailfile = open(self.entryTo.get(), 'r')
        mailaddr = mailfile.read()

        mail = re.split(',', mailaddr)
        msg = MIMEText(text, _charset = 'utf-8')
        msg['From'] = fromaddr
        msg['Subject'] = subject
        smtp = smtplib.SMTP()
        smtp.connect(host, port)
        smtp.login(user, pw)

        for toaddr in mail:
            msg['To'] = toaddr
            smtp.sendmail(fromaddr, toaddr, msg.as_string())
        smtp.close()

    def SaveConfig(self):
        Host = self.entryHost.get()
        Port = self.entryPort.get()
        User = self.entryUser.get()
        Passwd = self.entryPasswd.get()

        config = ConfigParser()
        config.add_section('setting')
        config.set('setting', 'Host', Host)
        config.set('setting', 'Port', Port)
        config.set('setting', 'User', User)
        config.set('setting', 'Passwd', Passwd)
        config.write(open('smtp.config', 'w'))

    def Help(self):
        help_str = ""
        if(not os.path.isfile('smtp.config')):
            config = ConfigParser()
            config.add_section('setting')
            config.set('setting', 'Host', 'smtp.qq.com')
            config.set('setting', 'Port', '25')
            config.set('setting', 'User', '123456')
            config.set('setting', 'Passwd', '123456')
            config.write(open('smtp.conf', 'w'))

root = Tkinter.Tk()
root.title("send mail")
root.geometry('650x500')
window = Window(root)
root.mailoop()
