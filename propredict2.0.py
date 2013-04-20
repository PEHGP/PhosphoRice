#!/usr/bin/python
import re,os,sys,math,time
def auc(t,rf):
	#ft=open("prot.roc","w")#only use test
	l=[]
	
	p=0.
	n=0.
	for x in t:
		if x[1]=="1" or x[1]=="+1":
			p+=1
		else:n+=1
	print p,n
	for x in t:
		TP=0.
		FP=0.
		for y in t:
			if float(y[0])>=float(x[0]) and (y[1]=="+1" or y[1]=="1"):
					TP+=1
			if float(y[0])>=float(x[0]) and y[1]=="-1":
					FP+=1
		rf.write(str(FP/n)+"\t"+str(TP/p)+"\n")
		l.append((FP/n,TP/p))
	l.sort()
	s=0.
	#for x in l:
		#print x[0],x[1]
		#ft.write(str(x[0])+"\t"+str(x[1])+"\n")
	
	for i in range(len(l)-1):
		s+=(l[i][1]+l[i+1][1])*(l[i+1][0]-l[i][0])/2
	return s
def collect(f,r):
	t=[]
	res=[]
	l=[]
	for x in open(f):
		m=re.search("(.*?)\s",x)
		t.append(m.group(1))
	for x in open(r):
		x=x.rstrip()
		res.append(x)
	for x in range(len(res)):
		l.append((res[x],t[x]))
	return l
def fsd(l):
	s=0.
	m=sum(l)/len(l)
	for x in l:
		s+=(x-m)**2
	return math.sqrt(s/len(l))
def rate(d):
	c_begin, c_end, c_step = -5,  15, 2
	g_begin, g_end, g_step =  3, -15, -2
	maxacc=0
	pd={}
	while c_begin<c_end:
		g_begin=3
		while g_begin>g_end:
			pd[(c_begin,g_begin)]=[[],[],[],[]]
			g_begin+=g_step
		c_begin+=c_step
	c_begin, c_end = -5,  15
	g_begin, g_end =  3, -15
	while c_begin<c_end:
		g_begin=3
		while g_begin>g_end:
			TP=0.
			FN=0.
			TN=0.
			FP=0.
			#print len(d[(c_begin,g_begin)])
			for x in d[(c_begin,g_begin)]:
				if (x[0]=="1" or x[0]=="+1") and (x[1]=="+1" or x[1]=="1"):
					TP+=1
				elif x[0]=="-1" and x[1]=="-1":
					TN+=1
				elif (x[0]=="1" or x[0]=="+1") and x[1]=="-1":
					FP+=1
				elif x[0]=="-1"	and (x[1]=="+1" or x[1]=="1"):
					FN+=1
			if float(TP+FN)==0:
				Sn=0
			else:
				Sn=float(TP)/float(TP+FN)
			Sp=float(TN)/float(TN+FP)
			Acc=float(TP+TN)/float(TP+FP+TN+FN)
			if ((TN+FN)*(TN+FP)*(TP+FN)*(TP+FP))**(1.0/2)==0:
				Mcc=0
			else:
				Mcc=float(TP*TN-FP*FN)/((TN+FN)*(TN+FP)*(TP+FN)*(TP+FP))**(1.0/2)
			print "c=%s,g=%s"%(2.0**c_begin,2.0**g_begin)
			print "Sn=%s,Sp=%s,Acc=%s,Mcc=%s"%(Sn,Sp,Acc,Mcc)
			pd[(c_begin,g_begin)][0].append(Sn)
			pd[(c_begin,g_begin)][1].append(Sp)
			pd[(c_begin,g_begin)][2].append(Acc)
			pd[(c_begin,g_begin)][3].append(Mcc)
			g_begin+=g_step
		c_begin+=c_step
	"""
			if Acc>maxacc:
				maxacc=Acc
				bSn=Sn
				bSp=Sp
				bMcc=Mcc
				bestc=c_begin
				bestg=g_begin
			g_begin+=g_step
		c_begin+=c_step
	print "best c=%s,g=%s,Sn=%s,Sp=%s,Acc=%s,Mcc=%s"%(2**bestc,2**bestg,bSn,bSp,maxacc,bMcc)
	return [bestc,bestg]
	"""
	return pd
def grid(v):
	global t
	d={}
	roc={}
	col=[]
	c_begin, c_end, c_step = -5,  15, 2
	g_begin, g_end, g_step =  3, -15, -2
	while c_begin<c_end:
		g_begin=3
		while g_begin>g_end:
			d[(c_begin,g_begin)]=[]
			roc[(c_begin,g_begin)]=[]
			g_begin+=g_step
		c_begin+=c_step
	
	for x in range(v):
		c_begin, c_end = -5,  15
		g_begin, g_end =  3, -15
		train=open("train."+str(t)+".pro."+str(x+1),"w")
		os.system("cat %s %s >%s"%("prope."+str(t)+"."+str(x+1),"prone."+str(t)+"."+str(x+1),"testpro."+str(t)+"."+str(x+1)))
		for y in range(v):
			if x==y:continue
			for line in open("prope."+str(t)+"."+str(y+1)):
				train.write(line)
			for line in open("prone."+str(t)+"."+str(y+1)):
				train.write(line)
		train.close()#this is important
		while c_begin<c_end:
			g_begin=3
			while g_begin>g_end:
				os.system("../svm-train -h 0 -c %s -g %s %s %s"%(2.0**c_begin,2.0**g_begin,"train."+str(t)+".pro."+str(x+1),"train.pro."+str(t)+"."+str(x+1)))
				out=os.popen("../svm-predict %s %s %s"%("testpro."+str(t)+"."+str(x+1),"train.pro."+str(t)+"."+str(x+1),"resultpro."+str(t)+"."+str(x+1)))
				p=out.readlines()
				print p[-1].rstrip()
				zf=[]
				for k in open("testpro."+str(t)+"."+str(x+1)):
					k.rstrip()
					m=re.search("(.*?)\s",k)
					zf.append(m.group(1))
				for j in range(len(p)-1):
					roc[(c_begin,g_begin)].append((p[j],zf[j]))
				d[(c_begin,g_begin)]+=collect("testpro."+str(t)+"."+str(x+1),"resultpro."+str(t)+"."+str(x+1))
				g_begin+=g_step
			c_begin+=c_step
	return [rate(d),roc]
"""	
	cg=rate(d)
	for x in roc[cg[0],cg[1]]:
		x=x.rstrip()
		print x
"""
def vfold(v,pf,nf):
	global t
	p=open(pf).readlines()
	n=open(nf).readlines()
	pnum=len(p)/v
	nnum=len(n)/v
	tempp="tempp."+str(t)
	tempn="tempn."+str(t)
	os.system("cp %s %s"%(pf,tempp))
	os.system("cp %s %s"%(nf,tempn))
	ptemp="prope."+str(t)+"."+str(v)
	ntemp="prone."+str(t)+"."+str(v)
	for x in range(v-1):
		pft="prope."+str(t)+"."+str(x+1)
		nft="prone."+str(t)+"."+str(x+1)
		os.system("./subset.py -s 1 %s %s %s %s"%(tempp,pnum,pft,ptemp))
		os.system("./subset.py -s 1 %s %s %s %s"%(tempn,nnum,nft,ntemp))
		os.system("cp %s %s"%(ptemp,tempp))
		os.system("cp %s %s"%(ntemp,tempn))
if __name__=="__main__":
	#fil=sys.argv[3] #notice
	#kf=open(fil+"jieguo","w")
	t=time.time()
	pf=sys.argv[1]
	#nf="nf."+str(t)
	nfkz=sys.argv[2]
	#allne=sys.argv[2]
	kf=open(nfkz+"jieguo","w")
	for x in range(1,2):#add negative need change
		rocf=open("roc"+nfkz+"."+str(x),"w")
		r={}
		thres={}
		c_begin, c_end, c_step = -5,  15, 2
		g_begin, g_end, g_step =  3, -15, -2
		while c_begin<c_end:
			g_begin=3
			while g_begin>g_end:
				r[(c_begin,g_begin)]=[[],[],[],[]]
				thres[(c_begin,g_begin)]=[]
				g_begin+=g_step
			c_begin+=c_step
		maxacc=0
		for y in range(1,11):#repeat need change
			nf="../../format/ne2310/"+str(y)+"."+nfkz
			#os.system("../../format/randomall2.py %s %s >%s"%(allne,k,nf))
			vfold(10,pf,nf)
			d=grid(10)
			c_begin, c_end, c_step = -5,  15, 2
			g_begin, g_end, g_step =  3, -15, -2
			while c_begin<c_end:
				g_begin=3
				while g_begin>g_end:
					thres[(c_begin,g_begin)]+=d[1][(c_begin,g_begin)]
					for i in range(4):
						r[(c_begin,g_begin)][i]+=d[0][(c_begin,g_begin)][i]
					g_begin+=g_step
				c_begin+=c_step
		c_begin, c_end = -5,  15
		g_begin, g_end =  3, -15
		while c_begin<c_end:
			g_begin=3
			while g_begin>g_end:
				Sn=sum(r[(c_begin,g_begin)][0])/len(r[(c_begin,g_begin)][0])
				Sp=sum(r[(c_begin,g_begin)][1])/len(r[(c_begin,g_begin)][1])
				Acc=sum(r[(c_begin,g_begin)][2])/len(r[(c_begin,g_begin)][2])
				Mcc=sum(r[(c_begin,g_begin)][3])/len(r[(c_begin,g_begin)][3])
				sdSn=fsd(r[(c_begin,g_begin)][0])
				sdSp=fsd(r[(c_begin,g_begin)][1])
				sdAcc=fsd(r[(c_begin,g_begin)][2])
				sdMcc=fsd(r[(c_begin,g_begin)][3])
				if Acc>maxacc:
					maxacc=Acc
					bestc=c_begin
					bestg=g_begin
					bSp=Sp
					bSn=Sn
					bMcc=Mcc
					bsdSp=sdSp
					bsdSn=sdSn
					bsdAcc=sdAcc
					bsdMcc=sdMcc
				g_begin+=g_step
			c_begin+=c_step
		kf.write("best c=%s,g=%s,Sp=%s+-%s,Sn=%s+-%s,Acc=%s+-%s,Mcc=%s+-%s\n"%(2**bestc,2**bestg,bSp,bsdSp,bSn,bsdSn,maxacc,bsdAcc,bMcc,bsdMcc))
		print "best c=%s,g=%s,Sp=%s+-%s,Sn=%s+-%s,Acc=%s+-%s,Mcc=%s+-%s"%(2**bestc,2**bestg,bSp,bsdSp,bSn,bsdSn,maxacc,bsdAcc,bMcc,bsdMcc)
		#print len(thres[(bestc,bestg)])
		area=auc(thres[(bestc,bestg)],rocf)
		kf.write(str(area)+"\n")
		print area

