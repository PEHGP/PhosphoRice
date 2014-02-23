#!/usr/bin/python
from predict import PhosphoRice

if __name__=="__main__":
	p=PhosphoRice(SeqName=name,Seq=seq)
	p.NetPhosk(0.5)#w=1
	p.NetPhosk2()#w=1
	p.Disphos(0)#w=3
	p.Disphos(1,genome=6)#w=3
	p.Kinsephos(90)#w=1
	p.Kinsephos(95)#w=1
	p.Kinsephos(100)#w=1
	p.Kinsephos2(2)#w=1
