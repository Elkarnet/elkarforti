**BUKATUGABE**


Docker erabiliko dugu elkarforti martxan jartzeko, beraz suposatzen da hau egin aurretik docker instalatuta duzula.
Lehenik eta behin git kodea deskargatu

`git clone https://github.com/Elkarnet/elkarforti.git`

Honek elkarforti izeneko karpeta bat sortu dizu. Sartu barruan eta bi karpeta berri sortu
```
# cd elkarforti
# mkdir db
# mkdir keys
```
* **db**: Karpeta honetan gordeko da sqlite datubasea
* **keys**: Karpeta honetan gordeko dira erabiliko diren gako zifratuak

Orain docker irudia sortuko dugu: `sudo docker-compose build`

Irudia sortu ondoren, berriro ere docker erabiliko dugu, oraingoan martxan jartzeko: `sudo docker-compose up`

Dena ondo joan bada, [http://127.0.0.1:8000/](http://127.0.0.1:8000/) helbidean sartzen bagara, login formularioa ikusiko dugu. Oraingoz **CTRL+C** sakatu eta zerbitzua geratuko dugu.

# Erabiltzaile eta pasahitzak: ActiveDirectory konexioa
Bi erabiltzaile mota ditugu:
* Elkarforti administratzailea: **admin** izena du, eta pasahitz lehentsia **admin** da. Instalazioa egin ondoren hau aldatzea komeni da.
* Elkarforti erabiltzaileak: Ikastetxe baten ikasgeletako Internet atzipena kudeatzeko erabiltzen denean, erabiltzaile naturalak irakasleak lirateke. 

Erabiltzaile hauen kredentzialak LDAP/AD batetik hartuko dira, eta horretarako elkarforti karpetan dagoen **env** fitxategian dauden **aldagaiak** aldatu behar dira. Ohiko parametroak dira, eta bereziki hauek aipatuko ditugu:
 * LDAP_REQUIRE_GROUP: Elkarforti-ko taldeen kudeaketa egin ahal izango duten erabiltzaileen taldea
 * LDAP_FLAG_IS_ACTIVE: Login eta eta automatikoki Elkarforti-n aktibo egongo diren erabiltzaileen taldea
Bi talde hauetan oraingoz behintzat jarri kudeaketa baimenak izango dituzten erabiltzaileen taldea. Balio lehenetsi moduan **FortiAccessGroup** agertzen den arren, bakoitzak bere erakundeko talde izen bat jarri beharko du.

# Erabilpena
## Fortinet suhesia prestatu
Elkarforti erabili ahal izateko, Fortinet suhesi bat izan behar duzu. Demagun ikastetxe batean ari zarela hau erabiltzen, eta ikasgeletako Internet atzipena irakasle bakoitzak kudeatu ahal izatea nahi duzula. Demagun Gela01, Gela02, Gela03 eta Gela04 direla kudeatu nahi dituzun gelen nabigazioa. Gela hauetako bakoitzean 10 ordenagailu dituzu, eta beraien IP helbideak ezagutzen dituzu, demagun hauek direla:
* Gela01: 192.168.10.10 - 192.168.10.19
* Gela02: 192.168.10.20 - 192.168.10.29
* Gela03: 192.168.10.30 - 192.168.10.39
* Gela04: 192.168.10.40 - 192.168.10.49

Suhesiko arauak:

* Suhesian gela hauen izenak **Policy Objects --> Addresses** atalean sortu behar dituzu. Adibidean bezala, IP helbideak jarraian badaude, **Address** moduko objetuak erabili ditzakezu, baina jarraian datozen IPak ez badira, **Address Group** motatako objetuak ere erabili ditzakezu, Elkarforti-k bi motatakoak kudeatu ahal izango ditu. Besterik egin ezean, suhesiak *gela horietako trafikoa debekatzeko konfiguratuta izan beharko zenuke*. 

* Suhesian nabigazioa baimenduta izango duten gelek osatuko duten talde bat sortu behar da, **Address Group** motatakoa. Aurrerago ikusiko dugun **env** fitxategiko **FortiAccessEnabledGroupName** aldagaian sartuko dugun izena izango da.

* Fortinet suhesiak ez du onartzen talde bat hutsik egotea. Une baten gela guzietako nabigazioa debekatu nahiko balitz, **FortiAccessEnabledGroupName** hutsik egon beharko litzake, baina Fortinet-ek ez luke onartuko. Hau konpontzeko, beste **Address** edo **Address Group** bat behar dugu ()


Zure Fortinet suhesia honela prestatu behar duzu:

Aurreko pausuan **env** fitxategia editatu eta gure erakundeko AD-arekin konexioa egin ahal izateko konfiguratu dugu. Orain martxan jarriko dugu eta oinarrizko erabilpena azalduko dugu.

## Fortinet suhesiarekin konektatu ahal izateko parametroak:
[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) -ra konektatu eta **admin** erabiltzailearekin sartuko gara. Gogoratu pasahitz lehenetsia **admin** dela eta aldatu beharko zenukeela.

**GROUPACCESS** ataleko **FortiParameters** taulan erregistro berri bat sortuko dugu: [http://127.0.0.1:8000/admin/groupaccess/fortiparameters/add/](http://127.0.0.1:8000/admin/groupaccess/fortiparameters/add/)


* FortiIP: Zure Fortinet suhesiko IP helbidea
* FortiPort: Konexioarako erabiltzen duzun portua
* FortiVdom: Fortinet barruan kudeatuko duzun VDOMare izena
* FortiUserName: Zure Fortinet erabiltzailea
* FortiPassword: Zure Fortinet pasahitza
* FortiAccessEnabledGroupName: Hemendik talde izen bat kudeatuko dugu, hemen jarri behar duzu Fortinet suhesian aurrez sortuta duzun talde horren izena
* FortiDefaultGroupName: Fortinet suhesiak ez du onartzen talde bat hutsik egotea, barruan gutxienez objetu bat izan behar du. Hau izango da FortiAccessEnabledGroupName taldean beti egongo den objetuaren izena.
* FortiKeyStorePath: Fortinet suhesia kudeatzeko erabiltzaile eta pasahitza behar dugunez, ondo zaindu behar ditugu. Horretarako pasahitza zifratu eta Docker irudiko karpeta baten barruan jarriko dugu. Karpeta hori zein izango den guk erabaki dezakegu, balio lehenetsia `/etc/elkarforti` da.
 
