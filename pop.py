#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lpavaneli - 2011

import  poplib, sys, traceback, argparse, imaplib

class IMAPCheck:

  def __init__(self, username, password, hostname, port, ssl):
    self.username = username
    self.password = password
    self.hostname = hostname
    self.port = port
    self.ssl = ssl

  def check(self):
    try:
      if self.ssl != None:
        M = imaplib.IMAP4(self.hostname,self.port)
      else:
        M = imaplib.IMAP4_SSL(self.hostname,self.port)
      M.login(self.username,self.password)
      Mails = M.select(mailbox='INBOX', readonly=False)
      print "OK: %s %s emails" % (Mails[0], Mails[1])

    except Exception, err:
      sys.stderr.write('ERROR: %s\n' % str(err))
    finally:
      try:
        M.quit()
      except:
        pass


class Pop3Check:

  def __init__(self, username, password, hostname, port, ssl):
    self.username = username
    self.password = password
    self.hostname = hostname
    self.port = port
    self.ssl = ssl

  def check(self):
    try:
      if self.ssl != None:
        M = poplib.POP3(self.hostname,self.port, 5)
      else:
        M = poplib.POP3_SSL(self.hostname,self.port)
      M.user(self.username)
      M.pass_(self.password)
      print "OK: %s [%s emails]" % (M.getwelcome(), len(M.list()[1]))

    except Exception, err:
      sys.stderr.write('ERROR: %s\n' % str(err))
    finally:
      try:
        M.quit()
      except:
        pass


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Check POP3 Auth',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('-u', '--username', nargs=1, dest='username', required=True, help='usage: username@domain')
  parser.add_argument('-p', '--password', nargs=1, dest='password', required=True, help='user password')
  parser.add_argument('-H', '--hostname', nargs=1, dest='hostname', required=True, help='host ip')
  parser.add_argument('-T', '--type', nargs=1, dest='type', required=True, choices=['imap','pop3'], help='check type imap/pop3')
  parser.add_argument('-P', '--port', type=int, nargs=1, dest='port', default=[110], help='port service')
  parser.add_argument('--ssl', type=int, nargs='?', dest='ssl', default=[0], help='enable ssl check')

  parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

  args = parser.parse_args()

  if args.type[0] == 'imap' and args.port[0] == 110:
    args.port[0] = 143
  if args.type[0] == 'imap':
    connect = IMAPCheck(args.username[0],args.password[0],args.hostname[0],args.port[0],args.ssl)
  else:
    #print (args.username[0],args.password[0],args.hostname[0],args.port[0],args.ssl)
    connect = Pop3Check(args.username[0],args.password[0],args.hostname[0],args.port[0],args.ssl)
  sys.exit(connect.check())
