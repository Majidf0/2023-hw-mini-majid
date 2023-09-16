Answers to the questions posed by the excercises

<h1>Excercise 1</h1>

Question 01  

Before running the exercise01.py program, about how long do you think the program above will take to run? Did you have the right answer -- what does the program print out?

<b>Answer:  

Before: The program runtime will be equal to the loop cycle number times the sleep duration amount.  

After: The measured runtime is always longer than the predicted runtime. Interestingly, this discrepiancy gets longer for more extreme testing cases with larger cycle numbers and shorter sleep duration. We tried to see if this corrolates to the clock speed, but the discrepiancies appear at much slower speeds of about 1MHZ (#Cycles/Sleep Duration) as compared to the Pico clock speed of about 125MHZ.
</b>

Question 02

What do the "int" and "float" notation mean?

Will the program run if these notations are removed or incorrect?  

<b>Answer: int and float refer to the types of data classified for sleep duration and cycle number, with the former reffering to integer numbers and the latter to floating point numbers. There cannot be "half" cycles, thus the int notaion is used for that variable, where as sleep duration is given the freedom to take on decimal values</b>


Question 03  

Why is "time.ticks_diff(toc, tic)" used to determine elapsed time instead of "toc - tic"?  

<b>Answer: in MicroPython, ticks.ms(), the method used to assign values to toc and tic, can wrap around upon reaching a certain number Tick MAX. Subtracting tic from toc as proposed would lead to incorrect answers as result of this wrap around.</b>

<h1>Excercise 2</h1>

Question 01  
Why do you think we would use a file (e.g. JSON file) for parameter storage instead of accepting the parameters as user input(), especially on an embedded system?  

<b>Answer:To reduce the need for external input or external storage accessing. Since the values are already stored in the system, it can quickly access the file internally. In an embedded system, this is even more crucial since the system and its internal components are optimized for quick internal communication.</b>

Question 02  
Why might we prefer to use a JSON file to store parameters instead of hard-coding values in the Python script?  

<b>Answer: We can alter the parameters without running the risk of changing the code. Might be faster since the board doesn't have to recheck the entire code since it hasnt changed, and just needs to refresh its view of the JSON file</b>

Question 03  
Why didn't the exercise02.py code use os.path.isfile, that is, why did I write the "is_regular_file()" function?

<b>Answer: Due to the limitations of MicroPython. The os.path.isfile method isn't within the MicroPython library, meaning the function must be created from scratch</b>

<h1>Excercise 3</h1>  

Question 1   

Suppose I want to add additional code that requires me to increase sample time, to allow more time for the additional code to execute. What is the tradeoff when I increase sample time relative to the "dot_dash_threshold" value? Try this by increasing "sample_ms" in exercise3.json on the Pico. The effect should be quite noticeable. 

<b>Answer: The accuracy of the recording drops signifigantly. This is because of the increased sleep time, which can misread button inputs or miss them</b>

<h1>Excercise 4</h1>  

Check top-level "Answers" folder.
