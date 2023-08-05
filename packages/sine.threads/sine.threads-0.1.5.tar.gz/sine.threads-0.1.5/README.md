# Example

```python
from sine.threads import *

def func(stop_event):
	while 1:
		if stop_event.is_set():
			break
		# do your work

thread = StoppableThread(target=func)
thread.start()
# ...
thread.stop()
# thread.stopped() == True
thread.join()


thread = ReStartableThread(target=func, event_name='stop_event') # can specify the parameter's name
thread.start()
# ...
thread.stop()
thread.join()
# ...
thread.start()
# ...
thread.stop()
thread.join()
# ...
```


# Changelog

#### v0.1.5, 2018-9-11

* fix logic about join(), when directly join() without start() but stop()

#### v0.1.4, 2018-6-7

* ReStartableThread support join the old thread instance  
* fix: ReStartableThread.start always creates new instance  
* *improve comment and change to English*  
* *change directory structure and update setup.py*  
* *add tests.py*  
