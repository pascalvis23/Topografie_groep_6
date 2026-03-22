"""
Bouwt provinces.js op basis van:
1. Strenge OCR-matches (alleen als de OCR-tekst daadwerkelijk de stadsnaam is)
2. Valt terug op geografische coördinaten voor steden die OCR niet vond
"""
import json, re, os

OCR_JSON = r"C:\Software\Topografiekaart_6\ocr_results.json"

with open(OCR_JSON, encoding="utf-8") as f:
    ocr_data = json.load(f)

# ─── Geografische coördinaten (backup) ────────────────────────────────────────
COORDS = {
    "Steenwijk":(52.788,6.119),"Giethoorn":(52.733,6.083),"Hardenberg":(52.574,6.617),
    "Kampen":(52.556,5.910),"Zwolle":(52.516,6.083),"Ommen":(52.518,6.421),
    "Deventer":(52.254,6.163),"Nijverdal":(52.363,6.463),"Almelo":(52.355,6.662),
    "Rijssen":(52.305,6.514),"Oldenzaal":(52.314,6.928),"Hengelo":(52.266,6.794),
    "Enschede":(52.222,6.893),"Haaksbergen":(52.157,6.740),
    "Zierikzee":(51.651,3.917),"Domburg":(51.563,3.499),"Veere":(51.558,3.667),
    "Middelburg":(51.500,3.610),"Goes":(51.504,3.890),"Yerseke":(51.496,4.054),
    "Vlissingen":(51.442,3.574),"Breskens":(51.401,3.557),"Terneuzen":(51.335,3.828),
    "Hulst":(51.278,4.044),
    "Roodeschool":(53.389,6.780),"Appingedam":(53.321,6.858),"Delfzijl":(53.327,6.920),
    "Groningen":(53.219,6.567),"Hoogezand-Sappemeer":(53.165,6.769),
    "Winschoten":(53.143,7.038),"Haren":(53.181,6.611),"Roden":(53.144,6.431),
    "Zuidlaren":(53.097,6.689),"Veendam":(53.107,6.877),"Assen":(52.993,6.563),
    "Stadskanaal":(52.986,6.953),"Borger":(52.904,6.797),"Ter Apel":(52.878,7.069),
    "Beilen":(52.861,6.511),"Westerbork":(52.838,6.600),"Hoogeveen":(52.726,6.478),
    "Emmen":(52.781,6.900),"Klazienaveen":(52.731,6.977),"Meppel":(52.696,6.194),
    "Coevorden":(52.661,6.742),"Schoonebeek":(52.665,6.885),
    "Urk":(52.664,5.601),"Emmeloord":(52.712,5.749),"Dronten":(52.524,5.722),
    "Lelystad":(52.518,5.471),"Almere":(52.350,5.265),"Zeewolde":(52.335,5.540),
    "Amersfoort":(52.157,5.387),"Soest":(52.177,5.301),"De Bilt":(52.106,5.175),
    "Woerden":(52.087,4.882),"Utrecht":(52.091,5.122),"Zeist":(52.088,5.234),
    "Nieuwegein":(52.025,5.082),"Veenendaal":(52.027,5.556),"Grebbeberg":(51.965,5.604),
    "Bergen op Zoom":(51.498,4.288),"Roosendaal":(51.531,4.463),"Waalwijk":(51.682,5.070),
    "'s-Hertogenbosch":(51.689,5.305),"Oss":(51.765,5.519),"Oisterhout":(51.577,4.867),
    "Kaatsheuvel":(51.657,5.040),"Breda":(51.589,4.779),"Boxtel":(51.594,5.331),
    "Uden":(51.659,5.619),"Boxmeer":(51.645,5.948),"Venray":(51.526,5.976),
    "Tilburg":(51.558,5.083),"Eindhoven":(51.441,5.478),"Helmond":(51.481,5.661),
    "Valkenswaart":(51.352,5.459),"Weert":(51.249,5.709),"Venlo":(51.370,6.172),
    "Roermond":(51.195,5.987),"Sittard":(51.004,5.866),"Geleen":(50.969,5.833),
    "Hoensbroek":(50.930,5.919),"Heerlen":(50.888,5.979),"Kerkrade":(50.864,6.061),
    "Maastricht":(50.851,5.688),"Valkenburg":(50.866,5.829),"Vaals":(50.773,6.025),
    "Noordwijk":(52.235,4.449),"Leiden":(52.160,4.497),"Wassenaar":(52.144,4.401),
    "Alphen aan den Rijn":(52.127,4.659),"Scheveningen":(52.108,4.272),
    "Den Haag":(52.075,4.299),"Zoetermeer":(52.057,4.494),"Gouda":(52.018,4.707),
    "Delft":(52.011,4.359),"Hoek van Holland":(51.979,4.132),"Vlaardingen":(51.913,4.340),
    "Schiedam":(51.919,4.396),"Rotterdam":(51.925,4.479),"Spijkenisse":(51.847,4.336),
    "Dordrecht":(51.814,4.668),"Gorinchem":(51.831,4.976),
    "Texel":(53.067,4.817),"Den Helder":(52.955,4.762),"Enkhuizen":(52.702,5.297),
    "Hoorn":(52.641,5.062),"Alkmaar":(52.631,4.740),"Purmerend":(52.502,4.955),
    "Volendam":(52.499,5.070),"IJmuiden":(52.457,4.620),"Zaandam":(52.433,4.813),
    "Zandvoort":(52.371,4.535),"Haarlem":(52.381,4.635),"Amsterdam":(52.372,4.894),
    "Amstelveen":(52.305,4.862),"Schiphol":(52.309,4.765),"Aalsmeer":(52.267,4.763),
    "Bussum":(52.275,5.162),"Hilversum":(52.223,5.174),
    "Dokkum":(53.325,5.999),"Leeuwarden":(53.201,5.800),"Franeker":(53.188,5.540),
    "Harlingen":(53.174,5.416),"Drachten":(53.108,6.100),"Bolsward":(53.065,5.531),
    "Sneek":(53.031,5.661),"Joure":(52.967,5.792),"Heerenveen":(52.961,5.919),
    "Stavoren":(52.879,5.365),"Lemmer":(52.845,5.714),"Wolvega":(52.878,5.993),
    "Vlieland":(53.253,5.063),"Terschelling":(53.398,5.260),
    "Ameland":(53.443,5.657),"Schiermonnikoog":(53.480,6.171),
    "Nunspeet":(52.358,5.783),"Harderwijk":(52.341,5.623),"Nijkerk":(52.217,5.493),
    "Apeldoorn":(52.212,5.970),"Barneveld":(52.143,5.590),"Zutphen":(52.138,6.196),
    "Ede":(52.042,5.665),"Wageningen":(51.969,5.664),"Arnhem":(51.985,5.898),
    "Groenlo":(51.998,6.624),"Doetinchem":(51.965,6.300),"Winterswijk":(51.975,6.716),
    "Tiel":(51.886,5.428),"Elst":(51.921,5.840),"Zevenaar":(51.927,6.074),
    "Nijmegen":(51.843,5.859),
}

MAP_EXTENTS = {
    1: (5.20,7.40,51.80,53.05), 2: (2.90,4.60,50.90,51.95),
    3: (5.60,7.50,52.20,53.90), 4: (4.30,6.10,51.65,52.95),
    5: (3.40,6.60,50.40,52.15), 6: (3.50,5.40,51.30,52.55),
    7: (3.90,5.55,51.95,53.55), 8: (4.30,6.80,52.20,53.90),
    9: (5.00,7.20,51.35,52.80),
}

def geo_to_img(lat, lon, lid):
    lon_min,lon_max,lat_min,lat_max = MAP_EXTENTS[lid]
    x = 5 + (lon-lon_min)/(lon_max-lon_min)*90
    y = 10 + (lat_max-lat)/(lat_max-lat_min)*82
    return round(x,1), round(y,1)

# ─── Strikte OCR-matching ─────────────────────────────────────────────────────
def clean(s):
    """Verwijder OCR-artefacten en normaliseer."""
    return re.sub(r"[*\(\)\[\]\"\'`\-=!@#@]","", s).strip()

def match_score(ocr_text, city_name):
    """
    Geeft een score hoe goed de OCR-tekst overeenkomt met de stadsnaam.
    Hogere score = betere match. 0 = geen match.
    """
    ocr_raw = clean(ocr_text)
    ocr_clean = ocr_raw.lower()
    # Vervang veelvoorkomende OCR-fouten
    ocr_clean = ocr_clean.replace("0", "o").replace("1", "l").replace("8", "b")
    city_lower = city_name.lower()
    city_parts = city_lower.split()

    # Score = lengte van de overeenkomende tekst gedeeld door max(beide lengtes)
    # Langer = beter
    def overlap_score(a, b):
        if not a or not b:
            return 0
        if a == b:
            return len(a)  # perfecte match → hoogste score
        if b in a:  # stadsnaam zit in OCR → goed
            return len(b)
        if a in b and len(a) >= 4:  # OCR zit in stadsnaam
            return len(a) * 0.9  # iets lager want korter
        # Eerste woord van meerwoordige naam
        if len(city_parts) > 1:
            for part in city_parts:
                if len(part) >= 4 and a == part:
                    return len(part) * 0.8
        return 0

    score = overlap_score(ocr_clean, city_lower)
    # Normaliseer op stadsnaamslengte zodat langere matches zwaarder wegen
    if score > 0:
        score = score / max(len(city_lower), 1)
    return score

def best_ocr_match(all_texts, city_name, min_score=0.5, y_min=15, y_max=92):
    """
    Vindt de beste OCR-match voor een stadsnaam, gefilterd op y-bereik.
    Geeft terug: item met x0 (linker rand = kaartmarkerpositie), y (midden).
    """
    best = None
    best_score = 0
    for item in all_texts:
        if item["y"] < y_min or item["y"] > y_max:
            continue
        sc = match_score(item["text"], city_name)
        if sc > best_score and sc >= min_score:
            best_score = sc
            best = item
    return best, best_score

# ─── Bouw per les de coordinaten op ──────────────────────────────────────────
LESSEN_DEF = [
    (1,"Overijssel","#4CAF50","/maps/les1_overijssel_namen.png","/maps/les1_overijssel_blanco.png",[
        ("Steenwijk","stad"),("Giethoorn","stad"),("Hardenberg","stad"),("Kampen","stad"),
        ("Zwolle","stad"),("Ommen","stad"),("Deventer","stad"),("Nijverdal","stad"),
        ("Almelo","stad"),("Rijssen","stad"),("Oldenzaal","stad"),("Hengelo","stad"),
        ("Enschede","stad"),("Haaksbergen","stad"),
        ("Vecht","water"),("Salland","streek"),("IJssel","water"),("Twente","streek"),
    ]),
    (2,"Zeeland","#2196F3","/maps/les2_zeeland_namen.png","/maps/les2_zeeland_blanco.png",[
        ("Zierikzee","stad"),("Domburg","stad"),("Veere","stad"),("Middelburg","stad"),
        ("Goes","stad"),("Yerseke","stad"),("Vlissingen","stad"),("Breskens","stad"),
        ("Terneuzen","stad"),("Hulst","stad"),
        ("Noordzee","water"),("Grevelingen","water"),("Oosterschelde","water"),
        ("Walcheren","streek"),("Zuid-Beveland","streek"),("Schelde-Rijnkanaal","water"),
        ("Westerschelde","water"),("Zeeuws-Vlaanderen","streek"),("Kanaal Gent-Terneuzen","water"),
    ]),
    (3,"Groningen en Drenthe","#FF9800","/maps/les3_groningen_drenthe_namen.png","/maps/les3_groningen_drenthe_blanco.png",[
        ("Roodeschool","stad"),("Appingedam","stad"),("Delfzijl","stad"),("Groningen","stad"),
        ("Hoogezand-Sappemeer","stad"),("Winschoten","stad"),("Haren","stad"),("Roden","stad"),
        ("Zuidlaren","stad"),("Veendam","stad"),("Assen","stad"),("Stadskanaal","stad"),
        ("Borger","stad"),("Ter Apel","stad"),("Beilen","stad"),("Westerbork","stad"),
        ("Hoogeveen","stad"),("Emmen","stad"),("Klazienaveen","stad"),("Meppel","stad"),
        ("Coevorden","stad"),("Schoonebeek","stad"),
        ("Lauwerssmeer","water"),("Waddenzee","water"),("Eemskanaal","water"),
        ("Dollard","water"),("Reitdiep","water"),
    ]),
    (4,"Flevoland en Utrecht","#9C27B0","/maps/les4_flevoland_utrecht_namen.png","/maps/les4_flevoland_utrecht_blanco.png",[
        ("Urk","stad"),("Emmeloord","stad"),("Dronten","stad"),("Lelystad","stad"),
        ("Almere","stad"),("Zeewolde","stad"),("Amersfoort","stad"),("Soest","stad"),
        ("De Bilt","stad"),("Woerden","stad"),("Utrecht","stad"),("Zeist","stad"),
        ("Nieuwegein","stad"),("Veenendaal","stad"),("Grebbeberg","stad"),
        ("IJsselmeer","water"),("Noordoost-polder","streek"),("Markermeer","water"),
        ("Oostelijk Flevoland","streek"),("Veluwemeer","water"),("Zuidelijk Flevoland","streek"),
        ("Gooimeer","water"),("Amsterdam-Rijnkanaal","water"),("Neder-Rijn","water"),
    ]),
    (5,"Noord-Brabant en Limburg","#F44336","/maps/les5_brabant_limburg_namen.png","/maps/les5_brabant_limburg_blanco.png",[
        ("Bergen op Zoom","stad"),("Roosendaal","stad"),("Waalwijk","stad"),
        ("'s-Hertogenbosch","stad"),("Oss","stad"),("Oisterhout","stad"),("Kaatsheuvel","stad"),
        ("Breda","stad"),("Boxtel","stad"),("Uden","stad"),("Boxmeer","stad"),
        ("Venray","stad"),("Tilburg","stad"),("Eindhoven","stad"),("Helmond","stad"),
        ("Valkenswaart","stad"),("Weert","stad"),("Venlo","stad"),("Roermond","stad"),
        ("Sittard","stad"),("Geleen","stad"),("Hoensbroek","stad"),("Heerlen","stad"),
        ("Kerkrade","stad"),("Maastricht","stad"),("Valkenburg","stad"),("Vaals","stad"),
        ("De Peel","streek"),("Juliana-kanaal","water"),
    ]),
    (6,"Zuid-Holland","#00BCD4","/maps/les6_zuidholland_namen.png","/maps/les6_zuidholland_blanco.png",[
        ("Noordwijk","stad"),("Leiden","stad"),("Wassenaar","stad"),
        ("Alphen aan den Rijn","stad"),("Scheveningen","stad"),("Den Haag","stad"),
        ("Zoetermeer","stad"),("Gouda","stad"),("Delft","stad"),("Hoek van Holland","stad"),
        ("Vlaardingen","stad"),("Schiedam","stad"),("Rotterdam","stad"),
        ("Spijkenisse","stad"),("Dordrecht","stad"),("Gorinchem","stad"),
        ("Westland","streek"),("Haringvliet","water"),("Hollands Diep","water"),("Waal","water"),
    ]),
    (7,"Noord-Holland","#FF5722","/maps/les7_noordholland_namen.png","/maps/les7_noordholland_blanco.png",[
        ("Texel","eiland"),("Den Helder","stad"),("Enkhuizen","stad"),("Hoorn","stad"),
        ("Alkmaar","stad"),("Purmerend","stad"),("Volendam","stad"),("IJmuiden","stad"),
        ("Zaandam","stad"),("Zandvoort","stad"),("Haarlem","stad"),("Amsterdam","stad"),
        ("Amstelveen","stad"),("Schiphol","stad"),("Aalsmeer","stad"),("Bussum","stad"),
        ("Hilversum","stad"),
        ("Wieringermeer","streek"),("Noordhollands kanaal","water"),("Beemster","streek"),
        ("Noordzeekanaal","water"),("IJmeer","water"),("Haarlemmermeer","streek"),
        ("Loosdrechtse Plassen","water"),("Het Gooi","streek"),
    ]),
    (8,"Fryslân","#009688","/maps/les8_fryslan_namen.png","/maps/les8_fryslan_blanco.png",[
        ("Vlieland","eiland"),("Terschelling","eiland"),("Ameland","eiland"),
        ("Schiermonnikoog","eiland"),("Dokkum","stad"),("Leeuwarden","stad"),
        ("Franeker","stad"),("Harlingen","stad"),("Drachten","stad"),("Bolsward","stad"),
        ("Sneek","stad"),("Joure","stad"),("Heerenveen","stad"),("Stavoren","stad"),
        ("Lemmer","stad"),("Wolvega","stad"),
        ("Noordzee","water"),("Waddenzee","water"),("Sneekermeer","water"),
        ("Gaasterland","streek"),("IJsselmeer","water"),
    ]),
    (9,"Gelderland","#8BC34A","/maps/les9_gelderland_namen.png","/maps/les9_gelderland_blanco.png",[
        ("Nunspeet","stad"),("Harderwijk","stad"),("Nijkerk","stad"),("Apeldoorn","stad"),
        ("Barneveld","stad"),("Zutphen","stad"),("Ede","stad"),("Wageningen","stad"),
        ("Arnhem","stad"),("Groenlo","stad"),("Doetinchem","stad"),("Winterswijk","stad"),
        ("Tiel","stad"),("Elst","stad"),("Zevenaar","stad"),("Nijmegen","stad"),
        ("Veluwe","streek"),("IJssel","water"),("Achterhoek","streek"),
        ("Betuwe","streek"),("Waal","water"),
    ]),
]

# Handmatige posities voor water/streek-labels (niet geocodeerbaar)
MANUAL = {
    1: {"Vecht":(37,47),"Salland":(35,61),"IJssel":(21,64),"Twente":(68,68)},
    2: {"Noordzee":(10,20),"Grevelingen":(62,24),"Oosterschelde":(50,36),
        "Walcheren":(20,44),"Zuid-Beveland":(38,50),"Schelde-Rijnkanaal":(72,52),
        "Westerschelde":(34,60),"Zeeuws-Vlaanderen":(35,74),"Kanaal Gent-Terneuzen":(38,77)},
    3: {"Lauwerssmeer":(20,22),"Waddenzee":(38,15),"Eemskanaal":(63,28),
        "Dollard":(84,30),"Reitdiep":(44,32)},
    4: {"IJsselmeer":(28,22),"Noordoost-polder":(72,22),"Markermeer":(28,38),
        "Oostelijk Flevoland":(65,43),"Veluwemeer":(70,51),"Zuidelijk Flevoland":(50,54),
        "Gooimeer":(37,56),"Amsterdam-Rijnkanaal":(32,75),"Neder-Rijn":(37,80)},
    5: {"De Peel":(60,43),"Juliana-kanaal":(67,71)},
    6: {"Westland":(17,50),"Rotterdam":(51,56),"Hoek van Holland":(28,53),
        "Haringvliet":(20,72),"Hollands Diep":(36,73),"Waal":(64,70)},
    7: {"Wieringermeer":(37,28),"Noordhollands kanaal":(21,37),"Beemster":(41,43),
        "Noordzeekanaal":(27,59),"IJmeer":(53,60),"Haarlemmermeer":(26,73),
        "Loosdrechtse Plassen":(50,76),"Het Gooi":(56,75)},
    8: {"Noordzee":(12,18),"Waddenzee":(28,35),"Sneekermeer":(50,59),
        "Gaasterland":(32,68),"IJsselmeer":(28,82)},
    9: {"Veluwe":(38,38),"IJssel":(60,35),"Achterhoek":(72,55),
        "Betuwe":(34,67),"Waal":(30,73)},
}

# ─── Verwerk elk les ──────────────────────────────────────────────────────────
print("Bouwen provinces.js...\n")
lessen_out = []

for (lid, titel, kleur, namen_img, blanco_img, plaatsen_def) in LESSEN_DEF:
    ocr_les = ocr_data.get(str(lid), {})
    all_texts = ocr_les.get("all_texts", [])

    # Bouw lookup: OCR-tekst → (x, y)  [niet meer direct gebruikt]
    ocr_lookup = {}
    for item in all_texts:
        ocr_lookup[item["text"]] = (item["x"], item["y"])

    plaatsen_out = []
    for (naam, ptype) in plaatsen_def:
        x, y = None, None
        bron = ""

        if ptype == "stad" or ptype == "eiland":
            # 1. Beste OCR-match (alle teksten, beste score wint)
            best_item, sc = best_ocr_match(all_texts, naam)
            if best_item:
                if ptype == "eiland":
                    # Eilandnaam staat als label OVER het eiland → gebruik midden
                    x = best_item["x"]
                else:
                    # Stad: op Geobas-kaarten staat de markerdot RECHTS van de naam ("Steenwijk*")
                    # x1 = rechter rand van de tekst-bounding-box = positie van de dot
                    x = best_item.get("x1", best_item["x"])
                y = best_item["y"]
                bron = f"OCR:'{best_item['text']}'(sc={sc:.2f})"

            # 2. Handmatige override (voor bekende OCR-fouten)
            if x is None:
                m = MANUAL.get(lid, {})
                if naam in m:
                    x, y = m[naam]
                    bron = "MANUAL"

            # 3. Fallback: geografische coördinaten
            if x is None and naam in COORDS:
                lat, lon = COORDS[naam]
                x, y = geo_to_img(lat, lon, lid)
                bron = "GEO"
        else:
            # Water/streek: gebruik handmatige posities
            m = MANUAL.get(lid, {})
            if naam in m:
                x, y = m[naam]
                bron = "MANUAL"
            elif naam in COORDS:
                lat, lon = COORDS[naam]
                x, y = geo_to_img(lat, lon, lid)
                bron = "GEO"

        if x is None:
            x, y = 50, 50
            bron = "FALLBACK"

        print(f"  Les{lid} {naam:30s} x={x:5.1f}  y={y:5.1f}  [{bron}]")
        plaatsen_out.append({
            "naam": naam, "x": round(float(x),1),
            "y": round(float(y),1), "type": ptype
        })

    lessen_out.append({
        "id": lid, "titel": titel, "kleur": kleur,
        "afbeeldingNamen": namen_img, "afbeeldingBlanco": blanco_img,
        "plaatsen": plaatsen_out
    })

# ─── Schrijf provinces.js ─────────────────────────────────────────────────────
def write_js(lessen, path):
    lines = [
        "// Geobas Groep 6 — coördinaten uit OCR op kaartafbeeldingen + geografische backup",
        "// type: 'stad' | 'water' | 'streek' | 'eiland'",
        "",
        "export const lessen = ["
    ]
    for les in lessen:
        lines.append("  {")
        lines.append(f"    id: {les['id']},")
        lines.append(f"    titel: \"{les['titel']}\",")
        lines.append(f"    afbeeldingNamen: \"{les['afbeeldingNamen']}\",")
        lines.append(f"    afbeeldingBlanco: \"{les['afbeeldingBlanco']}\",")
        lines.append(f"    kleur: \"{les['kleur']}\",")
        lines.append("    plaatsen: [")
        for p in les["plaatsen"]:
            n = p["naam"].replace('"', '\\"')
            lines.append(f"      {{ naam: \"{n}\", x: {p['x']}, y: {p['y']}, type: \"{p['type']}\" }},")
        lines.append("    ]")
        lines.append("  },")
    lines.append("];")
    lines.append("")
    lines.append("export const getLes = (id) => lessen.find(l => l.id === id);")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nGeschreven: {path}")

out = r"C:\Software\Topografiekaart_6\app\src\data\provinces.js"
write_js(lessen_out, out)
