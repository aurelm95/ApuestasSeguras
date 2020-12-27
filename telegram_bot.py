import requests
import time
# https://www.youtube.com/watch?v=q9YScw0YBB4
# https://github.com/magnitopic/YouTubeCode/blob/master/TelegramBot
# https://api.telegram.org/bot734567962:AAHxP5M7-rrOQLC0a1s6TQdh6AFHTsHc9yM/getUpdates
token="734567962:AAHxP5M7-rrOQLC0a1s6TQdh6AFHTsHc9yM"
link="https://api.telegram.org/bot{}/".format(token)
#print link

def enviar_mensaje(mensaje='k ase'):
  params = {'chat_id': 797207234, 'text': mensaje, 'parse_mode': 'HTML'}
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




