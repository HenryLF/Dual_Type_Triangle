from dataclasses import dataclass
import pandas as pd
from itertools import combinations,groupby
from progress.bar import Bar
type_chart = pd.read_csv("type_chart.csv",index_col = 0)
type_list = list(type_chart.columns)
all_neutral = [{1.0} ,{1.0} ,{1.0} ]
def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)
@dataclass
class type_triangle:
	a : (str,str)
	b: (str,str)
	c : (str,str)
	def iter1(self) :
		yield self.a,self.b
		yield self.b,self.c
		yield self.c,self.a
	def iter2(self) :
		yield self.a,self.c
		yield self.c,self.b
		yield self.b,self.a
		
	def attack(self, Reverse = False):
		iter_  = self.iter2 if Reverse else self.iter1 
		out = []
		for atk,tgt in iter_() :
			damage_multiplier =set() #i don't care which is primary and secondary type
			for a in atk:
				damage_multiplier.add( type_chart[tgt[0]][a] *type_chart[tgt[1]][a] )
			out.append(damage_multiplier)
		return out
	def is_not_pertinent(self) : #check if both orientation are "all neutral"
		return self.attack()==all_neutral and self.attack(Reverse = True)==all_neutral
		
	def is_valid(self) : #check if (at least) one of the triangle orientation is valid
		#discard all onsided "all neutral" triangle
		#this is done by checking first if the other side is valid
		#(it cannot be all neutral because of the 
		#is_not_pertinent check)
		#in order to avoid discarding a "only atk" or 
		#"only def" triangle
		
		if self.attack() == all_neutral :
			return all_equal(self.attack(Reverse = True))
		if self.attack(Reverse = True) == all_neutral :
			return all_equal(self.attack())
		return all_equal(self.attack()) or all_equal(self.attack(Reverse = True))
	
	def is_perfect(self) : #check if both orientation are valid
		return all_equal(self.attack()) and all_equal(self.attack(Reverse = True))
	
all_dual_type = combinations(type_list,2)
All_triangle = [type_triangle(a,b,c) for a,b,c in combinations(all_dual_type,3)]

Perfect = []
Valid = []
bar = Bar('Processing', max=len(All_triangle))
for triangle in All_triangle:
	bar.next()
	if triangle.is_not_pertinent() : continue #ignore all neutral
	if triangle.is_perfect() : #pick perfect
		print("Perfect")
		print(triangle)
		print(f'{triangle.attack()=}\n{triangle.attack(Reverse = True)=}')
		Perfect.append(triangle)
#	if triangle.is_valid() : #pick valid
#		print("Valid")
#		print(triangle)
#		print(f'{triangle.attack()=}\n{triangle.attack(Reverse = True)=}')
#		Valid.append(triangle)
#bar.finish()

with open('Valid.txt','w') as f :
	for i in Valid :
		f.write(f'{i}\t{i.attack()}\t{i.attack(Reverse = True)}\n')
with open('Perfect.txt','w') as f :
	for i in Perfect :
		f.write(f'{i}\t{i.attack()[0]=}\t{i.attack(Reverse = True)[0]}\n')
