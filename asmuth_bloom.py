from sieve import Sieve
from functools import reduce



class Holder : 

	
	def __init__(self):
		self.modulo = 0
		self.secret = 0
		
		
	def __str___(self):
		return "Modulo = " + str(self.modulo) + " | Secret = " + str(self.secret)
		


class AsmuthBloom :
	
	def __init__(self,n_holders,min_holder,secret) :
		self.__sieve = Sieve()
		self.__n_holder = n_holders
		self.__min_holder = min_holder
		self.__holders = [Holder() for _ in range(n_holders)]
		self.__secret = secret
		self.__generateHolders()
	
	
	def __generateHolders(self):
		self.__generateSequence()
		self.__generateRandom()
		
		
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
	SSS = AsmuthBloom(number_of_holders,min_number_to_solve,secret)

		
	
	
main()
