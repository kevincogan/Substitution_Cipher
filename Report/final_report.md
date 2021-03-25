The Beginning

How I Chose This Method

Before starting the project I set a clear goal which was to decrypt the cipher text in the fastest time. I then broke down the goal into smaller objectives keeping the specification requirements in mind. The objectives I set were:
Find the fastest algorithm that will enable me to decrypt my cipher
Use threading or multi-processing to enable my program to run as fast as possible.
Select an algorithm that allows threading/multi-processing to be integrated easily integrated into my code.
With these three objectives in mind  I research many different algoriths online. There were many algorithms that would decrypt the cipher code quickly however there was difficulty in implenting threading or multi-processing. I found this issue in the hill climbing algorithm. I finally found the perfect solution which was frequency analysis. 

Why I Chose This Method

I selected this method as it  fulfilled my three objectives above and I felt I could use knowledge from my other modules and demonstrate them in this assignment. Principles from software testing and probability and statistics came very useful to coming up with a solution using this method. Frequency Analysis deciphers the cipher text using probability and statistics based on how often letter and words occur. This enabled me to used R programming language to quickly and easily find a solution by the used of simulations. With this information I used the R program to find the cobinations that will give me the gratest probabilities of success. It will also show me what letters are mutially exculsive and what letters are dependant on other letter. This will help to mitigate the probability of getting failure while decrypting the cipher text. In conclusion, I selected frequency analysis as it fulfills my three objectives above and can be simulated using the R programming language easily.






How I Tested The Program To Determine Which Method Was Fastest

I tested my code regularly as I developed my code. Once I had my first functioning Frequency Analysis program I created an automated test that will take five texts of different lengths and run them through my program. A timer in my program record how long it takes to execute the program, my automated test verifies if the output mapping of letters of my program is incorrect as well as providing a list of letters not used. This enabled me to see comon issues across the different texts so I can modify the my code without any negative effects such as bugs.  
Once I was happy with the single threaded program I added it to my automated test to be compared against my code with multi-processing. All the times from the automated program are output into a text file and formated so it can easily be compared in a grid format. I discovered that small text files were faster with single threaded application while large text files were decrypted significantly faster by multi-processing program.

What Do These Results Mean

These results suggest that for small sized text files the single threaded application will process the information faster than the slower multi-processing application. However the multi-processing application becomes increasingly faster as the larger text file size increases. The large text file can be processed faster by multi-processing as the work is being shared between multiple CPU’s in parallel meaning it can complete large tasks very quickly. The single threaded application was very slow all the information had to be processed by that single thread. On the other hand the single threaded application achieved processing small text files faster. I used an application that monitored the CPU’s as I ran the programs and it was intresting to see that ehen the single threaded application was run with the large text file 100% of the selected CPU was being used while when it was ran against the small text file onlu 40-60% of the selected CPU was used. From this information I believe the single threaded application is slower with large text files as it is overloaded with inputted information so  the inputted information has to wait until a free space becomes available to be processed. I believe the multi-processes application is slower for small application as the processes have to communicate with each other, such as using locks and join methods in multi-processing, which is inefficent with small input.



What Would I Do Differently

If I were to undertake thus task again I would:

Use Classes in my program as it would make my code more strucured and make it easier for the modules  to communicate to each other. 

Used decrypted sample texts from different forms such as newspapers, books, online blogs. This is because the test cases I used in my automatic test used books written by Charles Dickenson. Dickenson’s writing technique are very simular throughout his novels so when I was testing it picked up very few errors. Next time I will pick a derverse range of texts from different media forms.

Repetition in my code is very prevelant. I would be able to reduce the repetitions of code by creating a single module with parameters to be inputted so the code can be resused easily. This will reducing the repetitions of my code significantly.
I would like to try implement threading with my multi-proccessing code as I feel it would my communication and processing of data more efficient. Threading was not on my mind from the beginning of the project so I did structure my code in a way that I could easily impliment the code quickly. Next time try implent threading when structuring my code.

I would constantly keep saving copies of my code as when I make modifications to my code to fix bugs it can oftne cause more errors. This happened to me at the start and I could’nt restore my code back to the original state resulting it hours spent try to debug the code. This lead to me creating patches to fix my code making it very unstructured.
