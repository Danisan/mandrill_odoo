# -*- coding: utf-8 -*-

#mandrill api
import xmlrpclib
#urllib3.disable_warnings()

import configparser
import mandrill
from datetime import datetime

print """
    Odoo Mandrill Integration (webservice flavour).
    Por Blanco Martin y Asociados
    http://blancomartin.cl
    

"""

config = configparser.ConfigParser()
try:
    config.read('config.ini')
except:
    print """
    
    ERROR: No pudo leer archivo de configuracion. config.ini.
    Revise si se encuentra en el directorio  de instalacion de 
    

    """
    raise SystemExit(0)

try:
    username = config['DEFAULT']['username']
    pwd = config['DEFAULT']['password']
    dbname = config['DEFAULT']['database']
    odoourl = config['DEFAULT']['url']
except:
    print """

    ERROR:
    No se pudieron obtener parámetros de acceso. 
    Por favor revise que el archivo \"config.ini\" contenga la
    información de acceso.
        TIPS: la seccion \"[DEFAULT]\" debe existir.
            Dentro de ella deben estar los siguientes parametros:
            username, password, database y url.


    """
    raise SystemExit(0)

sock_common = xmlrpclib.ServerProxy (odoourl + '/xmlrpc/common')
sock = xmlrpclib.ServerProxy (odoourl + '/xmlrpc/object')
uid = sock_common.login(dbname, username, pwd)


try:
    mandrill_client = mandrill.Mandrill(config['MAILCHIMP']['APIKEY'])
    responses = mandrill_client.rejects.list(include_expired=True,)
    for response in responses:
        print response['email']
        args = [
            ('email', '=', response['email'])
        ]
        give_me_fields = [
            'opt_out'
        ]
        values = {'opt_out': 'true'}

        try:
            mass_email_id = sock.execute(dbname, uid, pwd, 'mail.mass_mailing.contact', 'search', args)
            mass_email_records = sock.execute(dbname, uid, pwd, 'mail.mass_mailing.contact', 'read', mass_email_id, give_me_fields)
            for mass_email_record in mass_email_records:
            	if mass_email_record['opt_out'] == False:
            		a = sock.execute(dbname, uid, pwd, 'mail.mass_mailing.contact', 'write', mass_email_id, values)

            
        except:
            print """

            ERROR:
            No se pudo efectuar la consulta. Revise si los parametros de 
            ingreso a su sistema en \"config.ini\" son los correctos.


            """
            raise SystemExit(0)

    
except mandrill.Error, e:
    # Mandrill errors are thrown as exceptions
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
    raise