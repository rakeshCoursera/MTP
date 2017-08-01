#Building a basic Scheduling algorithm for IR with the given data
#in the excel file.
#****************************************************************
#Importing all required modules
#****************************************************************
import math	
import random 
import numpy as np 
import matplotlib.pyplot as plt
import scipy 
import xlwt
import xlrd
#*****************************************************************
Excel_File = "Input Data.xlsx"
Ship_Alive_Days = 10
StartDay = 0
EndDay = 32

def FCFS_SCHEDULING(Excel_File, Ship_Alive_Days, StartDay, EndDay):
    Data = input_excel(Excel_File)
    Alive_Data,Dead_Data = remove_dead_ship(Data,Ship_Alive_Days)
    Sort_Data_Reg = Sort_reg_wise(Alive_Data)
    Rake_Avail_Data,Rake_Not_Avail_Data = rake_available(Sort_Data_Reg)
    #Capacity_Matrix = input_excel(Capa_Mat_file)
    #print "Capacity Matrix",Capacity_Matrix
    Capacity_Matrix = ter_cap_matrix(Rake_Avail_Data,StartDay,EndDay)
    Scheduled_Data,Updated_Capacity_Matrix = schedulingFCFS(Rake_Avail_Data,Capacity_Matrix,StartDay,EndDay)
    workbook = xlwt.Workbook()
    write_excel(Rake_Avail_Data,"Rake available",workbook)
    write_excel(Scheduled_Data,"Scheduled Data",workbook)
    write_excel(Updated_Capacity_Matrix,"Capacity Matrix",workbook)
    return Scheduled_Data,Updated_Capacity_Matrix

def input_excel(file_name):
    #Taking the data from the excel file as input
    workbook = xlrd.open_workbook(file_name)
    sheet = workbook.sheet_by_index(0)
    #print "Sheet number",z
    row = sheet.nrows
    column = sheet.ncols
    #print row,column
    #print sheet

    #Appending the values row-wise
    row_wise_data = [] #make a data store
    for i in range(2,sheet.nrows):
        row_wise_data.append(sheet.row_values(i)) #drop all the values in the rows into data
    #print "Data from excel sheet",row_wise_data
    return row_wise_data

def remove_dead_ship(data,daysAlive):
    #Romoving the demand data whose date is exceeded and
    #they don't want to keep their shipment alive
    for i in range(len(data[0])):
        if(data[0][i]=='Ship_alive'):
            ShipAliveIndex = i
        if(data[0][i]=='WRD'):
            WRTindex = i
    live_shipment_data = []
    dead_shipment_data = []
    live_shipment_data.append(data[0])
    dead_shipment_data.append(data[0])
    for j in  range(1,len(data)):
        if(data[j][WRTindex] > daysAlive and data[j][ShipAliveIndex] == 'N'):
            dead_shipment_data.append(data[j])
        else:
            live_shipment_data.append(data[j])
    #print "Data after removing dead shipments",live_shipment_data
    #print "Data of dead shipments",dead_shipment_data
    return live_shipment_data,dead_shipment_data

def Sort_reg_wise(alive_data):
    for k in range(len(alive_data[0])):
        if(alive_data[0][k]=='R_no'):
            RegNo = k
            break
    for i in range(1,len(alive_data)-1):
        temp = []
        for j in range(i+1,len(alive_data)):
            if(alive_data[i][RegNo]>alive_data[j][RegNo]):
                temp = alive_data[i]
                alive_data[i] = alive_data[j]
                alive_data[j] = temp
    #print "Data After Acending order of ragistration", alive_data
    return alive_data

def rake_available(data):
    for k in range(len(data[0])):
        if(data[0][k]=='Rake_avail'):
            LTrakeAvailIndex = k
            break
    data_rake_avail = []
    data_rake_not_avail = []
    data_rake_avail.append(data[0])
    data_rake_not_avail.append(data[0])
    for i in range(1,len(data )):
        if(data[i][LTrakeAvailIndex]=='Y'):
            data_rake_avail.append(data[i])
        else:
            data_rake_not_avail.append(data[i])
    #print "Data where rake is available, can load", data_rake_avail
    #print "Data where rake is not available", data_rake_not_avail
    return data_rake_avail,data_rake_not_avail

def write_excel(data,name,workbook):
    sheet = workbook.add_sheet(name)
    for a in range(len(data)):
        for b in range(len(data[0])):
            sheet.write(a,b, data[a][b])
    workbook.save('result.xls')

def ter_cap_matrix(Rake_Avail_Data,StartDay,EndDay):
    for k in range(len(Rake_Avail_Data[0])):
        if(Rake_Avail_Data[0][k] == 'LTj'):
            LTindex = k
        if(Rake_Avail_Data[0][k]=='UTj'):
            UTindex = k
            
    Ter_names =[]
    for i in range(1,len(Rake_Avail_Data)):
            if(Rake_Avail_Data[i][LTindex] not in Ter_names):
                Ter_names.append(Rake_Avail_Data[i][LTindex])
            if(Rake_Avail_Data[i][UTindex] not in Ter_names):    
                Ter_names.append(Rake_Avail_Data[i][UTindex])
    #print "List of Terminals Name ",Ter_names
    
    Cap_matrix = []
    Cap_matrix.append([''])
    Cap_matrix[0] = Cap_matrix[0] + list(xrange(StartDay,EndDay))
    for j in range(0,len(Ter_names)):
        Cap_matrix.append([Ter_names[j]])
        for j1 in range(StartDay+1,EndDay+1):
            Cap_matrix[j+1].append(0)
    #print "Capacity matrix", Cap_matrix
    return Cap_matrix

def schedulingFCFS(data_rake_avail,Cap_matrix,startDay,endDay):
    for i1 in range(len(data_rake_avail[0])):
        if(data_rake_avail[0][i1] == 'LTj'):
            LTindex = i1
        if(data_rake_avail[0][i1]=='UTj'):
            UTindex = i1
        if(data_rake_avail[0][i1]=='Tj'):
            TravelTindex = i1
        if(data_rake_avail[0][i1]=='Uj'):
            UTimeIndex = i1
        if(data_rake_avail[0][i1]=='Lj'):
            LTimeIndex = i1
        if(data_rake_avail[0][i1]=='Pj'):
            ProTimeIndex = i1
        if(data_rake_avail[0][i1]=='H_lt'):
            HCapLTindex = i1
        if(data_rake_avail[0][i1]=='H_ut'):
            HCapUTindex = i1
    schedule = []
    sch_heading = ["StartLoadingLT","LeaveLT","WaitAtLT", "ArriveUT","DepartUT","WaitAtUT"]
    schedule.append(data_rake_avail[0]+sch_heading)
    schedule = schedule + data_rake_avail[1:]
    StartDIndex = len(data_rake_avail[0])
    LeaveDIndex = StartDIndex + 1
    WaitLTIndex = LeaveDIndex + 1
    ArriveDIndex = WaitLTIndex +1
    DepartDIndex = ArriveDIndex + 1
    WaitUTIndex = DepartDIndex + 1
    #print "Index of starting day of train from loading terminal",StartDIndex
    #print "Index of leaving day of train from loading terminal",LeaveDIndex
    #print "Index of Waiting column at Loading terminal for trains",WaitLTIndex
    #print "Index of arriving day of train at the unloading terminal",ArriveDIndex
    #print "Index of departing day of train at the unloading terminal",DepartDIndex
    #print "Index of Waiting column at unloading terminal for trains",WaitUTIndex
    #print "Data After adding header", schedule

    for k in range(1,len(schedule)):
        stop = False
        for k1 in range(1,len(Cap_matrix)):
            if(Cap_matrix[k1][0]==schedule[k][UTindex]):
                print "Planning unloaidng Terminal",schedule[k][UTindex]
                for StartDay in range(startDay,endDay):
                    signal = 0
                    for k2 in range(StartDay+int(schedule[k][LTimeIndex]+schedule[k][TravelTindex]),int(StartDay+schedule[k][ProTimeIndex])):
                        #print "range for unloading checking",k2
                        if(Cap_matrix[k1][k2+1] < schedule[k][HCapUTindex]):
                            signalUT = 0
                            signal = signal + signalUT
                            #print "Signal of availability at unloading terminal",signal
                        else:
                            signalUT = 1
                            signal = signal + signalUT
                    #print "Signal of non or /availability at unloading terminal",signal
                    if(signal ==0):
                        print "Unloading terminal available, now Check for loading requirements"
                        for k3 in range(1,len(Cap_matrix)):
                            if(Cap_matrix[k3][0]==schedule[k][LTindex]):
                                print "Planning  for loadidng Terminal",schedule[k][LTindex]
                                signal1 = 0
                                #print "Planning  Loading TerminalTerminal",Cap_matrix[k3][0]
                                for k4 in range(StartDay,StartDay+int(schedule[k][LTimeIndex])):
                                    #print "range for loading checking",k4
                                    if(Cap_matrix[k3][k4+1] < schedule[k][HCapLTindex]):
                                        signalLT = 0
                                        signal1 = signal1 + signalLT
                                        #print "Signal of availability at loading terminal",signal1
                                    else:
                                        signalLT = 1
                                        signal1 = signal1 + signalLT
                                #print "Signal of non/ availability at loading terminal",signal1
                                if(signal1 == 0):
                                    print"Loading Terminal Available, update the capacity matrix and make the schedule"
                                    schedule[k].append(StartDay)
                                    waitAtLT =0
                                    if(Cap_matrix[k3][StartDay:int(StartDay+schedule[k][LTimeIndex])]>0):
                                        for k6 in range(k-1,0,-1):
                                            if(schedule[k6][LTindex]==schedule[k][LTindex]):
                                                waitAtLT = schedule[k6][LeaveDIndex]-schedule[k][StartDIndex]
                                                break;
                                        if(waitAtLT<0):
                                            waitAtLT =0
                                    schedule[k].append(StartDay+ waitAtLT +schedule[k][LTimeIndex])
                                    schedule[k].append(schedule[k][LeaveDIndex]-schedule[k][StartDIndex])
                                    schedule[k].append(schedule[k][LeaveDIndex]+schedule[k][TravelTindex])
                                    waitAtUT =0
                                    if(Cap_matrix[k1][int(schedule[k][ArriveDIndex]):int(schedule[k][ArriveDIndex]+schedule[k][UTimeIndex])]>0):
                                       for k7 in range(k-1,0,-1):
                                            if(schedule[k7][UTindex]==schedule[k][UTindex]):
                                                print 
                                                waitAtUT = schedule[k7][DepartDIndex]-schedule[k][ArriveDIndex]
                                                break;
                                       if(waitAtUT<0):                                       
                                            waitAtUT =0                                    
                                    schedule[k].append(schedule[k][ArriveDIndex]+ waitAtUT +schedule[k][UTimeIndex])
                                    schedule[k].append(schedule[k][DepartDIndex] - schedule[k][ArriveDIndex])

                                    for k8 in range(int(schedule[k][StartDIndex]),int(schedule[k][LeaveDIndex])):
                                        Cap_matrix[k3][k8+1] = Cap_matrix[k3][k8+1]+1
                                    for k9 in range(int(schedule[k][ArriveDIndex]),int(schedule[k][DepartDIndex])):
                                        Cap_matrix[k1][k9+1] = Cap_matrix[k1][k9+1]+1
                                    stop = True
                                else:
                                    print "Again recheck for next schedule of UT"               
                    else:
                        print "Unloading terminal not available"
                    if(stop == True):
                        print"loop breaked"
                        break;
                if(stop==False):
                    print "Not able to schedule the train from Terminal -"+str(schedule[k][LTindex])+" to "+str(schedule[k][UTindex]) +"in this time frame"
                #print "Updated Data",schedule
                #print "Capacity matrix",Cap_matrix
    return schedule,Cap_matrix





