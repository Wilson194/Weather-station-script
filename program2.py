# -*- coding: utf-8 -*-

import serial           # slouĹľĂ­ pro komunikaci po COMnn portech
import time             # slouĹľĂ­ k ÄŤasovĂ˝m prodlevĂˇm
import csv,string       # slouĹľĂ­ pro export do csv formĂˇtu
import os.path


chyba = False

# naÄŤte data z seriovĂ© linky

def nacti_data():
    ser = serial.Serial()    # pĹ™ipojenĂ­ na seriovou linku
    ser.bytesize = 8
    ser.port = int(nastaveni["com_port"])
    ser.bautrate = 19200
    ser.timeout = 5
    ser.open()

    ser.write("\n")          # poslĂˇnĂ­ pĹ™Ă­kazĹŻ
    ser.write("LOOP 1\n")
    time.sleep(1)

    vystup = ser.read(ser.inWaiting())   # pĹ™eÄŤtenĂ­ dat
    ser.close()

    vystup = vystup[3:]

    return vystup

#naÄŤtenĂ­ nastavenĂ­

def nacti_nastaveni():
    global nastaveni
    nastaveni = {}

    
    f = file("settings.csv","r")        #otevĹ™enĂ­ souboru s nastavenĂ­m
    data = csv.reader(f,dialect="excel",delimiter=';',)
    for nazev,hodnota in data:          # naÄŤtenĂ­ hodnot do slovnĂ­ku
        nastaveni[nazev] = hodnota
    f.close()

    global poradi
    s = file("poradi.csv","r")          # naÄŤtenĂ­ souboru s poĹ™adĂ­m pro uklĂˇdĂˇnĂ­
    poradi = s.readline()
    poradi = poradi.split(";")
    s.close()

def zpracuj_data(data):                 # rozdÄ›lĂ­ data po bitech na pĹ™Ă­sluĹˇnĂ© data
    a = data
    
    h = {}
    
    h["bartrend"]       = ord(a[3])
    h["barometr"]       = float(ord(a[8]) * 256 + ord(a[7]))
    h["temp_in"]        = float(ord(a[10]) *256 + ord(a[9]))
    h["hum_in"]         = ord(a[11])
    h["temp_out"]       = float(ord(a[13]) *256 + ord(a[12]))
    h["wind_speed"]     = float(ord(a[14]))
    h["a_wind_speed"]   = float(ord(a[15]))
    h["wind_direct"]    = ord(a[17]) *256 + ord(a[16])
    h["extra_temp"]     = [ord(a[18]),ord(a[19]),ord(a[20]),ord(a[21]),ord(a[22]),ord(a[23]),ord(a[24])]
    h["soil_temp"]      = [ord(a[25]),ord(a[26]),ord(a[27]),ord(a[28])]
    h["leaf_temp"]      = [ord(a[29]),ord(a[30]),ord(a[31]),ord(a[32])]
    h["hum_out"]        = ord(a[33])
    h["extra_hum"]      = [ord(a[34]),ord(a[35]),ord(a[36]),ord(a[37]),ord(a[38]),ord(a[39]),ord(a[40])]
    h["rain_rate"]      = float(ord(a[42]) *256 + ord(a[41]))
    h["uv"]             = ord(a[43])
    h["solar_rad"]        = ord(a[45]) *256 + ord(a[44])
    h["storm_rain"]     = float(ord(a[47]) *256 + ord(a[46]))
    h["storm_date"]     = str(ord(a[49])) + str(ord(a[48]))
    h["day_rain"]       = ord(a[51]) *256 + ord(a[50])
    h["month_rain"]     = ord(a[53]) *256 + ord(a[52])
    h["year_rain"]      = ord(a[55]) *256 + ord(a[54])
    h["day_et"]         = ord(a[57]) *256 + ord(a[56])
    h["month_et"]       = ord(a[59]) *256 + ord(a[58])
    h["year_et"]        = ord(a[61]) *256 + ord(a[60])
    h["soil_moistures"] = [ord(a[62]),ord(a[63]),ord(a[64]),ord(a[65])]
    h["leaf_wet"]       = [ord(a[66]),ord(a[67]),ord(a[68]),ord(a[69])]
    h["alarm_in"]       = ord(a[70])
    h["alarm_rain"]     = ord(a[71])
    h["alarm_out"]      = [ord(a[72]),ord(a[73])]
    h["alarm_hum"]      = [ord(a[74]),ord(a[75]),ord(a[76]),ord(a[77]),ord(a[78]),ord(a[79]),ord(a[80]),ord(a[81])]
    h["alarm_leaf"]     = [ord(a[82]),ord(a[83]),ord(a[84]),ord(a[85])]
    h["trans_bat_stat"] = ord(a[86])
    h["cons_bat_stat"]  = ord(a[88]) *256 + ord(a[87])
    h["forecast"]       = ord(a[89])
    h["forecast_rule"]  = ord(a[90])
    h["time_sunrise"]   = str(ord(a[92]) *256 + ord(a[91]))
    h["time_sunset"]    = str(ord(a[94]) *256 + ord(a[93]))

    hodnoty = h
    return hodnoty

def preved_jednotky(hodnoty):           # pĹ™evede na potĹ™ebnĂ© jednotky
    h = hodnoty
    
    h["barometr"] = h["barometr"] * 25.39954 * 133.322387415/1000
    h["barometr"] = str(h["barometr"]).replace(".",",")
    h["temp_in"] = round(5*(h["temp_in"]/10-32)/9,1)
    h["temp_in"] = str(h["temp_in"]).replace(".",",")
    h["temp_out"] = round(5*(h["temp_out"]/10 -32)/9,1)
    h["temp_out"] = str(h["temp_out"]).replace(".",",")
    h["wind_speed"] = round(h["wind_speed"] / 0.44704,2)
    h["wind_speed"] = str(h["wind_speed"]).replace(".",",")
    h["a_wind_speed"] = round(h["a_wind_speed"] / 0.44704,2)
    h["a_wind_speed"] = str(h["a_wind_speed"]).replace(".",",")
    h["rain_rate"] = h["rain_rate"]/100 * 26.3
    h["rain_rate"] = str(h["rain_rate"]).replace(".",",")
    h["storm_rain"] = h["storm_rain"]/100 * 26.3
    h["storm_rain"] = str(h["storm_rain"]).replace(".",",")
    h["storm_date"] = h["storm_date"][2:4] + "." + h["storm_date"][0:2] + "." + h["storm_date"][4:]
    h["time_sunrise"] = h["time_sunrise"][0:1] + ":" + h["time_sunrise"][1:]
    h["time_sunset"] = h["time_sunset"][0:2] + ":" + h["time_sunset"][2:]
    return h



    




def archiv_dat(data):           # vystup do Meteo_rrrr_mm.csv
    
    cas = str(time.strftime("%d.%m.%Y %H:%M"))
    rok_mesic = str(time.strftime("%Y_%m"))
    
    cesta = "Meteo_"+rok_mesic+".csv"
    f = file(cesta,"a+")
    
    csvdata = []
    
    csvdata.append(cas)
    
    for i in range(0,len(poradi)):
        csvdata.append(data[poradi[i]])
        
    for i in csvdata:        
        f.write(str(i))
        if i == csvdata[-1]:
            f.write("\n")
        else:
            f.write(";")
            
    f.close()

def zobraz_data(data):          # vystup do souboru show.csv
    csvvystup = []
    csvvystup.append(str(time.strftime("%H:%M")))

    
    for i in poradi:                        #porovnĂˇnĂ­ s nastavenĂ­m, kterĂ© hodnoty mĂˇ uloĹľit 
        if nastaveni[i] == "1":
            csvvystup.append(data[i])

    cesta = nastaveni["shows_file_path"] + "show.csv"
    if os.path.exists(cesta):               # naÄŤtenĂ­ stĂˇvajĂ­cĂ­ch dat
        f = file(cesta,"r+")
        stare = f.readlines()
        f.close()
    else:
        stare=""
    
    if len(stare) >= int(nastaveni["number_lines"]):
        delka = int(len(stare)) - int(nastaveni["number_lines"])
        stare = stare[delka:]
    
    f = file(cesta,"w+")
    for i in stare:                         # zapsĂˇnĂ­ novĂ˝ch dat
        f.write(i)

    for i in csvvystup:        
        f.write(str(i))
        if i == csvvystup[-1]:
            f.write("\n")
        else:
            f.write(";")
    
    f.close()
    

def start():                                #spuĹˇtÄ›nĂ­ potĹ™ebnĂ˝ch funkcĂ­
    nacti_nastaveni()
    data = nacti_data()
    if len(data) > 20:
        zprac_data = zpracuj_data(data)
        final_data = preved_jednotky(zprac_data)
        archiv_dat(final_data)
        zobraz_data(final_data)
    else:
        chyba = True
        print "Nebyla vrácena data"

while True:

    start()                                 # ÄŤasovĂˇ smyÄŤka
    if chyba == True:
        chyba = False
        print "Nebyla vrácena data"
    else:
        print (time.strftime("Provedeno v: %H:%M"))
    time.sleep(int(nastaveni["time_period"])*60)
    
