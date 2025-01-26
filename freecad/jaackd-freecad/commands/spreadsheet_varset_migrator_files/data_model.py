import pandas as pd
import FreeCAD

class DataModel:
    def __init__(self, spreadsheet_path):
        self.spreadsheet_path = spreadsheet_path
        self.df = pd.read_excel(spreadsheet_path)

    def get_dataframe(self):
        return self.df

    def create_varset(self, mapping_df):
        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument()

        varset = doc.addObject("App::DocumentObjectGroupPython", "Parameters")
        varset.addProperty("App::PropertyStringList", "Names", "Base", "Parameter names")
        varset.addProperty("App::PropertyStringList", "Types", "Base", "Parameter types")
        varset.addProperty("App::PropertyStringList", "Descriptions", "Base", "Parameter descriptions")
        varset.addProperty("App::PropertyFloatList", "Values", "Base", "Parameter values")

        names = []
        types = []
        descriptions = []
        values = []

        for _, row in mapping_df.iterrows():
            purpose = row['Purpose']
            if purpose == 'Name':
                names.append(row['Parameter'])
            elif purpose == 'Type':
                types.append(row['Parameter'])
            elif purpose == 'Description':
                descriptions.append(row['Parameter'])
            elif purpose == 'Value':
                values.append(float(row['Parameter']))

        varset.Names = names
        varset.Types = types
        varset.Descriptions = descriptions
        varset.Values = values

        doc.recompute()
        return varset
    