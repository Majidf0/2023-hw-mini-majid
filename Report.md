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
