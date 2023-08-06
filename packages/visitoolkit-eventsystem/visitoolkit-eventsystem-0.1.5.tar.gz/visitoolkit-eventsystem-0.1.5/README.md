# visitoolkit_eventsystem
minimalistic event system  

**Installation via pip**   
https://pypi.org/project/visitoolkit-eventsystem   
*(runs on Python 3)*  


## description
Registered handlers (a bag of handlers) getting called when event gets fired  
using ideas from "axel events" https://github.com/axel-events/axel  
and "event system" from http://www.valuedlessons.com/2008/04/events-in-python.html

## usage
```python
from visitoolkit_eventsystem import eventsystem

# handlers are callback functions in your code,
# when firing an event visitoolkit_eventsystem will call them with the given argument(s)
def cb1(event_id, *arg, **args):
    if event_id > 0:
        # handle event...
        return True
    else:
        return False

# Default is synchronous execution of handlers (blocking main thread, collecting all results)
# sync_mode=False means asynchronous execution of handlers (one background thread calls all handlers) 
# =>Details about flag "exc_info"(default is True): https://docs.python.org/3/library/sys.html#sys.exc_info
# =>Flag "traceback" (default is False) controls verbosity of error_info when an exception occurred
es = eventsystem.EventSystem(sync_mode=True)

# adding or removing handlers in list-like syntax
es += cb1

#The execution result is returned as a list containing all results per handler having this structure:
#  exec_result = [
#      (True, result, handler),        # on success
#      (False, error_info, handler),   # on error
#      (None, None, handler), ...      # asynchronous execution
#  ]

# firing event
result = es(42)
```

Increasing logging level for bughunting:
```python
import logging
logging.getLogger('visitoolkit_eventsystem').setLevel(logging.DEBUG)
```

## background information
**visitoolkit_eventsystem** is used in **visitoolkit_connector** as core part of **visitoolkit**. 

**visitoolkit** is written for the proprietary Building and Process Management System
'ProMoS NT' (c) MST Systemtechnik AG'  
(also known as 'Saia Visi.Plus' (c) Saia-Burgess Controls AG) 

Intention:  
Support creator of visualisation projects...  
Add efficiency...  
Reduce manual error-prone processes...  
Add missing features...

Disclaimer: Use 'visitoolkit' at your own risk!
