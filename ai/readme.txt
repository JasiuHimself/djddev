Aby działało
https://pip.pypa.io/en/stable/installing/
zainstaluj pipa!
sudo pip install numpy
sudo pip install scipy
sudo pip install matplotlib


Co jest zrobione:

-zostało ogarnięte, że jak jest range (0,N) to znaczy for i=0;i<=N-1;i++, generalnie wtf
-wczytanie danych z pliku
-filtracja filtrem Butterwortha 10 rzędu
-obliczenie normy ze względnu na brak znaczenia orientacji - nie mam jak tego zrobić bo
-usuwanie dc component



do zrobienia

co trzeba zainstalować, żeby zainstalować theano i kerasa?

sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

sudo pip install theano 
sudo pip install keras
i jest ok


WALIDACJA USUWANIA DC COMPONENT!!!!!!!!!!!!!
WYDAJE SIE ŻE COŚ NIE DO KOŃCA DZIAŁA, ALE PRZEKLEPAŁEM WZÓR

the gyroscope energy Es˜ω,
the accelerometer energy Es˜a,
the gyroscope variance σs˜ω2,
the accelerometer variance σs˜a2, and
the dominant frequencies of the gyroscope and accelerometer, respectively fs˜ω and fs˜a




miscellaneous
wyższe częstotliwości mogą być wykorzystane do wykrywania np jazdy
samochodem


CELE
    żeby działało na sieciach neuronowych
    behavioral deep learning :D
