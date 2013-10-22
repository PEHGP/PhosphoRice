#!/usr/bin/python2.7
# header need change
import re,os,urllib2,time,sys
from multiprocessing import Process, Queue
t1=time.time() #seconds since 1/1/1970 00:00:00
def request_tools(url,param):
	p=os.popen("curl -m 900 -d \"%s\" %s"%(param,url))
	return p.readlines()
def netphosk(seq,threshold):
	flag=0
	flag2=0
	url = "http://www.cbs.dtu.dk/cgi-bin/nph-webface"
	param="configfile=/usr/opt/www/pub/CBS/services/NetPhosK-1.0/NetPhosK.cf&SEQPASTE=%s&method=--no-ess&threshold=%s"%(seq,threshold)
	s=request_tools(url,param)
	for x in s:
		m=re.search("href=\"(.*?)\"",x)
		if m:
			#print m.group(1)
			r=urllib2.urlopen(m.group(1))
			flag=1
			break
	if flag==0:
		return "error"
	else:
		for x in r.readlines():
			x=x.rstrip()
			m=re.search("[STY]-(\d+)\s+\w+\s+(.*)",x)
			if m:
				print m.group(1),m.group(2)

def netphos2(seq,q,finfor):
	#t1=time.time()
	url="http://www.cbs.dtu.dk/cgi-bin/nph-webface"
	param="configfile=/usr/opt/www/pub/CBS/services/NetPhos-2.0/NetPhos.cf&SEQPASTE=%s&Tyrosine=ps&Serine=ps&Threonine=ps"%seq
	s=request_tools(url,param)
	res=[]
	ok=0
	for x in s:
		m=re.search("href=\"(.*?)\"",x)
		time.sleep(5)
		if m:
			r=urllib2.urlopen(m.group(1))
			for x in r.readlines():
				x=x.rstrip()
				m=re.search("^626\s+(\d+).*?(\*[STY]\*)",x)
				if m:
					a=m.group(1)
					b=m.group(2)
					#print a,b
					res.append(a)
				m=re.search("</html>",x)
				if m:
					ok=1
			break

	#t2=time.time()
	#print "netphos2:"+str(t2-t1)
	if ok==0:
		finfor.write("Netphos2-----------------------------Failed\n")
		finfor.flush()
		res.append("failed")
		q.put(res)
	else:
		q.put(res)
		finfor.write("Netphos2-----------------------------OK\n")
		finfor.flush()
def kinsephos2_80(seq,q,finfor):
	#t1=time.time()
	l=[]
	url='http://kinasephos2.mbc.nctu.edu.tw/predict.php'
	param="SEQ=%s&probability_b=2&S_KINASE_COM[]=S_AKT1&S_KINASE_COM[]=S_DNA-PK&S_KINASE_COM[]=S_PKA&S_KINASE_COM[]=S_AMPK&S_KINASE_COM[]=S_GRK&S_KINASE_COM[]=S_PKB&S_KINASE_COM[]=S_ATM&S_KINASE_COM[]=S_GSK-3&S_KINASE_COM[]=S_PKC&S_KINASE_COM[]=S_Aurora&S_KINASE_COM[]=S_IKK&S_KINASE_COM[]=S_PKG&S_KINASE_COM[]=S_CaM&S_KINASE_COM[]=S_IPL1&S_KINASE_COM[]=S_PLK1&S_KINASE_COM[]=S_CDC2&S_KINASE_COM[]=S_MAPK&S_KINASE_COM[]=S_RSK&S_KINASE_COM[]=S_CDK&S_KINASE_COM[]=S_MAPKAPK2&S_KINASE_COM[]=S_STK4&S_KINASE_COM[]=S_CHK1&S_KINASE_COM[]=S_PAK1&S_KINASE_COM[]=S_CHK2&S_KINASE_COM[]=S_PAK2&S_KINASE_COM[]=S_CK1&S_KINASE_COM[]=S_PDK&S_KINASE_COM[]=S_CK2&S_KINASE_COM[]=S_PHK&T_KINASE_COM[]=T_CaM&T_KINASE_COM[]=T_GRK&T_KINASE_COM[]=T_PKB&T_KINASE_COM[]=T_CDC2&T_KINASE_COM[]=T_GSK-3&T_KINASE_COM[]=T_PKC&T_KINASE_COM[]=T_CDK&T_KINASE_COM[]=T_LKB1&T_KINASE_COM[]=T_PLK1&T_KINASE_COM[]=T_CK1&T_KINASE_COM[]=T_MAPK&T_KINASE_COM[]=T_ROCK&T_KINASE_COM[]=T_CK2&T_KINASE_COM[]=T_PDK&T_KINASE_COM[]=T_DAPK&T_KINASE_COM[]=T_PKA&Y_KINASE_COM[]=Y_Abl&Y_KINASE_COM[]=Y_Fgr&Y_KINASE_COM[]=Y_MET&Y_KINASE_COM[]=Y_ALK&Y_KINASE_COM[]=Y_Fyn&Y_KINASE_COM[]=Y_PDGFR&Y_KINASE_COM[]=Y_BTK&Y_KINASE_COM[]=Y_Hck&Y_KINASE_COM[]=Y_Ret&Y_KINASE_COM[]=Y_CSK&Y_KINASE_COM[]=Y_IGF1R&Y_KINASE_COM[]=Y_Src&Y_KINASE_COM[]=Y_EGFR&Y_KINASE_COM[]=Y_INSR&Y_KINASE_COM[]=Y_Syk&Y_KINASE_COM[]=Y_EPH&Y_KINASE_COM[]=Y_IR&Y_KINASE_COM[]=Y_TRK&Y_KINASE_COM[]=Y_FAK&Y_KINASE_COM[]=Y_JAK2&Y_KINASE_COM[]=Y_TYK2&Y_KINASE_COM[]=Y_Fes&Y_KINASE_COM[]=Y_Lck&Y_KINASE_COM[]=Y_ZAP70&Y_KINASE_COM[]=Y_FGFR1&Y_KINASE_COM[]=Y_Lyn"%seq
	s=request_tools(url,param)
	ok=0
	for x in s:
		x=x.rstrip()
		m=re.search('<font color=\"\#999999\" face=\"Courier New, Courier, mono\" size=\"2\">(\d+)</font>',x)
		if m:
			lo=m.group(1)
			if not lo in l:
				#print lo
				l.append(lo)
		m=re.search("</html>",x)
		if m:
			ok=1
	#t2=time.time()
	#print "kinsephos2_80:"+str(t2-t1)

	if ok==0:
		finfor.write("Kinsephos2_80-----------------------------Failed\n")
		finfor.flush()
		l.append("failed")
		q.put(l)
	else:
		q.put(l)
		#print l
		finfor.write("Kinsephos2_80-----------------------------OK\n")
		finfor.flush()
def test(seq):
	url="http://localhost/hlx/kcgi/predict.php"
	param="SEQ=%s&kemail=bigkk913@126.com"%seq
	s=request_tools(url,param)
	print s
def kinsephos(seq,sp,q,finfor):
	#t1=time.time()
	l=[]
	url="http://kinasephos.mbc.nctu.edu.tw/predict.php"
	param="SEQ=%s&TYPE[]=S&TYPE[]=T&TYPE[]=Y&filter_type=Sp&Sp_value=%s&KINASE=PKC,PKA,CKII,CaM-II,PKG,CKI,cdc2,MAPK,EGFR,Src,INSR,CDK,ATM,IKK,PKB,Abl,Syk,Jak,Other_MDD"%(seq,sp)
	s=request_tools(url,param)
	ok=0
	for x in s:
		x=x.rstrip()
		m=re.search('<font color=\"\#999999\" face=\"Courier New, Courier, mono\" size=\"2\">(\d+)</font>',x)
		if m:
			lo=m.group(1)
			if not lo in l:
				#print lo
				l.append(lo)
		m=re.search("</html>",x)
		if m:
			ok=1
	#t2=time.time()

	#print "kinsephos:"+str(t2-t1)
	if ok==0:
		finfor.write("Kinsephos_"+str(sp)+"-----------------------------Failed\n")
		finfor.flush()
		l.append("failed")
		q.put(l)
	else:
		q.put(l)
		#print l
		finfor.write("Kinsephos_"+str(sp)+"-----------------------------OK\n")
		finfor.flush()
def disphos(seq,org,q,finfor):#org=0=default,org=1=euk,org=ala
	#t1=time.time()
	res=[]
	ok=0
	url="http://www.dabi.temple.edu/disphos/pred/predict"
	if org=="ala":
		param="seq=%s&org=1&genome=6"%seq
	else:
		param="seq=%s&org=%s"%(seq,org)
	s=request_tools(url,param)
	for x in s:
		x=x.rstrip()
		m=re.search('<tr><td>(\d+)</td><td>\w+</td><td>.*?</td><td><span class=\"seq\">\w+<span class=\"\w+\">\w+</span>\w+</span></td><td><span cls=\"yes\">(YES)</span></td></tr>',x)
		if m:
			a=m.group(1)
			b=m.group(2)
			res.append(a)
			#print a,b
		m=re.search("</html>",x)
		if m:
			ok=1

	#t2=time.time()
	#print "disphos:"+str(t2-t1)
	if ok==0:
		finfor.write("Disphos_"+str(org)+"-----------------------------Failed\n")
		finfor.flush()
		res.append("failed")
		q.put(res)
	else:
		q.put(res)
		finfor.write("Disphos_"+str(org)+"-----------------------------Ok\n")
		finfor.flush()
def scansite(seq,leve,q,finfor):
	#t1=time.time()
	l=[]
	ok=1
	url="http://scansite.mit.edu/cgi-bin/motifscan_seq"
	param="protein_id=626&sequence=%s&stringency=%s&motif_option=all"%(seq,leve)
	s=request_tools(url,param)
	for x in s:
		m=re.search("<tr><td>[STY](\d+)</td><td>",x)
		if m:
			lo=m.group(1)
			if not lo in l:
				#print lo
				l.append(lo)
		m=re.search("</html>",x)
		if m:
			ok=1

	#t2=time.time()
	#print "scansite:"+str(t2-t1)
	if ok==0:
		finfor.write("Scansite_"+str(leve)+"-----------------------------Failed\n")
		finfor.flush()
		l.append("failed")
		q.put(l)
	else:
		finfor.write("Scansite_"+str(leve)+"-----------------------------OK\n")
		finfor.flush()
		q.put(l)
def formatseq(seq,pos,f):
	l=len(seq)
	al=(l/80+1)*80
	c=0
	for x in seq:
		c+=1
		if c==l:
			if c in pos:
				f.write("<font color=red>"+x+"</font>"+" "*(al-len(seq))+" "+str(c).rjust(4)+"<br/>")
			else:
				f.write(x+" "*(al-len(seq))+" "+str(c).rjust(4)+"<br/>")
		elif c%80==0 and c!=l:
			if c in pos:
				f.write("<font color=red>"+x+"</font>"+" "+str(c).rjust(4)+"<br/>")
			else:
				f.write(x+" "+str(c).rjust(4)+"<br/>")
		else:
			if c in pos:
				f.write("<font color=red>"+x+"</font>")
			else:
				f.write(x)
if __name__=="__main__":
	seq=sys.argv[1] #need change
	#fi="123"
	fi=sys.argv[2] #file name need change
	finfor=open("infor"+fi,"w")
	#name="626"
	name=sys.argv[3] #seq name need change
	f=open(fi,"w")
	ftr=open(fi+"track","w")
	h="""<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\"
  \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">
<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang="en" lang=\"en\">

<head>
	<title>results</title>
	<meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\" />
	<meta name=\"generator\" content=\"Geany 0.18\" />
</head>

<body bgcolor="#f8f8f8"><pre>"""
	f.write(h)

	#seq="MSTWQLFPDSSGDGFRWEVAGRILQSVSDSTPTKALESTAPLPSMADLLLQGCSKLIAREEAMPGEIPMFRTGLGKSVVLKESSIAKAKSILAEKVTYSDLRNTNCSIPQMRQVDTAETLPMFRTASGKSVPLKESSIAKAMSILGSDKIIDSDNVLPRESGFGVSNSLFQTASNKKVNVSSAGLARAKALLGLEEDDLNGFNHVNQSSSSSQQHGWSGLKTHEEFDATVVKHHSGTPGQYEDYVSGKRSEVLNPSLKVPPTKFQTAGGKSLSVSAEALKRARNLLGDPELGSFFDDVAGGDQFFTPEKDERLSDIAINNGSANRGYIAHEEKTSNKHTPNSFVSPLWSSSKQFSSVNLENLASGGNLIKKFDAAVDETDCALNATHGLSNNRSLASDMAVNNSKVNGFIPRGRQPGRPADQPLVDITNRRDTAYAYNKQDSTQKKRLGKTVSVSPFKRPRISSFKTPSKKHALQASSGLSVVSCDTLTSKKVLSTRYPEKSPRVYIKDFFGMHPTATTRMDYVPDHVRRIKSSNADKYVFCDESSSNKVGAETFLQMLAESEKVCDRSFEACMWIVWKLACYDIYYPAKCRGNFLTITNVLEELKYRYEREVNHGHCSAIKRILSGDAPASSMMVLCISAINPKTDNDSQEAHCSDSCSNVKVELTDGWYSMNAALDVVLTKQLNAGKLFVGQKLRILGAGLSGWATPTSPLEAVISSTICLLLNINGTYRAHWADRLGFCKEIGVPLALNCIKCNGGPVPKTLAGIKRIYPILYKERLGEKKSIVRSERIESRIIQLHNQRRSALVEGIMCEYQRGINGVHSQNDTDSEEGAKIFKLLETAAEPEFLMAEMSPEQLRSFTTYKAKFEAAQQMRKEKSVAETLEDAGLGERNVTPFMRIRLVGLTSLSYEGEHNPKEGIVTIWDPTERQRTELTEGKIYMMKGLVPINSDSEILYLHARGSSSRWQPLSPKDSENFQPFFNPRKPISLSNLGEIPLSSEFDIAAYVVYVGNAYTDVLQKKQWVFVTDGSAQHSGEISNSLLAISFSTSFMDDSSVSHISHNLVGSVVGFCNLIKRAKDVTNEIWVAEAAENSVYFINAEAAYSSHLKTSSAHIQTWAKLSSSKSVRSRRLPLSIIIRVLSIIGACPSGLNSPDKCRAFNFFWSHSTLKLPHTAFQNRAMRVADKPP"
	d={}
	q={}
	sty={}
	for x in range(1,12):
		q[x]=Queue()
	count=0
	for x in list(seq):
		count+=1
		if x.upper()=="S" or x.upper()=="T" or x.upper()=="Y":
			d[count]=[0,0,0,0,0,0,0,0,0,0,0]
			sty[count]=x.upper()
	#netphosk(">626\n"+seq,0.50) #no use
	#netphosk(">626\n"+seq,0.70) #no use
	p=Process(target=netphos2,args=(">626\n"+seq,q[1],finfor))#1 w=1.23
	p.start()
	p=Process(target=kinsephos2_80, args=(">626\n"+seq,q[2],finfor))#2 w=0.71
	p.start()
	#test(seq)
	p=Process(target=kinsephos,args=(">627\n"+seq,90,q[3],finfor))#3 w=2.76
	p.start()
	p=Process(target=kinsephos,args=(">628\n"+seq,95,q[4],finfor))#4 w=0.79
	p.start()
	#kinsephos(">626\n"+seq,100) #no use
	p=Process(target=kinsephos,args=(">629\n"+seq,"default",q[5],finfor))#5 w=2.75
	p.start()
	p=Process(target=disphos,args=(">626\n"+seq,"ala",q[6],finfor))#6 w=2.22
	p.start()
	p=Process(target=disphos,args=(">626\n"+seq,0,q[7],finfor))#7 w=4.25
	p.start()
	p=Process(target=disphos,args=(">626\n"+seq,1,q[8],finfor))#8 w=1.65
	p.start()
	p=Process(target=scansite,args=(seq,"Low",q[9],finfor))#9 w=3.9
	p.start()
	p=Process(target=scansite,args=(seq,"High",q[10],finfor))#10 w=2.57
	p.start()
	p=Process(target=scansite,args=(seq,"Medium",q[11],finfor))#11 w=1.6
	p.start()

	p.join()
	where_failed=[]
	for x in range(1,12):
		que=q[x].get()
		if que!=[]:
			if que[0]=="failed":
				where_failed.append(x)
				continue
		#print x
			for i in que:
				#print i
				i=int(i)
				d[i][x-1]=1
	order={1:"netphos2",2:"kinsephos2_80",3:"kinsephos_90",4:"kinsephos_95",5:"kinsephos_defa",6:"disphos_ala",7:"disphos_0",8:"disphos_1",9:"scansite_low",10:"scansite_high",11:"scansite_medium"}
	failed_num=len(where_failed)
	if failed_num==0:
		weight={1:1.23,2:0.71,3:2.76,4:0.79,5:2.75,6:2.22,7:4.25,8:1.65,9:3.90,10:2.57,11:1.60}
		sor=[]
		pos=[]
		f.write(" Position Score Amino_acid<br/>")
		f.write("--------------------------<br/>")
		for x in d.keys():
			score=0
			count=0
			for s in d[x]:
				count+=1
				score+=s*weight[count]
			if score>=11.47:
				sor.append((x,"%.2f"%score))
				pos.append(x)
		sor.sort()
		pos.sort()
		ps=0
		pt=0
		py=0
		for x in sor:
			f.write(str(x[0]).rjust(4)+"      "+str(x[1])+"     "+str(sty[x[0]]).rjust(2)+"<br/>")
			if sty[x[0]]=="S":
				ps+=1
			elif sty[x[0]]=="T":
				pt+=1
			elif sty[x[0]]=="Y":
				py+=1
			#print x[0],x[1],sty[x[0]]
		f.write("--------------------------<br/>")
		f.write("Potential phosphorylation sites:	Ser: %s	Thr: %s	Tyr: %s<br/><br/>"%(ps,pt,py))
		f.write("Sequence name: %s<br/>"%name)
		formatseq(seq,pos,f)
		t2=time.time()
		#print t2-t1
		ftr.write("success")
		ftr.close()
	elif failed_num==3 and 3 in where_failed and 4 in where_failed and 5 in where_failed:
		weight={1:1,2:3,3:0,4:0,5:0,6:3,7:1,8:0,9:1,10:1,11:1}
		sor=[]
		pos=[]
		f.write("Kinasephos is failed.The result used alternative strategies.<br/>")
		f.write(" Pos Score Pred<br/>")
		f.write("---------------<br/>")
		for x in d.keys():
			score=0
			count=0
			for s in d[x]:
				count+=1
				score+=s*weight[count]
			if score>=5:
				sor.append((x,"%.2f"%score))
				pos.append(x)
		sor.sort()
		pos.sort()
		ps=0
		pt=0
		py=0
		for x in sor:
			f.write(str(x[0]).rjust(4)+" "+str(x[1])+" "+str(sty[x[0]]).rjust(2)+"<br/>")
			if sty[x[0]]=="S":
				ps+=1
			elif sty[x[0]]=="T":
				pt+=1
			elif sty[x[0]]=="Y":
				py+=1
			#print x[0],x[1],sty[x[0]]
		f.write("---------------<br/>")
		f.write("Phosphorylation sites predicted:	Ser: %s	Thr: %s	Tyr: %s<br/><br/>"%(ps,pt,py))
		f.write("name: %s<br/>"%name)
		formatseq(seq,pos,f)
		ftr.write("Kinasephos_failed")
		ftr.close()
		#t2=time.time()
		#print t2-t1
	elif failed_num==1 and 2 in where_failed:
		weight={1:1,2:0,3:1,4:0,5:3,6:1,7:3,8:1,9:3,10:1,11:0}
		sor=[]
		pos=[]
		f.write("Kinasephos2_80 is failed.The result used alternative strategies.<br/>")
		f.write(" Pos Score Pred<br/>")
		f.write("---------------<br/>")
		for x in d.keys():
			score=0
			count=0
			for s in d[x]:
				count+=1
				score+=s*weight[count]
			if score>=8:
				sor.append((x,"%.2f"%score))
				pos.append(x)
		sor.sort()
		pos.sort()
		ps=0
		pt=0
		py=0
		for x in sor:
			f.write(str(x[0]).rjust(4)+" "+str(x[1])+" "+str(sty[x[0]]).rjust(2)+"<br/>")
			if sty[x[0]]=="S":
				ps+=1
			elif sty[x[0]]=="T":
				pt+=1
			elif sty[x[0]]=="Y":
				py+=1
			#print x[0],x[1],sty[x[0]]
		f.write("---------------<br/>")
		f.write("Phosphorylation sites predicted:	Ser: %s	Thr: %s	Tyr: %s<br/><br/>"%(ps,pt,py))
		f.write("name: %s<br/>"%name)
		formatseq(seq,pos,f)
		ftr.write("Kinasephos2_80_failed")
		ftr.close()
		#t2=time.time()
		#print t2-t1
	else:
		f.write("All failed.Please try again.<br/>")
		ftr.write("failed")
		ftr.close()
	f.write("</pre></body></html>")
	f.close()
