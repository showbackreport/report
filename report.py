#!/usr/bin/python  -OO
# -*- coding: utf-8 -*-

'''
Relatorio de showback com base no pacct + mysql
Carlos Morais <carlos_morais@banrisul.com.br> 
maio 2015

Manutenção de todas as funções de uso comum.

'''

# Modulos

import MySQLdb
import config
import urllib
import os,socket
from time import gmtime, strftime , localtime
from datetime import datetime

# Variaveis globais

dbhost = config.ConfigSectionMap("mysql")['dbhost']
dbuser = config.ConfigSectionMap("mysql")['dbuser']
dbpass = config.ConfigSectionMap("mysql")['dbpass']
dbbase = config.ConfigSectionMap("mysql")['dbbase']
tempoproc=['time_effect','time_user','time_system', '(time_user + time_system)', '(time_user + time_system)/time_effect','time_effect-(time_user + time_system)']
Legenda=['Tempo Efetivo (real)','Tempo Usuario (user)','Tempo Sistema (sys)','Tempo ( User + Sys)', 'CPU utilização','IO wait']
Local = "/tmp/svg"
if not  os.path.exists(Local) :
        os.makedirs(Local)




###########################
#  registro de hosts 

# chave,host,descricao,ativo
def registro(chave,host,descricao,ativo):
  dbtable = "host_desc"
  con=MySQLdb.connect(dbhost,dbuser,dbpass)
  con.select_db(dbbase)
  with con:
    cur = con.cursor()
    # "(%s ,%s, %s, '%s' )" % (uid, gid , Username,"grupo")
    a ="INSERT INTO %s VALUES ( '%s', '%s' , '%s' , %s, now() ) " %(dbtable,host,descricao,chave,ativo)
    #print a
    try:
       cur.execute(a)
       result = 0
    except:
       result = 1 

  con.close()
  return result


# chave,host,descricao,ativo
# atualizar 

#UPDATE  host_desc SET usuario = 'b35417' , ativo= 0 , descricao = 'R poc poc poc' , data_insc = now()  WHERE  host = 'lipx';
def atualizar(chave,host,descricao,ativo):
  dbtable = "host_desc"
  con=MySQLdb.connect(dbhost,dbuser,dbpass)
  con.select_db(dbbase)
  row=0
  with con:
    cur = con.cursor()
    a = """
         UPDATE %s SET usuario = '%s' , ativo = %s , descricao = '%s' , data_insc = now()  WHERE  host = '%s'  
        """ % (dbtable,chave,ativo,descricao,host.lower())
    #print a
    try:
       cur.execute(a)
       row=int(cur.rowcount)
       result = 0
    except:
       result = 1
  if int(row) == 0:  result = 1 
  con.close()
  return result




def quais_hosts():
  conn=MySQLdb.connect(dbhost,dbuser,dbpass)
  conn.select_db(dbbase)
  tbcs = conn.cursor()
  query='''
     SELECT
           host,descricao,usuario,ativo,data_insc
     FROM
           host_desc

     ORDER BY  host
        '''
  # print query
  tbcs.execute(query)
  #print tbcs
  row_ue=[]
  for a in  tbcs:
     #print a
     ue="%s,%s,%s,%s,%s" % (a[0],a[1],a[2],a[3],a[4])
     row_ue.append(ue)
  conn.close()
  return row_ue


def quais_hosts_ativos():
  conn=MySQLdb.connect(dbhost,dbuser,dbpass)
  conn.select_db(dbbase)
  tbcs = conn.cursor()
  query='''
     SELECT
           host,descricao,usuario,ativo,data_insc
     FROM
           host_desc
     WHERE
         ativo = 1

     ORDER BY  host
        '''

  # print query
  tbcs.execute(query)
  #print tbcs
  row_ue=[]
  for a in  tbcs:
     #a=a.split(",")
     b="%s,%s" % (a[0],a[1])
     row_ue.append(b)
  conn.close()
  return row_ue


####################
# usuarios


def lista_users():
  conn=MySQLdb.connect(dbhost,dbuser,dbpass)
  conn.select_db(dbbase)
  tbcs = conn.cursor()
  query='''
     SELECT
            user_name,user_descr
     FROM
           acct_auth
     ORDER BY  user_name
        '''
  # print query
  tbcs.execute(query)
  #print tbcs
  row_ue=[]
  for a in  tbcs:
     #print a
     ue="%s,%s" % (a[0],a[1])
     row_ue.append(ue)
  conn.close()
  return row_ue

def registro_user(user,descricao,passwd):
  con=MySQLdb.connect(dbhost,dbuser,dbpass)
  con.select_db(dbbase)
  with con:
    cur = con.cursor()
    #    insert into acct_auth values ('b35417', ENCRYPT('191009'),'Carlos Morais');
    a ="INSERT INTO acct_auth VALUES ( '%s', ENCRYPT('%s') , '%s' ) " %(user,passwd,descricao)
    #print a
    try:
       cur.execute(a)
       result = 0
    except:
       result = 1

  con.close()
  return result


def atualizar_user(chave,user,descricao,passwd):
  con=MySQLdb.connect(dbhost,dbuser,dbpass)
  con.select_db(dbbase)
  row=0
  with con:
    cur = con.cursor()
    a = """
         UPDATE  acct_auth  SET user_passwd  = ENCRYPT('%s') , user_descr = '%s'  WHERE  user_name = '%s'
        """ % (passwd,descricao,user)
    #print a
    try:
       cur.execute(a)
       row=int(cur.rowcount)
       result = 0
    except:
       result = 1
  if int(row) == 0:  result = 1
  con.close()
  return result

def desc_user(username):
  conn=MySQLdb.connect(dbhost,dbuser,dbpass)
  conn.select_db(dbbase)
  tbcs = conn.cursor()
  query="SELECT  user_descr  FROM  acct_auth   WHERE   user_name = '%s' " % username
  #print query
  tbcs.execute(query)
  #print tbcs
  row_ue=[]
  for a in  tbcs:
     b="%s" % a[0]
     row_ue.append(b)
  conn.close()
  return row_ue


######################

def desc_host(host):
  conn=MySQLdb.connect(dbhost,dbuser,dbpass)
  conn.select_db(dbbase)
  tbcs = conn.cursor()
  query="SELECT  descricao  FROM   host_desc    WHERE   host = '%s' " % host
  #print query
  tbcs.execute(query)
  #print tbcs
  row_ue=[]
  for a in  tbcs:
     b="%s" % a[0]
     row_ue.append(b)
  conn.close()
  return row_ue





def intervalo(host,S):

  if S == '1': S ="asc"
  if S == '0': S ="desc"
  conn=MySQLdb.connect(dbhost,dbuser,dbpass)
  conn.select_db(dbbase)
  tbcs = conn.cursor()
  query='''

 select date(data_pross)  from acct_uid where host='%s' group by date(data_pross) order by date(data_pross) %s
        ''' % (host,S)
  #print query
  tbcs.execute(query)
  #print tbcs
  row_ue=[]
  for a in  tbcs:
     #print a[0]
     row_ue.append(a[0])
  conn.close()
  return row_ue


###########################

#IP = socket.gethostbyaddr(HOST)
#IP=IP[2]


def menu():
   print """
        <p><nav>
             <ul class="menu">
               <li><a href=/report/ >Home</a></li>
               <li><a href=/report/registro.php >Hosts</a></li>
               <li><a href=/report/usuario.php >Usuário</a></li>
			</ul>
        </nav></p>
		<br><br><br>		
        """  


def cabecalho(Inicio,Fim,HOST,T):
  date_format = "%Y-%m-%d" # 2015-06-24
  a = datetime.strptime(Inicio, date_format)
  b = datetime.strptime(Fim, date_format)
  delta = b - a
  print"<center>"
  print "<h1> Servidor - %s - %s </h1>" % (HOST.upper(),Legenda[T])
  print desc_host(HOST)[0]
  dia ="dia"
  if delta.days >= 2: dia = "dias"
  print "<h2> Intervalo de analise: %s - %s  (%s %s) </h2>" % (Inicio,Fim,delta.days,dia)
  print "<h3>",strftime("%a, %d %b %Y %X", localtime()),"</h3>"


def username(uid):
    conn=MySQLdb.connect(dbhost,dbuser,dbpass)
    conn.select_db(dbbase)
    tbcs = conn.cursor()
    query='''
         SELECT username FROM users WHERE uid=%s
          ''' % uid 
    tbcs.execute(query)
    for a in  tbcs:
       #print a
        user=a[0]
    conn.close()
    return user

def cmd_hosts(cmd,uid,N):
    N=int(N)
    conn=MySQLdb.connect(dbhost,dbuser,dbpass)
    conn.select_db(dbbase)
    tbcs = conn.cursor()
    query='''
         SELECT host FROM acct_cmd  WHERE comando='%s'  group by host
          ''' % cmd

    query0='''
         SELECT host FROM acct_cmd  WHERE uid='%s'  group by host
          ''' % uid
    queris=[query,query0]
    
    tbcs.execute(queris[N])
    comando=[]
    for a in  tbcs:
       #print a
        comando.append(a[0])
    conn.close()
    return comando





# todos os usuarios por tempo efetivo.
def T_users(Inicio,Fim,host,colm):
        conn=MySQLdb.connect(dbhost,dbuser,dbpass)
        conn.select_db(dbbase)
        tbcs = conn.cursor()
        query='''
    SELECT  users.username , acct_uid.uid as User_id , 
     (SUM( %s )/
        (SELECT  SUM( %s )  FROM  acct_uid  WHERE  host='%s' AND data_pross BETWEEN '%s'  AND   '%s') 
      )*100 AS TempEff  
    FROM  acct_uid, users  
    WHERE host='%s'  AND data_pross BETWEEN '%s'  AND  '%s' AND  acct_uid.uid = users.uid GROUP BY User_id ORDER BY TempEff DESC


               ''' % (colm,colm,host,Inicio,Fim,host,Inicio,Fim)
        # print query
        tbcs.execute(query)
        #print tbcs
        row_ue=[]
        for a in  tbcs:
            #print a
            username=a[0]
            uid=a[1]
            t_efetivo=str(a[2])
            n="%s;%s;%s" % (username,t_efetivo,uid)	
            row_ue.append(n)
        conn.close()
        return row_ue

# pega os 10 comandos mais urados por usuario.
def T10proc(uid,Inicio,Fim,host,colm):
        conn=MySQLdb.connect(dbhost,dbuser,dbpass)
        conn.select_db(dbbase)
        tbcs = conn.cursor()
        query='''
              SELECT    
               comando, (
               sum(%s )/   (SELECT  SUM( %s )  FROM  acct_cmd  WHERE  host='%s' AND data_pross BETWEEN '%s'  AND   '%s')  )*100 AS TempoEfetivo 
              FROM
               acct_cmd 
             WHERE
                host='%s'  AND 
                data_pross  BETWEEN  '%s'  AND   '%s'   AND  uid = %s    
              GROUP BY   comando  ORDER BY   TempoEfetivo   DESC LIMIT 20
               ''' % (colm,colm,host,Inicio,Fim,host,Inicio,Fim,uid)

        ##print query
        tbcs.execute(query)
        row_ue=[]
        for a in  tbcs:
            comando=a[0]
            t_efetivo=str(a[1])
            n="%s;%s" % (comando,t_efetivo)
            row_ue.append(n)
        conn.close()
        return row_ue



### BAR ###



def B_users(Inicio,Fim,host,colm,uid,tipo):
        conn=MySQLdb.connect(dbhost,dbuser,dbpass)
        conn.select_db(dbbase)
        tbcs = conn.cursor()
        query_a='''
SELECT
     DATE_FORMAT(data_pross,'%%Y-%%m-%%d %%H')  , (SUM( %s )/
         (SELECT  SUM( %s )  FROM  acct_uid  WHERE  host='%s' AND data_pross BETWEEN '%s'  AND   '%s')
      )*100 AS TempEff
FROM
           acct_cmd
 WHERE
          uid=%s   AND   host='%s' AND data_pross BETWEEN '%s'  AND '%s'
GROUP BY DATE_FORMAT(data_pross,'%%Y-%%m-%%d %%H')
               ''' % (colm,colm,host,Inicio,Fim,uid,host,Inicio,Fim)


        query_b='''
SELECT
     DATE_FORMAT(data_pross,'%%Y-%%m-%%d')  , (SUM( %s )/
         (SELECT  SUM( %s )  FROM  acct_uid  WHERE  host='%s' AND data_pross BETWEEN '%s'  AND   '%s')
      )*100 AS TempEff
FROM
           acct_cmd
 WHERE
          uid=%s   AND   host='%s' AND data_pross BETWEEN '%s'  AND '%s'
GROUP BY DATE_FORMAT(data_pross,'%%Y-%%m-%%d')
               ''' % (colm,colm,host,Inicio,Fim,uid,host,Inicio,Fim)

        query=[query_a,query_b]
        #print query
        t=1
        if tipo == "D" : t=1
        if tipo == "H" : t=0

        #print t,query[t]
        tbcs.execute(query[t])
        #print tbcs
        row_ue=[]
        for a in  tbcs:
            #print a
            username=a[0]
            t_efetivo=a[1]
            n="%s;%s" % (username,t_efetivo)
            row_ue.append(n)
        conn.close()
        return row_ue

# pega os 10 comandos mais urados por usuario.
def B10proc(uid,Inicio,Fim,host,colm,cmd,tipo):
        conn=MySQLdb.connect(dbhost,dbuser,dbpass)
        conn.select_db(dbbase)
        tbcs = conn.cursor()
        query_a='''

             SELECT 
                    DATE_FORMAT(data_pross,'%%Y-%%m-%%d %%H'),
                   ( sum(%s)/
                   ( SELECT  SUM( %s )  FROM  acct_cmd  WHERE  uid=%s AND host='%s' AND data_pross BETWEEN '%s'  AND   '%s'  ))*100 AS TempoEfetivo
             FROM   acct_cmd
             WHERE   host='%s'  AND  uid=%s AND comando='%s' AND  data_pross BETWEEN '%s'  AND   '%s'
             GROUP BY  DATE_FORMAT(data_pross,'%%Y-%%m-%%d %%H')

               ''' % (colm,colm,uid,host,Inicio,Fim,host,uid,cmd,Inicio,Fim)

        query_b='''
             SELECT
                    DATE_FORMAT(data_pross,'%%Y-%%m-%%d'),
                   ( sum(%s)/
                   ( SELECT  SUM( %s )  FROM  acct_cmd  WHERE  uid=%s AND host='%s' AND data_pross BETWEEN '%s'  AND   '%s'  ))*100 AS TempoEfetivo
             FROM   acct_cmd
             WHERE   host='%s'  AND  uid=%s AND comando='%s' AND  data_pross BETWEEN '%s'  AND   '%s'
             GROUP BY  DATE_FORMAT(data_pross,'%%Y-%%m-%%d')
               ''' % (colm,colm,uid,host,Inicio,Fim,host,uid,cmd,Inicio,Fim)

        query=[query_a,query_b]
        #print query
        t=1
        if tipo == "D" : t=1
        if tipo == "H" : t=0

        #print query
        tbcs.execute(query[t])
        row_ue=[]
        for a in  tbcs:
            data=a[0]
            t_efetivo=str(a[1])
            n="%s;%s" % (data,t_efetivo)
            row_ue.append(n)
        conn.close()
        return row_ue

# gera os graficos
def pizza_graf(name,pie,titulo,Local):
  filename = "%s/%s" % ( Local, name)
  import pygal                                                       # First import pygal
  from pygal.style import LightSolarizedStyle
  pie_chart = pygal.Pie(width=600, height=600, style=LightSolarizedStyle)
  pie_chart.title = titulo
  for lote in pie:
   slote=lote.split(";")
   #pie_chart.add(slote[0],float(slote[1]))
   pie_chart.add(slote[0], [{'value':float(slote[1]), 'label': slote[0]}])
  pie_chart.render_to_file(filename)
  #pie_chart.render()



# gera os graficos
def barra_graf(name,pie,titulo,Local):
  filename = "%s/%s" % ( Local, name)
  import pygal                                                       # First import pygal
  from pygal.style import LightSolarizedStyle
  bar_chart = pygal.Bar( style=LightSolarizedStyle,x_label_rotation=90,show_minor_x_labels=True)
  #bar_chart = pygal.HorizontalBar(width=600, height=600, style=LightSolarizedStyle)
  bar_chart.title = titulo
  #label=[]
  for lote in pie:
   slote=lote.split(";")
   ##bar_chart.add(slote[0],float(slote[1]))
   #label.append(slote[0])
   bar_chart.add(slote[0], [{'value':float(slote[1]), 'label': slote[0]}])
  #bar_chart.x_labels = label
  bar_chart.render_to_file(filename)
  #pie_chart.render()





def showback(HOST,Inicio,Fim,T,chave):
  T=int(T)
  cabecalho(Inicio,Fim,HOST,T)

  IP = socket.gethostbyaddr(HOST)
  IP=IP[2]
  print '''
  <table width=80%  border='0' rules='all' bgcolor='#D0D0D0'>
  <td>
        '''
  print '''
    <p><b>HOST:</b>  %s - %s </p> 
    <p><b>PERÍODO:</b> de %s a %s
    <p><b>MÉTODO:</b> Coleta de dados usando o <a href=http://www.tldp.org/HOWTO/text/Process-Accounting > pacct </a> com conversão e integralização de dados para base MySQL. 
Para a totalização de recursos utilizados, foi usado como parâmetro o tempo efetivo de processamento, parâmetro interno ao kernel Linux, e informado pelo pacct em unidades de segundo.  Para processos menores que 1s, o pacct agrupa a informação. </p>
    </td>
    </table>
        ''' % ( HOST.upper(),IP[0],Inicio,Fim)

  ###  Grafico Principal
  titulo="Distribuição de Usuários por %s de Processamento" % Legenda[T]
  rep1=T_users(Inicio,Fim,HOST,tempoproc[T])
  print "<h2>",titulo,"</h2>"
  print "<table width=80%  border='0' rules='none' bgcolor='#CCCCFF' >"
  print "<td width=30% valign=top>"
  print "  <table width=100%  border='1' rules='all' bgcolor='white'>"
  print "  <th>Usuario </th><th>Tempo efetivo (%) </th>"
  for lote in rep1:
     slote=lote.split(";")
     print "<tr><td><a href='/cgi-bin/report/showback.cgi?chave=%s&host=%s&inicio=%s&fim=%s&tempo=%s&uid=%s&tipo=D'>%s </a></td>" %(chave,HOST,Inicio,Fim,T,slote[2],slote[0])
     print "<td align=right >%s</td></tr>" % slote[1]

  print "  </table>"
  print "</td><td width=80% valign=middle>"

  name="Ue_%s.svg" % HOST
  pizza_graf(name,rep1,HOST,Local)

  filename="%s/%s" % (Local,name)

  print "<figure>"
  print open(filename).read()
  print "</figure>"
  print "</td>"
  print "</table>"

  print "<br><hr><br>"
  #sys.exit()

  for lote in rep1:
     slote=lote.split(";")
     user=slote[0]
     percente=slote[1]
     uid=slote[2]
     com_efetivo=T10proc(uid,Inicio,Fim,HOST,tempoproc[T])
     print "<table width=80%  border='0' rules='none' bgcolor='#CCCCFF' >"
     print "<tr><th>",user.upper()," - [",percente,"%]","</th><th>Comandos por consumo de processador</th></tr>"
     print "<tr><td width=30% valign=top>"
     print "<table width=100%  border='1' rules='all' bgcolor='white'>"
     print "<th>Comando </th><th>Tempo efetivo (%) </th>"
     for comlote in com_efetivo:
            clote=comlote.split(";")
            #print clote
            print "<tr><td><a href='/cgi-bin/report/showback.cgi?chave=%s&host=%s&inicio=%s&fim=%s&tempo=%s&uid=%s&cmd=%s&tipo=D'>%s </a></td>" %(chave,HOST,Inicio,Fim,T,uid,clote[0],clote[0])
            print "<td align=right >%s</td></tr>" % clote[1]
            #print "<tr><td>",clote[0],"</td><td align=right >",clote[1],"</td></tr>"
     print "</table>"
     print "</td><td valign=middle>"
     name="comando-%s_%s.svg" % (HOST,uid)
     pizza_graf(name,com_efetivo,user.upper(),Local)
     filename = "%s/%s" % ( Local, name)
     print "<figure>"
     print open(filename).read() 
     print "</figure>"
     print "</td></tr>"
     print "</table>"
     print "<br><br>"
  print "</center>"


def bar(HOST,Inicio,Fim,T,chave,uid,tipo):
  T=int(T)
  cabecalho(Inicio,Fim,HOST,T)
  IP = socket.gethostbyaddr(HOST)
  IP=IP[2]


  print '''
  <table width=80%  border='0' rules='all' bgcolor='#D0D0D0'>
  <td>
        '''
  print '''
    <p><b>HOST:</b>  %s - %s </p>
    <p><b>PERÍODO:</b> de %s a %s
    <p><b>MÉTODO:</b> Coleta de dados usando o <a href=http://www.tldp.org/HOWTO/text/Process-Accounting > pacct </a> com conversão e integralização de dados para base MySQL.
Para a totalização de recursos utilizados, foi usado como parâmetro o tempo efetivo de processamento, parâmetro interno ao kernel Linux, e informado pelo pacct em unidades de segundo.  Para processos menores que 1s, o pacct agrupa a informação. </p>
    </td>
    </table>
        ''' % ( HOST.upper(),IP[0],Inicio,Fim)
  ###  Grafico Principal
  titulo="Distribuição do  %s Percentual no Período - %s" % (Legenda[T],username(uid))
  rep1=B_users(Inicio,Fim,HOST,tempoproc[T],uid,tipo)
  print "<h2>",titulo,"</h2>"
  #                                                chave   HOST    Inicio    Fim        T       uid
  print '''
        Expande a distribuição por  <b>HORA</b>
        <a href='/cgi-bin/report/showback.cgi?chave=%s&host=%s&inicio=%s&fim=%s&tempo=%s&uid=%s&tipo=H'>%s </a></td>
        '''  %(chave,HOST,Inicio,Fim,T,uid,username(uid))


  print "<table width=80%  border='0' rules='none' bgcolor='#CCCCFF' >"
  print "<td width=30% valign=top>"
  print "  <table width=100%  border='1' rules='all' bgcolor='white'>"
  print "  <th>Data </th><th>Tempo efetivo (%) </th>"
  for lote in rep1:
     slote=lote.split(";")
     print "<tr><td>%s </a></td>" %(slote[0])
     print "<td align=right >%s</td></tr>" % slote[1]
  print "  </table>"
  print "</td><td width=80% valign=middle>"
  name="barUe_%s.svg" % HOST
  label="Uso de processamento em (%%) -  %s " % username(uid)
  barra_graf(name,rep1,label,Local)
  filename="%s/%s" % (Local,name)
  print "<figure>"
  print open(filename).read()
  print "</figure>"
  print "</td>"
  print "</table>"

  print "<br><hr><br>"
  Lista_cmd_hosts=cmd_hosts(HOST,uid,'1')
  print "O Usuarioo <b> %s </b> é encontrado em %s hosts " % (username(uid),len(Lista_cmd_hosts))
  print "<table width=80%  border='0' rules='none' bgcolor='#CCCCFF' >"
  print "<tr><th> Host </th> <th>Descrição </th></tr>"
  for m in Lista_cmd_hosts:
      #print m
      if len(desc_host(m)) == 0 : 
            descritor = " == SEM DESCRIÇÃO =="
      else:
            descritor = desc_host(m)[0]
      print"<tr><td> %s </td><td> %s </td> </tr>" % (m.upper(),descritor)
  print "</table>"
  print "<br><hr><br>"



def bar_cmd(HOST,Inicio,Fim,T,chave,uid,cmd,tipo):
  T=int(T)
  cabecalho(Inicio,Fim,HOST,T)
  IP = socket.gethostbyaddr(HOST)
  IP=IP[2]

  print '''
  <table width=80%  border='0' rules='all' bgcolor='#D0D0D0'>
  <td>
        '''

  print '''
    <p><b>HOST:</b>  %s - %s </p>
    <p><b>PERÍODO:</b> de %s a %s
    <p><b>MÉTODO:</b> Coleta de dados usando o <a href=http://www.tldp.org/HOWTO/text/Process-Accounting > pacct </a> com conversão e integralização de dados para base MySQL.
Para a totalização de recursos utilizados, foi usado como parâmetro o tempo efetivo de processamento, parâmetro interno ao kernel Linux, e informado pelo pacct em unidades de segundo.  Para processos menores que 1s, o pacct agrupa a informação. </p>
    </td>
    </table>
        ''' % ( HOST.upper(),IP[0],Inicio,Fim)
  ###  Grafico Principal
  
  titulo="Distribuição do  %s Percentual no Período - %s " % ( Legenda[T],cmd)
  rep1=B10proc(uid,Inicio,Fim,HOST,tempoproc[T],cmd,tipo)
  #rep1=B_users(Inicio,Fim,HOST,tempoproc[T],uid)
  
  print "<h2>",titulo,"</h2>"
  print "<h3> O comando <b> %s </b> é encontrado nos seguintes hosts:  </h3>" %cmd

  print '''
        Expande a distribuição por  <b>HORA</b>
        <a href='/cgi-bin/report/showback.cgi?chave=%s&host=%s&inicio=%s&fim=%s&tempo=%s&uid=%s&cmd=%s&tipo=H'>%s </a></td>
        '''  %(chave,HOST,Inicio,Fim,T,uid,cmd,cmd)

 


  print "<table width=80%  border='0' rules='none' bgcolor='#CCCCFF' >"
  print "<td width=30% valign=top>"
  print "  <table width=100%  border='1' rules='all' bgcolor='white'>"
  print "  <th>Data </th><th>Tempo efetivo (%) </th>"
  for lote in rep1:
     slote=lote.split(";")
     print "<tr><td>%s </a></td>" %(slote[0])
     print "<td align=right >%s</td></tr>" % slote[1]
  print "  </table>"
  print "</td><td width=80% valign=middle>"
  name="barUe_%s.svg" % HOST
  label="Uso de processamento em (%%) - %s" % cmd
  barra_graf(name,rep1,label,Local)
  filename="%s/%s" % (Local,name)
  print "<figure>"
  print open(filename).read()
  print "</figure>"
  print "</td>"
  print "</table>"
  print "O comando <b> %s </b> é encontrado nos seguintes hosts " %cmd
  print "<table width=80%  border='0' rules='none' bgcolor='#CCCCFF' >"
  print "<tr><th> Host </th> <th>Descrição </th></tr>"
  for m in cmd_hosts(cmd,'0','0'):
      #print m
      if len(desc_host(m)) == 0 :
            descritor = " == SEM DESCRIÇÃO =="
      else:
            descritor = desc_host(m)[0]
      print"<tr><td> %s </td><td> %s </td> </tr>" % (m.upper(),descritor)


  print "</table>"
  print "<br><hr><br>"


