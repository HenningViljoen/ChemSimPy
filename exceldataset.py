import pandas as pd

class exceldataset:
    def __init__(self, filename):
        excel = pd.ExcelFile(filename)
        #print(xl.sheet_names)
        df = excel.parse(excel.sheet_names[0]) #data is a Pandas DataFrame object
        self.data = df.values #Numpy array
        self.arraysize = len(self.data)


