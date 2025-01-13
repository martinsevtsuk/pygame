**Soccer Game**
See on 2D jalgpallimäng, mis võimaldab kahel mängijal mängida ühe klaviatuuri taga. Mäng on loodud Pygame'i raamistikus ja sisaldab graafikat, heli, füüsikat ning mängumehhaanikaid. Selgitan, mida kood teeb ja kuidas mäng toimib.

**Mängu ülesehitus**

Mäng algab vajalike raamatukogude ja kaustade seadistamisega. Kõik graafika- ja helifailid asuvad spetsiaalsetes kaustades (Game Files/Images ja Game Files/music).

Mänguakna suurus on 1280x720 pikslit, ja mängu taust, väravad, mängijad ning pall laaditakse vastavatest failidest, kohandades nende suurust ja algasendit.

**Heli ja muusika**

Mängus mängitakse taustamuusikat (worldcup.mp3), mida saab põhimenüüs reguleerida helitugevuse suurendamise ja vähendamise nuppudega. Maksimaalne helitugevus on 100% ja minimaalne 0%. Valida saab kahe mängumoodi vahel ning mõlemal poolel on 4 karakterit valikus.
Kaootilises moodis esinevad efektid nagu "low gravity", "speedy gonzales", "no jumping".

**Mängijate juhtimine**

Igal mängijal on oma klahvid liikumiseks:

- **Vasak mängija** kasutab Whüppamiseks, A vasakule liikumiseks ja D paremale liikumiseks. Löömiseks Q.
- **Parem mängija** kasutab ÜLES-noolt hüppamiseks, VASAK-noolt vasakule liikumiseks ja PAREM-noolt paremale liikumiseks. Löömiseks RCtrl.

Mängijad saavad hüpata, ja neid mõjutab gravitatsioon, mis toob nad lõpuks maapinnale tagasi. Mängijad ei saa väljuda mänguväljaku piiridest.

**Palli füüsika**

Pall reageerib gravitatsioonile, löökidele ja kokkupuutele mängijatega. Kui pall puutub mängijaga, muutub selle suund ja kiirus sõltuvalt kokkupuutepunktist. Pall võib põrkuda ka vastu seinu ja väravaid, kusjuures iga kokkupuude aeglustab või muudab selle liikumist. Kui pall jõuab maapinnale, aeglustub see lõpuks ja jääb seisma. Värava pealt veereb pall alati alla.

**Skoorimine**

Kui pall läheb ühte väravasse, saab vastasmängija punkti. Seejärel lähtestatakse nii mängijad kui ka pall algasendisse. Mäng lõpeb, kui üks mängija saavutab 7 punkti.

**Graafika ja animatsioonid**

Mängus kuvatakse dünaamiliselt:

- **Taust ja väravad**
- **Mängijad ja nende animatsioonid**: Kui mängija lööb, kasutatakse spetsiaalseid animatsioone, mis näitavad mängijat löömas.
- **Palli pöörlemine**: Pall pöörleb sõltuvalt selle kiirusest, lisades visuaalset efekti.
- **Skoor**: Mängijate punkte kuvatakse ekraanil reaalajas.
- **Efektid**: Kaootilises mängumoodis kuvatakse all ääres efekte. 

**Mängumenüüd**

Mängul on mitu menüüd:

1. **Põhimenüü**: Kuvab mängu nime ja pakub võimalust alustada mängu, samuti reguleerida helitugevust.
2. **Pausimenüü**: Kui mängija vajutab ESC, mäng peatatakse ja taust hägustatakse, näidates pausi olekut.
3. **Võitjate ekraan**: Kui üks mängija võidab (saavutab 7 punkti), kuvatakse tema võit koos võimalusega mäng uuesti alustada.
4. **Karakteri menüü**: Pärast mängumoodi valimist valitakse karaktereid.

**Eripärad**
Kood on üles ehitatud nii, et seda saab laiendada – näiteks lisada uusi animatsioone, efekte, helisid või muuta füüsikareegleid. See on lihtne ja lõbus mäng, mis sobib kahele mängijale.
