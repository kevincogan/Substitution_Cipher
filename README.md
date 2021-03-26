# Substitution Cipher with Multi-Threading

This code uses multi-threading to decipher text by substitution cipher.


**How I Chose This Method**

Before starting the project I set a clear goal which was to decrypt the cipher text in the fastest time. I then broke down the goal into smaller objectives keeping the specification requirements in mind. The objectives I set were:
1.  Find the fastest algorithm that will enable me to decrypt my cipher.
2.  Use threading or multiprocessing to enable my program to run as fast as possible.
3.  Select an algorithm that allows threading/multi-processing to be easily integrated into my code.


With these three objectives in mind  I research many different algorithms online. There were many algorithms that would decrypt the cipher code quickly however there was difficulty in implementing threading or multiprocessing. I found this issue in the hill climbing algorithm. I finally found the perfect solution which was frequency analysis. 


**Why I Chose This Method**

I selected this method as it  fulfilled my three objectives above and I felt I could use knowledge from my other modules and demonstrate them in this assignment. Principles from software testing and probability and statistics came very useful to coming up with a solution using this method. Frequency Analysis deciphers the cipher text using probability and statistics based on how often letters and words occur. This enabled me to use R programming language to quickly and easily find a solution by the use of simulations. With this information I used the R program to find the combinations that will give me the greatest probabilities of success. It will also show me what letters are mutually exclusive and what letters are dependent on other letters. This will help to mitigate the probability of getting failure while decrypting the cipher text. In conclusion, I selected frequency analysis as it fulfills my three objectives above and can be simulated using the R programming language easily.



**How I Tested The Program To Determine Which Method Was Fastest**

I tested my code regularly as I developed my code. Once I had my first functioning Frequency Analysis program I created an automated test that will take five texts of different lengths and run them through my program. A timer in my program records how long it takes to execute the program, my automated test verifies if the output mapping of letters of my program is incorrect as well as providing a list of letters not used. This enabled me to see common issues across the different texts so I can modify my code without any negative effects such as bugs.  
Once I was happy with the single threaded program I added it to my automated test to be compared against my code with multi-processing. All the times from the automated program are output into a text file and format so it can easily be compared in a grid format. I discovered that small text files were faster with single threaded applications while large text files were encrypted significantly faster by multi-processing programs.


**What Do These Results Mean**

These results suggest that for small sized text files the single threaded application will process the information faster than the slower multi-processing application. However the multi-processing application becomes increasingly faster as the larger text file size increases. The large text file can be processed faster by multi-processing as the work is being shared between multiple CPUs in parallel meaning it can complete large tasks very quickly. The single threaded application was very slow; all the information had to be processed by that single thread. On the other hand the single threaded application achieved processing small text files faster. I used an application that monitored the CPU’s as I ran the programs and it was interesting to see that when the single threaded application was run with the large text file 100% of the selected CPU was being used while when it was ran against the small text file only 40-60% of the selected CPU was used. From this information I believe the single threaded application is slower with large text files as it is overloaded with inputted information so  the inputted information has to wait until a free space becomes available to be processed. I believe the multi-processes application is slower for small applications as the processes have to communicate with each other, such as using locks and join methods in multi-processing, which is inefficient with small input.

