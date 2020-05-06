from sieve import Sieve
from crt import chinese_remainder
import random


class Holder : 

	
	def __init__(self):
		self.modulo = 0
		self.secret = 0
		
		
	def __str__(self):
		return "Modulo = " + str(self.modulo) + " | Secret = " + str(self.secret)
		


class AsmuthBloom :
	
	def __init__(self,n_holders,min_holder,secret,verbose=False) :
		self.__verbose = verbose
		self.__sieve = Sieve()
		self.__n_holder = n_holders
		self.__min_holder = min_holder
		self.__holders = [Holder() for _ in range(n_holders)]
		self.__secret = secret
		self.__generateHolders()

	
	def __generateHolders(self):
		self.__generateSequence()
		self.__generateRandom()
		

		for i in range(self.__n_holder) :
			self.__holders[i].modulo = self.__sequence[i+1]
			self.__holders[i].secret = self.__y%self.__holders[i].modulo
			
	def __generateSequence(self):
	
		initial_multiplier = int(self.__secret/10);
		
		# Get first prime in sequence
		first_prime = self.__sieve.getFirstPrimeLargerThan(self.__secret)
		sequenceValid = False
		
		# Get the rest of sequence
		while not sequenceValid :
			current_sequence = [first_prime]
			temp_prime = self.__sieve.getFirstPrimeLargerThan(self.__secret*initial_multiplier)
			for _ in range(self.__n_holder) :
				temp_prime = self.__sieve.getFirstPrimeLargerThan(temp_prime)
				current_sequence.append(temp_prime)
			
			if self.__isSequenceValid(current_sequence):
				sequenceValid = True
			
			else : 
				initial_multiplier = initial_multiplier + 1
				
		
		self.__sequence = current_sequence
		self.__M = self.__seqprod(self.__sequence[1:self.__min_holder+1])
		
		if self.__verbose :
			print ("Sequence : " + str(self.__sequence))
			print("Big-M : " + str(self.__M))
	

	# Generate a random number
	def __generateRandom(self):
	
		max = int((self.__M - self.__secret)/self.__sequence[0])
		
		self.__random_number = random.randint(1,max)
		self.__y = self.__secret + self.__random_number*self.__sequence[0]
		
		if self.__verbose :
			print("Random number : " + str(self.__random_number))
			print("Y-value : " + str(self.__y))
		
		
	
	
	
	
	### UTILS
	def __isSequenceValid(self,seq):
		lower_product = self.__seqprod(seq[1:self.__min_holder+1])
		upper_product = seq[0]*self.__seqprod(seq[self.__n_holder - self.__min_holder + 2:])
	
		return lower_product > upper_product
		
		
	def getSequence(self):
		return self.__sequence
		
		
	def __seqprod(self,iterable):
		product = 1
		for item in iterable :
			product=product*item
			
		return product
		
	def getHolders(self):
		return self.__holders
		
	### Solver
	def solve(self):
	
		chosen_holders = random.sample(self.__holders,self.__min_holder)
		
		if self.__verbose :
			print("Chosen holders :")
			for holder in chosen_holders :
				print(holder)
		
		## Solver CRT
		modulo_list = [holder.modulo for holder in chosen_holders]
		remainder_list = [holder.secret for holder in chosen_holders]
		
		
		solution = chinese_remainder(modulo_list,remainder_list)
		if self.__verbose :
			print("CRT Solution : " + str(solution))			
		return (solution)%self.__sequence[0]
			
	
	# Find inverse
	# Assume coprime 
	# Using native methods. We can fix them later 
	def __inverse(self,multiplier,modulo) :
		for i in range(modulo):
			if ((multiplier*i)%modulo)==1 :
				return i
		
	
		

def main():

	sieve = Sieve()
	

	number_of_holders = int(input("Input number of holders : "))
	while number_of_holders<1 :
		number_of_holders = int(input("Number must be larger than one. Try again : "))
	min_number_to_solve = int(input("Input minimum number of holders to retrieve the secret : "))
	while min_number_to_solve>number_of_holders or min_number_to_solve < 1:
		min_number_to_solve = int(input("Number of minimum must be between 1 and number of holders. Try again : "))
	secret = int(input("Input secret : "))
	while secret < 0 :
		secret = int(input("Secret must not be less than zero. Try again :"))
	
	# SSS Object
	SSS = AsmuthBloom(number_of_holders,min_number_to_solve,secret,verbose=True)
	
	# Sequence
	print("Sequence")
	for sequence in SSS.getSequence():
		print(sequence)
		
	
	# Print holders
	for holder in SSS.getHolders():
		print(holder)
		
	# Solve secret
	# For now choice is totally random
	secret = SSS.solve()
	
	print(secret)

main()
