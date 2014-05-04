#!/usr/bin/env python
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2,time,re,sys
class PhosphoRice:
	def __init__(self,SeqName="",Seq="",SeqFile=""):
		register_openers()#important
		self.Seq=Seq
		self.SeqName=SeqName
		self.SeqFile=SeqFile
		self.proname=sys.argv[0]
	def NetPhosk(self,threshold,method="--no-ess"):#At most 10 sequences and 10,000 amino acids per submission; each sequence not less than 15 and not more than 4,000 amino acids.threshold:0.00-0.95,step=0.05;metho:--no-ess:Prediction without filtering (fast),--ess:rediction with ESS(Evolutionary Stable Sites) Filter (very slow),--cgi:Kinase Landscapes (Graphics)
		r={}
		if self.SeqFile:
			param={"configfile":"/usr/opt/www/pub/CBS/services/NetPhosK-1.0/NetPhosK.cf","SEQSUB":open(self.SeqFile,"rb"),"method":method,"threshold":threshold}
		else:
			param={"configfile":"/usr/opt/www/pub/CBS/services/NetPhosK-1.0/NetPhosK.cf","SEQPASTE":">"+self.SeqName+"\n"+self.Seq,"method":method,"threshold":threshold}
		datagen, headers = multipart_encode(param)
		request = urllib2.Request("http://www.cbs.dtu.dk/cgi-bin/nph-webface", datagen, headers)
		try:
			l=urllib2.urlopen(request).readlines()
		except urllib2.URLError:
			print "\nNetPhosk web may be not work.\n"
			sys.exit(1)
		u="http://www.cbs.dtu.dk"+l[1].split(":")[1].rstrip().replace(" ","")
		if "predict.py" in self.proname or "test" in self.proname:
			print u
		c=urllib2.urlopen(u).readlines()
		flag=1
		t=0
		while flag and t<=50:
			t+=1
			if "<pre>\n" in c:
				flag=0
			else:
				time.sleep(10)
				c=urllib2.urlopen(u).readlines()
		if t<=50:
			for x in c:
				x=x.rstrip()
				mm=re.search("Query:\s+(.*)",x)
				if mm:
					p=mm.group(1)
					r[p]=[]
					continue
				m=re.search("[STY]-(\d+)\s+(\w+)\s+(.*)",x)#group(1):position,group(2):kinase,group(3):score
				if m:
					r[p].append(m.group(1))
					if "predict.py" in self.proname or "test" in self.proname:
						print m.group(1),m.group(2),m.group(3)
		else:
			print "netphosk can't calculate results."
		return r
	def NetPhosk2(self,):#At most 50 sequences and 200,000 amino acids per submission; each sequence not more than 4,000 amino acids.
		r={}
		if self.SeqFile:
			param={"configfile":"/usr/opt/www/pub/CBS/services/NetPhos-2.0/NetPhos.cf","SEQSUB":open(self.SeqFile,"rb"),"Tyrosine":"ps","Serine":"ps","Threonine":"ps"}
		else:
			param={"configfile":"/usr/opt/www/pub/CBS/services/NetPhos-2.0/NetPhos.cf","SEQPASTE":">"+self.SeqName+"\n"+self.Seq,"Tyrosine":"ps","Serine":"ps","Threonine":"ps"}
		datagen, headers = multipart_encode(param)
		request = urllib2.Request("http://www.cbs.dtu.dk/cgi-bin/nph-webface", datagen, headers)
		try:
			l=urllib2.urlopen(request).readlines()
		except urllib2.URLError:
			print "\nNetPhosk2 web may be not work.\n"
			sys.exit(1)
		u="http://www.cbs.dtu.dk"+l[1].split(":")[1].rstrip().replace(" ","")
		if "predict.py" in self.proname or "test" in self.proname:	
			print u
		c=urllib2.urlopen(u).readlines()
		flag=1
		t=0
		while flag and t<=50:
			t+=1
			if "<pre>\n" in c:
				flag=0
			else:
				time.sleep(10)
				c=urllib2.urlopen(u).readlines()
		if t<=50:
			for x in c:
				x=x.rstrip()
				m=re.search("^(.*?)\s+(\d+)\s+.*?\s+(.*?)\s+(\*[STY]\*)",x)
				if m:
					a=m.group(1)#name
					b=m.group(2)#position
					c=m.group(3)#score
					d=m.group(4)#S|T|Y
					if "predict.py" in self.proname or "test" in self.proname:
						print a,b,c,d
					if not a in r:
						r[a]=[b]
					else:
						r[a].append(b)
		else:
			print "netphosk2 can't calculate results."
		return r
	def Kinsephos2(self,speci):#spec 1:Default,2:80%,3:90%,4:100%
		r={}
		param=[("probability_b",speci),("S_KINASE_COM[]","S_AKT1"),("S_KINASE_COM[]","S_DNA-PK"),("S_KINASE_COM[]","S_PKA"),("S_KINASE_COM[]","S_AMPK"),("S_KINASE_COM[]","S_GRK"),("S_KINASE_COM[]","S_PKB"),("S_KINASE_COM[]","S_ATM"),("S_KINASE_COM[]","S_GSK-3"),("S_KINASE_COM[]","S_PKC"),("S_KINASE_COM[]","S_Aurora"),("S_KINASE_COM[]","S_IKK"),("S_KINASE_COM[]","S_PKG"),("S_KINASE_COM[]","S_CaM"),("S_KINASE_COM[]","S_IPL1"),("S_KINASE_COM[]","S_PLK1"),("S_KINASE_COM[]","S_CDC2"),("S_KINASE_COM[]","S_MAPK"),("S_KINASE_COM[]","S_RSK"),("S_KINASE_COM[]","S_CDK"),("S_KINASE_COM[]","S_MAPKAPK2"),("S_KINASE_COM[]","S_STK4"),("S_KINASE_COM[]","S_CHK1"),("S_KINASE_COM[]","S_PAK1"),("S_KINASE_COM[]","S_CHK2"),("S_KINASE_COM[]","S_PAK2"),("S_KINASE_COM[]","S_CK1"),("S_KINASE_COM[]","S_PDK"),("S_KINASE_COM[]","S_CK2"),("S_KINASE_COM[]","S_PHK"),("T_KINASE_COM[]","T_CaM"),("T_KINASE_COM[]","T_GRK"),("T_KINASE_COM[]","T_PKB"),("T_KINASE_COM[]","T_CDC2"),("T_KINASE_COM[]","T_GSK-3"),("T_KINASE_COM[]","T_PKC"),("T_KINASE_COM[]","T_CDK"),("T_KINASE_COM[]","T_LKB1"),("T_KINASE_COM[]","T_PLK1"),("T_KINASE_COM[]","T_CK1"),("T_KINASE_COM[]","T_MAPK"),("T_KINASE_COM[]","T_ROCK"),("T_KINASE_COM[]","T_CK2"),("T_KINASE_COM[]","T_PDK"),("T_KINASE_COM[]","T_DAPK"),("T_KINASE_COM[]","T_PKA"),("Y_KINASE_COM[]","Y_Abl"),("Y_KINASE_COM[]","Y_Fgr"),("Y_KINASE_COM[]","Y_MET"),("Y_KINASE_COM[]","Y_ALK"),("Y_KINASE_COM[]","Y_Fyn"),("Y_KINASE_COM[]","Y_PDGFR"),("Y_KINASE_COM[]","Y_BTK"),("Y_KINASE_COM[]","Y_Hck"),("Y_KINASE_COM[]","Y_Ret"),("Y_KINASE_COM[]","Y_CSK"),("Y_KINASE_COM[]","Y_IGF1R"),("Y_KINASE_COM[]","Y_Src"),("Y_KINASE_COM[]","Y_EGFR"),("Y_KINASE_COM[]","Y_INSR"),("Y_KINASE_COM[]","Y_Syk"),("Y_KINASE_COM[]","Y_EPH"),("Y_KINASE_COM[]","Y_IR"),("Y_KINASE_COM[]","Y_TRK"),("Y_KINASE_COM[]","Y_FAK"),("Y_KINASE_COM[]","Y_JAK2"),("Y_KINASE_COM[]","Y_TYK2"),("Y_KINASE_COM[]","Y_Fes"),("Y_KINASE_COM[]","Y_Lck"),("Y_KINASE_COM[]","Y_ZAP70"),("Y_KINASE_COM[]","Y_FGFR1"),("Y_KINASE_COM[]","Y_Lyn"),("submit","Submit")]
		if self.SeqFile:
			param.append(("SEQFILE",open(self.SeqFile,"rb")))
		else:
			param.append(("SEQ",">"+self.SeqName+"\n"+self.Seq))
		datagen, headers = multipart_encode(param)
		request = urllib2.Request("http://kinasephos2.mbc.nctu.edu.tw/predict.php", datagen, headers)
		try:
			l=urllib2.urlopen(request,timeout=300).readlines()
		except urllib2.URLError:
			print "\nKinsephos2 web may be not work.\n"
			sys.exit(1)
		#print l
		for x in l:
			x=x.rstrip()
			mm=re.search("<a name=\'(.*?)\'",x)
			if mm:
				p=mm.group(1)
				r[p]=[]
				continue
			m=re.search('<font color=\"\#999999\" face=\"Courier New, Courier, mono\" size=\"2\">(\d+)</font>',x)
			if m:
				if "predict.py" in self.proname or "test" in self.proname:
					print m.group(1)
				r[p].append(m.group(1))
		if not r:
			print "kinsephos2 has no results."
		return r
	def Kinsephos(self,speci,kinase="PKC,PKA,CKII,CaM-II,PKG,CKI,cdc2,MAPK,EGFR,Src,INSR,CDK,ATM,IKK,PKB,Abl,Syk,Jak,Other_MDD"):#speci 100:100%,95:95%,90:90% kinase PKC,PKA,PKB,CKII,CDK,Cam-II,PKG,CKI,cdc2,ATM,IKK,MAPK,Jak,Abl,Syk,EGFR,Src,INSR
		r={}
		param=[("TYPE[]","S"),("TYPE[]","T"),("TYPE[]","Y"),("KINASE",kinase),("filter_type","Sp"),("Sp_value",speci)]
		if self.SeqFile:
			param.append(("SEQFILE",open(self.SeqFile,"rb")))
		else:
			param.append(("SEQ",">"+self.SeqName+"\n"+self.Seq))
		datagen, headers = multipart_encode(param)
		request = urllib2.Request("http://kinasephos.mbc.nctu.edu.tw/predict.php", datagen, headers)
		try:
			l=urllib2.urlopen(request,timeout=300).readlines()
		except urllib2.URLError:
			print "\nKinsephos web may be not work.\n"
			sys.exit(1)
		for x in l:
			x=x.rstrip()
			mm=re.search("<a name=\'(.*?)\'",x)
			if mm:
				p=mm.group(1)
				r[p]=[]
				continue
			m=re.search('<font color=\"\#999999\" face=\"Courier New, Courier, mono\" size=\"2\">(\d+)</font>',x)
			if m:
				r[p].append(m.group(1))
		if not r:
			print "Kinsephos has no results."
		return r
	def Disphos(self,org,genome="",func=""):#org 0:Default Predictor,1:Eukaryotes,2:Viruses,3:Bacteria,4:Archaea; genome 0:H.sapiens,1:M.musculus,2:R.norvegicus,3:C.elegans,4:S.cerevisiae,5:D.melanogaster,6:A.thaliana; func 0:regulation,1:cancer,2:cytoskeleton,3:membrane,4:ribosomal,5:inhibitors,6:transport,7:kinases,8:degradation,9:biosynthesis,10:metabolism,11:GPCRs
		r=[]
		param=[("org",org)]
		if genome:
			param.append(("genome",genome))
		if func:
			param.append(("func",func))
		if self.SeqFile:
			param.append(("seqfile",open(self.SeqFile,"rb")))
		else:
			param.append(("seq",">"+self.SeqName+"\n"+self.Seq))
		datagen, headers = multipart_encode(param)
		request = urllib2.Request("http://www.dabi.temple.edu/disphos/pred/predict", datagen, headers)
		try:
			l=urllib2.urlopen(request,timeout=300).readlines()
		except urllib2.URLError:
			print "\nDisphos web may be not work.\n"
			sys.exit(1)	
		for x in l:
			#print x
			m=re.search('<tr><td>(\d+?)</td><td>(.*?)</td><td>(.*?)</td><td><span class=\"seq\">.*?<span class=\".*?\">.*?</span>.*?</span></td><td><span cls=\"yes\">(YES)</span>',x)
			if m:
				a=m.group(1)#position
				b=m.group(2)#S/T/Y
				c=m.group(3)#score
				if "predict.py" in self.proname or "test" in self.proname:
					print a,b,c
				r.append(a)
		if not r:
			print "Disphos has no results."
		return r
	def ScanSite(self,stringency):#stringency:High,Medium,Low
		r=[]
		param=[("protein_id",self.SeqName),("sequence",self.Seq),("motif_option","all"),("stringency",stringency)]#need change
		datagen, headers = multipart_encode(param)
		request = urllib2.Request("http://scansite.mit.edu/cgi-bin/motifscan_seq", datagen, headers)
		try:
			l=urllib2.urlopen(request,timeout=300).readlines()
		except urllib2.URLError:
			print "\nScanSite web may be not work.\n"
			sys.exit(1)
		for x in l:
			m=re.search("<tr><td>([STY])(\d+)</td><td><a href=.*?>(.*?)</a>",x)
			if m:
				a=m.group(1)#site
				b=m.group(2)#position
				c=m.group(3)#score
				if "predict.py" in self.proname or "test" in self.proname:
					print a,b,c
				r.append(b)
		if not r:
			print "Scansite has no results."
		return r
if __name__=="__main__":
	seq="MGSGPRGALSLLLLLLAPPSRPAAGCPAPCSCAGTLVDCGRRGLTWASLPTAFPVDTTELVLTGNNLTALPPGLLDALPALRTAHLGANPWRCDCRLVPLRAWLAGRPERAPYRDLRCVAPPALRGRLLPYLAEDELRAACAPGPLCWGALAAQLALLGLGLLHALLLVLLLCRLRRLRARARARAAARLSLTDPLVAERAGTDES"
	name="kuan"
	p=PhosphoRice(SeqName=name,Seq=seq)
	#r=p.NetPhosk(0.5)
	#r=p.Kinsephos(90)
	#r=p.Disphos(1,genome=6)
	#r=p.Kinsephos2(1)
	r=p.ScanSite("Low")
	print r
