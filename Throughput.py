import re

def calculate_throughput(dl_bytes, ul_bytes, start_time, end_time):
    dl_throughput = dl_bytes / (end_time - start_time)
    ul_throughput = ul_bytes / (end_time - start_time)
    return dl_throughput, ul_throughput

def process_rlc_characteristics(dl_file, ul_file):
    user_data = {}
    
    with open(dl_file, 'r') as dl_stats, open(ul_file, 'r') as ul_stats:
        dl_lines = dl_stats.readlines()
        ul_lines = ul_stats.readlines()
        
        for dl_line, ul_line in zip(dl_lines[1:], ul_lines[1:]):
            dl_data = re.findall(r'\S+', dl_line)
            ul_data = re.findall(r'\S+', ul_line)
            
            start_time = float(dl_data[0])
            end_time = float(dl_data[1])
            cell_id = int(dl_data[2])
            ue_id = int(dl_data[3])
            dl_bytes = int(dl_data[7])
            ul_bytes = int(ul_data[7])
            
            if ue_id not in user_data:
                user_data[ue_id] = {
                    'DL_Throughput': 0,
                    'UL_Throughput': 0
                }
            
            dl_throughput, ul_throughput = calculate_throughput(dl_bytes, ul_bytes, start_time, end_time)
            user_data[ue_id]['DL_Throughput'] += dl_throughput
            user_data[ue_id]['UL_Throughput'] += ul_throughput

    return user_data

dl_file = "DlRlcStats.txt"
ul_file = "UlRlcStats.txt"

processed_data = process_rlc_characteristics(dl_file, ul_file)

for ue_id, data in processed_data.items():
    print("UE ID:", ue_id)
    print("DL Throughput:", data['DL_Throughput'], "bytes/second")
    print("UL Throughput:", data['UL_Throughput'], "bytes/second")
    print("--------------------")
