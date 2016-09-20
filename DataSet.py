class Case:
    def __init__(self, SepalLength, SepalWidth, PetalLength, PetalWidth, Classification):
        self.SepalLength = float(SepalLength)
        self.SepalWidth = float(SepalWidth)
        self.PetalLength = float(PetalLength)
        self.PetalWidth = float(PetalWidth)
        self.Classification = int(Classification)
        
    def ToString(self):
        Str = 'Case: ' 
        Str += 'SepalLength: ' + str(self.SepalLength)
        Str += ', SepalWidth: ' + str(self.SepalWidth)
        Str += ', PetalLength: ' + str(self.PetalLength)
        Str += ', PetalWidth: ' + str(self.PetalWidth)
        Str += ', Classification: ' + str(self.Classification)
        return Str

class DataSet:
    def __init__(self):
        self.FileName = 'FID.txt'
        InFile = open(self.FileName,'r')

        ## Variables that need an initial value
        self.MaxSepalLength = 7.9
        self.MaxSepalWidth = 4.4
        self.MaxPetalLength = 6.9
        self.MaxPetalWidth = 2.5        
    
        ## Parse the header line
        Header = InFile.readline().split()
        self.DataSetName = Header[0]
        self.NumberOfFactors = int(Header[1])
        self.NumberOfOutputs = int(Header[2])

        ## Parse the file and fill self.ListOfCases
        self.ListOfCases = [] # a fixed list of the data in the dataset
        for Line in InFile:
            CaseAsList = Line.split()
            if CaseAsList != []:
                NewCase = Case(CaseAsList[0], CaseAsList[1], CaseAsList[2], CaseAsList[3], CaseAsList[-1])
                self.ListOfCases.append(NewCase)
##                self.InitializeMaximumParameterValues(NewCase)
        InFile.close()

        ## Initialize other variables
        self.Length = len(self.ListOfCases)
        self.ListOfClassifications = self.ListOfClassifications()

##    def InitializeMaximumParameterValues(Case):
##        if self.MaxSepalLength < Case.SepalLength:
##            self.MaxSepalLength = Case.SepalLength
##        if self.MaxSepalWidth < Case.SepalWidth:
##            self.MaxSepalWidth = Case.SepalWidth
##        if self.MaxSepalWidth < Case.SepalWidth:
##            self.MaxSepalWidth = Case.SepalWidth
            
    def InitializeCase(self, CaseAsList):
        return Case(CaseAsList.SepalLength, CaseAsList.SepalWidth, CaseAsList.PetalLength, CaseAsList.PetalWidth, CaseAsList.Classification)

    def ListOfClassifications(self):
        ListOfClassifications = []
        for Case in self.ListOfCases:
            ListOfClassifications.append(Case.Classification)
        return ListOfClassifications

    def LineToStr(self, Line):
        s = ''
        s = s + str(Line[0])
        for x in range(1, len(Line)):
            s = s + ' ' + str(Line[x])
        return s

    def main(self):
        print('called from some other file')

##DataSet = DataSet()
##print('DataSetName: ' + DataSet.DataSetName)
##print('Factors: ' + str(DataSet.NumberOfFactors))
##print('Outputs: ' + str(DataSet.NumberOfOutputs))
##print('ListOfCases: ' + str(DataSet.ListOfCases))
##print('ListOfClassifications: ' + str(DataSet.ListOfClassifications))
##c = DataSet.InitializeCase(DataSet.ListOfCases[0])
##print(c.ToString())
