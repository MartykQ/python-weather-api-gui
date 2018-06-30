from math import sqrt
import datetime

def skosnosc(tablica):

    ave = sum(tablica)/len(tablica)
    suma_kwadratow = 0
    suma_szes = 0
    for element in tablica:
        suma_kwadratow += pow(element-ave,2)
        suma_szes += pow(element-ave,3)

    odchyl = sqrt((suma_kwadratow/len(tablica)))
    mom3 = suma_szes/len(tablica)

    return mom3/pow(odchyl, 3)


def connectionError():
    error = Tk()
    label1 = Label(error, text="Check your Internet Connection and try again!", font=(40))
    label1.pack()
    exitButt2 = Button(error, text="EXIT", command=exitApp)
    exitButt2.pack()
    error.mainloop()

def exitApp():
    exit()

def kelv_to_cel(a):
    """concerts kelvins to celsius"""
    return a-273.15

def now_string():
    """returns current date as a string"""
    now=datetime.datetime.now()
    string_z_data=str(now)
    return string_z_data[:10]

def add_to_now(days_am):
    """Dodaje X dni do daty obecnej, zwraca string z data w postaci """
    now=datetime.datetime.now()
    new_date=now+datetime.timedelta(days=days_am)
    new_date=str(new_date)
    return new_date[0:10]



class DayTemp:
    """Prosta klasa, pomaga w przechowywaniu danych dot. pogody"""
    date_txt = ''
    temperature = 1
    description = ''
    pressure = 1

