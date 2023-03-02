import glob
import sys
sys.path.append("../lib/")

import pandas as pd
import os
import numpy as np

class EvaluationUtils:
    
    # This method takes an object, converts it into a dict and stores it into a CSV file
    def save_results(file_name, results):
        if len(results) > 0:
            data_frame = pd.DataFrame(columns=results[0].to_dict().keys())
            for result in results:
                data_frame = data_frame.append(result.to_dict(), ignore_index=True)

            # Check if file exists, if so, append the file.
            # If not, create a new one.
            if os.path.isfile(file_name):
                data_frame.to_csv(file_name, mode='a', header=False, index=False)
            else:
                data_frame.to_csv(file_name, index=False)
