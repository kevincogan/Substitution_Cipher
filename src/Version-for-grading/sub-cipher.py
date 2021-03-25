import re
import string
import time
import sys
from multiprocessing import *
characters = "1234567890@%#'$[]/()*:,!;-_\n.?}{`<>+&‘—”“’" + '"=£éàêöêôæñ'

#This module takes all takes the string of all non english letters and non alphabetical characters and replaces the cipher text with nothing effectively removing the character from the cipher text.
def strip_punctuation(attempt):
	for char in characters:
		if char in attempt:
			attempt = attempt.replace(char, "")
	return attempt

#This counts the frequency of all the letters in the cipher text and stores them in a dictions.
def frequency_analysis(input):
	distribution_freq = {}
	for char in input:
		if char not in distribution_freq:
			distribution_freq[char] = 1

		else:
			distribution_freq[char] += 1
	return distribution_freq


#This module finds the most frequent letter E and assigns the most frequent letter to E. A capital E now replaces the associated cipher letter in the cipher text.
def single_letter(attempt, freq_single_letters, q, letters_in_uses,original_letter,lock):
	attempt = attempt.lower()#this splits the cipher text into a list so it can be processed.
	sorted_freq_letters = sorted(freq_single_letters,key=freq_single_letters.get, reverse=True) #This orders the the most frequent cipher letters into a list from the most frequent to least frequent.
	sorted_freq_letters.remove(" ") #This spaces from the frequency list.
	lock.acquire() #This puts a lock in place so any other processes running in paralell do not add to the queue at the same time causing error.
	letters_in_uses.put("E") #Adds the newly assigned letter to the queue.
	original_letter.put(sorted_freq_letters[0])#Adds the replaced letter to the queue.
	lock.release() #This realeases the lock and allows other module to add to the queue.

def single_letter_word(attempt, q,letters_in_uses, original_letter,lock):
	attempt1 = attempt.strip().split() # Splits the cipher text into a list.
	one_letter_word = [] # All the one letter words are added to this list.
	access_1 = 0 #This acts as a flag and grants access if the value is changed to 1.
	access_2 = 0 #This acts as a flag and grants access if the value is changed to 1.
	i = 0
	while (i != len(attempt1)): #This while loop finds all the single letter words and adds them to the list above.
		if len(attempt1[i]) == 1  and attempt1[i].isalpha():
			one_letter_word.append(attempt1[i])
		i = i + 1

	if len(one_letter_word) != 0: #Checks to see if  the list is empty. If it is empty it skips it.
		freq_of_one_letter_words = frequency_analysis(one_letter_word) # finds the frequency of the list inputted.
		most_freq = sorted(freq_of_one_letter_words,key=freq_of_one_letter_words.get, reverse=True) #Orders the dictionary into a list from most to least frequent.

		used_1 = "A" 
		original_1 = most_freq[0]
		access_1 = 1 #Changes flag to 1 which enable the the value above to be added to the queue unless it is change again below.

		if len(most_freq) > 1: #If most_freq has more than 1 letter in the list it means that the second letter will more than likely be I.
			used_2 = "I"
			original_2 = most_freq[1]
			access_2 = 1 #Changes flag to 1 and allows access for it to add to the queue below unless it is changed below.

	attempt1 = attempt.strip().split()
	new_one_letter_word = []
	i = 0
	while (i != len(attempt1)): #This finds all the one letter words that appear infront of a full stop. It is more likely to have an I.
		if len(attempt1[i]) == 1 and attempt1[i - 1][len(attempt1[i -1]) -1] == "." and attempt1[i].isalpha(): # This adds to the new_one_letter_list.
			new_one_letter_word.append(attempt1[i])
		i = i + 1

	#This counts the frequency then places it in an ordered list from most frequent to least frequent.
	freq_of_one_letter_words = frequency_analysis(new_one_letter_word)
	most_freq_2 = sorted(freq_of_one_letter_words,key=freq_of_one_letter_words.get, reverse=True)
	
	#If the list is greater than 1 and "A" is not the same a "I" comparing them from their original values then we change the mapping of the original value to "I".
	if len(most_freq_2) > 1: 
		if most_freq[1] != most_freq_2[0]:
			used_1 = "I" #We assigned the variable to these value so they can be easily swapped if needed.
			original_1 = most_freq[0]
			if access_2 == 1: #If this flag is set to one then we swap the values with the value from used_1.
				used_2 = "A"
				original_2 = most_freq[1] 

	if access_1 == 1: #If the flag is set to 1 then this will allow to the most frequent letters to the queue.
		lock.acquire()
		original_letter.put(original_1)
		letters_in_uses.put(used_1)
		lock.release()

	if access_2 == 1: #This will allow to add to the queue if there are two letters in the list above as the flag was changed above.
		lock.acquire()
		original_letter.put(original_2)
		letters_in_uses.put(used_2)
		lock.release()


#This finds all two letter words with one lower case letter in it. The lower case letter means the the letter has not be mapped yet.
#This then assigns the appropriate value using the two letter string of all the most common two letter words. Using regular expressions it identifies what letter should be mapped to the lower case letter of the teo letter word.
def two_letter_word(attempt, two):
	two_letter_freq = []
	attempt1 = attempt.strip().split()

	i = 0
	while i != len(attempt1):
		if len(attempt1[i]) == 2 and not attempt1[i].isupper() and attempt1[i].isalpha(): #finds all teo letter words with lowercase in them.
			two_letter_freq.append(attempt1[i])
		i = i + 1

	#Finds the most frequent letter and puts them into a list
	f = frequency_analysis(two_letter_freq)
	fr = sorted(f,key=f.get, reverse=True)

	i = 0
	while i != len(fr): #This will loop through the entire list untill all letters that can be matched are mapped to a value.
		letter_1 = fr[i][0]
		letter_2 = fr[i][1]
		#print(fr[i])
		two_letters = "of to in it is as at so by or on do if my up an go us" #List of most frequent two letter words.

#Case 1: left is uppercase and right is lowercase.
		if letter_1 == (letter_1).upper() and fr[i] != fr[i].upper():
			regex = re.escape(letter_1.lower()) + r"\w"
			result = re.findall(regex , two_letters)
			if len(result) != 0:
				j = 0
				while result[j][1].upper() in used_letters and j < len(result) -1:
					j = j + 1

				if result[j][1].upper() not in used_letters: #Checks if it is in used letters alreday
					char = result[j][1].upper()
					used_list.append(result[j])
					attempt = attempt.replace(letter_2, char)#replaces all value in the cipher text with the new mapping.
					string = " ". join(fr)
					fr = (string.replace(letter_2, char)).strip().split()
					if char not in used_letters:
						used_letters.append(char)
						original_letter_list.append(letter_2)



#Case 2: lowercase on the left and uppercase on the right.
		elif letter_2 == (letter_2).upper() and fr[i] != fr[i].upper():
			regex = r"\w" + re.escape(letter_2.lower())
			result = re.findall(regex , two_letters)
			#print(result)

			if len(result) != 0:
				j = 0
				while result[j][0].upper() in used_letters and j < len(result) -1:
					j = j + 1

				if result[j][0].upper() not in used_letters:
					char = (result[j][0]).upper()
					used_list.append(result[j])
					attempt = attempt.replace(letter_1, char)
					string = " ". join(fr)
					fr = (string.replace(letter_1, char)).strip().split()
					if char not in used_letters:
						used_letters.append(char)
						original_letter_list.append(letter_1)


		i = i + 1
	return attempt #returns the new cipher texted with the replaced values.

#This module finds all double letters in the cipher text and assigns the values in the same_letter_list providing the letter are not in the used list.
def double_two_letters(attempt):
	attempt1 = attempt.strip().split()
	j = 0
	double_letters = []
	same_letters_list = ["ee", "ll", "ss", "oo", "tt", "ff" "rr", "nn", "pp"] #Most frequent double letters
	for word in attempt1:
		i = 0
		while i < len(word) -1: #finds all the double letters and adds them to a list.
			first_letter = word[i]
			second_letter = word[i + 1]
			togther_letters = first_letter + second_letter
			if first_letter == second_letter and not togther_letters.isupper(): 
				double_letters.append(first_letter)
				pass
			i = i + 1

	freq = frequency_analysis(double_letters) #finds the most frequent double letters and puts them in a frequency ordered list.
	most_freq = sorted(freq,key=freq.get, reverse=True)

	#This part below checks to see if firstly if the frequecy of the word is greater or equal to the second in the list or if there is just one value in the list.
	if len(most_freq) != 0:
		i = 0
		while i <= len(most_freq) - 1: #itterate through the list.
			j = 0
			while same_letters_list[j][0].upper() in used_letters and j < len(same_letters_list) -1: #Finds the next available letter to map to from our list.
				j = j + 1
			#print(same_letters_list[j])
			if same_letters_list[j][0].upper() not in used_letters:
				char = same_letters_list[j][0].upper() #value to map to is called char.

				if len(most_freq) == (most_freq.index(most_freq[i]) + 1): #check to see if there is one letter in the list.
					attempt = attempt.replace(most_freq[i], char)
					used_letters.append(char)
					original_letter_list.append(most_freq[i])

				elif freq[most_freq[i]] > freq[most_freq[i + 1]]: #checks if the first frequency value is greater than the second frequency value if so then it takes the first value and replaces it with the variable char.
					attempt = attempt.replace(most_freq[i], char)
					used_letters.append(char)
					original_letter_list.append(most_freq[i])


				elif freq[most_freq[i]] == freq[most_freq[i + 1]]:#Checks if the frequency values are equal.
					if freq_single_letters[most_freq[i]] > freq_single_letters[most_freq[i + 1]]: #checks the frequency of each word and if the first one is bigger than the second it will use the first value.
						attempt = attempt.replace(most_freq[i], char)
						used_letters.append(char)
						original_letter_list.append(most_freq[i])

					elif freq_single_letters[most_freq[i]] < freq_single_letters[most_freq[i + 1]]: #checks if the frequency of the first value is bigger thant he frequency of the second value and if so it will take the second value and replac it with the variable char.
						attempt = attempt.replace(most_freq[i + 1], char)
						used_letters.append(char)
						original_letter_list.append(most_freq[i + 1])

			i = i + 1

			#print(most_freq)
	return attempt

#This finds all the double letters at the end of words.
def double_two_letters_ending(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	j = 0
	double_letters = []
	same_letters_list = ["ee", "ll", "ss","ff"]
	for word in attempt1:
		i = 0
		while i < len(word) -1: #finds all the double letters at the end of a word.
			first_letter = word[i]
			second_letter = word[i + 1]
			togther_letters = first_letter + second_letter
			if first_letter == second_letter and i == len(word) -2 and not togther_letters.isupper():
				double_letters.append(first_letter)
				break
			i = i + 1

	freq = frequency_analysis(double_letters) #finds the frequency of the letters and put them into a sorted list.
	most_freq = sorted(freq,key=freq.get, reverse=True)

	if len(most_freq) != 0: #check if the list is not empty.
		i = 0
		while i <= len(most_freq) - 1:
			j = 0
			while same_letters_list[j][0].upper() in used_letters and j < len(same_letters_list) -1: #finds the next available letter to map to.
				j = j + 1
			#print(same_letters_list[j])
			if same_letters_list[j][0].upper() not in used_letters: #checks if the letter is in the used list. So we do not enter it twice.
				char = same_letters_list[j][0].upper()
				lock.acquire()
				original_letter.put(most_freq[i]) #adds to the queue.
				letters_in_uses.put(char)
				lock.release()
				if char not in used_letters: # if the character is not in used list append to used_list.
					used_letters.append(char)
			i = i + 1

#This find three letter words with one lower case letter then trys to map the most appropriate value to that word using a list of frequent three letter words.
def three_letter_word_double_case(attempt, three):
	most_freq = ""
	can_pass = 0
	result = []
	attempt1 = attempt.strip().split()
	three_letter_list = []
	three_letters = three 
	i = 0
	#This finds all the three letter words with one or more lower case in the three letter word.
	while i != len(attempt1):
		if len(attempt1[i]) == 3 and attempt1[i] != attempt1[i].upper() and (attempt1[i]).isalpha():
			three_letter_list.append(attempt1[i])
			freq_3 = frequency_analysis(three_letter_list)
			most_freq = sorted(freq_3,key=freq_3.get, reverse=True)
		i = i + 1

	#This orders the list to find the words with at least one upper so they will be put at the top of the list.
	n = 0
	upper_list = []
	lower_list = []
	for word in most_freq:
		first = word[0]
		second = word[1]
		third = word[2]
		#print(word)
		if (first.isupper() or second.isupper() or third.isupper()) and word.isalpha():
			upper_list.append(word)
		else:
			lower_list.append(word)
	new_list = upper_list + lower_list

	i = 0
	k = 0
	while k != 2: #####iterated twice over the list.
		i = 0
		while i != len(new_list):
			letter_1 = new_list[i][0]
			letter_2 = new_list[i][1]
			letter_3 = new_list[i][2]
			#print(new_list[i])

#Double case 1: One uppercase on the left and centre.
			if letter_1 == (letter_1).upper() and letter_2 == (letter_2).upper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + re.escape(letter_2.lower()) + r"\w"
				result = re.findall(regex , three_letters)
				position = 2
				can_pass = 1

#Double case 2: One uppercase on the left and far right.
			elif letter_1 == (letter_1).upper() and letter_3 == (letter_3).upper() and new_list[i] != new_list[i].upper():
				regex = re.escape(letter_1.lower()) + r"\w" + re.escape(letter_3.lower())
				result = re.findall(regex , three_letters)
				position = 1
				can_pass = 1

#Double case 3: One uppercase in the centre and far right.
			elif letter_2 == (letter_2).upper() and letter_3 == (letter_3).upper() and new_list[i] != new_list[i].upper():
				regex =  r"\w" + re.escape(letter_2.lower()) + re.escape(letter_3.lower())
				result = re.findall(regex , three_letters)
				position = 0
				can_pass = 1

			if len(result) > 0 and can_pass == 1: #checks if the list is empty and has the flag (can_pass) set 1.
				can_pass = 0
				j = 0
				while result[j][position].upper() in used_letters and j < len(result) -1: #finds the first available letter to map to.
					j = j + 1

				if result[j][position].upper() not in used_letters: #checks the letter is not in the list.
					char = (result[j][position]).upper()
					used_list.append(result[j]) #adds mapped value to the list
					attempt = attempt.replace(new_list[i][position], char) #replaces the letter with the new mapping.
					string = " ". join(new_list)
					if char not in used_letters:
						used_letters.append(char)
						original_letter_list.append(new_list[i][position])
					new_list = (string.replace(new_list[i][position], char)).strip().split() #once a letter is found it updates the existing list so we do not have itterate over the list many times.

			i = i + 1
		k = k + 1
	return attempt

#This finds four letter words that with one lower case letter that needs to be mapped a value.
def four_letter_word(attempt, words):
	most_freq = ""
	result = []
	attempt1 = attempt.strip().split()
	four_letter_list = []
	four_letters = words #words contains a list of all the most frequent four letter words.
	i = 0

	#This finds all the four letter words that are not uppercase.
	while i != len(attempt1):
		if len(attempt1[i]) == 4 and not attempt1[i].isupper() and attempt1[i].isalpha():
			four_letter_list.append(attempt1[i])
			freq_4 = frequency_analysis(four_letter_list)
			most_freq = sorted(freq_4,key=freq_4.get, reverse=True)
		i = i + 1

	n = 0
	upper_list = []
	lower_list = []
	for word in most_freq:
		first = word[0]
		second = word[1]
		third = word[2]
		fourth = word[3]
		#This separates all the four letter words with an uppercase in them
		if (first.isupper() or second.isupper() or third.isupper() or fourth.isupper()) and word.isalpha():#########
			upper_list.append(word)
		else:
			lower_list.append(word)
	new_list = upper_list + lower_list #This puts all the four letter words with an uppercase in the at the top of the list while four letter word with no uppercase letters go to the end of the list.

	i = 0
	k = 0
	while k != 1: #####iterated twice over the list.
		i = 0
		while i != len(new_list):
			can_pass = 0
			letter_1 = new_list[i][0]
			letter_2 = new_list[i][1]
			letter_3 = new_list[i][2]
			letter_4 = new_list[i][3]
#Triple case 1: One lower case on the far left and all other are upper.
			if letter_2.isupper() and letter_3.isupper() and letter_4.isupper() and not new_list[i].isupper():
				regex = r"\w" + re.escape(letter_2.lower()) + re.escape(letter_3.lower()) + re.escape(letter_4.lower())
				result = re.findall(regex , four_letters)
				position = 0 #this tells what position needs to be swapped at the end
				can_pass = 1 #this allows the pass the if statement below

#Triple case 2: Upper on the far left followed by a lower then two uppers.
			elif letter_1.isupper() and letter_3.isupper() and letter_4.isupper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + r"\w" + re.escape(letter_3.lower()) + re.escape(letter_4.lower())
				result = re.findall(regex , four_letters)
				position = 1
				can_pass = 1

#Triple 3: two letters on the left are upper followed by a lower than an upper.
			elif letter_1.isupper() and letter_2.isupper() and letter_4.isupper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + re.escape(letter_2.lower()) + r"\w" + re.escape(letter_4.lower())
				result = re.findall(regex , four_letters)
				position = 2
				can_pass = 1
				#print(result)

#Triple 4: three letters on the left are upper followed by a lower.
			elif letter_1.isupper() and letter_2.isupper() and letter_3.isupper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + re.escape(letter_2.lower()) + re.escape(letter_3.lower()) + r"\w"
				result = re.findall(regex , four_letters)
				position = 3
				can_pass = 1
				#print(result)

			if len(result) != 0 and can_pass == 1: #checks if it is empty and if the can_pass is set to 1.
				j = 0
				while result[j][position].upper() in used_letters and j < len(result) -1:
					j = j + 1

				#replaces the value and add then to there associated lists.
				if result[j][position].upper() not in used_letters:
					char = (result[j][position]).upper()
					used_list.append(result[j])
					attempt = attempt.replace(new_list[i][position], char)
					string = " ". join(new_list)
					if char not in used_letters:
						used_letters.append(char)
						original_letter_list.append(new_list[i][position])
					new_list = (string.replace(new_list[i][position], char)).strip().split()

			i = i + 1
		k = k + 1
	return attempt

def last_letter(attempt):
	attempt1 = attempt.strip().split()
	last_list = []
	last_letter = []

	for word in attempt1:
		if not word.isupper() and word.isalpha():
			i = 0
			while word[i].isupper():
				i = i + 1
				last_list.append(word[i])
			if word[i] not in last_letter:
				last_letter.append(word[i])
	#print(last_letter)

	if len(last_letter) >= 2:
		counted_1 = last_list.count(last_letter[0])
		counted_2 = last_list.count(last_letter[1])
		if counted_1 > counted_2:
			attempt = attempt.replace(last_letter[1], "Z")
			if "Z" not in used_letters:
				used_letters.append("Z")
			attempt = attempt.replace(last_letter[0], "X")
			if "X" not in used_letters:
				used_letters.append("X")
		else:
			attempt = attempt.replace(last_letter[1], "X")
			if "X" not in used_letters:
				used_letters.append("X")
			attempt = attempt.replace(last_letter[0], "Z")
			if "Z" not in used_letters:
				used_letters.append("Z")

	elif len(last_letter) == 1:
		alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		attempt = attempt.replace(last_letter[0], "X")
		if "X" not in used_letters:
			used_letters.append("X")

		i = 0
		while alphabet[i] in used_letters:
			i = i + 1
		attempt = attempt.replace(last_letter[1], "Z")
		if "Z" not in used_letters:
			used_letters.append("Z")

	return attempt

#This finds all words that have E in it and after finding the most frequent it assigns the T to the position 0 and H to position 1.
def finding_H_by_THE(attempt, q, letters_in_uses, original_letter,lock):
	attempt1 = attempt.strip().split()
	T_E = []
	last_letter = []

	for word in attempt1: #finds all words with E in it.
		if len(word) == 3 and word[2] == "E" and not word.isupper() and word.isalpha():
			T_E.append(word)

	freq = frequency_analysis(T_E) #finds the frequency of the list found above and put it in list ordered in frequency.
	most_freq = sorted(freq,key=freq.get, reverse=True)
	if len(most_freq) > 0:
		lock.acquire()
		original_letter.put(most_freq[0][1])
		letters_in_uses.put("H")

		original_letter.put(most_freq[0][0])
		letters_in_uses.put("T")
		lock.release()

#This finds all words ending in E then adds the to a list letter before E will be H and after E will be R.
def bigram_E(attempt, q, letters_in_uses,original_letter,lock):
	attempt1 = attempt.strip().split()
	bigrams_text = []
	letter_before = []
	letter_after = []

	for word in attempt1:
		if len(word) >= 2 and "E" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)

	#This finds all the values of E in the words the add the letter before and after to two different lists.
	for word in bigrams_text:
		index = 0
		if word.count("E") >= 2:
			for letter in word:
				if letter == "E":
					if index == 0:
						letter_after.append(word[index + 1]) 

					elif index == len(word) -1:
						letter_before.append(word[index - 1])

					else:
						letter_after.append(word[index + 1])
						letter_before.append(word[index - 1])

				index = index + 1

		elif word.count("E") == 1:
			for letter in word:
				if letter == "E":
					if index == 0:
						letter_after.append(word[index + 1]) 

					elif index == len(word) -1:
						letter_before.append(word[index - 1])

					else:
						letter_after.append(word[index + 1])
						letter_before.append(word[index - 1])
				index = index + 1


	if "H" not in used_letters:
		freq = frequency_analysis(letter_before) #finds sorted frequency of the list.
		most_freq_1 = sorted(freq,key=freq.get, reverse=True)

		lock.acquire()
		original_letter.put(most_freq_1[0]) #This adds to the queue
		letters_in_uses.put("H")
		lock.release()

	freq = frequency_analysis(letter_after)
	most_freq_2 = sorted(freq,key=freq.get, reverse=True) #finds the sorted frequency of the list.

	for letter in most_freq_2:
		if letter.isupper():
			most_freq_2.remove(letter)

	if "R" not in used_letters:
		lock.acquire()
		original_letter.put(most_freq_2[0])#Adds to the queue.
		letters_in_uses.put("R")
		lock.release()

#This module find all words with I then finds words after every occurance of I and finds the most frequend letter after I and replaces it with N.
def bigram_I(attempt, q, letters_in_uses,original_letter, used_letters, freq_single_letters, lock):
	attempt1 = attempt.strip().split()
	bigrams_options = ["N"]
	bigrams_text = []
	letter_after = []

	for word in attempt1:
		if len(word) >= 2 and "I" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)

	for word in bigrams_text:
		index = 0
		if word.count("I") >= 2:
			for letter in word:
				if letter == "I":
					if index == 0:
						letter_after.append(word[index + 1]) 

					elif index == len(word) -1:
						pass

					else:
						letter_after.append(word[index + 1])

				index = index + 1

	freq_2 = frequency_analysis(letter_after)
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.


	if len(most_freq_2) > 0:
		i = 0
		j = 0
		while i < len(bigrams_options):
			if not most_freq_2[i].isupper():
				if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
					lock.acquire()
					original_letter.put(most_freq_2[i]) #adds to the queue.
					letters_in_uses.put(bigrams_options[i])
					lock.release()
				#This checks if the one value and the one next to it is the same if so it will take the more frequent value
				elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
					if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list #if the first value is greater than the second value.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #adds to the queue.
						letters_in_uses.put(bigrams_options[i])
						lock.release()

					elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of the position of i in the list is less than the position so i+1 in the list.
						j = j + 1

						#adds the values to the queue.
						lock.acquire()
						original_letter.put(most_freq_2[j]) #adds to the queue
						letters_in_uses.put(bigrams_options[i])
						lock.release()

			i = i + 1
			j = j + 1

#This take ever word with N in it and records the letter before and after the letter N. I will replace the most frequent occurance after N with. The most and second most frequent occurance before N will be replaces with I and O respectively.
def bigram_N(attempt, q, letters_in_uses,original_letter, used_letters, freq_single_letters, lock):
	attempt1 = attempt.strip().split()
	bigrams_options_after = ["O"]
	bigrams_options_before = ["I", "O"]
	bigrams_text = []
	letter_before = []
	letter_after = []
	new_letter_before = []
	new_letter_after = []

	for word in attempt1:
		if len(word) >= 2 and "N" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)
#Find the occurance of letter before and after N.
	for word in bigrams_text:
		index = 0
		if word.count("N") >= 2:
			for letter in word:
				if letter == "N":
					if index >= 1:
						letter_before.append(word[index - 1]) 

					elif index <= len(word) - 2:
						letter_after.append(word[index + 1])


				index = index + 1

		elif word.count("N") == 1:
			for letter in word:
				if letter == "N":
					if index >= 1:
						letter_before.append(word[index - 1]) 

					elif index <= len(word) -2:
						letter_after.append(word[index + 1])


				index = index + 1
#Removes all uppercase letters.
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)
#Removes all uppercase letters.
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_1 = frequency_analysis(new_letter_before)
	most_freq_1 = sorted(freq_1,key=freq_1.get, reverse=True) #finds the most frequent letters

	freq_2 = frequency_analysis(new_letter_after)
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.

	if len(most_freq_1) > 0:
			if len(most_freq_1) == 1 and bigrams_options_before[i] not in used_letters:
				if bigrams_options_before[0] not in used_letters:
					lock.acquire()
					original_letter.put(most_freq_1[0])
					letters_in_uses.put(bigrams_options_before[0])
					lock.release()

			else:
				i = 0
				j = 0
				k = 0
				while i <= len(bigrams_options_before) -1:
					if not most_freq_1[i].isupper():
						while bigrams_options_before[k] in used_letters and k < len(bigrams_options_before) - 1: #finds the first available letter in the list it can map to.
							k = k + 1

						if freq_1[most_freq_1[i]] > freq_1[most_freq_1[i + 1]]:# checks if frequency is greater in the first letter than the second letter in the frequency list.
							lock.acquire()
							original_letter.put(most_freq_1[i])
							letters_in_uses.put(bigrams_options_before[k])
							used_letters.append(bigrams_options_before[k])
							lock.release()

						elif freq_1[most_freq_1[i]] == freq_1[most_freq_1[i + 1]]:#checks if the first and second have the same frequency.
							if freq_single_letters[most_freq_1[i].lower()] > freq_single_letters[most_freq_1[i + 1].lower()]:#checks if the first is bigger then the second.
								lock.acquire()
								original_letter.put(most_freq_1[i])
								letters_in_uses.put(bigrams_options_before[k]) #maps the first value to the letter.
								used_letters.append(bigrams_options_before[k])
								lock.release()

							elif freq_single_letters[most_freq_1[i].lower()] < freq_single_letters[most_freq_1[i + 1].lower()]: #check is the second letter frequency is greater then the first letter frequency.
								j = j + 1
								attempt = attempt.replace(most_freq_1[j], bigrams_options_before[k])
								lock.acquire()
								original_letter.put(most_freq_1[j])
								letters_in_uses.put(bigrams_options_before[k])# maps the second value to the letter.
								used_letters.append(bigrams_options_before[k])
								lock.release()

					elif most_freq_1[j].isupper():
						i = i - 1

					i = i + 1
					j = j + 1

#This module finds G with the third and second last letter being I and N respectively.
def ending_ing(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["G"]
	trigrams_text = []
	letter_before = []
	letter_after = []
	new_letter_before = []
	new_letter_after = []

#finds all words with IN in them and add then to a list.
	for word in attempt1: 
		if len(word) > 3 and "IN" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)

#Finds all the words after IN in the sorted list above
	for word in trigrams_text:
		index = 0
		if word.count("IN") >= 2: #checks if IN appears twice in the word.
			for letter in word:
				if letter == "I":
					if index == 0:
						letter_after.append(word[index + 2]) 

					elif index <= len(word) - 3:
						letter_after.append(word[index + 2])

				index = index + 1

		elif word.count("IN") == 1: #checks if IN appears once in the word.
			for letter in word:
				if letter == "I":
					if index == 0:
						letter_after.append(word[index + 2])

					elif index <= len(word) - 3:
						letter_after.append(word[index + 2])

				index = index + 1

#Removes all uppercase letters.
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_2 = frequency_analysis(new_letter_after) #Finds the frequency of the letters and places then in a ordered frequecy list.
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True)

	if len(most_freq_2) > 0:
		i = 0
		j = 0
		while i < len(trigrams_options):
			if not most_freq_2[i].isupper():
				if len(most_freq_2) == 1: #Checks if there is only one letter in the list
					attempt = attempt.replace(most_freq_2[i], trigrams_options[i])
					lock.acquire()
					original_letter.put(most_freq_2[i]) #adds to the queue.
					letters_in_uses.put(trigrams_options[i])
					lock.release()  

				elif freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
					lock.acquire()
					original_letter.put(most_freq_2[i]) #The greater value gets added to the queue.
					letters_in_uses.put(trigrams_options[i])
					lock.release()  

				elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
					if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #The greater value gets added to the queue.
						letters_in_uses.put(trigrams_options[i])
						lock.release()

					elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]: #Checks if the frequency of the second value is greater than the frequency of the first value.
						j = j + 1
						lock.acquire()
						original_letter.put(most_freq_2[j]) #The greater value gets added to the queue.
						letters_in_uses.put(trigrams_options[i])
						lock.release()

			elif most_freq_2[j].isupper():
				i = i - 1

			i = i + 1
			j = j + 1

#This module finds all three letter words with AN in them and replaces the last lowercase letter with D.
def trigrams_AND(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["D"]
	trigrams_text = []

	if "D" not in used_letters:
		for word in attempt1:
			if len(word) == 3 and "AN" in word and not word.isupper() and word.isalpha(): #Finds all letters with AN in it.
				trigrams_text.append(word)

		freq_2 = frequency_analysis(trigrams_text)
		most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #finds the most frequent words with AN
		if len(most_freq_2[0]) >= 2:
			lock.acquire()
			original_letter.put(most_freq_2[0][2]) #The last letter is mapped to D and added to the queue.
			letters_in_uses.put("D")
			lock.release()


#This module finds all words with O in them and whatever the most frequent letter after O is will be replaced with F.
def bigram_OF(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["F"]
	trigrams_text = []
	letter_after = []
	new_letter_after = []

	for word in attempt1: #Finds all words that contain O and add the word to a list.
		if len(word) >= 2 and "O" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)

#finds all the letters that occur after O and add them to a dictionary.
	for word in trigrams_text:
		index = 0
		if word.count("O") >= 2: #checks if O occurs twice.
			for letter in word:
				if letter == "O":
					if index < len(word) -1:
						letter_after.append(word[index + 1])

				index = index + 1

		elif word.count("O") == 1: #checks if O occurs once.
			for letter in word:
				if letter == "O":
					if index < len(word) -1:
						letter_after.append(word[index + 1])
				index = index + 1
#removes all uppercases
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_2 = frequency_analysis(new_letter_after) #finds the frquency
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True)#put the frequency in order from most frequent to least frequent.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list
			lock.acquire()
			original_letter.put(most_freq_2[0]) #adds to queue.
			letters_in_uses.put(trigrams_options[0])
			lock.release()

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #checks if the frequency value of the first is greater than the second value
						lock.acquire()
						original_letter.put(most_freq_2[i + 1]) # adds the smaller value to the queue.
						letters_in_uses.put(trigrams_options[i])
						lock.release()
						

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the two values side by side are the same.
						if freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]: #finds the overall frequecy of the letter and compares if that value is bigger than the next value in the list.
							lock.acquire()
							original_letter.put(most_freq_2[i]) #adds the smaller vale to the list.
							letters_in_uses.put(trigrams_options[i])
							lock.release()

						elif freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #invers of the elif statement above.
							j = j + 1
							#print(i)
							#print(trigrams_options)
							lock.acquire()
							original_letter.put(most_freq_2[j]) #adds the smaller value.
							letters_in_uses.put(trigrams_options[i])
							lock.release()

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1

#This modules finds all word with ITH and adds them to a list. Then find the most frequent and add W to the first letter position.
def quadgram_WITH(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["W"]
	trigrams_text = []
	letter_before = []
	new_letter_before = []

	for word in attempt1: #finds all the words with ITH in them.
		if len(word) >= 4 and "ITH" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)
#finds all the letters before ITH and adds it to a list.
	for word in trigrams_text:
		index = 0
		if word.count("ITH") >= 2: #checks if ITH occurs twice.
			for letter in word:
				if letter == "I":
					if index >= 1:
						letter_before.append(word[index - 1])

				index = index + 1

		elif word.count("ITH") == 1: #check if ITH occurs once.
			for letter in word:
				if letter == "I":
					if index >= 1:
						letter_before.append(word[index - 1])
				index = index + 1
#removes all uppercases from the list.
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)

	freq_2 = frequency_analysis(new_letter_before) #finds the frequency of the letters in the list.
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True)#orders the frequecy above into most to least frequent.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list.
			lock.acquire()
			original_letter.put(most_freq_2[0]) #adds to the queue
			letters_in_uses.put(trigrams_options[0])
			lock.release()

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first is grater than the second letter.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #add the greater valued letter to the queue.
						letters_in_uses.put(trigrams_options[i])
						lock.release()

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequecy of the letters are the same for the first and second letters.
						if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of the first letter is greater than the second letter.
							lock.acquire()
							original_letter.put(most_freq_2[i]) #adds the bigger frequency letter to the list.
							letters_in_uses.put(trigrams_options[i])
							lock.release()

						elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of the second letter is greater than the first letter.
							j = j + 1
	
							attempt = attempt.replace(most_freq_2[j], trigrams_options[i])
							lock.acquire()
							original_letter.put(most_freq_2[j]) #adds the bigger value to the queue
							letters_in_uses.put(trigrams_options[i])
							lock.release()

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1

#This module takes a five letter word and if it contains one lowercase letter this will assign the most likely letter to that lowercase word. 
def five_letter_word(attempt, words):
	most_freq = ""
	result = []
	attempt1 = attempt.strip().split()
	five_letter_list = []
	five_letters = five
	i = 0
	while i != len(attempt1):
		#this finds the value all five letter words that contain at least one lowercase letter.
		if len(attempt1[i]) == 5 and not attempt1[i].isupper() and attempt1[i].isalpha():
			five_letter_list.append(attempt1[i])
			freq_4 = frequency_analysis(five_letter_list)
			most_freq = sorted(freq_4,key=freq_4.get, reverse=True)
		i = i + 1

	n = 0
	upper_list = []
	lower_list = []
	for word in most_freq:
		first = word[0]
		second = word[1]
		third = word[2]
		fourth = word[3]
		fifth = word[4]
		#This will sort the list to have all letters with at least one uppercase letter at the front of the list while letters with no uppercased letters will be at the end.
		if (first.isupper() or second.isupper() or third.isupper() or fourth.isupper()) or fifth.isupper() and word.isalpha():#########
			upper_list.append(word)
		else:
			lower_list.append(word)
	new_list = upper_list + lower_list

	i = 0
	k = 0
	while k != 2: #####iterated twice over the list.
		i = 0
		while i != len(new_list):
			letter_1 = new_list[i][0]
			letter_2 = new_list[i][1]
			letter_3 = new_list[i][2]
			letter_4 = new_list[i][3]
			letter_5 = new_list[i][4]
#using regular expressions below to find words most likely to suit the word.
#Triple case 1: One lowercase on the far left and all other are uppercase.
			if letter_2.isupper() and letter_3.isupper() and letter_4.isupper() and letter_5.isupper() and not new_list[i].isupper():
				regex = r"\w" + re.escape(letter_2.lower()) + re.escape(letter_3.lower()) + re.escape(letter_4.lower()) + re.escape(letter_5.lower())
				result = re.findall(regex , five_letters)
				position = 0
#Triple case 2: Uppercase on the far left followed by a lower then two uppers.
			elif letter_1.isupper() and letter_3.isupper() and letter_4.isupper() and letter_5.isupper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + r"\w" + re.escape(letter_3.lower()) + re.escape(letter_4.lower()) + re.escape(letter_5.lower())
				result = re.findall(regex , five_letters)
				position = 1
#Triple 3: two letters on the left are uppercased followed by a lowercased than an upper.
			elif letter_1.isupper() and letter_2.isupper() and letter_4.isupper() and letter_5.isupper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + re.escape(letter_2.lower()) + r"\w" + re.escape(letter_4.lower()) + re.escape(letter_5.lower())
				result = re.findall(regex , five_letters)
				position = 2
#Triple 4: three letters on the left are uppercased followed by a lowercased.
			elif letter_1.isupper() and letter_2.isupper() and letter_3.isupper() and letter_5.isupper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + re.escape(letter_2.lower()) + re.escape(letter_3.lower()) + r"\w" + re.escape(letter_5.lower())
				result = re.findall(regex , five_letters)
				position = 3
#Triple 5: three letters on the left are uppercased followed by a lowercased.
			elif letter_1.isupper() and letter_2.isupper() and letter_3.isupper() and letter_4.isupper() and not new_list[i].isupper():
				regex = re.escape(letter_1.lower()) + re.escape(letter_2.lower()) + re.escape(letter_3.lower()) + re.escape(letter_4.lower()) + r"\w"
				result = re.findall(regex , five_letters)
				position = 4




			if len(result) != 0:
				j = 0
				while result[j][position].upper() in used_letters and j < len(result) -1: #finds the next available letter to map to.
					j = j + 1

				if result[j][position].upper() not in used_letters:
					char = (result[j][position]).upper()
					used_list.append(result[j])
					attempt = attempt.replace(new_list[i][position], char) #replace cipher text with the new mapping
					string = " ". join(new_list)
					if char not in used_letters:
						used_letters.append(char)
						original_letter_list.append(new_list[i][position])
					new_list = (string.replace(new_list[i][position], char)).strip().split() #Update the list being iterated through with the new values that are newly mapped.

			i = i + 1
		k = k + 1
	return attempt

#This module finds all the words with H in them and takes the letter before and after H and maps them to the most frequent letter before and after H.
def bigram_H(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	bigrams_options_after = ["A"]
	bigrams_options_before = ["T"]
	bigrams_text = []
	letter_before = []
	letter_after = []
	new_letter_before = []
	new_letter_after = []

#This finds all the letters that contain H.
	for word in attempt1: 
		if len(word) >= 2 and "H" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)
#finds the letter before and after H.
	for word in bigrams_text:
		index = 0
		if word.count("H") >= 2: #checks if there are more than 1 occurrance of H in the word.
			for letter in word:
				if letter == "H":
					if index >= 1:
						letter_before.append(word[index - 1]) 
					elif index <= len(word) - 2:
						letter_after.append(word[index + 1])
				index = index + 1

		elif word.count("H") == 1: #checks if H occurs once.
			for letter in word:
				if letter == "H":
					if index >= 1:
						letter_before.append(word[index - 1]) 

					elif index <= len(word) -2:
						letter_after.append(word[index + 1])


				index = index + 1
#removes the uppercase letters from the list.
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)
#removes the uppercase letters from the list.
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_1 = frequency_analysis(new_letter_before) #finds the frequency of the lettes in the list.
	most_freq_1 = sorted(freq_1,key=freq_1.get, reverse=True) #put them in a list in order of frequency. 

	freq_2 = frequency_analysis(new_letter_after) #finds the frequency of the lettes in the list.
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #put them in a list in order of frequency. 


	if len(most_freq_2) > 0 and "A" not in used_letters: #check if the list is not empty and if the letter a is already mapped.
		i = 0
		j = 0
		while i < len(bigrams_options_after): #itterate through the available letter to be mapped to.
			if not most_freq_2[i].isupper():
				#checks if the list has only one element in the list.
				if len(most_freq_2) == 1:
					lock.acquire()
					original_letter.put(most_freq_2[i]) #adds to the queue.
					letters_in_uses.put(bigrams_options_after[i])
					lock.release()
				#checks if element i is more frequent than element i+1 in the list.
				elif freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]:
					lock.acquire()
					original_letter.put(most_freq_2[i]) #adds to the queue.
					letters_in_uses.put(bigrams_options_after[i])
					lock.release()
				#checks if elemet i is equal to element i+1 in the list.
				elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]:
					#if the frequency of element i is greater than the frequency of element i+1 than element i is added to the queue.
					if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]:
						lock.acquire()
						original_letter.put(most_freq_2[i]) #element i is added to the queue.
						letters_in_uses.put(bigrams_options_after[i])
						lock.release()
					#if the frequency of the element i is less than the frequency of element i+1 than element i+1 is added to the queue.
					elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:
						j = j + 1

						lock.acquire()
						original_letter.put(most_freq_2[j]) # adds i+1 to the queue.
						letters_in_uses.put(bigrams_options_after[i])
						lock.release()

			elif most_freq_2[j].isupper(): 
				i = i - 1

			i = i + 1
			j = j + 1
#checks if the list is empty and if T isnt already used.
	if len(most_freq_1) > 0 and "T" not in used_letters:
			if len(most_freq_1) == 1: #chekcs if there is only one element in the list.
				original_letter.put(most_freq_1[0])#adds to the queue.
				letters_in_uses.put(bigrams_options_before[0])

			else:
				i = 0
				j = 0
				while i < len(bigrams_options_before): #itterates through the available letters to be mapped to.
					if not most_freq_1[i].isupper():
						if freq_1[most_freq_1[i]] > freq_1[most_freq_1[i + 1]]: #checks if element i in the list is greater than element i+1 int the list.
							original_letter.put(most_freq_1[i]) #adds element i to the list.
							letters_in_uses.put(bigrams_options_before[i])                          

						elif freq_1[most_freq_1[i]] == freq_1[most_freq_1[i + 1]]: #checks if element i is equal to element i+1 in the list.
							if freq_single_letters[most_freq_1[i].lower()] > freq_single_letters[most_freq_1[i + 1].lower()]:#checks if the frequency of element i is greater than element i+1 in the list.
								original_letter.put(most_freq_1[i]) #adds i to the queue.
								letters_in_uses.put(bigrams_options_before[i])
							#checks if the element i is less than element i+1 in the list.
							elif freq_single_letters[most_freq_1[i].lower()] < freq_single_letters[most_freq_1[i + 1].lower()]:
								j = j + 1

								original_letter.put(most_freq_1[j]) #adds i+1 to the queue.
								letters_in_uses.put(bigrams_options_before[i])

					elif most_freq_1[j].isupper():
						i = i - 1

					i = i + 1
					j = j + 1
#This module finds all words with A in them and finds the most frequent word after A and maps that to N.
def bigram_AN(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	bigrams_options = ["N"]
	bigrams_text = []
	letter_before = []
	letter_after = []
	new_letter_before = []
	new_letter_after = []

	for word in attempt1:
		#This finds all words that contain an A and is not an uppercase word and is alphabetical.
		if len(word) >= 2 and "A" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)
#finds the position of A then add the word after A to a list.
	for word in bigrams_text:
		index = 0
		if word.count("A") >= 2: #checks if A occurs twice or more in a word.
			for letter in word:
				if letter == "A":
					if index == 0:
						letter_after.append(word[index + 1]) 

					elif index == len(word) -1: 
						letter_before.append(word[index - 1])

					else:
						letter_after.append(word[index + 1])
						letter_before.append(word[index - 1])
				index = index + 1

		elif word.count("A") == 1: #checks if A occurs only once.
			for letter in word:
				if letter == "A":
					if index == 0:
						letter_after.append(word[index + 1]) 

					elif index == len(word) -1:
						letter_before.append(word[index - 1])

					else:
						letter_after.append(word[index + 1])
						letter_before.append(word[index - 1])

				index = index + 1
#removes all uppercase from the list
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)
#removes all uppercase from the list
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_1 = frequency_analysis(new_letter_before) #find the frequncy of the list of letters
	most_freq_1 = sorted(freq_1,key=freq_1.get, reverse=True) #sorts into most to least frequent.

	freq_2 = frequency_analysis(new_letter_after) #finds the frequncy of the list of letters
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True)#sorts from most to least frequent.

	if len(most_freq_2) > 0:
		i = 0
		j = 0
		while i < len(bigrams_options):
			if not most_freq_2[i].isupper():
				if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #checks if element i is greater than element i+1 in the list.
					lock.acquire()
					original_letter.put(most_freq_2[i]) #adds i to the queue.
					letters_in_uses.put(bigrams_options[i])
					lock.release()

				elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if element i is equal to element i+1 in the list.
					if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of element i is greater then the frequency of element i+1.
						lock.acquire()
						original_letter.put(most_freq_2[i]) # element i of the list is added to the queue.
						letters_in_uses.put(bigrams_options[i])
						lock.release()

					elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]: #checks to see if the frequency of element i is less than element i+1 in the list.
						j = j + 1

						lock.acquire()
						original_letter.put(most_freq_2[j]) #adds i+1 to the queue.
						letters_in_uses.put(bigrams_options[i])
						lock.release()

			elif most_freq_2[j].isupper():
				i = i - 1

			i = i + 1
			j = j + 1
#This module take word with E in them then takes the most frequent letter after E and maps it to S.
def bigram_ES(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	bigrams_options_after = ["S"]
	bigrams_text = []
	letter_after = []
	new_letter_after = []
	#finds all the words that contain an E that are not all uppercased and is alphabetical.
	for word in attempt1:
		if len(word) >= 2 and "E" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)
	#fnd all the letters after E and adds them to a list.
	for word in bigrams_text:
		index = 0
		if word.count("E") >= 2: #checks if E occurs more tha once.
			for letter in word:
				if letter == "E":

					if index <= len(word) - 2: #adds letter after E to a list.
						letter_after.append(word[index + 1])


				index = index + 1

		elif word.count("E") == 1: #checks to see if E occurs only once.
			for letter in word:
				if letter == "E":

					if index <= len(word) -2: #adds letter after E to a list.
						letter_after.append(word[index + 1])

				index = index + 1

#removes all the uppercased letters from the list.
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_2 = frequency_analysis(new_letter_after) #find the frequency of the letters in the list.
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the list into most to least frequent.

	if len(most_freq_2) > 0 and "S" not in used_letters: #checks if S is already used.
		i = 0
		j = 0
		while i < len(bigrams_options_after): #itterates through the available letter to be mapped to.
			if not most_freq_2[i].isupper():

				if len(most_freq_2) == 1: #if there is only one element in the list then add to the queue.
					lock.acquire()
					original_letter.put(most_freq_2[i]) #adds i in the list to the queue.
					letters_in_uses.put(bigrams_options_after[i])
					lock.release()

				elif freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #checks if the frequency of i in the list is greater then the frequency of i+1 in the list
					lock.acquire()
					original_letter.put(most_freq_2[i]) #add position i in the list to the queue
					letters_in_uses.put(bigrams_options_after[i])
					lock.release()

				elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of position i in the list is equal to the frequency of position i+1 in the list.
					if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of position i is greater than the frequency of position i+1 in the list.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #adds to the position i in the list to the queue.
						letters_in_uses.put(bigrams_options_after[i])
						lock.release()

					elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of position i is less than the frequency of position i+1 in the list.
						j = j + 1

						lock.acquire()
						original_letter.put(most_freq_2[j]) #adds the frequency of position i+1 in the list to the queue.
						letters_in_uses.put(bigrams_options_after[i])
						lock.release()

			elif most_freq_2[j].isupper():
				i = i - 1

			i = i + 1
			j = j + 1
#This module adds all the words with O to a list then find the most frequent word after O and maps that word to U.
def bigram_OU(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	bigrams_options = ["U"]
	bigrams_text = []
	letter_after = []
	new_letter_after = []

	for word in attempt1:
		#find all the word that contain a O and that is not all uppercased anf is alphabetical.
		if len(word) >= 2 and "O" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)
#finds all the letters after O and adds it to a list.
	for word in bigrams_text:
		index = 0
		if word.count("O") >= 2: #checks if O occurs more than once.
			for letter in word:
				if letter == "O":
					if index <= len(word) -2:
						letter_after.append(word[index + 1]) 

				index = index + 1

		elif word.count("O") == 1: #checks if O occurs only once.
			for letter in word:
				if letter == "O":
					if index <= len(word) -2:
						letter_after.append(word[index + 1])

				index = index + 1
#removes all the uppercase letters.
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_2 = frequency_analysis(new_letter_after) #finds the frequency of all the letters
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) # orders the frequency into a list from most to least frequent.


	if len(most_freq_2) > 0:
		i = 0
		j = 0
		while i < len(bigrams_options): #itterates through the available letters to be mapped to.
			if not most_freq_2[i].isupper():
				if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #checks if the frequency of i in the list is greater then the frequency of i+1 in the list
					lock.acquire()
					original_letter.put(most_freq_2[i])
					letters_in_uses.put(bigrams_options[i])
					lock.release()

				elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]:#checks if the frequency of position i in the list is equal to the frequency of position i+1 in the list.
					if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater then the frequency of i+1 in the list
						lock.acquire()
						original_letter.put(most_freq_2[i]) #adds to the position i in the list to the queue.
						letters_in_uses.put(bigrams_options[i])
						lock.release()

					elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of the position of i in the list is less than the position so i+1 in the listchecks if the frequency of position i is less than the frequency of position i+1 in the list.
						j = j + 1

						attempt = attempt.replace(most_freq_2[j], bigrams_options[i])
						lock.acquire()
						original_letter.put(most_freq_2[j]) #adds to the position i+1 in the list to the queue.
						letters_in_uses.put(bigrams_options[i])
						lock.release()

			elif most_freq_2[j].isupper():
				i = i - 1

			i = i + 1
			j = j + 1
#This module finds all the word that second last letter are L then find the most frequent last letter and maps it to Y.
def ending_LY(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	LY = []
	last_letter = []

	for word in attempt1: #this finds all words greater than 2 letters and that have a second last letter that ends in L.
		if len(word) >= 3 and word[len(word) - 2] == "L" and word[len(word) - 1].islower() and not word.isupper() and word.isalpha():
			LY.append(word)
			last_letter.append(word[len(word) - 1])

	freq = frequency_analysis(last_letter)#finds the frequency of the letters in the list.
	most_freq = sorted(freq,key=freq.get, reverse=True)#orders the frequency from most to least frequent.


	if len(most_freq) > 0:
		lock.acquire()
		original_letter.put(most_freq[0]) #add to the queue.
		letters_in_uses.put("Y")
		lock.release()
#This module findsall the words with ENT and then find all the words that appear infront of ENT.The most frequent letter that appears in front of ENT is mapped to M.
def quadgram_MENT(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["M"]
	trigrams_text = []
	letter_before = []
	new_letter_before = []

	for word in attempt1: #finds all the words that contain ENT and are not all uppercased and is alphabetical.
		if len(word) >= 4 and "ENT" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)
#finds all the letters before ENT.
	for word in trigrams_text:
		index = 0
		if word.count("ENT") >= 2: #check if ENT appears more than once.
			for letter in word:
				if letter == "E":
					if index >= 1:
						letter_before.append(word[index - 1])

				index = index + 1

		elif word.count("ENT") == 1: #checks if ENT appears only once.
			for letter in word:
				if letter == "E":
					if index >= 1:
						letter_before.append(word[index - 1])
				index = index + 1
#removes all words that are lowercased.
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)

	freq_2 = frequency_analysis(new_letter_before) #finds the frequency of the letters in the list
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list
			lock.acquire()
			original_letter.put(most_freq_2[0])
			letters_in_uses.put(trigrams_options[0])
			lock.release()

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #adds to the queue
						letters_in_uses.put(trigrams_options[i])
						lock.release()

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
						if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list
							lock.acquire()
							original_letter.put(most_freq_2[i]) #adds to the queue.
							letters_in_uses.put(trigrams_options[i])
							lock.release()

						elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of the position of i in the list is less than the position so i+1 in the list
							j = j + 1
							attempt = attempt.replace(most_freq_2[j], trigrams_options[i])
							lock.acquire()
							original_letter.put(most_freq_2[j]) #adds to the queue
							letters_in_uses.put(trigrams_options[i])
							lock.release()

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1
#This module finds all the words with ER and find the most frequent letter that appears in front of ER and it is mapped to V.
def trigrams_VER(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["V"]
	trigrams_text = []
	letter_before = []
	new_letter_before = []
#finds the letters with ER in them
	for word in attempt1:
		if len(word) >= 3 and "ER" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)
#find the letters before ER.
	for word in trigrams_text:
		index = 0
		if word.count("ER") >= 2: #finds the words where ER occurs more than once.
			for letter in word:
				if letter == "O":
					if index >= 1:
						letter_before.append(word[index - 1])

				index = index + 1

		elif word.count("ER") == 1: #finds the words where ER occurs only once.
			for letter in word:
				if letter == "E":
					if index >= 1:
						letter_before.append(word[index - 1])
				index = index + 1
#remove all the uppercased letters.
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)

	freq_2 = frequency_analysis(new_letter_before) #finds the frequency of the letters in the list
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list
			attempt = attempt.replace(most_freq_2[0], trigrams_options[0])
			original_letter.put(most_freq_2[0])#Adds to the queue
			letters_in_uses.put(trigrams_options[0])

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
						attempt = attempt.replace(most_freq_2[i], trigrams_options[i])
						original_letter.put(most_freq_2[i]) #adds to the queue.
						letters_in_uses.put(trigrams_options[i])

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
						if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list
							attempt = attempt.replace(most_freq_2[i], trigrams_options[i])
							original_letter.put(most_freq_2[i]) #adds to the queue.
							letters_in_uses.put(trigrams_options[i])

						elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of the position of i in the list is less than the position so i+1 in the list
							j = j + 1
							attempt = attempt.replace(most_freq_2[j], trigrams_options[i])
							original_letter.put(most_freq_2[j]) #adds to the queue
							letters_in_uses.put(trigrams_options[i])

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1
#This module finds all the words the end in A followed by a lowercase followed by LE. The most frequent lower case letter will be mapped to B.
def ending_ABLE(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	ABOUT = []
	b_letter = []

	for word in attempt1:
		#this finds all the words the end in A followed by a lowercase followed by LE.
		if len(word) >= 5 and word[len(word) - 4] == "A" and word[len(word) - 3].islower() and word[len(word) - 2:] == "LE" and not word.isupper() and word.isalpha():
			ABOUT.append(word)
			b_letter.append(word[len(word) - 3])

	freq = frequency_analysis(b_letter) #this finds the frequency of all the letters.
	most_freq = sorted(freq,key=freq.get, reverse=True) #this orders the frequencies from most to least frequent.

	if len(most_freq) > 0:
		lock.acquire()
		original_letter.put(most_freq[0]) #adds to the queue.
		letters_in_uses.put("B")
		lock.release()
#finds all the words that contain AN followed by a lowercase then followed by an E. The most frequent lowercae will be mapped to C.
def quadgram_ANCE(attempt, q, letters_in_uses,original_letter, used_letters, freq_single_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["C"]
	trigrams_text = []
	letter_before = []
	new_letter_before = []

	for word in attempt1:
		#finds all the words that contain AN followed by a lowercase then followed by an E.
		if len(word) >= 4 and word[len(word) -4] == "A" and word[len(word) -3] == "N" and word[len(word) -2].islower() and word[len(word) -1] == "E" and not word.isupper() and word.isalpha():
			trigrams_text.append(word)
#finds all the letters that apear before AN
	for word in trigrams_text:
		AN_position = word.index("AN")
		index = 0
		if (len(word) - AN_position) > 2: #checks that the length of the word is long enough so it does give an index out of bounds error.
			letter_before.append(word[AN_position + 2])
#removes all uppercased letters.
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)

	freq_2 = frequency_analysis(new_letter_before) #finds the frequency of the letters in the list
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list
			lock.acquire()
			original_letter.put(most_freq_2[0])#Adds to the queue
			letters_in_uses.put(trigrams_options[0])
			lock.release()

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #adds to the queue.
						letters_in_uses.put(trigrams_options[i])
						lock.release()

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
						if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list
							lock.acquire()
							original_letter.put(most_freq_2[i]) #adds to the queue.
							letters_in_uses.put(trigrams_options[i])
							lock.release()

						elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of the position of i in the list is less than the position so i+1 in the list
							j = j + 1
							#print(i)
							#print(trigrams_options)
							attempt = attempt.replace(most_freq_2[j], trigrams_options[i])
							lock.acquire()
							original_letter.put(most_freq_2[j]) #adds to the queue
							letters_in_uses.put(trigrams_options[i])
							lock.release()

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1
#This finds all words that contain OR and finds the word before OR.The most frequent letter before OR will be mapped to F.
def trigrams_FOR(attempt):
	attempt1 = attempt.strip().split()
	trigrams_options = ["F"]
	trigrams_text = []
	letter_before = []
	new_letter_before = []
#This finds all words that contain OR
	for word in attempt1:
		if len(word) >= 3 and "OR" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)
#finds the word before OR.
	for word in trigrams_text:
		index = 0
		if word.count("OR") >= 2: #checks if OR occurs more than once.
			for letter in word:
				if letter == "O":
					if index >= 1:
						letter_before.append(word[index - 1])

				index = index + 1

		elif word.count("OR") == 1: #checks if OR occurs only once.
			for letter in word:
				if letter == "O":
					if index >= 1:
						letter_before.append(word[index - 1])
				index = index + 1
#removes all the uppercased letters.
	for word in letter_before:
		if word.islower():
			new_letter_before.append(word)

	freq_2 = frequency_analysis(new_letter_before) #finds the frequency of the letters in the list
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list
			attempt = attempt.replace(most_freq_2[0], trigrams_options[0])
			if trigrams_options[0] not in used_letters:
				used_letters.append(trigrams_options[0]) #adds to the list.
				original_letter_list.append(most_freq_2[0])

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
						attempt = attempt.replace(most_freq_2[0], trigrams_options[0])
						if trigrams_options[0] not in used_letters:
							used_letters.append(trigrams_options[0]) #adds to the list
							original_letter_list.append(most_freq_2[0])

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
						if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list
							attempt = attempt.replace(most_freq_2[i], trigrams_options[i])
							if trigrams_options[i] not in used_letters:
								used_letters.append(trigrams_options[i]) #adds to the list

						elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of the position of i in the list is less than the position so i+1 in the list
							j = j + 1

							attempt = attempt.replace(most_freq_2[j], trigrams_options[i])
							if trigrams_options[i] not in used_letters:
								used_letters.append(trigrams_options[i]) #adds to the list.

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1


	return attempt

#This find the words that contain THE and the most frequent letrer after the is mapped to M.
def quadgram_THEM(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["M"]
	trigrams_text = []
	letter_after = []
	new_letter_after = []
#find the words that contain THE.
	for word in attempt1:
		if len(word) >= 4 and "THE" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)
#finds the letters that after THE.
	for word in trigrams_text:
		index = 0
		if word.count("THE") >= 2: #checks if THE appears more than once.
			for letter in word:
				if letter == "T":
					if index <= len(word) -4:
						letter_after.append(word[index + 3])

				index = index + 1

		elif word.count("THE") == 1: #checks if THE appears only once.
			for letter in word:
				if letter == "T":
					if index <= len(word) -4:
						letter_after.append(word[index + 3])
				index = index + 1
#remove all the uppercased letters.
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_2 = frequency_analysis(new_letter_after)
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list
			lock.acquire()
			original_letter.put(most_freq_2[0])#Adds to the queue
			letters_in_uses.put(trigrams_options[0])
			lock.release()

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #adds to the queue.
						letters_in_uses.put(trigrams_options[i])
						lock.release()

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
						if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list
							lock.acquire()
							original_letter.put(most_freq_2[i]) #adds to the queue.
							letters_in_uses.put(trigrams_options[i])
							lock.release()

						elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of the position of i in the list is less than the position so i+1 in the list
							j = j + 1

							attempt = attempt.replace(most_freq_2[j], trigrams_options[i])
							lock.acquire()
							original_letter.put(most_freq_2[j]) #adds to the queue
							letters_in_uses.put(trigrams_options[i])
							lock.release()

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1
#This finds all the words that contain FRO then find the most frequent letter after FRO and maps it to M.
def quadgram_FROM(attempt, q, letters_in_uses,original_letter, used_letters, lock):
	attempt1 = attempt.strip().split()
	trigrams_options = ["M"]
	trigrams_text = []
	letter_after = []
	new_letter_after = []
#This finds all the words that contain FRO.
	for word in attempt1:
		if len(word) >= 4 and "FRO" in word and not word.isupper() and word.isalpha():
			trigrams_text.append(word)
#find the letters the appear after FRO.
	for word in trigrams_text:
		index = 0
		if word.count("FRO") >= 2:#finds all the words that contain FRO more than once.
			for letter in word:
				if letter == "F":
					if index <= len(word) -4:
						letter_after.append(word[index + 3])

				index = index + 1

		elif word.count("FRO") == 1: #finds all the words that contain FRO more than once.
			for letter in word:
				if letter == "F":
					if index <= len(word) -4:
						letter_after.append(word[index + 3])
				index = index + 1
#removes all the uppercased letters.
	for word in letter_after:
		if word.islower():
			new_letter_after.append(word)

	freq_2 = frequency_analysis(new_letter_after) #finds the frequency of all the letters.
	most_freq_2 = sorted(freq_2,key=freq_2.get, reverse=True) #orders the letters from most to least frequent in a list.

	if len(most_freq_2) > 0:
		if len(most_freq_2) == 1: #Checks if there is only one letter in the list
			lock.acquire()
			original_letter.put(most_freq_2[0])#Adds to the queue
			letters_in_uses.put(trigrams_options[0])
			lock.release()

		else:
			i = 0
			j = 0
			while i < len(trigrams_options):
				if not most_freq_2[i].isupper():
					if freq_2[most_freq_2[i]] > freq_2[most_freq_2[i + 1]]: #If the frequency of the first value is greater than the frequency of the second letter.
						lock.acquire()
						original_letter.put(most_freq_2[i]) #adds to the queue.
						letters_in_uses.put(trigrams_options[i])
						lock.release()

					elif freq_2[most_freq_2[i]] == freq_2[most_freq_2[i + 1]]: #checks if the frequency of the first and second frequency values are the same.
						if freq_single_letters[most_freq_2[i].lower()] > freq_single_letters[most_freq_2[i + 1].lower()]: #checks if the frequency of i in the list is greater than the frequency of i+1 in the list
							lock.acquire()
							original_letter.put(most_freq_2[i]) #adds to the queue.
							letters_in_uses.put(trigrams_options[i])
							lock.release()

						elif freq_single_letters[most_freq_2[i].lower()] < freq_single_letters[most_freq_2[i + 1].lower()]:#checks if the frequency of the position of i in the list is less than the position so i+1 in the list
							j = j + 1

							attempt = attempt.replace(most_freq_2[j], trigrams_options[i])
							lock.acquire()
							original_letter.put(most_freq_2[j]) #adds to the queue
							letters_in_uses.put(trigrams_options[i])
							lock.release()

				elif most_freq_2[j].isupper():
					i = i - 1

				i = i + 1
				j = j + 1
#This find all the words that contain the letter T. This finds the most frequent letter before T and maps it to S.
def bigram_T(attempt, q, letters_in_uses,original_letter, used_letters,lock):
	attempt1 = attempt.strip().split()
	bigrams_text = []
	letter_before = ["S"]
#finds all the words that contain T.
	for word in attempt1:
		if len(word) >= 2 and "T" in word and not word.isupper() and word.isalpha():
			bigrams_text.append(word)
#finds all the letters that occur before T.
	for word in bigrams_text:
		index = 0
		if word.count("T") >= 2: #finds words where T occurs more than once.
			for letter in word:
				if letter == "T":
					if index == 0:
						pass 

					elif index == len(word) -1:
						letter_before.append(word[index - 1])

					else:
						letter_before.append(word[index - 1])

				index = index + 1

		elif word.count("T") == 1: #finds T where T occurs only once.
			for letter in word:
				if letter == "T":
					if index == 0:
						pass 

					elif index == len(word) -1:
						letter_before.append(word[index - 1])

					else:
						letter_before.append(word[index - 1])

				index = index + 1

	if "S" not in used_letters:
		freq = frequency_analysis(letter_before) #find the frequency of the letters.
		most_freq_1 = sorted(freq,key=freq.get, reverse=True) #orders the frequency from most to least frequent in a list.

		lock.acquire()
		original_letter.put(most_freq_1[0]) #adds to the queue.
		letters_in_uses.put("S")
		lock.release()


if __name__ == '__main__':
	import time

	file = input('Please enter filename wish to decrypt: ') #asks for the file you want to decrypt.
	key_file = file + '-key.txt' #adds the end as requested in the specification requirements.
	decrypted_file = file + '-decrypted.txt' #adds the end as requested in the specification requirements.

	start = time.perf_counter() #timer is started to meaure the execution of the program.
	f = open(file, "r") #opens the cipher text file that is inputted.
	encrypted_message = f.read() #renames the file.
	attempt = encrypted_message.lower() #makes the file lowercased
	freq_single_letters = frequency_analysis(attempt) # counts the frequency of all the letters in the cipher text.


	words_2 = open("most_freq_two_letter.txt", "r")#opens the file with the most common two letter words 
	two = words_2.read()

	words_3 = open("most_freq_three_letter.txt", "r")#opens the file with the most common three letter words
	three = words_3.read()

	words_4 = open("most_freq_four_letter.txt", "r")#opens the file with the most common four letter words
	four = words_4.read()

	words_5 = open("most_freq_five_letter.txt", "r")#opens the file with the most common five letter words
	five = words_5.read()

	used_letters = []
	original_letter_list = []
	used_list = []

	q = Queue() #creates a queue.
	lock = Lock() #creates a lock.
	letters_in_uses = Queue() #create a new queue.
	original_letter = Queue() #creates a new queue.
	#processes run in parallel.
	P1= Process(target=single_letter, args=(attempt, freq_single_letters, q, letters_in_uses, original_letter,lock))
	P2 = Process(target=single_letter_word, args=(attempt, q, letters_in_uses,original_letter,lock))
	P1.start() #starts the process
	P2.start() #starts the process
	P1.join()#this stops the parent process untill the child process is finished
	P2.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		used_letters.append(str(used)) #appends to list 
		original_letter_list.append(str(original)) #appends to a list.
		attempt = attempt.replace(original, used)

	attempt = strip_punctuation(attempt)

	P3 = Process(target=finding_H_by_THE, args=(attempt, q, letters_in_uses,original_letter,lock))
	P4 = Process(target=bigram_E, args=(attempt, q, letters_in_uses,original_letter,lock))
	P3.start() #starts the process
	P4.start() #starts the process
	P3.join()#this stops the parent process untill the child process is finished
	P4.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	P6 = Process(target=bigram_H, args=(attempt, q, letters_in_uses,original_letter, used_letters,lock))
	P7 = Process(target=bigram_AN, args=(attempt, q, letters_in_uses,original_letter, used_letters,lock))
	P6.start() #starts the process
	P7.start() #starts the process
	P6.join()#this stops the parent process untill the child process is finished
	P7.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	P12 = Process(target=trigrams_AND, args=(attempt, q, letters_in_uses,original_letter, used_letters,lock))
	P12.start() #starts the process

	if "I" not in used_letters:
		P24 = Process(target=bigram_T, args=(attempt, q, letters_in_uses,original_letter, used_letters,lock))
		P24.start() #starts the process

	P12.join()#this stops the parent process untill the child process is finished
	if "I" not in used_letters:
		P24.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	P8 = Process(target=bigram_ES, args=(attempt, q, letters_in_uses,original_letter, used_letters,lock))
	P9 = Process(target=bigram_N, args=(attempt, q, letters_in_uses,original_letter, used_letters, freq_single_letters, lock))
	P10 = Process(target=bigram_I, args=(attempt, q, letters_in_uses,original_letter, used_letters, freq_single_letters, lock))
	P8.start() #starts the process
	P9.start() #starts the process
	P10.start() #starts the process
	P8.join()#this stops the parent process untill the child process is finished
	P9.join()#this stops the parent process untill the child process is finished
	P10.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	P11 = Process(target=ending_ing, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P13 = Process(target=quadgram_WITH, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P11.start() #starts the process
	P13.start() #starts the process
	P11.join()#this stops the parent process untill the child process is finished
	P13.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	attempt = trigrams_FOR(attempt)

	P23 = Process(target=quadgram_FROM, args=(attempt, q, letters_in_uses,original_letter, used_letters,lock))
	P21 = Process(target=quadgram_ANCE, args=(attempt, q, letters_in_uses,original_letter, used_letters, freq_single_letters, lock))
	P23.start() #starts the process	
	P21.start() #starts the process
	P21.join()#this stops the parent process untill the child process is finished
	P23.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	P18 = Process(target=quadgram_MENT, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P18.start() #starts the process
	P18.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	attempt = double_two_letters(attempt)

	P15 = Process(target=bigram_OU, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P16 = Process(target=double_two_letters_ending, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P15.start() #starts the process
	P16.start() #starts the process
	P15.join()#this stops the parent process untill the child process is finished
	P16.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)


	P20 = Process(target=ending_ABLE, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P20.start() #starts the process
	P20.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	P17 = Process(target=ending_LY, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P19 = Process(target=trigrams_VER, args=(attempt, q, letters_in_uses,original_letter, used_letters, lock))
	P17.start() #starts the process
	P19.start() #starts the process
	P17.join()#this stops the parent process untill the child process is finished
	P19.join()#this stops the parent process untill the child process is finished

	while letters_in_uses.qsize() > 0: #checks if the q is not empty
		original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
		used = letters_in_uses.get()
		if used not in used_letters:
			used_letters.append(str(used)) #appends to list 
			original_letter_list.append(str(original)) #appends to a list.
			attempt = attempt.replace(original, used)

	if "M" not in used_letters: #checks to see if M is already used
		P22 = Process(target=quadgram_THEM, args=(attempt, q, letters_in_uses,original_letter, used_letters,lock))
		P22.start() #starts the process
		P22.join()#this stops the parent process untill the child process is finished

		while letters_in_uses.qsize() > 0: #checks if the q is not empty
			original = original_letter.get() #assigns a variable name to the retrieved letter from the queue.
			used = letters_in_uses.get()
			if used not in used_letters:
				used_letters.append(str(used)) #appends to list 
				original_letter_list.append(str(original)) #appends to a list.
				attempt = attempt.replace(original, used)
#These find any lettes that are remaining and try to associate the word woth words in a list of common words stored in a file.
	for i in range(2): #itterates over this twice.
		attempt = two_letter_word(attempt, two)
	attempt = three_letter_word_double_case(attempt, three)
	attempt = four_letter_word(attempt, four)
	attempt= five_letter_word(attempt, five)

	finish = time.perf_counter()

	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	not_found = ""
	for letter in alphabet:
		if letter not in used_letters:
			not_found = not_found + " " + letter

	print(f"Finished in {round(finish-start, 2)} second(s)")

	sorted_keys = {}
	i = 0
	for letter in used_letters:
		sorted_keys[letter] = original_letter_list[i]
		i = i + 1

	keys_list = ''
	i = 0
	for letter in sorted(sorted_keys.keys()):
		keys_list += '{} = {}\n'.format(letter, (sorted_keys[letter].upper()))


	with open(key_file, 'w') as f:
		f.write(keys_list)
	with open(decrypted_file, 'w') as f:
		f.write(attempt.lower())
	print('Keys saved in file: {}\nDecrypted text saved in file: {}'.format(key_file, decrypted_file))
	sys.exit(1)