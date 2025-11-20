import os
from time import time 

from dpkt.pcap import Reader
from dpkt.ethernet import Ethernet
from socket import inet_ntoa
import pyarrow
import pyarrow.parquet

#This is a small (and janky) thingy which can be used to turn pcap files into some more useful formats (specifically parquet, csv, orc and feather). I have only tested if the parquet and csv parts work.
#Use at own peril

def pcap2arrowtable(pcap_location):
    
    pcap_file=open(pcap_location,"rb")
    pcap_contents=Reader(pcap_file)

    fields = ["time","source_ip", "destination_ip", 'packet_length']
    columns=[[],[],[],[]]
    for timestamp, buf in pcap_contents:
        
        ip_data = Ethernet(buf).data

        columns[0].append(timestamp)
        columns[1].append(inet_ntoa(ip_data.src))
        columns[2].append(inet_ntoa(ip_data.dst))
        columns[3].append(ip_data.len)

    return(pyarrow.table(columns,fields))   


def pcap2parquet(pcap_location, parquet_name):
    arrowtable=pcap2arrowtable(pcap_location)
    pyarrow.parquet.write_table(arrowtable,parquet_name)


def pcap2orc(pcap_location, orc_name):
    arrowtable=pcap2arrowtable(pcap_location)
    pyarrow.orc.write_table(arrowtable,orc_name)

def pcap2feather(pcap_location, feather_name):
    arrowtable=pcap2arrowtable(pcap_location)
    pyarrow.feather.write_feather(arrowtable,feather_name)

def pcap2csv(pcap_location, csv_name):
    arrowtable=pcap2arrowtable(pcap_location)
    pyarrow.csv.write_csv(arrowtable,csv_name)

def pcaps2format(new_format, pcap_directory, write_directory, names=None, updates=False):
    if updates==True:
        true_start=time()

        print("Task Begun")
        print("Converting .pcap files in "+pcap_directory+" to .parquet format.\n")
    
    os.chdir(write_directory)
    pcap_files=[file for file in os.listdir(pcap_directory) if file.endswith(".pcap")]

    for num in range(len(pcap_files)):
        current_file=pcap_directory+"/"+pcap_files[num]

        if updates==True:
            start_time=time() 
            print("File Location: ")
            print(current_file)
            print("File Size (bytes):")
            print(os.path.getsize(current_file))

        if new_format=="parquet":
            pcap2parquet(current_file,names[num])
        elif new_format=="orc":
            pcap2orc(current_file,names[num])
        elif new_format=="feather":
            pcap2feather(current_file,names[num])
        elif new_format=="csv":
            pcap2csv(current_file,names[num])

        if updates==True:
            end_time=time()
            print("Time Taken:")
            print(end_time-start_time)
            print("Time Since Program Start")
            print(end_time-true_start)
            print("")
        
    if updates==True:
        print("Task Completed!")
        print("Total Runtime: ")
        print(end_time-true_start)

