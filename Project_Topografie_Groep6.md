# Topografie Groep 6 — Projectplan
**Geobas-methode | Interactieve App + YouTube Video**
*Datum: 22 maart 2026*

---

## OPDRACHT 1: INTERACTIEVE APP — BLAUWDRUK

### Concept: "Kaartridder Nederland"
Een gamified web-app (ook mobiel bruikbaar) waarbij leerlingen als 'Kaartridder' heel Nederland veroveren door topografievragen te beantwoorden. De kaart van Nederland staat centraal en wordt stap voor stap 'ontgrendeld'.

---

### 1.1 Gamification

| Element | Uitwerking |
|---|---|
| **Levels per provincie** | Elke provincie is een 'wereld'. Je begint in jouw eigen provincie en reist naar de rest. |
| **Sterren-systeem** | Per level verdien je 1–3 sterren (snel + fout-vrij = 3 sterren). |
| **Badges** | "Hollandse Held" (G&ZH), "Friese Kampioen", "Deltawerken-expert", etc. |
| **Voortgangsbalk** | Visuele kaart van Nederland vult zich met kleur naarmate provincies worden voltooid. |
| **Race tegen de klok** | Optionele tijdmodus: 60 seconden, zo veel mogelijk steden goed plaatsen. |
| **Dagelijkse uitdaging** | Eén korte quiz per dag (3 vragen) met bonuspunten. |
| **Highscore-lijst** | Klassikale ranglijst (alleen voornamen, privacyvriendelijk). |

---

### 1.2 Drie Spelvormen

#### Spelvorm 1: "Sleep de Stad" (Drag & Drop)
- Een lijst met 5 steden verschijnt rechts in beeld.
- De leerling sleept elke stad naar de juiste plek op de interactieve kaart.
- **Feedbackmechanisme:** Stad 'klapt' op de goede plek vast (groen vinkje + vrolijk geluidje), of stuitert terug met een vriendelijk "Bijna!" bij een fout.
- **Moeilijkheidsgraad:** Beginner = steden met een hint-cirkel; Gevorderd = blanco kaart.

#### Spelvorm 2: "Zoek de Hoofdstad" (Multiple Choice + Kaart)
- Een provincie licht op in de kaart.
- Vraag: *"Wat is de hoofdstad van deze provincie?"*
- Vier antwoordknoppen verschijnen (A, B, C, D) met kleurrijke icoontjes.
- **Feedbackmechanisme:** Correct = confetti-animatie + uitroep van het mascotte ("Geweldig, held!"). Fout = de kaart zoomt in op de juiste stad met een korte uitleg.

#### Spelvorm 3: "Welke Provincie Is Dit?" (Silhouet-quiz)
- Een witte silhouet van een provincie verschijnt op een gekleurde achtergrond.
- Leerling tikt de juiste naam aan (of typt die in voor extra uitdaging).
- **Bonus:** Na een goed antwoord verschijnt een leuke feitje: *"Wist je dat Friesland de enige provincie is met een eigen taal?"*
- **Moeilijkheidsgraad:** Gekleurd silhouet → zwart silhouet → alleen de vorm zonder kleur.

---

### 1.3 Feedback-systeem (kindvriendelijk)

| Situatie | Feedback |
|---|---|
| **Goed antwoord** | Groene animatie + applaus-geluid + "Super goed!" van mascotte |
| **Fout antwoord (1e poging)** | Oranje animatie + "Probeer nog eens!" + kleine hint |
| **Fout antwoord (2e poging)** | Rood + "Het goede antwoord is…" + korte uitleg + kaartanimatie |
| **Perfecte ronde** | Gouden ster-explosie + speciale badge |
| **Lange sessie** | Pauze-herinnering: "Je speelt al 20 minuten — even stretchen?" |

**Mascotte:** "Topo" — een vrolijke kompasroos-figuur met grote ogen en een kapiteinshoeksje. Topo begeleidt de leerling door de app met korte, bemoedigende zinnen.

---

### 1.4 User Interface (UI) — Visueel Ontwerp

#### Kleurpalet
- **Achtergrond:** Lichtblauw (zee-gevoel), zacht groen voor het land
- **Provincies:** Elk een eigen pastelkleur (niet te druk)
- **Knoppen:** Groot, afgerond, contrastrijke kleuren (toegankelijk)
- **Lettertype:** Ronde, goed leesbare fonts (bijv. Nunito of Baloo 2)

#### Schermindeling (web-app)
```
+------------------------------------------+
|  [Logo: Kaartridder]    [Sterren: ★★☆]   |
|  [Voortgang: 4/12 provincies]             |
+------------------------------------------+
|                                           |
|        INTERACTIEVE KAART                 |
|        van Nederland                      |
|        (centraal, groot)                  |
|                                           |
+------------------------------------------+
|  [Spelvorm 1] [Spelvorm 2] [Spelvorm 3]  |
|  [Terug]                   [Dagelijkse!] |
+------------------------------------------+
```

#### Extra UI-tips
- **Grote touch-targets** (min. 48x48px) voor kleine vingers op tablet
- **Weinig tekst per scherm** — prentjes en icoontjes domineren
- **Geluiden aan/uit** knop zichtbaar (voor klaslokaal gebruik)
- **Donkere modus** niet nodig voor deze leeftijd — felle, vrolijke kleuren werken beter
- **Toegankelijkheid:** Hoog contrast, ondersteuning voor dyslexie-vriendelijk font (optie)

---

### 1.5 Technische Stack (aanbeveling)

| Onderdeel | Technologie |
|---|---|
| Frontend | React + Vite (web-app, ook mobiel via browser) |
| Kaart-component | SVG kaart van Nederland (per provincie apart klikbaar) |
| Drag & Drop | React DnD of @dnd-kit/core |
| Animaties | Framer Motion of CSS animations |
| Geluidseffecten | Howler.js |
| Backend (optioneel) | Supabase (highscores, voortgang opslaan) |
| Mobiel (fase 2) | React Native of PWA |

---

## OPDRACHT 2: YOUTUBE VIDEO — SCRIPT & STORYBOARD

### Concept: "Kaartavontuur — De 12 Provincies van Nederland"
**Duur:** ~5 minuten | **Stijl:** Het Klokhuis / Topdoks — energiek, vriendelijk, beeldend

---

### 2.1 Ezelsbruggetje voor de 12 Provincies

**Zin-methode (eerste letters):**
> **"G**roningen **F**ietst **D**oor **O**verijs**s**el **G**elderlijk **U**trecht **N**oord **Z**uid **Z**eeland **N**oord-**B**rabant **L**imburg"

**Of de rijm-methode (beter voor kinderen):**
> *"Groningen, Friesland, Drenthe drie,*
> *Dan Overijssel, Gelderland — zie!*
> *Utrecht, Noord- en Zuid-Holland gaan,*
> *Zeeland, Noord-Brabant, Limburg — klaar met slaan!"*

*(12 provincies in geografische volgorde, van noord naar zuid)*

**Visuele koppeling (voor de video):**
| Provincie | Ezelsbruggetje / Associatie |
|---|---|
| Groningen | Martinitoren (herkenningsteken) |
| Friesland | Friese koe / Elfstedentocht |
| Drenthe | Hunebedden (stenen) |
| Overijssel | Giethoorn (bootje) |
| Gelderland | Veluwe / Hoge Veluwe |
| Utrecht | Dom-toren |
| Noord-Holland | Tulpen / windmolens / Amsterdam |
| Zuid-Holland | Kinderdijk / Den Haag / Rotterdam |
| Zeeland | Delta / zee / Deltawerken |
| Noord-Brabant | Carnaval / Efteling |
| Limburg | Heuvels / Maastricht |
| Flevoland | *"De provincie die we bijna vergeten!"* — nieuwste, in zee gebouwd |

---

### 2.2 Script + Storyboard

---

#### SCÈNE 1 — INTRO (0:00–0:25)

**AUDIO:**
> *"Hey! Hé jij daar! Weet jij hoeveel provincies Nederland heeft? Twaalf! En weet jij ze allemaal? Geen paniek — aan het einde van deze video ken jij ze allemaal uit je hoofd. Ik beloof het. Laten we gaan!"*

**BEELD:**
- Snelle montage: kaart van Nederland 'explodeert' in 12 stukken en valt weer samen
- Vrolijke muziek, energiek tempo
- Presentator (of animatie-avatar) springt in beeld
- Tekst op scherm: **"12 PROVINCIES IN 5 MINUTEN!"**

---

#### SCÈNE 2 — DE KAART UITGELEGD (0:25–1:15)

**AUDIO:**
> *"Kijk, dit is Nederland. Klein landje, maar o zo bijzonder! Boven: de zee. Rechts: Duitsland en België. En kijk — de grote rivieren snijden dwars door het land. Die Rijn, Maas en Waal verdelen Nederland eigenlijk in twee stukken: het natte westen en het droge oosten. En dat is precies waarom de provincies er zo uitzien als ze er uitzien!"*

**BEELD:**
- Animatie: kaart van Nederland op scherm, omringende landen vervagen
- Rivieren worden ingetekend met blauwe animatielijnen (met geluidseffect: 'plons')
- Pijlen wijzen west/oost
- Infographic: "West = laag land & polders" | "Oost = hogere grond"
- Kaart flitst heel even: de 12 provincie-grenzen verschijnen

---

#### SCÈNE 3 — DE 12 PROVINCIES (1:15–3:30)

**AUDIO (per provincie kort, ~10 sec):**

> *"Oké, we beginnen bovenaan en gaan naar beneden. Klaar? Gaan!"*

| Provincie | Gesproken tekst | Beeld |
|---|---|---|
| **Groningen** | "Helemaal in het noorden: Groningen. Grote stad, naamgever én provincie. Makkelijk!" | Provincie licht geel op, Martinitoren-icoon verschijnt |
| **Friesland** | "Friesland — de enige provincie met een eigen taal! Frysk prate? Nee? Dan leer je het nu: 'Goeie!' betekent 'Hallo!'" | Friese vlag, koe-animatie |
| **Drenthe** | "Drenthe — bekend van de hunebedden. Dat zijn enorme stenen van vroeger, duizenden jaren oud!" | Animatie van hunebedden |
| **Overijssel** | "Overijssel! Hier ligt Giethoorn, het dorp zonder wegen — alleen maar bootjes!" | Bootje vaart door gracht |
| **Gelderland** | "Gelderland — de grootste provincie van Nederland. Hier is de Veluwe, een groot bos vol wilde dieren." | Silhouet van hert in bos |
| **Utrecht** | "Utrecht — midden in Nederland, en de Dom-toren is het hoogste kerkgebouw van het land!" | Dom-toren groeit omhoog |
| **Noord-Holland** | "Noord-Holland: Amsterdam, tulpen en windmolens. Dit ken je vast al!" | Grachtenpand + tulpen-animatie |
| **Zuid-Holland** | "Zuid-Holland: Rotterdam heeft de grootste haven van Europa. En in Den Haag zitten de ministers." | Haven met schepen, vergaderzaal |
| **Zeeland** | "Zeeland — bijna een eiland! Het water is overal. De Deltawerken houden het droog." | Deltawerken animatie |
| **Noord-Brabant** | "Noord-Brabant: carnaval, feest, en de Efteling! Wist je dat Brabant vroeger bij België hoorde?" | Carnaval + Efteling-silhouet |
| **Limburg** | "Limburg — de enige provincie met echte heuvels. En de lekkerste vlaai!" | Heuvels, vlaai |
| **Flevoland** | "En dan… de geheime provincie! Flevoland! Die is ín de zee gebouwd. Letterlijk. Door mensen. Hoe gaaf is dat?!" | Animatie: land rijst op uit water |

---

#### SCÈNE 4 — HET EZELSBRUGGETJE (3:30–4:15)

**AUDIO:**
> *"Oké, twaalf provincies — dat is best veel om te onthouden. Maar heb je dit rijmpje gehoord?"*
>
> *(langzaam, met ritme):*
> *"Groningen, Friesland, Drenthe drie,*
> *Dan Overijssel, Gelderland — zie!*
> *Utrecht, Noord- en Zuid-Holland gaan,*
> *Zeeland, Noord-Brabant, Limburg — klaar met slaan!"*
>
> *"Probeer het mee te zeggen! Nog een keer, sneller!"*

**BEELD:**
- Tekst van het rijmpje verschijnt woord voor woord op scherm
- Kaart: elke provincie licht op op het moment dat die in het rijmpje wordt genoemd
- Tweede herhaling: tempo is hoger, tekst springt mee met muziek

---

#### SCÈNE 5 — AFSLUITING & OPROEP (4:15–5:00)

**AUDIO:**
> *"En? Ken jij ze nu? Test jezelf: zet de video op pauze en schrijf alle twaalf op zonder te kijken! Lukt het? Dan ben jij een echte Kaartridder! Wil je nog meer oefenen? Zoek dan de interactieve kaart-app — link staat in de beschrijving. Doe je best op de toets, en tot de volgende keer!"*

**BEELD:**
- Presentator/avatar doet een duim omhoog
- Animatie: kaart van Nederland met alle provincies ingekleurd en namen erbij
- Einde-scherm: [Abonneren] [Volgende video] [App-link]
- Vrolijke afsluitmuziek

---

### 2.3 Productie-tips

| Aspect | Aanbeveling |
|---|---|
| **Presentatievorm** | Animatie-avatar (Canva / After Effects) of echte presentator |
| **Muziek** | Vrolijke achtergrondmuziek (rechtenvrij), bijv. Bensound of Pixabay |
| **Animaties** | Malatopia / Canva voor kaart-animaties; Adobe Express voor tekst-effecten |
| **Teksteditor op scherm** | Grote, gekleurde tekst — minimaal 60px lettergrootte |
| **Spreektempo** | Bewust langzamer dan normaal voor 9-jarigen, duidelijke articulatie |
| **Lengte check** | Scènes 1-5 samen = ~5 min; trim bij nodig na opname |
| **Thumbnail** | Kaart van NL + grote tekst "ALLE 12 PROVINCIES" + vrolijke avatar |

---

## VOLGENDE STAPPEN

### Fase 1 — Fundament (Week 1-2)
- [ ] SVG-kaart van Nederland per provincie inkopen/maken
- [ ] Script finaliseren en voice-over opnemen
- [ ] Basis app-structuur opzetten (React + Vite)

### Fase 2 — Bouw (Week 3-4)
- [ ] Drie spelvormen implementeren
- [ ] Feedback-animaties en geluidseffecten
- [ ] Mascotte "Topo" ontwerpen

### Fase 3 — Video (Week 4-5)
- [ ] Kaart-animaties maken (Canva of After Effects)
- [ ] Video opnemen/renderen
- [ ] Monteren, ondertiteling toevoegen

### Fase 4 — Test & Launch (Week 6)
- [ ] Testen met echte Groep 6 leerlingen
- [ ] Feedback verwerken
- [ ] YouTube video publiceren + app online zetten

---

*Gegenereerd op 22 maart 2026 | Kaartridder Nederland — Topografie Groep 6*
