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
user = form.getvalue('user')
validador =  form.getvalue('validador')
descricao = form.getvalue('descricao')
passwd = form.getvalue('passwd')
ativo = form.getvalue('ativo')

if chave == None:
   print """
           <center>
         <h1> Quem é vocÊ! Você não deveria estar AQUI! </h1>
                   </center>

        """
   sys.exit()




###  funcoes
def update_user(a,chave,user,descricao):
  print " <form  method='post' action='/report/usuario.php'>"
  print " <input type=hidden  name=chave value=%s >" % chave   
  print "<tr>"
  print "<td> %s <input type=hidden  name=validador value=2 > </td>" %a
  print "<td> <input type=text name=user value=%s size=8 readonly >  </td>" % user
  print "<td> <input type=text name=descricao value='%s' size=20> </td>" % descricao
  print "<td><input type=password name=passwd size=20   > </td>"
  print "<td> <input class=submit type=submit value=Submit> </td>"
  print "</form>" 
  print "</tr>"






def novo_usuario(chave):
  print " <form  method='post' action='/report/usuario.php'>" 
  print " <fieldset>   <legend>Adicionar Usuário</legend>"
  print " <input type=hidden  name=validador value=1 >"
  print " <input type=hidden  name=chave value=%s >" % chave 
  print "Login: <input type=text name=user size=10 >"
  print "Senha: <input type=password name=passwd  size=8 >"
  print "Nome : <input type=text name=descricao size=25 >"

  print """
                        <input class="submit" type="submit" value="Submit"/>
                        <button type="reset" value="Reset">Reset</button>
   </fieldset>
   </form>
        """




### fim das funcoes
print "<p aling=left> Login: ",chave ,"</P>"
#print form
report.menu()
novo_usuario(chave)

if not validador == None :
  if int(validador) == 1 : 
     #print chave,host,descricao,ativo 
     n=report.registro_user(user,descricao,passwd)
     print n
     if int(n) ==  0 : 
          print "<p><font color = green >  Usuário %s registrado com sucesso</font></p>" % user
     else:
          print "<p><font color = red >  Usuario %s já  registrado, verifique na lista de <b>Usuarios Cadastrados </b> </font> </p>" % user


  if int(validador) == 2 :
     n= report.atualizar_user(chave,user,descricao,passwd)
     #n= report.atualizar(chave,host.lower(),descricao,ativo)
     #print n
     if int(n) ==  0 :
          print "<p><font color = green > Usuário %s Atualizado com sucesso</font></p>" % user
     else:
          print "<p><font color = red > Não foi possivel atuzalizar o usuário <b>%s </b>  </font></p>" % user



print "<h2> Usuarios Cadastrados </h2>"
print "<p> Ao atualizar informações do usuario, uma nova senha será necessaria.</p>"

a=1
b=1

print "<table>"
print "<th>#</th>"
print "<th>Usuário</th>"
print "<th>Descrição</th>"
print "<th>Nova Senha</th>"
for lista in report.lista_users():
   lista=lista.split(",")
   user=lista[0]
   descricao=lista[1]
   update_user(a,chave,user,descricao)
   a+=b

print "</table>"

#select_initervalo(host)



##### 
print open('foot.html').read()
