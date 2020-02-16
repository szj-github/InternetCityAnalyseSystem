import pandas as pd
path = 'qcwy_pre1.csv'
data = pd.read_csv(path, encoding='utf-8', error_bad_lines=False)  # 读取csv
Info = pd.DataFrame(data)
for i in Info:
    print(i)