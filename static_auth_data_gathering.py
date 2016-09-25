import pyxhook
import time
import signal
import sys
import pickle

sample_number = 1
curr_str = ''

current_milli_time = lambda: int(round(time.time() * 1000))

down_events = []
up_events = []

def print_event(event, prefix):
    if (event.Ascii >= 48 and event.Ascii <= 57) or (event.Ascii >= 65 and event.Ascii <= 90) or (event.Ascii >= 97 and event.Ascii <= 122):
        print prefix, event.Key, current_milli_time()

def record_event(event, prefix):
    if prefix == 'KeyDown:':
        global curr_str
        curr_str = curr_str + event.Key
        down_events.append([event.Key, current_milli_time()])
    elif prefix == 'KeyUp:':
        up_events.append([event.Key, current_milli_time()])

def kb_down_event(event):
    #print_event(event, 'KeyDown:')
    record_event(event, 'KeyDown:')

def kb_up_event(event):
    record_event(event, 'KeyUp:')

    if event.Ascii == 32:
        global sample_number
        global curr_str
        global up_events
        global down_events

        if curr_str == 'passwordspace':
            print curr_str
            #del up_events[0]
            data = dict()
            data['key_down_events'] = down_events
            data['key_up_events'] = up_events
            print data
            pickle.dump(data, open('sample_steve_' + str(sample_number) + '.pickle', 'wb')) 
            #sys.exit(0)
            print 'Saved to sample', sample_number
            sample_number = sample_number + 1
            print 'Incremented sample number to ', sample_number
        else:
            print 'Incorrect string. Skipping...'
        
        curr_str = ''
        up_events = []
        down_events = []


hookman = pyxhook.HookManager()

hookman.KeyDown = kb_down_event
hookman.KeyUp = kb_up_event

hookman.HookKeyboard()
hookman.start()
    
#Close the listener when we are done
#hookman.cancel()
