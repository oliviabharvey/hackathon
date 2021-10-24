# SI la commande est lancée à partir du remote, il faut rajouer ça avant la commande python 
# DISPLAY=":0" python /home/pi/hackathon_souris/hackathon/module_touchscreen/tutoriel_souris.py
# après, le log est noté dans mouse_log.txt et on peut voir en temps réel, le log s'ajuster aux récents touch
import os
os.environ["DISPLAY"]=":0"
from pynput.mouse import Listener
import logging

logging.basicConfig(filename="module_touchscreen/mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_move(x, y):
    logging.info("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()