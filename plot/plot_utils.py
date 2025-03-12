import pandas as pd


def read_rst(path):
    column_names = ['id', 'proc1', 'proc2','walltime', 'run', 'wait', 'submit', 'start', 'end']
    df = pd.read_csv(f'{path}', sep=';', header=None) 
    df.columns = column_names
    df_sorted = df.sort_values(by='id')
    return df_sorted

def read_ult(path):
    data = []
    with open(f'{path}', 'r') as f:
        for line in f:
            parts = line.strip().split(';')
            timestamp1, event_type, timestamp2 = parts[0:3]
            metrics = dict(item.split('=') for item in parts[3].split())
            data.append(
                [
                    float(timestamp1), 
                    event_type, 
                    float(timestamp2), 
                    float(metrics['uti']), 
                    float(metrics['waitNum']), 
                    float(metrics['waitSize'])
                ]
            )

    df = pd.DataFrame(data, columns=['timestamp', 'event_type', 'timestamp2', 'utilization', 'waitNum', 'waitSize'])
    df_sorted = df.sort_values(by='timestamp')
    return df_sorted