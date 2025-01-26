from data_model import DataModel

class ViewModel:
    def __init__(self, spreadsheet_path):
        self.data_model = DataModel(spreadsheet_path)
        self.df = self.data_model.get_dataframe()

    def get_dataframe(self):
        return self.df

    def save_mapping(self, mapping_df):
        self.data_model.create_varset(mapping_df)