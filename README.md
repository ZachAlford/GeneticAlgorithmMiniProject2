# Genetic Algorithm Mini-Project 2

Zach Alford

SYS 411 Machine Learning

Spring 2016 (edited 9/20/16)

For this project, I use a genetic algorithm (“GA”) to build a classifier for the Fisher’s Iris Data, a well-known dataset with 150 subjects. Each subject has 4 defining characteristics (“petal length,” “petal width,” “sepal length,” and “sepal width”), and each subject is classified into 1 of 3 classes (“0,” “1,” and “2”). See [https://en.wikipedia.org/wiki/Iris_flower_data_set](https://en.wikipedia.org/wiki/Iris_flower_data_set).

The GA finds individuals with optimal parameters for a linear function whose output is a rational number near 0, 1, or 2; whichever of those three numbers the output is closest to, the classification is that number. More specifically, the function is *f(PetalLength, PetalWidth) = ((A/B)* \* *PetalLength) + ((C/D)* \* *PetalWidth) + (E/F)*, and the parameters are *A, B, C, D, E, F*. I allowed these parameters to have the integer range -100 and 100 (inclusive). I have chosen the function to disregard the other two features of the cases (that is, sepal length and sepal width) as noisy data.

This project’s implementation built off of last project’s implementation in several ways. In this project, I implemented a class called *Gene*, and a class called *Genotype*, to be able to handle a genotype with varying numbers of genes (the genes all being the same size). I changed the *Individual* class to allow for each individual in the population to be a classifier, with access to a data structure (which comes from the file *Dataset.py*, which processes the data in the file *FID.txt*) to access the Fisher’s Iris Data.

Run the program by using `python3 GA.py` at the command line (I have used python version 3.5.2). I have found my results by using a population size of 10, a mutation rate of 0.01, a cross-over rate of 0.6, using two crossover points, with 1000 being the maximum number of generations (the program will ask you for your preference). The program is set to stop if it calculates an individual with 96% correctness in classification. The program reports the genotype of the most fit individual by printing out “Most fit individual: Genotype’s values:” followed by the genotype’s encoded values for parameters *A* through *F* (respectively).

In the file *FIDClassifier.xlsx*, I have cross-checked the correctness of the parameter values of one individual (“Classifier1”) that is a result of the GA. Note that, in *FIDClassifier.xlsx*, column G mimics the function *f*, using the parameter values embodied within an individual’s genotype (that is, I used the parameter values printed out by *GA.py*; in this case, the values   -5, -53, -56, -56, 49, -103 for parameters *A* through *F*, respectively). This individual classified correctly 141 of the 150 subjects, for a 94% correct classification. I have realized, however, that the print statements in the output of *GA.py*, however, sometimes reports slightly different fitness values for the individual than does *FIDClassifier.xlsx*; this is because the formula in column G of *FIDClassifier.xlsx* will round up, to sometimes give the (always incorrect) classification of ‘3’, whereas the individuals in *GA.py* are set to classify as high as ‘2.’ Regardless, *FIDClassifier.xlsx* should not report significantly different performance of the individual than does GA.py’s print statements. In conclusion, *FIDClassifier.xlsx* indicates that my genetic algorithm program can produce classifiers that are nearly completely correct in their classifying the Fisher’s Iris Dataset.

