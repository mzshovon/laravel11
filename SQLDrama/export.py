import pandas as pd

def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
def export_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
