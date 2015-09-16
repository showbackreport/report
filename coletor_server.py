#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setembro/2015

Servidor RPC para receber os dados do coletor e gravar no banco de dados

'''
import config
import syslog
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer
from datetime import datetime
   
   
   
def log_msg(msg,f,n):
  name="Trac_disk"
  # EMERG=0   Alert=1 CRIT=2 ERR=3 WARN=4 NOTICE =5  INFO=6 DEBUG=7  
  prior =  [syslog.LOG_EMERG,syslog.LOG_ALERT,syslog.LOG_CRIT,syslog.LOG_ERR,syslog.LOG_WARNING,syslog.LOG_NOTICE,syslog.LOG_INFO,syslog.LOG_DEBUG]  
  facil= [syslog.LOG_KERN, syslog.LOG_USER, syslog.LOG_MAIL, syslog.LOG_DAEMON, syslog.LOG_AUTH,
  syslog.LOG_LPR, syslog.LOG_NEWS, syslog.LOG_UUCP, syslog.LOG_CRON, syslog.LOG_SYSLOG, 
  syslog.LOG_LOCAL0, syslog.LOG_LOCAL1, syslog.LOG_LOCAL2,syslog.LOG_LOCAL3,syslog.LOG_LOCAL4,syslog.LOG_LOCAL5,syslog.LOG_LOCAL6,syslog.LOG_LOCAL7]  
  #syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL) 
  #print msg, "| " ,  name , prior[f], len(facil) , facil[n]
  syslog.openlog(name,prior[f],facil[n])
  syslog.syslog(prior[f],msg)
  syslog.closelog()

# syslog.LOG_ERR , syslog.LOG_LOCAL5 
log_pri = [3,15]
  
try:
	import MySQLdb
except:
	msg="ERRO: Sem suporte a mysql - MySQLdb"
	log_msg(msg,log_pri[0],log_pri[1])
	print msg
	sys.exit(1)

  
address = ('0.0.0.0', 56667)
server = SimpleXMLRPCServer(address)


dbhost = config.ConfigSectionMap("mysql")['dbhost']
dbuser = config.ConfigSectionMap("mysql")['dbuser']
dbpass = config.ConfigSectionMap("mysql")['dbpass']
dbbase = config.ConfigSectionMap("mysql")['dbbase']

agora=datetime.now()
  
# l130  
# ['mpath47 36000144000000010700b1c798bc6b905 107374182400.0'] 
# ['sdec 128:64 active ready - sdez 129:176 active ready - sdfy 131:64 active ready - sdgk 132:0 active ready'] 
#[] 
#[]

def valida_host(HOST):
	print HOST,
	con=MySQLdb.connect(dbhost,dbuser,dbpass)
	con.select_db(dbbase)

	query="""
		SELECT ativo  FROM  host_desc  WHERE host = '%s'
		""" % HOST
	#print query
	with con:
		cur = con.cursor()
	try:
		cur.execute(query)
		row=int(cur.rowcount)
		result = 0
	except:
		result = 1
	if int(row) == 0:  result = 1 
	con.close()
	print result
	return result

	
def remote_into(Linhas,N,host):
  dbtable = ['acct_uid','acct_cmd']
  con=MySQLdb.connect(dbhost,dbuser,dbpass)
  con.select_db(dbbase)
  b=len(Linhas)
  count=0
  with con:
    cur = con.cursor()
    for tulpas in Linhas:
         if N == 0 :
            a ="INSERT INTO %s VALUES ( '%s', %s , %s , %s  , %s , '%s' ) " %(dbtable[N],host,tulpas[0],tulpas[1],tulpas[2],tulpas[3],tulpas[4])
         if N == 1 :
            a ="INSERT INTO %s VALUES ( '%s', '%s' , %s , %s  , %s , %s , '%s')  " %(dbtable[N],host,tulpas[0],tulpas[1],tulpas[2],tulpas[3],tulpas[4],tulpas[5])
         try:
             cur.execute(a)
         except: 
            count+=1
          
  con.close()
  print "REMOTE INTO:",dbtable[N], b
  return b-count

def remote_local_users(Linhas,ghost):
  dbtable = "users"
  import MySQLdb
  #con=MySQLdb.connect(dbhost,dbuser,dbpass,dbbase)
  con=MySQLdb.connect(host=dbhost,user=dbuser,passwd=dbpass)
  con.select_db(dbbase)
  b=len(Linhas)
  count=0
  with con:
    cur = con.cursor()
    for tulpas in Linhas:
         tulpas=tulpas.split(",")
         # "(%s ,%s, %s, '%s' )" % (uid, gid , Username,"grupo")
         a ="INSERT INTO %s VALUES ( %s, %s , '%s' , '%s'  ) " %(dbtable,tulpas[0],tulpas[1],tulpas[2],tulpas[3])
         #print a
         try:
             cur.execute(a)
         except:
            count+=1
  con.close()
  print "LOCAL INTO",dbtable,b
  return b-count


  
  
	
def psacct_db(all):	
	return all
	



	
	
	
# registro das funções	
server.register_function(psacct_db)
server.register_function(valida_host)
server.register_function(remote_into)
server.register_function(remote_local_users)



####  start do servidor

if __name__ == '__main__':
    try:
        print "Server running on %s:%s" % address
        print "Use Ctrl-C to Exit"
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print "Exiting"
