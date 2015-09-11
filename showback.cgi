#!/usr/bin/python  -OO
# -*- coding: utf-8 -*-

print "Content-Type: text/html; charset=UTF-8\n\n"
print ""
print open('head.html').read()

## select host from acct_uid group by host <= quais osd hosts disponiveis
import config
import report
import cgi
import sys

form  = cgi.FieldStorage()
host  = form.getvalue('host')
inicio  = form.getvalue('inicio')
fim  = form.getvalue('fim')
chave = form.getvalue('chave')
tempo = form.getvalue('tempo')
uid =  form.getvalue('uid')
cmd =  form.getvalue('cmd')
tipo =  form.getvalue('tipo')


if chave == None:
   print """
           <center>
         <h1> Quem é vocÊ! Você não deveria estar AQUI! </h1>
                   </center>

        """
   sys.exit()

###  funcoes

def select_initervalo(host,tempo):
   tempo=int(tempo)
   #tempoproc=['time_effect','time_user','time_system', '(time_user + time_system)', '(time_user + time_system)']
   Legenda=['Tempo Efetivo (real)','Tempo Usuario (user)','Tempo Sistema (sys)','Tempo ( User + Sys)', 'CPU utilização','IO wait']
   #Legenda=['Tempo Efetivo (real)','Tempo Usuario (user)','Tempo Sistema (sys)','Tempo ( User + Sys)', 'CPU Percente']

   #tempoproc=['Tempo Efetivo (Real)','Tempo Usuario (User) ','Tempo Sistema (Sys) ','Tempo (User+Sys)']
   print "<p>O servidor escolhido foi: <b> ", host.upper() ,"</b> - ",report.desc_host(host)[0], "</p>"
   print "<p>  Método : ",Legenda[tempo] ,"  -  Informe o intervalo: </p>"

   print """
        <form  method="post" action="/report/index.php">
        <input id="host" name="host" value="%s" TYPE="hidden" />
        <input id="tempo" name="tempo" value="%s" TYPE="hidden" />
          Intervalo :

        """ % (host,tempo)
   lista_a=report.intervalo(host,'1')
   lista_b=report.intervalo(host,'0')

   print "<select id='inicio' name='inicio' >"
   for a in lista_a:
      print "<option  value='%s' >%s</option>" % (a, a)
   print "</select>"

   print "<select id='fim' name='fim' >"
   for b in lista_b:
      print "<option  value='%s' >%s</option>" % (b, b)
   print "</select>"
   print """
                        <input class="submit" type="submit" value="Submit"/>
                        <button type="reset" value="Reset">Reset</button>
   </form>
        """

def select_host():
  print """<p>
          <form  method="post" action="/report/index.php">
          Servidor :
        """
  lista=report.quais_hosts_ativos()
  print "<select id='host' name='host' >"
  for a in lista:
     a=a.split(",")
     #print a
     print "<option  value='%s' >%s - %s </option>" % (a[0], a[0].upper(),a[1])
  print "</select>"
  print "<select id='tempo' name='tempo' >"
  print "<option  value='0' >Tempo Efetivo  (Real)</option>" 
  print "<option  value='1' >Tempo Usuario  (User)</option>" 
  print "<option  value='2' >Tempo Sistema  (Sys)</option>" 
  print "<option  value='3' >Tempo User Sys (User+Sys)</option>" 
  print "<option  value='4' >CPU utilização  (User+Sys/Real)</option>" 
  print "<option  value='5' >IO wait  (Real - User+Sys)</option>" 
  print "</select>"

  print """
                        <input class="submit" type="submit" value="Enviar"/>                        
   </form>
       </p>
        """

### fim das funcoes
print "<p aling=left> Login: ",chave ,"</P>"
report.menu()


if not tempo == None :
  if inicio == None and fim == None:
      select_initervalo(host,tempo)
  else:
    if uid == None :
        report.showback(host,inicio,fim,tempo,chave)
    else:
       if cmd == None:
          report.bar(host,inicio,fim,tempo,chave,uid,tipo)
       else:
          report.bar_cmd(host,inicio,fim,tempo,chave,uid,cmd,tipo)
else:
     select_host()



##### 
print open('foot.html').read()
