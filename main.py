import requests
import datetime
from tkinter import *
import statistics
from functions import *


FONT_MAIN = "Gill Sans MT Condensed"


def main():

    def destroyWeather():
        """Zamyka mmenu glowne, przechodzi do funkcji take_city, ktora wyswietla pogode na 5 dni dla wybranego miasta"""
        root.destroy()
        take_city()

    def statDestroy():
        """Zamyka menu glowne, przechodzi do okna statystyk"""
        root.destroy()
        statView()

    def statView():
        """Pobiera z pliku tekstowego dane historyczne dot. pogody w Krakowie, na ich podstawie oblicza podstawowe wskazniki"""


        def backMain():
            """Zamyka okno statystyki, wraca do menu"""
            rootStat.destroy()
            main()

        temp_hist = []
        for key in dict_from_file.keys():
            temp_hist.append(float(dict_from_file[key][0]))


        print(temp_dict)
        print(temp_hist)

        average = sum(temp_hist)/len(temp_hist)
        mediana = statistics.median(temp_hist)
        odchylenie = statistics.stdev(temp_hist)
        minimalna = min(temp_hist)
        maxymalna = max(temp_hist)
        skos = skosnosc(temp_hist)

        print("SREDNIAaaaa")
        print(average)
        print("MEDIANA")
        print(mediana)
        print("ODCHYLENIE")
        print(odchylenie)
        print("MIN")
        print(minimalna)
        print("MAX")
        print(maxymalna)
        print("SKOSCNOSC")
        print(skos)

        rootStat = Tk()

        rootStat.resizable(False, False)
        rootStat.geometry("1280x720")

        photostat = PhotoImage(file='images/backstat.png')
        backLabelstat = Label(rootStat, image=photostat)
        backLabelstat.place(x=0, y=0, relwidth=1, relheight=1)

        labelSrednia = Label(rootStat, text="AVERAGE", font=(FONT_MAIN, 23), bg='white')
        labelSrednia.place(x=500, y=150)

        labelSrednia = Label(rootStat, text=str(average)[:5], font=(FONT_MAIN, 23), bg='white')
        labelSrednia.place(x=720, y=150)


        labelMediana = Label(rootStat, text="MEDIAN", font=(FONT_MAIN, 23), bg='white')
        labelMediana.place(x=500, y=190)

        labelMediana = Label(rootStat, text=str(mediana)[:5], font=(FONT_MAIN, 23), bg='white')
        labelMediana.place(x=720, y=190)

        labelSD = Label(rootStat, text="ST. DEVIATION", font=(FONT_MAIN, 23), bg='white')
        labelSD.place(x=500, y=230)

        labelSD = Label(rootStat, text=str(odchylenie)[:5], font=(FONT_MAIN, 23), bg='white')
        labelSD.place(x=720, y=230)

        labelMin = Label(rootStat, text="MINIMUM", font=(FONT_MAIN, 23), bg='white')
        labelMin.place(x=500, y=270)

        labelMin = Label(rootStat, text=str(minimalna)[:5], font=(FONT_MAIN, 23), bg='white')
        labelMin.place(x=720, y=270)

        labelMax = Label(rootStat, text="MAXIMUM", font=(FONT_MAIN, 23), bg='white')
        labelMax.place(x=500, y=310)

        labelMax = Label(rootStat, text=str(maxymalna)[:5], font=(FONT_MAIN, 23), bg='white')
        labelMax.place(x=720, y=310)

        labelSk = Label(rootStat, text="SKEWNESS", font=(FONT_MAIN, 23), bg='white')
        labelSk.place(x=500, y=350)

        labelSk = Label(rootStat, text=str(skos)[:5], font=(FONT_MAIN, 23), bg='white')
        labelSk.place(x=720, y=350)

        statImg = PhotoImage(file='images/backbut2.png')
        statBut = Button(rootStat, image=statImg, command=backMain, borderwidth=0)
        statBut.place(x=530, y=573)

        labelN = Label(rootStat, text="Number of observations: "+str(len(temp_hist)), font=(FONT_MAIN, 30), bg='white')
        labelN.place(x=480, y=400)

        labelB = Label(rootStat, text="Data from 26-05-2018 to "+add_to_now(5), font=(FONT_MAIN, 26),
                       bg='white')
        labelB.place(x=450, y=460)

        rootStat.mainloop()


    def take_city():
        """W zaleznosci od wpisanego miasta wyswietla pogode na 5 dni"""
        """W przypadku braku Internetu/niepoprawnym wpisaniu miasta wysywietla komunikat o bledzie"""


        def goBack():
            root2.destroy()
            main()



        # sciaganie do pamieci info o obecnej pogodzie w wybranym miescie
        try:
            api_city_current = 'http://api.openweathermap.org/data/2.5/weather?appid=dbe8768275cfe8611428248a9fc9ffdf&q=' + str(
            cityVar.get())
            json_current = requests.get(api_city_current).json()


            current = DayTemp()
            current.date_txt = now_string()
            current.temperature = kelv_to_cel(json_current['main']['temp'])
            current.description = json_current['weather'][0]['description']
            current.pressure = int(json_current['main']['pressure'])
        except:
            connectionError()
        # ****************************

        api_city_future = 'http://api.openweathermap.org/data/2.5/forecast?&appid=dbe8768275cfe8611428248a9fc9ffdf&q=' + str(
            cityVar.get())
        json_future = requests.get(api_city_future).json()

        help_list = json_future['list']

        # USUWANIE NIEPOTRZEBNYCH ELEMENTOW Z HELP LIST
        i = 0
        while i < len(help_list):
            pom = help_list[i]['dt_txt']
            if now_string() in pom:
                del help_list[i]

            elif add_to_now(5) in pom:
                del help_list[i]
            else:
                i += 1
        ################################

        temp_help_list = []
        for i in help_list:
            temp_help_list.append(float(i['main']['temp']))

        mainList = []  # tworzenie struktury
        for i in range(0, 4):
            object = DayTemp()
            mainList.append(object)

        ######################

        # przypisywanie wartosci do elementow struktury
        i = 0
        pom = 0
        while i < len(help_list):
            mainList[pom].temperature = kelv_to_cel(sum(temp_help_list[i:i + 8]) / 8)
            mainList[pom].description = help_list[i + 4]['weather'][0]['description']
            mainList[pom].pressure = help_list[i + 4]['main']['pressure']
            mainList[pom].date_txt = add_to_now(pom + 1)
            pom = pom + 1
            i = i + 8

        # GUI ZACZYNA DZIALAC
        root2 = Tk()
        root2.geometry("1280x720")
        root2.resizable(False, False)

        photo2 = PhotoImage(file='images/background2.png')
        backLabel_back1 = Label(root2, image=photo2)
        backLabel_back1.place(x=0, y=0, relwidth=1, relheight=1)

        labelxd = Label(root2, text=cityVar.get(), font=(FONT_MAIN, 34), bg="#c8c9c9")
        labelxd.place(y=560, height=70, width=1280)

        label_day1 = Label(root2, text=str(current.date_txt), font=(FONT_MAIN, 20), bg="#e2ebea")
        label_day1.place(width=200, height=30, x=46, y=135)

        label_day2 = Label(root2, text=str(mainList[0].date_txt), font=(FONT_MAIN, 20), bg="#e2ebea")
        label_day2.place(width=200, height=30, x=293, y=135)

        label_day3 = Label(root2, text=str(mainList[1].date_txt), font=(FONT_MAIN, 20), bg="#e2ebea")
        label_day3.place(width=200, height=30, x=539.8, y=135)

        label_day4 = Label(root2, text=str(mainList[2].date_txt), font=(FONT_MAIN, 20), bg="#e2ebea")
        label_day4.place(width=200, height=30, x=786.4, y=135)

        label_day5 = Label(root2, text=str(mainList[3].date_txt), font=(FONT_MAIN, 20), bg="#e2ebea")
        label_day5.place(width=200, height=30, x=1033, y=135)

        ###################################

        # WYSWIETLANIE ODPOWIENIEGO ZDJECIA W ZALEZNOSCI OD POGODY

        photo_full_cloud = PhotoImage(file='images/full_cloud.png')
        photo_rain = PhotoImage(file='images/rain.png')
        photo_snow = PhotoImage(file='images/snow.png')
        photo_sun = PhotoImage(file='images/sun.png')
        photo_sun_cloud = PhotoImage(file='images/sun_cloud.png')
        photo_thunder = PhotoImage(file='images/thunder.png')

        if "rain" in current.description:
            day_1_photo = Label(root2, image=photo_rain, bg="#929696")
            day_1_photo.place(x=46, y=180, width=200, height=170)
        elif "clouds" in current.description:
            day_1_photo = Label(root2, image=photo_full_cloud, bg="#929696")
            day_1_photo.place(x=46, y=180, width=200, height=170)
        elif "snow" in current.description:
            day_1_photo = Label(root2, image=photo_snow, bg="#929696")
            day_1_photo.place(x=46, y=180, width=200, height=170)
        elif "sun" in current.description:
            day_1_photo = Label(root2, image=photo_sun, bg="#929696")
            day_1_photo.place(x=46, y=180, width=200, height=170)
        elif "thunder" in current.description:
            day_1_photo = Label(root2, image=photo_thunder, bg="#929696")
            day_1_photo.place(x=46, y=180, width=200, height=170)
        else:
            day_1_photo = Label(root2, image=photo_sun_cloud, bg="#929696")
            day_1_photo.place(x=46, y=180, width=200, height=170)

        #Petla, wyswietlajac odpowiednia grafike, w zaleznosci od pogody, w odpowiednim miejscu
        #Kazde przejscie zwieksza wsp. X

        x_cord = 1
        pom = 0
        for i in mainList:
            if pom == 0:
                x_cord = 293.2
            elif pom == 1:
                x_cord = 539.8
            elif pom == 2:
                x_cord = 786.4
            elif pom == 3:
                x_cord = 1033

            if "rain" in i.description:
                day_1_photo = Label(root2, image=photo_rain, bg="#929696")
                day_1_photo.place(x=x_cord, y=180, width=200, height=170)
            elif "clouds" in i.description:
                day_1_photo = Label(root2, image=photo_full_cloud, bg="#929696")
                day_1_photo.place(x=x_cord, y=180, width=200, height=170)
            elif "snow" in i.description:
                day_1_photo = Label(root2, image=photo_snow, bg="#929696")
                day_1_photo.place(x=x_cord, y=180, width=200, height=170)
            elif "sun" in i.description:
                day_1_photo = Label(root2, image=photo_sun, bg="#929696")
                day_1_photo.place(x=x_cord, y=180, width=200, height=170)
            elif "thunder" in i.description:
                day_1_photo = Label(root2, image=photo_thunder, bg="#929696")
                day_1_photo.place(x=x_cord, y=180, width=200, height=170)
            else:
                day_1_photo = Label(root2, image=photo_sun_cloud, bg="#929696")
                day_1_photo.place(x=x_cord, y=180, width=200, height=170)

            label_temp = Label(root2, text=i.description.title(), font=(FONT_MAIN, 16), bg="#929696")
            label_temp.place(x=x_cord, y=320, width=200)

            label_int = Label(root2, text=str(i.temperature)[0:4] + '°', font=(FONT_MAIN, 15), bg="#929696")
            label_int.place(x=x_cord, y=360, width=80)

            label_int2 = Label(root2, text=str(i.pressure) + " hPa", font=(FONT_MAIN, 15), bg="#929696")
            label_int2.place(x=x_cord + 80, y=360, width=120)

            pom = pom + 1
            #koniec petli


        label_temp_cur = Label(root2, text=current.description.title(), font=(FONT_MAIN, 16), bg="#929696")
        label_temp_cur.place(x=46, y=320, width=200)

        label_int = Label(root2, text=str(current.temperature)[0:4] + '°', font=(FONT_MAIN, 15), bg="#929696")
        label_int.place(x=46, y=360, width=80)

        label_int2 = Label(root2, text=str(current.pressure) + " hPa", font=(FONT_MAIN, 15), bg="#929696")
        label_int2.place(x=46 + 80, y=360, width=120)

        backBut = PhotoImage(file='images/backbut.png')
        backButton=Button(root2, command=goBack, borderwidth=0, image=backBut)
        backButton.place(x= 1038, y=20)

        root2.mainloop()

        ######################Koniec Funkcji TAKE CITY########################3






    #GUI Menu glownego

    root = Tk()

    root.resizable(False, False)
    root.geometry("1280x720")
    buttonOK = PhotoImage(file='images/button1.png')
    photo = PhotoImage(file='images/background3.png')
    backLabel = Label(root, image=photo)
    backLabel.place(x=0, y=0, relwidth=1, relheight=1)
    cityVar = StringVar()

    cityEntry = Entry(root, textvariable=cityVar, width=100, bg='white', borderwidth=0, font=(FONT_MAIN, 16))
    cityEntry.place(x=465, y=244, height=20, width=240)

    sumbitbut = Button(root, image=buttonOK, command=destroyWeather, borderwidth=0)
    sumbitbut.place(x=735, y=235)


    photo_full_cloud2 = PhotoImage(file='images/full_cloud2.png')
    photo_rain2 = PhotoImage(file='images/rain2.png')
    photo_snow2 = PhotoImage(file='images/snow2.png')
    photo_sun2 = PhotoImage(file='images/sun2.png')
    photo_sun_cloud2 = PhotoImage(file='images/sun_cloud2.png')
    photo_thunder2 = PhotoImage(file='images/thunder2.png')



    if "rain" in temp_dict[now_string()][1]:
        day_1_photo = Label(root, image=photo_rain2, bg="white")
        day_1_photo.place(x=490, y=410, width=100, height=100)
    elif "clouds" in temp_dict[now_string()][1]:
        day_1_photo = Label(root, image=photo_full_cloud2, bg="white")
        day_1_photo.place(x=490, y=410, width=100, height=100)
    elif "snow" in temp_dict[now_string()][1]:
        day_1_photo = Label(root, image=photo_snow2, bg="white")
        day_1_photo.place(x=490, y=410, width=100, height=100)
    elif "sun" in temp_dict[now_string()][1]:
        day_1_photo = Label(root, image=photo_sun2, bg="white")
        day_1_photo.place(x=490, y=410, width=100, height=100)
    elif "thunder" in temp_dict[now_string()][1]:
        day_1_photo = Label(root, image=photo_thunder2, bg="white")
        day_1_photo.place(x=490, y=410, width=100, height=100)
    else:
        day_1_photo = Label(root, image=photo_sun_cloud2, bg="white")
        day_1_photo.place(x=490, y=410, width=100, height=100)


    labelpies = Label(root, text=str(temp_dict[now_string()][0])+'°', font=(FONT_MAIN, 30), bg="white")
    labelpies.place(x=680, y=400)

    labelpies2 = Label(root, text=str(temp_dict[now_string()][1]).title()+'°', font=(FONT_MAIN, 24), bg="white")
    labelpies2.place(x=660, y=460)

    exitImg = PhotoImage(file='images/exitBut.png')
    exitBut = Button(root, image=exitImg, command = exitApp, borderwidth=0)
    exitBut.place(x=655, y=575)

    statImg = PhotoImage(file='images/statBut.png')
    statBut = Button(root, image=statImg, command=statDestroy, borderwidth=0)
    statBut.place(x=447, y=573)

    root.mainloop()








#######################
#Pobieranie danych dot. pogody w kraokwie w dniu obecnym, oraz na kolejne 4 dni
try:
    api_url = 'http://api.openweathermap.org/data/2.5/weather?appid=dbe8768275cfe8611428248a9fc9ffdf&q=Krakow' #current krakow
    json_data=dict(requests.get(api_url).json())
    api_adres='http://api.openweathermap.org/data/2.5/forecast?&appid=dbe8768275cfe8611428248a9fc9ffdf&q=Krakow' #5 days krakow
    json_dane=requests.get(api_adres).json()
    data_list = json_dane['list']
except requests.exceptions.ConnectionError:
    connectionError()

#################

#usuwanie niepotrzebnych elementow tablicy uzyskanej z API openweathermap
i=0
while i<len(data_list):
    pom=data_list[i]['dt_txt']
    if now_string() in pom:
        del data_list[i]

    elif add_to_now(5) in pom:
        del data_list[i]
    else:
        i+=1


#tworzenie tablicy pomocniczej z temperaturami (API udostepnia dane na kolejne dni podajac przewidywania co kolejne 3
#godziny. Nas interesuje tylko srednia temperatura w danym dniu


temp_list=[]
for i in data_list:
    temp_list.append(float(i['main']['temp']))


#tworzenie dictionary , gdzie klucze to daty odpowiednich dni a wartosc to lista z temperatura srednia, opisem pogody i cisnieniem
temp_dict={}

temp_dict[now_string()]=[]
temp_dict[now_string()].append(kelv_to_cel(json_data['main']['temp']))
temp_dict[now_string()].append(json_data['weather'][0]['description'])
temp_dict[now_string()].append(json_data['main']['pressure'])


i=0
pom=0
while i<len(data_list):
    temp_dict[add_to_now(pom+1)]=[]
    temp_dict[add_to_now(pom+1)].append(kelv_to_cel(sum(temp_list[i:i+8])/8))
    temp_dict[add_to_now(pom+1)].append(data_list[i+4]['weather'][0]['description'])
    temp_dict[add_to_now(pom+1)].append(data_list[i+4]['main']['pressure'])
    i=i+8
    pom+=1
#*********************


#tworzenie dictionary, ktory bedzie przechowywal dane dot. pogody z dni z przeszlosci

dict_from_file={}

print(dict_from_file)


def read_from_file():
    """Otwiera plik z danymi, wczytuje dane do pamieci"""

    plik=open('data.txt')
    for line in plik:
        (key, temp, weat, pres)=line.split()
        dict_from_file[key]=[temp, weat.replace('_',' '), pres]



def save_to_file():
    """Aktualizuje dane wczesniej pobrane z pliku, zapisuje"""
    dict_from_file.update(temp_dict)
    plik=open('data.txt', 'w')
    for key in dict_from_file.keys():
        plik.write(key)
        plik.write(" ")
        plik.write(str(dict_from_file[key][0]))
        plik.write(' ')
        plik.write(dict_from_file[key][1].replace(' ','_'))
        plik.write(' ')
        plik.write(str(dict_from_file[key][2]))
        plik.write('\n')


read_from_file()
save_to_file()
read_from_file()



main()



