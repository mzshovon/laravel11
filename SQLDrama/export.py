import pandas as pd

def export_to_file(filetype, data, filename):
    df = pd.DataFrame(data)
    if filetype == "csv":
        df.to_csv(filename, index=False)
    elif filetype == "excel":
        df.to_excel(filename, sheet_name="data", index=False)
    elif filetype == "pdf":
        df.to_hdf(filename, index=False)
    else:
        raise Exception("Invalid file type given")
