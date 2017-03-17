import threading
import time
lock=threading.Lock()
con = threading.Condition()
con2 = threading.Condition()
global source
global slen
global state
def son(thread_id):
	global source
	global slen
	global state
	state[thread_id]=1
	while(1):
		print source
		if con.acquire():
			if slen>0:
				a=source[slen-1]
				source[slen-1]=0
				slen-=1
				con.release()
			else :
				state[thread_id]=0
				con.wait()
		state[thread_id]=1
		if a<4:
			if con.acquire():
				slen+=1
				source[slen-1]=a+1
				slen+=1
				source[slen-1]=a+1
				con.notifyAll()
				con.release()
source=[0 for i in range(16)]
state=[0 for i in range(16)]
source[0]=0
slen=1
t1=threading.Thread(target=son,args=(0,))
t2=threading.Thread(target=son,args=(1,))
t3=threading.Thread(target=son,args=(3,))
t1.setDaemon(True)
t2.setDaemon(True)
t3.setDaemon(True)
t1.start()
t2.start()
t3.start()
while(1):
	if (state[0]==0)and(state[1]==0)and(state[2]==0):
		break
	else:
		time.sleep(5)
print state[2]
print state[1]
print state[0]
