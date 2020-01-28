**BUKATUGABE**

# HELBURUA

Ikastetxe baten kontestuan, irakasleek klaseak ekipo informatikoak dauden geletan ematen dutenean, eta gelako PCak sarera konektaturik daudean, gerta daiteke ikasleek Internet sarean nabigatzen aritzea irakasleak dionari kasurik egin beharrean.

Kontestu honetan, interesgarria litzateke irakasleak berak gelako trafikoa baimendu ala ez erabaki ahal izatea, hau da, berak nahi duenean gelako Internet konexioa edo atzipena gaitu eta desgaitu ahal izatea, baina normalean, Interneteko konexioa suehesian kudeatzen da, eta irakasle arrunt batek ez du ez ezagutzarik, ezta baimenik, suhesia konfiguratu ahal izateko.

Aplikazio honen helburua, irakasleei lan hori erraztea da. Web interfaze minimalista bat eskura jarri, non klik batekin ikasgela bateko Internet atzipena gaitu eta desgaitu ahal izango duen. Hau egin ahal izateko, sistemak erabiltzaile eta pasahitza eskatuko dio, eta baimendutako erabiltzaileek bakarrik kudeatu ahal izango dute Internet atzipena. Erabiltzaile eta pasahitza txekeatzeko, erakundeak jadanik duen ActiveDirectory edo LDAP-a erabiliko dira.

Suhesi asko daude merkatuan, baina soluzio hau Fortinet suhesientzat bakarrik diseinatuta dago.

Aurrerago azalduko dugun moduan, Fortinet suhesian aurrez gauzak konfiguratuta izan beharko ditugu:
1. **Address** edo **Addres Group** motatako objetuak erabiliz, gela bakoitzaren izena eta gelan dauden ekipoen IP helbideak.
2. Beti nabigazioa baimenduta izango duen **Address** edo **Address Group** motatako objetu bat. Hau zergatik ? Ba Fortinet-ek ez duelako onartzen hutsik dagoen **Address Group** bat, aurrerago hobeto azalduko dugu. Konfigurazio parametroetan *fortiDefaultGroupName* aldagaian sartu beharko dugu.
3. Gela guztietaz (lehen pausoan sortu ditugunak) osatuta egongo den beste **AddresGroup** bat. Konfigurazio parametroetan *fortiAccessEnabledGroupName* aldagaian sartu beharko dugu.
4. Fortinet-en arau bat jarri beharko dugu, hirugarren puntuan definitu dugun **Address Group**-ari Internet nabigazioa baimentzen diona. Hau da, **Address Group** horretan dauden *"ikasgelak"* nabigazioa baimenduta izango dute, baina hor ez daudenak nabigazioa debekatuta izan beharko dute, eta portaera hau Fortinet suhesian konfiguratuta egon behar da.

Orain instalatuko dugun aplikazioak hirugarren puntuan definitu dugun **Address Group** hortatik (*fortiAccessEnabledGroupName*) gelak atera eta sartu egingo ditu, eta honela nabigazioa baimendu eta debekatu.


# Instalazioa eta prestaketa lanak

Docker erabiliko dugu elkarforti martxan jartzeko, beraz suposatzen da hau egin aurretik docker [instalatuta duzula](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
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

## Erabiltzaile eta pasahitzak: ActiveDirectory konexioa
Bi erabiltzaile mota ditugu:
* Elkarforti administratzailea: **admin** izena du, eta pasahitz lehentsia **admin** da. Instalazioa egin ondoren hau aldatzea komeni da.
* Elkarforti erabiltzaileak: Ikastetxe baten ikasgeletako Internet atzipena kudeatzeko erabiltzen denean, erabiltzaile naturalak irakasleak lirateke. 

Erabiltzaile hauen kredentzialak LDAP/AD batetik hartuko dira, eta horretarako elkarforti karpetan dagoen **env** fitxategian dauden **aldagaiak** aldatu behar dira. Ohiko parametroak dira, eta bereziki hauek aipatuko ditugu:
 * LDAP_REQUIRE_GROUP: Elkarforti-ko taldeen kudeaketa egin ahal izango duten erabiltzaileen taldea
 * LDAP_FLAG_IS_ACTIVE: Login eta eta automatikoki Elkarforti-n aktibo egongo diren erabiltzaileen taldea.
 
Bi talde hauetan oraingoz behintzat jarri kudeaketa baimenak izango dituzten erabiltzaileen taldea. Balio lehenetsi moduan **FortiAccessGroup** agertzen den arren, bakoitzak bere erakundeko talde izen bat jarri beharko du.

## Fortinet suhesia prestatu
Elkarforti erabili ahal izateko, Fortinet suhesi bat izan behar duzu. Demagun ikastetxe batean ari zarela hau erabiltzen, eta ikasgeletako Internet atzipena irakasle bakoitzak kudeatu ahal izatea nahi duzula. Demagun Gela01, Gela02, Gela03 eta Gela04 direla kudeatu nahi dituzun gelen nabigazioa. Gela hauetako bakoitzean 10 ordenagailu dituzu, eta beraien IP helbideak ezagutzen dituzu, demagun hauek direla:
* Gela01: 192.168.10.10 - 192.168.10.19
* Gela02: 192.168.10.20 - 192.168.10.29
* Gela03: 192.168.10.30 - 192.168.10.39
* Gela04: 192.168.10.40 - 192.168.10.49

Suhesiko arauak:

* Suhesian gela hauen izenak **Policy Objects --> Addresses** atalean sortu behar dituzu. Adibidean bezala, IP helbideak jarraian badaude, **Address** moduko objetuak erabili ditzakezu, baina jarraian datozen IPak ez badira, **Address Group** motatako objetuak ere erabili ditzakezu, Elkarforti-k bi motatakoak kudeatu ahal izango ditu. Besterik egin ezean, suhesiak *gela horietako trafikoa baimentzako konfiguratuta izan beharko zenuke*. 

* Suhesian nabigazioa baimenduta izango duten gelek osatuko duten talde bat sortu behar da, **Address Group** motatakoa. Aurrerago ikusiko dugun **env** fitxategiko **FortiAccessEnabledGroupName** aldagaian sartuko dugun izena izango da.

* Fortinet suhesiak ez du onartzen talde bat hutsik egotea. Une baten gela guzietako nabigazioa debekatu nahiko balitz, **FortiAccessEnabledGroupName** hutsik egon beharko litzake, baina Fortinet-ek ez luke onartuko. Hau konpontzeko, beste **Address** edo **Address Group** bat behar dugu, **FortiAccessEnabledGroupName** beti egongo dena. Adibide moduan, **Address** objetu bat sortu dezakezu Fortinet-eko IParekin, edo bestela beti nabigazioa baimenduta izango duen zure sareko beste IP batekin.

## ActiveDirectory konfigurazioa

Zure erakundeko AD-arekin konektatu ahal izateko, **env** fitxategia editatu eta parametroak aldatu. 

# ElkarForti konfigurazioa

Jarri dezagun berrio martxan: `sudo docker-compose up`

## FortiParameters

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) -ra konektatu eta **admin** erabiltzailearekin sartuko gara. Gogoratu pasahitz lehenetsia **admin** dela eta aldatu beharko zenukeela.

**GROUPACCESS** ataleko **FortiParameters** taulan erregistro berri bat sortuko dugu: [http://127.0.0.1:8000/admin/groupaccess/fortiparameters/add/](http://127.0.0.1:8000/admin/groupaccess/fortiparameters/add/)


* FortiIP: Zure Fortinet suhesiko IP helbidea
* FortiPort: Konexioarako erabiltzen duzun portua
* FortiVdom: Fortinet barruan kudeatuko duzun VDOMaren izena
* FortiUserName: Zure Fortinet erabiltzailea
* FortiPassword: Zure Fortinet pasahitza
* FortiAccessEnabledGroupName: Aurrez azaldu den moduan, hemen jarri behar duzu Fortinet suhesian aurrez sortu duzun eta barruan baimendutako gelen izena izango duen  **Address Group** objetuaren izena.
* FortiDefaultGroupName: Aurrez azaldu den moduan, hemen jarri behar duzu Fortinet suhesian aurrez sortuta duzun eta Internet atzipena **beti baimenduta** izango duen **Address** edo **Address Group** objetuaren izena.
* FortiKeyStorePath: Fortinet suhesia kudeatzeko baimenak dituen erabiltzaile izena eta bere pasahitza behar dugunez, ondo zaindu behar ditugu. Horretarako pasahitza zifratu eta Docker irudiak irakurri eta idatzi ahal izango duen karpeta baten barruan jarriko dugu. Karpeta hori zein izango den guk erabaki dezakegu, balio lehenetsia `/etc/elkarforti` da. Aldatzen baduzu, gogoratu docker-compose.yml fitxategian ere keys bolumena ere aldatu beharko duzula.
* AutomaticOpenClose: Oraindik ez du ezer egiten. Aurrerantzen, parametro honen balioa erabiliko da ordu jakin batean gelen egoera automatikoki aldatu behar den erabakitzeko.
* automaticOpenTime: Oraindik ez du ezer egiten. Aurrerantzean, AutomaticOpenClose balioa baiezkoa bada, aldagai honetan ezarritako orduan gela deneri nabigazioa baimenduko zaie.
* automaticCloseTime: Oraindik ez du ezer egiten. Aurrerantzean, AutomaticOpenClose balioa baiezkoa bada, aldagai honetan ezarritako orduan gela deneri nabigazioa debekatuko zaie.
 
 Datuak sartu ondoren, konfigurazio erregistroa gorde.
 
 ## FortiGroups
 
 Azken pausoa, gelen izenak sartzea da. Horretarako sartu FortiGroups atalean [http://127.0.0.1:8000/admin/groupaccess/fortigroup/](http://127.0.0.1:8000/admin/groupaccess/fortigroup/) eta sortu gelaren izena **Add Forti Group** botoian klikatuz.
 * Name: Gelaren izena, Fortinet suhesian duen izen berbera izan behar du. 
 * Enabled: Gelaren nabigazioa baimenduta izatea nahi baduzu.
 
 Gela guztiak sortu aurreko pausoak jarraituz.
 
 # ElkarForti erabilpena
 
 Aurreko pausoak ondo joan badira, orain nola erabiltzen den ikus dezagun. Sartu zaitez irakasleek erabiliko duten interfazean: http://127.0.0.1:8000/
 
 Gogoan izan, hemen bi aukera izango dituzu:
 * edo AD/LDAP-aren kontra balidatzen da 
 * edo bestela admin erabiltzaile lokalarekin 
 
 Gela batek Internet atzipena debekatuta duenea, ikono gorri batekin azalduko da, eta baimenduta duenean ikono berde batekin. 
 
 Egoera aldateko, gainean klikatu, eta agertuko den formularioan egoera aldatu, besterik ez.
 
 
 
