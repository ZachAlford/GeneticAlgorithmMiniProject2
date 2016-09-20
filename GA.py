from random import *
from DataSet import *

class Gene:
    def __init__(self, InclusiveLowerBound, InclusiveUpperBound, NumberOfGeneDigits):
        X = randint(InclusiveLowerBound, InclusiveUpperBound) # an integer, 0 to 2**16 - 1
        self.__BitString = self.Int2BitString(X, NumberOfGeneDigits)

    def Int2BitString(self, Int, NumberOfGeneDigits): ## example Int2BitString(128) -> '10000000'
        IntIsNegative = Int < 0
        BitString = (bin(Int))[2:]
        if IntIsNegative:
            BitString = (bin(Int)[3:])
        else:
            BitString = (bin(Int)[2:])
        # BitString is as short as 1 character, so pad 0's until len(BitString) == GeneLength
        while len(BitString) < NumberOfGeneDigits:
            BitString = '0' + BitString
        if IntIsNegative:
            BitString = '1' + BitString
        else:
            BitString = '0' + BitString
        return BitString

    def BitString2Int(self): ## example BitString2Int('1111111111111111') -> 65535
        AbsoluteValue = int(self.__BitString[1:], 2)
        if self.__BitString[0] == '1':			
            return -1 * AbsoluteValue
        else:
            return AbsoluteValue

    def BitString(self):
        return self.__BitString

    def ToString(self):
        Str = ''
        if self.BitString2Int() < 0:
            Str += '-' + self.BitString()[1:]
        else:
            Str += '+' + self.BitString()[1:]
        return Str + ', '

    def SetBitString(self, NewBitString):
        self.__BitString = NewBitString

'''
G = Gene(-3, 3, 5)
print(G.ToString())
print(str(G.BitString2Int()))
'''

class Genotype:#where each of the genes are the same length
    def __init__(self, NumberOfGenes, InclusiveLowerBound, InclusiveUpperBound, NumberOfGeneDigits):
        self.__NumberOfGeneDigits = NumberOfGeneDigits
        self.__NumberOfGenes = NumberOfGenes
        self.__GeneList = []
        for i in range(0, NumberOfGenes):
            self.__GeneList.append(Gene(InclusiveLowerBound, InclusiveUpperBound, NumberOfGeneDigits))

    def BitString(self):
        Str = ''
        for Gene in self.__GeneList:
            #print(Gene.ToString())
            Str += Gene.BitString()
        return Str

    def BitStringToString(self):
        Str = ''
        for Gene in self.__GeneList:
            Str += Gene.ToString()
        return Str
    
    def ValuesToString(self):
        Str = 'Genotype\'s values: '
        for Gene in self.__GeneList:
            Str += str(Gene.BitString2Int()) + ', '
        return Str

    def SetBitString(self, NewBitString):
        for i in range(0, len(self.__GeneList)):
            LowIndex = i*(self.__NumberOfGeneDigits + 1)
            HighIndex = LowIndex + self.__NumberOfGeneDigits + 1
            self.__GeneList[i].SetBitString( NewBitString[LowIndex:HighIndex] )

    def Gene(self, Index):
        return self.__GeneList[Index]

    def Invalid(self):
        for i in range(0, self.__NumberOfGenes):
            if i == 1 or i == 3 or i == 5:
                if self.Gene(i).BitString2Int() == 0:
                    return True
        return False
'''
G = Genotype(2, -10, 10, 6)
G2 = Genotype(2, -10, 10, 6)
print('G.BitString():  ' + G.BitString())
print(G.ToString())
print('G2.BitString(): ' + G2.BitString())
print(G2.ToString())
G.SetBitString(G2.BitString())
print('G.BitString():  ' + G.BitString())
print(G.ToString())
print('G2.BitString(): ' + G2.BitString())
print(G2.ToString())
'''

class Individual:
    DataSet = DataSet()
    
    def Classification(self, Case):
        A = self.Genotype.Gene(0).BitString2Int()
        B = self.Genotype.Gene(1).BitString2Int()
        C = self.Genotype.Gene(2).BitString2Int()
        D = self.Genotype.Gene(3).BitString2Int()
        E = self.Genotype.Gene(4).BitString2Int()
        F = self.Genotype.Gene(5).BitString2Int()
        Number = (Case.PetalLength)*(A/B) + (Case.PetalWidth)*(C/D) + (E/F)
##        print('Number: ' + str(Number))
        DifferenceToZero = abs(Number - 0)
        DifferenceToOne = abs(Number - 1)
        DifferenceToTwo = abs(Number - 2)
##        if (DifferenceToZero <= DifferenceToOne) and (DifferenceToZero <= DifferenceToTwo):
##            return 0
##        elif (DifferenceToOne <= DifferenceToZero) and (DifferenceToOne <= DifferenceToTwo):
##            return 1
##        else:
##            return 2
        if abs(Number) > 1.5:
            return 2
        elif abs(Number) > .5:
            return 1
        else:
            return 0
        
    def Fitness(self):
        # returns a numeric value as the raw fitness
        if self.Genotype.Invalid():
            return 0
        CorrectnessCount = 0
        for Case in Individual.DataSet.ListOfCases:
            if self.Classification(Case) == Case.Classification:
                CorrectnessCount += 1
        return CorrectnessCount

    def WriteCorrectnessToFile(self):
        if self.Genotype.Invalid():
            return 0
        OutputFile = open( 'Classifier1.txt' , 'w')
        CorrectnessCount = 0
        for Case in Individual.DataSet.ListOfCases:
            OutputFile.write("%s\n" % (self.Classification(Case)))
            if self.Classification(Case) == Case.Classification:
                CorrectnessCount += 1
        return CorrectnessCount
        OutputFile.close()

    
    def Solution(self):
        # returns a numeric value as the solution to the fitness function
        return Individual.DataSet.Length

    def FitnessAsPercentage(self, Fitness):
        CorrectnessFraction = Fitness / Individual.DataSet.Length
        return round(CorrectnessFraction*100, 4)

    def __init__(self):
##        self.Genotype = XAsBitString + YAsBitString
##        self.Genotype = '0'
        self.Genotype = Genotype(6, -100, 100, 7)
        

    def OnePointCrossover(self, OtherIndividual):
        CrossoverIndex = randint(0, len(self.Genotype.BitString()) )
##        print('CrossoverIndex: ' + str(CrossoverIndex))
        SelfLeftHalf = self.Genotype.BitString()[:CrossoverIndex]
        SelfRightHalf = self.Genotype.BitString()[CrossoverIndex:]
##        print('I1: ' + SelfLeftHalf + '   ' + SelfRightHalf)
        OtherLeftHalf = OtherIndividual.Genotype.BitString()[:CrossoverIndex]
        OtherRightHalf = OtherIndividual.Genotype.BitString()[CrossoverIndex:]
##        print('I2: ' + OtherLeftHalf + '   ' + OtherRightHalf)


        self.Genotype.SetBitString(SelfLeftHalf + OtherRightHalf)
        OtherIndividual.Genotype.SetBitString(OtherLeftHalf + SelfRightHalf)
##        print('I1: ' + self.Genotype.BitString()[:CrossoverIndex] + '   ' + self.Genotype.BitString()[CrossoverIndex:])
##        print('I2: ' + OtherIndividual.Genotype.BitString()[:CrossoverIndex] + '   ' + OtherIndividual.Genotype.BitString()[CrossoverIndex:])

    def TwoPointCrossover(self, OtherIndividual):
        LeftCrossoverIndex = randint(0, len(self.Genotype.BitString()) )
        RightCrossoverIndex = randint(LeftCrossoverIndex, len(self.Genotype.BitString()) )
##        print('LeftCrossoverIndex: ' + str(LeftCrossoverIndex))
##        print('RightCrossoverIndex: ' + str(RightCrossoverIndex))
        SelfLeftThird = self.Genotype.BitString()[:LeftCrossoverIndex]
        SelfMiddleThird = self.Genotype.BitString()[LeftCrossoverIndex:RightCrossoverIndex]
        SelfRightThird = self.Genotype.BitString()[RightCrossoverIndex:]
##        print('I1: ' + SelfLeftThird + '   ' + SelfMiddleThird + '   ' + SelfRightThird)
        OtherLeftThird = OtherIndividual.Genotype.BitString()[:LeftCrossoverIndex]
        OtherMiddleThird = OtherIndividual.Genotype.BitString()[LeftCrossoverIndex:RightCrossoverIndex]
        OtherRightThird = OtherIndividual.Genotype.BitString()[RightCrossoverIndex:]
##        print('I2: ' + OtherLeftThird + '   ' + OtherMiddleThird + '   ' + OtherRightThird)

        self.Genotype.SetBitString(OtherMiddleThird + SelfLeftThird + SelfRightThird)
        OtherIndividual.Genotype.SetBitString(SelfMiddleThird + OtherLeftThird + OtherRightThird)

        NewLeftCrossoverIndex = RightCrossoverIndex - LeftCrossoverIndex

##        print('I1: ' + self.Genotype.BitString()[:NewLeftCrossoverIndex] + '   ' + self.Genotype.BitString()[NewLeftCrossoverIndex:RightCrossoverIndex] + '   ' + self.Genotype.BitString()[RightCrossoverIndex:])
##        print('I2: ' + OtherIndividual.Genotype.BitString()[:NewLeftCrossoverIndex] + '   ' + OtherIndividual.Genotype.BitString()[NewLeftCrossoverIndex:RightCrossoverIndex] + '   ' + OtherIndividual.Genotype.BitString()[RightCrossoverIndex:])

    def ApplyCrossover(self, OtherIndividual, NumberOfCrossoverPoints):
        ## Applies Crossover to self and to OtherInvidual, editing their Genotype
        if NumberOfCrossoverPoints == 1:
            self.OnePointCrossover(OtherIndividual)
        else:
            self.TwoPointCrossover(OtherIndividual)

    def ApplyMutation(self):
        RandomIndex = randint(0, len(self.Genotype.BitString()) - 1)
        GenotypeAsList = list(self.Genotype.BitString())
        if GenotypeAsList[RandomIndex] == '1':
            GenotypeAsList[RandomIndex] = '0'
        else:
            GenotypeAsList[RandomIndex] = '1'
        NewGenotype = ''
        for Character in GenotypeAsList:
            NewGenotype += Character
        self.Genotype.SetBitString(NewGenotype)

    def ToString(self, NumberOfSpaces):
        return self.Genotype.BitStringToString()
##        Str = str(self.FitnessAsPercentage(self.Fitness()))
##        Str = NumberOfSpaces + 'Genotype:     ' + self.Genotype + '\n' 
####        Str += NumberOfSpaces + 'XAsBitString: ' + self.XAsBitString() + '\n' 
####        Str += NumberOfSpaces + 'YAsBitString:                 ' + self.YAsBitString() + '\n' 
####        Str += NumberOfSpaces + 'XAsInt: ' + str(self.XAsInt()) + '\n' 
####        Str += NumberOfSpaces + 'YAsInt: ' + str(self.YAsInt())
##        Str += NumberOfSpaces + 'Fitness: ' + str(self.Fitness())
##        return Str

##I1 = Individual()
##print(I1.ToString(''))
##print(I1.Fitness())
##print(I1.FitnessAsPercentage(I1.Fitness()))
##I1.ApplyMutation()
##print(I1.ToString(''))
##print(I1.Fitness())
##I2 = Individual()
##print(I2.ToString(''))
##print('ApplyCrossover')
##I1.ApplyCrossover(I2, 2)
##print(I1.ToString(''))
##print(I2.ToString(''))
####print(Int2BitString(65535))
####print(BitString2Int( Int2BitString(65535) ))
####print(Int2BitString(1))
####print(BitString2Int( Int2BitString(1) ))
####print(Int2BitString(0))
####print(BitString2Int( Int2BitString(0) ))
####print(BitString2Int('1111111111111111'))
####print(BitString2Int('0000000000000001'))



class IndividualList:
    def __init__(self):
        self.List = []

    def GetRandomIndividualWithReplacement(self):
        return sample(self.List, 1)[0]

    def GetAndRemoveRandomIndividual(self):
        RandomIndividual = self.GetRandomIndividualWithReplacement()
        self.List.remove( RandomIndividual )
        return RandomIndividual

    def ResetList(self):
        self.List = []

    def ShuffleList(self):
        shuffle(self.List)

    def BestFitness(self):
        BestFitness = self.List[0].Fitness()
        for Individual in self.List:
            IndividualFitness = Individual.Fitness()
            if IndividualFitness > BestFitness:
                BestFitness = IndividualFitness
        return BestFitness

    def MostFitIndividual(self):
        MostFitIndividual = self.List[0]
        for Individual in self.List:
            if Individual.Fitness() > MostFitIndividual.Fitness():
                MostFitIndividual = Individual
        return MostFitIndividual

    def ToString(self, NumberOfSpaces, NumberOfAdditionalSpacesForIndividualObject):
        Str = 'BestFitness: ' + str(self.BestFitness()) + '\n'
        for i in range(1, len(self.List) + 1):
            Str += NumberOfSpaces + 'Individual ' + str(i)
            Str += self.List[i-1].ToString(NumberOfSpaces + NumberOfAdditionalSpacesForIndividualObject)
            Str += '\n'
        return Str


##I1 = Individual()
##print(I1.ToString(' '))
##I2 = Individual()
##IL = IndividualList()
##IL.List.append(I1)
##IL.List.append(I2)
##print(IL.ToString('', ' '))
##print(I1 == I2)
##I3 = I1
##print(I1 == I3)

class GA:
    def __init__(self, PopulationSize, MutationRate, CrossoverRate, NumberOfCrossoverPoints, MaxNumberOfGenerations):
        self.MutationRate = MutationRate
        self.CrossoverRate = CrossoverRate
        self.NumberOfCrossoverPoints = NumberOfCrossoverPoints
        self.MaxNumberOfGenerations = MaxNumberOfGenerations
        self.Population = IndividualList()
        self.MatingPool = IndividualList()
        self.PopulationSize = PopulationSize
        self.MatingPoolSize = PopulationSize
        self.Finished = False
        self.GenerationCount = 1
        self.InitialBestFitness = 0
        self.FinalBestFitness = 0
        self.PercentInitialBestFitness = 0
        self.PercentFinalBestFitness = 0
        self.AverageFitnessDelta = 0
        self.InitializePopulation()

    def CalculateAverageFitnessDelta(self): # e.g. if fitness improves, then the average improvement per generation
        self.AverageFitnessDelta = (self.PercentFinalBestFitness - self.PercentInitialBestFitness) / self.GenerationCount

    def InitializePopulation(self):
        # return an IndividualList object of random Individual objects
        while len(self.Population.List) < self.PopulationSize:
            self.Population.List.append( Individual() )

    def InitializeMatingPool(self):
        self.MatingPool.ResetList()
        while len(self.MatingPool.List) < self.MatingPoolSize:
            Individual1 = self.Population.GetRandomIndividualWithReplacement()
            Individual2 = self.Population.GetRandomIndividualWithReplacement()
            if Individual1.Fitness() >= Individual2.Fitness():
                self.MatingPool.List.append(Individual1)
            else:
                self.MatingPool.List.append(Individual2)

    def ShouldApplyCrossover(self):
        RandomFraction = uniform(0, 1)
        if self.CrossoverRate >= RandomFraction:
            return True
        else:
            return False

    def ShouldApplyMutation(self):
        RandomFraction = uniform(0, 1)
        if self.MutationRate >= RandomFraction:
            return True
        else:
            return False

    def NOffspring(self, N, ParentList):
        OffSpringList = IndividualList()
        for i in range(0, N):
            # make OffSpring a clone of a random parent
            ParentList.ShuffleList()
            OffSpring = ParentList.List[0]
            if self.ShouldApplyCrossover():
                # choose to cross OffSpring with a non-cloned parent, unless len(ParentList.List) == 0,
                # then cross with OffSpring (crossing Offspring with Offspring does not change OffSpring whatsoever)
                OffSpring.ApplyCrossover( ParentList.List[-1], self.NumberOfCrossoverPoints )
            if self.ShouldApplyMutation():
                OffSpring.ApplyMutation()
            OffSpringList.List.append( OffSpring )
##        print('OffSpringList:\n' + OffSpringList.ToString('   ', ' '))
        return OffSpringList

    def UpdatePopulation(self):
        self.Population.ResetList()
        while len(self.Population.List) < self.PopulationSize:
            ParentList = IndividualList()
            ParentList.List.append( self.MatingPool.GetAndRemoveRandomIndividual() )

            ## if MatingPool is empty, but we need 1 more Parent, then the two parents are clones
            if len(self.MatingPool.List) == 0:
                ParentList.List.append( ParentList.List[0] )
            else:
                ParentList.List.append( self.MatingPool.GetAndRemoveRandomIndividual() )
##            print('ParentList:\n' + ParentList.ToString('   ', ' '))
            self.Population.List += self.NOffspring(2, ParentList).List

        ## too many offspring can be added to Population, so remove the latest added offspring until
        ## len(self.Population.List) == self.PopulationSize
        while len(self.Population.List) != self.PopulationSize:
            self.Population.List = self.Population.List[:-1]

    def HasConverged(self):
        if Individual().FitnessAsPercentage(self.Population.BestFitness()) >= 96:
            return True
        if self.GenerationCount == self.MaxNumberOfGenerations:
            return True
        return False

    def Run(self):
##        print('InitialPopulation.List:\n'+ self.Population.ToString('   ', ' '))

        # calculate a statistic
        self.InitialBestFitness = self.Population.BestFitness()

        # the actual body of the GA
        while not self.Finished:
            self.InitializeMatingPool()
##            print('MatingPool:\n' + self.MatingPool.ToString('   ', ' '))
            self.UpdatePopulation()
            self.Finished = self.HasConverged()
            self.GenerationCount += 1
        if self.GenerationCount == self.MaxNumberOfGenerations + 1:
            self.GenerationCount -= 1

        # calculate the rest of the statistics for this GA run
        self.FinalBestFitness = self.Population.BestFitness()
        self.PercentInitialBestFitness = Individual().FitnessAsPercentage(self.InitialBestFitness)
        self.PercentFinalBestFitness = Individual().FitnessAsPercentage(self.FinalBestFitness)
        self.CalculateAverageFitnessDelta()



class GARunner:
    def __init__(self):
        self.PopulationSize = 10
        self.MutationRate = .01
        self.CrossoverRate = .6
        self.NumberOfCrossoverPoints = 2
        self.NumberOfTimesToRun = 4
        self.RunCount = 0
        self.TotalNumberOfGenerations = 0
        self.TotalOfFitnessDeltas = 0
        self.OutputFileName = 'a.txt'
        self.MaxNumberOfGenerations = 1000

    def SetPreferences(self):
        print("Please state the population size (an integer >= 1)")
        self.PopulationSize = int(input("=> "))
        print("Please state the mutation rate (a decimal point '.', followed by a nonnegative integer, so that 0 <= mutation rate <= 1)")
        self.MutationRate = float(input("=> "))
        print("Please state the crossover rate (a decimal point '.', followed by a nonnegative integer, so that 0 <= crossover rate <= 1)")
        self.CrossoverRate = float(input("=> "))
        print("Please state the number of crossover points (either '1' or '2')")
        self.NumberOfCrossoverPoints = int(input("=> "))
        print("Please state the maximum number of generations (an integer >= 1)")
        self.MaxNumberOfGenerations = int(input("=> "))
        print("Please state the number of times to run the GA with these parameters (an integer >= 1)")
        self.NumberOfTimesToRun = int(input("=> "))
##        print("Please state the name of the output file. (file.txt)")
##        self.OutputFileName = input("=> ")

    def PrintRunResults(self):
##        print('Population.List: \n'+ self.GA.Population.ToString('   ', ' '))
        print()
        print('Results of Run #' + str(self.RunCount) + ':')
        print('Generation count: ', str(self.GA.GenerationCount))
        print('Population\'s initial best fitness: ' + str(self.GA.InitialBestFitness) + ', or ' + str(self.GA.PercentInitialBestFitness) + ' percent fit')
        print('Population\'s final best fitness:   ' + str(self.GA.FinalBestFitness) + ', or ' + str(self.GA.PercentFinalBestFitness) + ' percent fit')
        print('Average fitness delta: ' + str(round(self.GA.AverageFitnessDelta, 3)))
        print('Most fit individual: ' + self.GA.Population.MostFitIndividual().Genotype.ValuesToString())

    def WriteResultsToOutputFile(self):
        OutputFile = open( self.OutputFileName , 'a')
        OutputFile.write("%s, %s\n" % (self.GA.GenerationCount, self.GA.AverageFitnessDelta))
        OutputFile.close()

    def PrintSummary(self):
        print()
        print('Summary of runs of GA with the given parameters:')

    def main(self):
        self.SetPreferences()
##        OutputFile = open( self.OutputFileName , 'a')
##        OutputFile.write("%s, %s\n" % ('Run\'s total number of generations', 'Run\'s average fitness delta (a percentage)'))
##        OutputFile.close()
        while self.RunCount < self.NumberOfTimesToRun:            
            self.RunCount += 1

            # initialize the GA
            self.GA = GA(self.PopulationSize, self.MutationRate, self.CrossoverRate, self.NumberOfCrossoverPoints, self.MaxNumberOfGenerations)

            # run the GA, print the run's results, print the results, write the results to the output file
            self.GA.Run()
            self.PrintRunResults()
##            self.WriteResultsToOutputFile()
##            if self.RunCount == 1:
##                self.GA.Population.MostFitIndividual().WriteCorrectnessToFile()



GARunner = GARunner()
GARunner.main()
