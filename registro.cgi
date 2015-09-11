#!/usr/bin/python  -OO
# -*- coding: utf-8 -*-

print "Content-Type: text/html; charset=UTF-8\n\n"
print ""

print open('head.html').read()

import cgi
import report
import sys

form  = cgi.FieldStorage()
chave = form.getvalue('chave')
host = form.getvalue('host')
validador =  form.getvalue('validador')
descricao = form.getvalue('descricao')
ativo = form.getvalue('ativo')

if chave == None:
   print """
           <center>
         <h1> Quem é vocÊ! Você não deveria estar AQUI! </h1>
                   </center>

        """
   sys.exit()




###  funcoes

def update_host(a,chave,host,descricao,quem_fez,ativo,quando):
  print " <form  method='post' action='/report/registro.php'>" 
  print " <input type=hidden  name=chave value=%s >" % chave
  print "<tr>"
  print "<td>%s ) <input type=hidden  name=validador value=2 > </td>" %a
  print "<td><input type=text name=host value=%s size=8 readonly > </td>" % host
  #print len(descricao)
  print "<td><input type=text name=descricao value='%s'  > </td>" % descricao
  print "<td> "
  if int(ativo) == 1: 
    print " <input type=radio name=ativo value=1 checked> | "
    print " <input type=radio name=ativo value=0>"
  else:  
    print " <input type=radio name=ativo value=1  > |"
    print " <input type=radio name=ativo value=0 checked >"

  print """
        </td>
        <td>   <input class="submit" type="submit" value="Submit"/>
        </td>
        <td>   %s | %s    </form> </td>
       </tr>
        """ % ( report.desc_user(quem_fez)[0],quando)






def novo_host(chave):
  print " <form  method='post' action='/report/registro.php'>" 
  print " <fieldset>   <legend>Novo Servidor</legend>"
  print " <input type=hidden  name=validador value=1 >"
  print " <input type=hidden  name=chave value=%s >" % chave
  print "Host: <input type=text name=host size=10 >"
  print "Descriçãot: <input type=text name=descricao  >"
  print "Ativar: " 
  print "Sim: <input type=radio name=ativo value=1 checked >"
  print "Não: <input type=radio name=ativo value=0>"
  print " <input class='submit' type='submit' value='Enviar'/> "
  print "  </fieldset>   </form>"
     





### fim das funcoes
#print form
print "<p aling=left> Login: ",chave ,"</P>"
report.menu()

novo_host(chave)

if not validador == None :
  if int(validador) == 1 and not host == None: 
     #print chave,host,descricao,ativo 
     n= report.registro(chave,host.lower(),descricao,ativo)
     #print n
     if int(n) ==  0 : 
          print "<p><font color = green >  Host %s registrado com sucesso</font></p>" % host.upper()
     else:
          print "<p><font color = red >  Host %s já  registrado, verifique na lista de <b>Servidores cadastrados </b> </font> </p>" % host.upper()


  if int(validador) == 2 :
     n= report.atualizar(chave,host.lower(),descricao,ativo)
     print n,chave,host.lower(),descricao,ativo
     if int(n) ==  0 :
          print "<p><font color = green > Host %s Atualizado com sucesso</font></p>" % host.upper()
     else:
          print "<p><font color = red > Não foi possivel atuzalizar o host <b>%s </b> </b> </font></p>" % host.upper()



print "<h2> Servidores cadastrados </h2>"
a=1
b=1
print "<table>"
print "<th>#</th>"
print "<th>HOST</th>"
print "<th>Descrição</th>"
print "<th>Ativar <br> Sim | Não</th>"
print "<th></th>"
print "<th>Registro</th>"
for lista in report.quais_hosts():
   lista=lista.split(",")
   host=lista[0]
   descricao=lista[1]
   #print descricao
   ativo=lista[3]
   quem_fez=lista[2]
   quando = lista[4]
   update_host(a,chave,host,descricao,quem_fez,ativo,quando)
   a+=b
print "</table>"


#select_initervalo(host)



##### 
print open('foot.html').read()
