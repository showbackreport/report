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

def insert_mapper(host,path,wwnid,size):
	dbtable="mapper"
	con=MySQLdb.connect(dbhost,dbuser,dbpass)
	con.select_db(dbbase)
	query="""
	INSERT INTO %s VALUES ( NULL,'%s','%s','%s',%s,'%s')
	""" % (\
	dbtable,host,path,wwnid,size,agora)
	with con:
		cur = con.cursor()
		cur.execute(query)
		last=cur.lastrowid
	return last
'''
mysql> explain mapper;
+----------+---------------+------+-----+---------+----------------+
| Field    | Type          | Null | Key | Default | Extra          |
+----------+---------------+------+-----+---------+----------------+
| idmapper | int(11)       | NO   | PRI | NULL    | auto_increment |
| host     | varchar(20)   | NO   | PRI | NULL    |                |
| mpath    | varchar(20)   | YES  |     | NULL    |                |
| wwid     | varchar(50)   | NO   | PRI | NULL    |                |
| size     | decimal(16,0) | YES  |     | NULL    |                |
| criado   | datetime      | NO   | PRI | NULL    |                |
+----------+---------------+------+-----+---------+----------------+
'''
	#insert_sd_associados(last_id,sd_disco,inode_major,inode_minor,status,ativo)
def insert_sd_associados(idmapper,sd_disco,inode_major,inode_minor,status,ativo):
	dbtable="sd_associados"
	con=MySQLdb.connect(dbhost,dbuser,dbpass)
	con.select_db(dbbase)
	query="""
	INSERT INTO %s VALUES ( NULL,%s,"%s",%s,%s,%s,%s)
	""" % (\
	dbtable,idmapper,sd_disco,int(inode_major),int(inode_minor),status,ativo)
	#print query
	with con:
		cur = con.cursor()
		cur.execute(query)
		last=cur.lastrowid
	return last

'''
mysql> explain sd_associados;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| idsd        | int(11)     | NO   | PRI | NULL    | auto_increment |
| idmapper    | int(11)     | NO   |     | NULL    |                |
| disco       | varchar(10) | NO   | PRI | NULL    |                |
| inode_major | int(11)     | YES  |     | NULL    |                |
| inode_minor | int(11)     | YES  |     | NULL    |                |
| status      | binary(1)   | YES  |     | 1       |                |
| ativo       | binary(1)   | YES  |     | 1       |                |
+-------------+-------------+------+-----+---------+----------------+
7 rows in set (0.01 sec)
'''
def insert_asm(idmapper,mppart,volume,inode_major,inode_minor):
	dbtable="asm"
	con=MySQLdb.connect(dbhost,dbuser,dbpass)
	con.select_db(dbbase)
	query="""
	INSERT INTO %s VALUES ( NULL,%s,"%s","%s",%s,%s)
	""" % (\
	dbtable,idmapper,mppart,volume,inode_major,inode_minor)
	#print query
	with con:
		cur = con.cursor()
		cur.execute(query)
		last=cur.lastrowid
	return last


'''
mysql> explain asm;
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| idasm       | int(11)     | NO   | PRI | NULL    |       |
| idmapper    | int(11)     | NO   |     | NULL    |       |
| mppart      | varchar(30) | NO   |     | NULL    |       |
| volume      | varchar(45) | YES  |     | NULL    |       |
| inode_major | int(11)     | YES  |     | NULL    |       |
| inode_minor | int(11)     | YES  |     | NULL    |       |
+-------------+-------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
'''
def insert_lvm(idmapper,mpathd,vg,lvm):
	dbtable="lvm"
	con=MySQLdb.connect(dbhost,dbuser,dbpass)
	con.select_db(dbbase)
	query="""
	INSERT INTO %s VALUES ( NULL,%s,"%s","%s","%s")
	""" % (\
	dbtable,idmapper,mpathd,vg,lvm)
	#print query
	with con:
		cur = con.cursor()
		cur.execute(query)
		last=cur.lastrowid
	return last

	
	
def psacct():	
	


def dados_db(host,mpath,discos,asm,lv):
	#print host
	#['mpath29', '36000144000000010700b1c798bc69f47', '107374182400.0']
	D_mpath=mpath[0].split()
	path=D_mpath[0]
	wwnid=D_mpath[1]
	size=D_mpath[2]
	last_id=insert_mapper(host,path,wwnid,size)
	#print last_id
	msg0="%s [%s]" % (host, last_id)
	msg0 = msg0 +" PATH: %s %s %s"  % ( path , wwnid ,size)
	#print msg0
	if len(discos) > 0:
		D_discos=discos[0].split("|")
		#['sdea 128:32 active ready ', ' sdex 129:144 active ready ', ' sdfw 131:32 active ready ', ' sdgj 131:240 active ready']
		status=1
		ativo=1
		msg1=" DISCOS: "
		msg2=""
		#print D_discos
		for n in range(len(D_discos)):
			linha=D_discos[n].split()
			#print linha
			sd_disco=linha[0]
			msg2=msg2+sd_disco+"(" 
			inode_major=int(linha[1].split(":")[0])
			inode_minor=int(linha[1].split(":")[1])
			msg2=msg2+"%s %s" % (inode_major,inode_minor)
			if linha[2] == "active" : status=0
			if linha[3] == "ready" : ativo=0
			sd_id=str(insert_sd_associados(last_id,sd_disco,inode_major,inode_minor,status,ativo))
			msg2=msg2+str(status)+" "+str(ativo)+" ["+sd_id+"]) "
			#print msg2
		
	
	
	if len(asm) > 0:
		#['mpath29p1', 'VOL1033', '253', '62']
		linha0=asm[0].split()
		mppart=linha0[0]
		volume=linha0[1]
		inode_major=linha0[2]
		inode_minor=linha0[3]
		asm_id = insert_asm(last_id,mppart,volume,inode_major,inode_minor)
		msg3 = " ASM ( %s %s %s %s [%s] ) " % (mppart,volume,inode_major,inode_minor,asm_id)
	else:
	    msg3 = "ASM ( None)"
		
	
	
	if len(lv) > 0:
		print "\tLVM","|",
		for l in range(len(lv)):
			lvdisplay=lv[l].split()
			vg=lvdisplay[1]
			lvm=lvdisplay[2]
			mpathd=lvdisplay[0]
			id_lvm=insert_lvm(last_id,mpathd,vg,lvm)
			msg4=" LVM ( %s %s %s [%s])" % (mpathd,vg,lvm,id_lvm)
	else:
		msg4=" LVM (None)"
	
	msg=msg0+msg1+msg2+msg3+msg4
	log_msg(msg,log_pri[0],log_pri[1])
	### prepara dados para a base de dados.
	# aqui vou precisar brincar de dba.
	
	ok="Dados Inseridos : %s - %s" % (last_id,path)
	return ok




	
	
	
	
	
# registro das funções	
#server.register_function(multiply)
#server.register_function(now)
server.register_function(psacct_db)


####  start do servidor

if __name__ == '__main__':
    try:
        print "Server running on %s:%s" % address
        print "Use Ctrl-C to Exit"
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print "Exiting"
