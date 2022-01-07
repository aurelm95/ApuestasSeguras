import requests
import time
# https://www.youtube.com/watch?v=q9YScw0YBB4
# https://github.com/magnitopic/YouTubeCode/blob/master/TelegramBot
# https://api.telegram.org/bot1421379418:AAHWPUo-fM6CNnoZT2A7Rs4VtLWiZceGShU/getUpdates
token="1421379418:AAHWPUo-fM6CNnoZT2A7Rs4VtLWiZceGShU"
link="https://api.telegram.org/bot{}/".format(token)
#print link

agenda={'aure':1339004426,'marta':659119325}

def enviar_mensaje(mensaje='k ase',destinatario='aure'):
  params = {'chat_id': agenda[destinatario], 'text': mensaje, 'parse_mode': 'HTML'}
  s=requests.Session()
  r=s.post(link+'sendMessage',data=params)

def leer_mensajes():
  params = {'timeout': 30, 'offset': 0}
  r = requests.get(link + 'getUpdates', params)
  result_json = r.json()['result']
  print('En la respuesta hay ',len(result_json),' mensajes')
  #print 'son las ', time.time()
  '''for mensaje in result_json:
    if time.time()-mensaje['message']['date']<300:
      print mensaje['message']['text']
      print 'este mensaje ha sido enviado hace menos de 5 min'''
  if time.time()-result_json[-1]['message']['date']<300:
    #print 'Ultimo mensaje: '+result_json[-1]['message']['text']
    #enviar_mensaje('El ultimo mensaje que me has enviado en menos de 5 minutos es: '+result_json[-1]['message']['text'])
    print(result_json[-1]['message']['text'])
    return result_json[-1]['message']['text']
  else:
  	print(' ')
  	return ' '

#enviar_mensaje()
#leer_mensajes()