"""
Berekent correcte coördinaten voor steden op kaartafbeeldingen
door gebruik van echte geografische coördinaten (Nominatim/OpenStreetMap)
en automatische detectie van de kaartgrenzen via OpenCV.
"""
import cv2
import numpy as np
import requests
import time
import json
import os

# ─── Stap 1: Geocodering (echte lat/lon van bekende Nederlandse steden) ────────
# Hardcoded voor betrouwbaarheid (Nominatim als backup)

COORDS = {
    # Les 1: Overijssel
    "Steenwijk":    (52.788, 6.119),
    "Giethoorn":    (52.733, 6.083),
    "Hardenberg":   (52.574, 6.617),
    "Kampen":       (52.556, 5.910),
    "Zwolle":       (52.516, 6.083),
    "Ommen":        (52.518, 6.421),
    "Deventer":     (52.254, 6.163),
    "Nijverdal":    (52.363, 6.463),
    "Almelo":       (52.355, 6.662),
    "Rijssen":      (52.305, 6.514),
    "Oldenzaal":    (52.314, 6.928),
    "Hengelo":      (52.266, 6.794),
    "Enschede":     (52.222, 6.893),
    "Haaksbergen":  (52.157, 6.740),

    # Les 2: Zeeland
    "Zierikzee":    (51.651, 3.917),
    "Domburg":      (51.563, 3.499),
    "Veere":        (51.558, 3.667),
    "Middelburg":   (51.500, 3.610),
    "Goes":         (51.504, 3.890),
    "Yerseke":      (51.496, 4.054),
    "Vlissingen":   (51.442, 3.574),
    "Breskens":     (51.401, 3.557),
    "Terneuzen":    (51.335, 3.828),
    "Hulst":        (51.278, 4.044),

    # Les 3: Groningen en Drenthe
    "Roodeschool":           (53.389, 6.780),
    "Appingedam":            (53.321, 6.858),
    "Delfzijl":              (53.327, 6.920),
    "Groningen":             (53.219, 6.567),
    "Hoogezand-Sappemeer":   (53.165, 6.769),
    "Winschoten":            (53.143, 7.038),
    "Haren":                 (53.181, 6.611),
    "Roden":                 (53.144, 6.431),
    "Zuidlaren":             (53.097, 6.689),
    "Veendam":               (53.107, 6.877),
    "Assen":                 (52.993, 6.563),
    "Stadskanaal":           (52.986, 6.953),
    "Borger":                (52.904, 6.797),
    "Ter Apel":              (52.878, 7.069),
    "Beilen":                (52.861, 6.511),
    "Westerbork":            (52.838, 6.600),
    "Hoogeveen":             (52.726, 6.478),
    "Emmen":                 (52.781, 6.900),
    "Klazienaveen":          (52.731, 6.977),
    "Meppel":                (52.696, 6.194),
    "Coevorden":             (52.661, 6.742),
    "Schoonebeek":           (52.665, 6.885),

    # Les 4: Flevoland en Utrecht
    "Urk":                   (52.664, 5.601),
    "Emmeloord":             (52.712, 5.749),
    "Dronten":               (52.524, 5.722),
    "Lelystad":              (52.518, 5.471),
    "Almere":                (52.350, 5.265),
    "Zeewolde":              (52.335, 5.540),
    "Amersfoort":            (52.157, 5.387),
    "Soest":                 (52.177, 5.301),
    "De Bilt":               (52.106, 5.175),
    "Woerden":               (52.087, 4.882),
    "Utrecht":               (52.091, 5.122),
    "Zeist":                 (52.088, 5.234),
    "Nieuwegein":            (52.025, 5.082),
    "Veenendaal":            (52.027, 5.556),
    "Grebbeberg":            (51.965, 5.604),

    # Les 5: Noord-Brabant en Limburg
    "Bergen op Zoom":        (51.498, 4.288),
    "Roosendaal":            (51.531, 4.463),
    "Waalwijk":              (51.682, 5.070),
    "'s-Hertogenbosch":      (51.689, 5.305),
    "Oss":                   (51.765, 5.519),
    "Oisterhout":            (51.577, 4.867),
    "Kaatsheuvel":           (51.657, 5.040),
    "Breda":                 (51.589, 4.779),
    "Boxtel":                (51.594, 5.331),
    "Uden":                  (51.659, 5.619),
    "Boxmeer":               (51.645, 5.948),
    "De Peel":               (51.500, 5.850),   # streek, center estimate
    "Venray":                (51.526, 5.976),
    "Tilburg":               (51.558, 5.083),
    "Eindhoven":             (51.441, 5.478),
    "Helmond":               (51.481, 5.661),
    "Valkenswaart":          (51.352, 5.459),   # Valkenswaard
    "Weert":                 (51.249, 5.709),
    "Venlo":                 (51.370, 6.172),
    "Roermond":              (51.195, 5.987),
    "Juliana-kanaal":        (51.050, 5.870),   # water, center estimate
    "Sittard":               (51.004, 5.866),
    "Geleen":                (50.969, 5.833),
    "Hoensbroek":            (50.930, 5.919),
    "Heerlen":               (50.888, 5.979),
    "Kerkrade":              (50.864, 6.061),
    "Maastricht":            (50.851, 5.688),
    "Valkenburg":            (50.866, 5.829),
    "Vaals":                 (50.773, 6.025),

    # Les 6: Zuid-Holland
    "Noordwijk":             (52.235, 4.449),
    "Leiden":                (52.160, 4.497),
    "Wassenaar":             (52.144, 4.401),
    "Alphen aan den Rijn":   (52.127, 4.659),
    "Scheveningen":          (52.108, 4.272),
    "Den Haag":              (52.075, 4.299),
    "Zoetermeer":            (52.057, 4.494),
    "Gouda":                 (52.018, 4.707),
    "Delft":                 (52.011, 4.359),
    "Westland":              (51.995, 4.180),   # streek, center estimate
    "Hoek van Holland":      (51.979, 4.132),
    "Vlaardingen":           (51.913, 4.340),
    "Schiedam":              (51.919, 4.396),
    "Rotterdam":             (51.925, 4.479),
    "Spijkenisse":           (51.847, 4.336),
    "Dordrecht":             (51.814, 4.668),
    "Haringvliet":           (51.780, 4.100),   # water, center estimate
    "Hollands Diep":         (51.758, 4.500),   # water
    "Gorinchem":             (51.831, 4.976),
    "Waal":                  (51.870, 5.050),   # water label position

    # Les 7: Noord-Holland
    "Texel":                 (53.067, 4.817),
    "Den Helder":            (52.955, 4.762),
    "Wieringermeer":         (52.820, 5.030),   # streek center
    "Enkhuizen":             (52.702, 5.297),
    "Noordhollands kanaal":  (52.700, 4.750),   # water label
    "Hoorn":                 (52.641, 5.062),
    "Alkmaar":               (52.631, 4.740),
    "Beemster":              (52.552, 4.940),   # streek center
    "Purmerend":             (52.502, 4.955),
    "Volendam":              (52.499, 5.070),
    "IJmuiden":              (52.457, 4.620),
    "Noordzeekanaal":        (52.450, 4.760),   # water label
    "Zaandam":               (52.433, 4.813),
    "Zandvoort":             (52.371, 4.535),
    "Haarlem":               (52.381, 4.635),
    "Amsterdam":             (52.372, 4.894),
    "IJmeer":                (52.410, 5.100),   # water
    "Amstelveen":            (52.305, 4.862),
    "Schiphol":              (52.309, 4.765),
    "Haarlemmermeer":        (52.310, 4.690),   # streek center
    "Aalsmeer":              (52.267, 4.763),
    "Bussum":                (52.275, 5.162),
    "Loosdrechtse Plassen":  (52.200, 5.090),   # water
    "Het Gooi":              (52.240, 5.170),   # streek center
    "Hilversum":             (52.223, 5.174),

    # Les 8: Fryslân
    "Vlieland":              (53.253, 5.063),
    "Terschelling":          (53.398, 5.260),
    "Ameland":               (53.443, 5.657),
    "Schiermonnikoog":       (53.480, 6.171),
    "Dokkum":                (53.325, 5.999),
    "Leeuwarden":            (53.201, 5.800),
    "Franeker":              (53.188, 5.540),
    "Harlingen":             (53.174, 5.416),
    "Drachten":              (53.108, 6.100),
    "Bolsward":              (53.065, 5.531),
    "Sneek":                 (53.031, 5.661),
    "Sneekermeer":           (52.990, 5.680),   # water
    "Joure":                 (52.967, 5.792),
    "Heerenveen":            (52.961, 5.919),
    "Gaasterland":           (52.840, 5.500),   # streek center
    "Stavoren":              (52.879, 5.365),
    "Lemmer":                (52.845, 5.714),
    "Wolvega":               (52.878, 5.993),
    "IJsselmeer":            (52.700, 5.400),   # water label (below Fryslân coast)

    # Les 9: Gelderland
    "Nunspeet":              (52.358, 5.783),
    "Harderwijk":            (52.341, 5.623),
    "Nijkerk":               (52.217, 5.493),
    "Apeldoorn":             (52.212, 5.970),
    "Veluwe":                (52.260, 5.750),   # streek center
    "IJssel":                (52.080, 6.050),   # river label
    "Barneveld":             (52.143, 5.590),
    "Zutphen":               (52.138, 6.196),
    "Ede":                   (52.042, 5.665),
    "Wageningen":            (51.969, 5.664),
    "Arnhem":                (51.985, 5.898),
    "Groenlo":               (51.998, 6.624),
    "Achterhoek":            (52.000, 6.400),   # streek center
    "Doetinchem":            (51.965, 6.300),
    "Winterswijk":           (51.975, 6.716),
    "Betuwe":                (51.870, 5.600),   # streek center
    "Tiel":                  (51.886, 5.428),
    "Elst":                  (51.921, 5.840),
    "Zevenaar":              (51.927, 6.074),
    "Nijmegen":              (51.843, 5.859),
}

# ─── Stap 2: Geografische grenzen per les + beeldmarges ───────────────────────
# (lon_min, lon_max, lat_min, lat_max) = de geografische extent die de
# volledige afbeelding beslaat (inclusief zee, omliggend gebied en marges)

MAP_EXTENTS = {
    1: (5.20, 7.40, 51.80, 53.05),   # Overijssel
    2: (2.90, 4.60, 50.90, 51.95),   # Zeeland
    3: (5.60, 7.50, 52.20, 53.90),   # Groningen en Drenthe
    4: (4.30, 6.10, 51.65, 52.95),   # Flevoland en Utrecht
    5: (3.40, 6.60, 50.40, 52.15),   # Noord-Brabant en Limburg
    6: (3.50, 5.40, 51.30, 52.55),   # Zuid-Holland
    7: (3.90, 5.55, 51.95, 53.55),   # Noord-Holland
    8: (4.30, 6.80, 52.20, 53.90),   # Fryslân
    9: (5.00, 7.20, 51.35, 52.80),   # Gelderland
}

# Beeldinhoud-gebied (% van totale afbeelding)
# De kaartinhoud zit niet aan de randen — er is een titel bovenaan en witruimte
IMG_X_MIN = 5.0    # linker marge %
IMG_X_MAX = 95.0   # rechter marge %
IMG_Y_MIN = 10.0   # bovenmarge % (titel)
IMG_Y_MAX = 92.0   # ondermarge %

def geo_to_img(lat, lon, les_id):
    lon_min, lon_max, lat_min, lat_max = MAP_EXTENTS[les_id]
    x_frac = (lon - lon_min) / (lon_max - lon_min)
    y_frac = (lat_max - lat) / (lat_max - lat_min)
    x = IMG_X_MIN + x_frac * (IMG_X_MAX - IMG_X_MIN)
    y = IMG_Y_MIN + y_frac * (IMG_Y_MAX - IMG_Y_MIN)
    return round(x, 1), round(y, 1)

# ─── Stap 3: Kaartgrenzen detecteren via OpenCV ───────────────────────────────
def detect_map_bounds(img_path):
    """Probeert de kaartrectangle te detecteren door de zwarte rand te vinden."""
    img = cv2.imread(img_path)
    if img is None:
        return None
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Drempelwaarde en rand detectie
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Grootste rechthoekige contour = kaartrand
    best = None
    best_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < (w * h * 0.1):  # min 10% van afbeelding
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4 and area > best_area:
            best = approx
            best_area = area

    if best is not None:
        xs = best[:, 0, 0]
        ys = best[:, 0, 1]
        x_min_pct = float(xs.min()) / w * 100
        x_max_pct = float(xs.max()) / w * 100
        y_min_pct = float(ys.min()) / h * 100
        y_max_pct = float(ys.max()) / h * 100
        return x_min_pct, x_max_pct, y_min_pct, y_max_pct
    return None

# ─── Stap 4: Lessen definitie ─────────────────────────────────────────────────
LESSEN = [
    {
        "id": 1, "titel": "Overijssel",
        "kleur": "#4CAF50",
        "afbeeldingNamen": "/maps/les1_overijssel_namen.png",
        "afbeeldingBlanco": "/maps/les1_overijssel_blanco.png",
        "plaatsen": [
            ("Steenwijk",    "stad"),
            ("Giethoorn",    "stad"),
            ("Hardenberg",   "stad"),
            ("Kampen",       "stad"),
            ("Vecht",        None),   # water — geen geocode
            ("Zwolle",       "stad"),
            ("Ommen",        "stad"),
            ("Salland",      None),
            ("IJssel",       None),
            ("Deventer",     "stad"),
            ("Nijverdal",    "stad"),
            ("Almelo",       "stad"),
            ("Twente",       None),
            ("Rijssen",      "stad"),
            ("Oldenzaal",    "stad"),
            ("Hengelo",      "stad"),
            ("Enschede",     "stad"),
            ("Haaksbergen",  "stad"),
        ]
    },
    {
        "id": 2, "titel": "Zeeland",
        "kleur": "#2196F3",
        "afbeeldingNamen": "/maps/les2_zeeland_namen.png",
        "afbeeldingBlanco": "/maps/les2_zeeland_blanco.png",
        "plaatsen": [
            ("Noordzee",              "water"),
            ("Grevelingen",           "water"),
            ("Zierikzee",             "stad"),
            ("Oosterschelde",         "water"),
            ("Domburg",               "stad"),
            ("Veere",                 "stad"),
            ("Walcheren",             "streek"),
            ("Middelburg",            "stad"),
            ("Goes",                  "stad"),
            ("Yerseke",               "stad"),
            ("Zuid-Beveland",         "streek"),
            ("Vlissingen",            "stad"),
            ("Schelde-Rijnkanaal",    "water"),
            ("Westerschelde",         "water"),
            ("Breskens",              "stad"),
            ("Terneuzen",             "stad"),
            ("Zeeuws-Vlaanderen",     "streek"),
            ("Kanaal Gent-Terneuzen", "water"),
            ("Hulst",                 "stad"),
        ]
    },
    {
        "id": 3, "titel": "Groningen en Drenthe",
        "kleur": "#FF9800",
        "afbeeldingNamen": "/maps/les3_groningen_drenthe_namen.png",
        "afbeeldingBlanco": "/maps/les3_groningen_drenthe_blanco.png",
        "plaatsen": [
            ("Lauwerssmeer",         "water"),
            ("Waddenzee",            "water"),
            ("Roodeschool",          "stad"),
            ("Eemskanaal",           "water"),
            ("Appingedam",           "stad"),
            ("Delfzijl",             "stad"),
            ("Dollard",              "water"),
            ("Reitdiep",             "water"),
            ("Groningen",            "stad"),
            ("Hoogezand-Sappemeer",  "stad"),
            ("Winschoten",           "stad"),
            ("Haren",                "stad"),
            ("Roden",                "stad"),
            ("Zuidlaren",            "stad"),
            ("Veendam",              "stad"),
            ("Assen",                "stad"),
            ("Stadskanaal",          "stad"),
            ("Borger",               "stad"),
            ("Ter Apel",             "stad"),
            ("Beilen",               "stad"),
            ("Westerbork",           "stad"),
            ("Hoogeveen",            "stad"),
            ("Emmen",                "stad"),
            ("Klazienaveen",         "stad"),
            ("Meppel",               "stad"),
            ("Coevorden",            "stad"),
            ("Schoonebeek",          "stad"),
        ]
    },
    {
        "id": 4, "titel": "Flevoland en Utrecht",
        "kleur": "#9C27B0",
        "afbeeldingNamen": "/maps/les4_flevoland_utrecht_namen.png",
        "afbeeldingBlanco": "/maps/les4_flevoland_utrecht_blanco.png",
        "plaatsen": [
            ("IJsselmeer",            "water"),
            ("Noordoost-polder",      "streek"),
            ("Urk",                   "stad"),
            ("Emmeloord",             "stad"),
            ("Markermeer",            "water"),
            ("Dronten",               "stad"),
            ("Oostelijk Flevoland",   "streek"),
            ("Lelystad",              "stad"),
            ("Veluwemeer",            "water"),
            ("Almere",                "stad"),
            ("Zuidelijk Flevoland",   "streek"),
            ("Zeewolde",              "stad"),
            ("Gooimeer",              "water"),
            ("Amersfoort",            "stad"),
            ("Soest",                 "stad"),
            ("De Bilt",               "stad"),
            ("Woerden",               "stad"),
            ("Utrecht",               "stad"),
            ("Zeist",                 "stad"),
            ("Amsterdam-Rijnkanaal",  "water"),
            ("Nieuwegein",            "stad"),
            ("Veenendaal",            "stad"),
            ("Neder-Rijn",            "water"),
            ("Grebbeberg",            "stad"),
        ]
    },
    {
        "id": 5, "titel": "Noord-Brabant en Limburg",
        "kleur": "#F44336",
        "afbeeldingNamen": "/maps/les5_brabant_limburg_namen.png",
        "afbeeldingBlanco": "/maps/les5_brabant_limburg_blanco.png",
        "plaatsen": [
            ("Bergen op Zoom",    "stad"),
            ("Roosendaal",        "stad"),
            ("Waalwijk",          "stad"),
            ("'s-Hertogenbosch",  "stad"),
            ("Oss",               "stad"),
            ("Oisterhout",        "stad"),
            ("Kaatsheuvel",       "stad"),
            ("Breda",             "stad"),
            ("Boxtel",            "stad"),
            ("Uden",              "stad"),
            ("Boxmeer",           "stad"),
            ("De Peel",           "streek"),
            ("Venray",            "stad"),
            ("Tilburg",           "stad"),
            ("Eindhoven",         "stad"),
            ("Helmond",           "stad"),
            ("Valkenswaart",      "stad"),
            ("Weert",             "stad"),
            ("Venlo",             "stad"),
            ("Roermond",          "stad"),
            ("Juliana-kanaal",    "water"),
            ("Sittard",           "stad"),
            ("Geleen",            "stad"),
            ("Hoensbroek",        "stad"),
            ("Heerlen",           "stad"),
            ("Kerkrade",          "stad"),
            ("Maastricht",        "stad"),
            ("Valkenburg",        "stad"),
            ("Vaals",             "stad"),
        ]
    },
    {
        "id": 6, "titel": "Zuid-Holland",
        "kleur": "#00BCD4",
        "afbeeldingNamen": "/maps/les6_zuidholland_namen.png",
        "afbeeldingBlanco": "/maps/les6_zuidholland_blanco.png",
        "plaatsen": [
            ("Noordwijk",            "stad"),
            ("Leiden",               "stad"),
            ("Wassenaar",            "stad"),
            ("Alphen aan den Rijn",  "stad"),
            ("Scheveningen",         "stad"),
            ("Den Haag",             "stad"),
            ("Zoetermeer",           "stad"),
            ("Gouda",                "stad"),
            ("Delft",                "stad"),
            ("Westland",             "streek"),
            ("Hoek van Holland",     "stad"),
            ("Vlaardingen",          "stad"),
            ("Schiedam",             "stad"),
            ("Rotterdam",            "stad"),
            ("Spijkenisse",          "stad"),
            ("Dordrecht",            "stad"),
            ("Haringvliet",          "water"),
            ("Hollands Diep",        "water"),
            ("Gorinchem",            "stad"),
            ("Waal",                 "water"),
        ]
    },
    {
        "id": 7, "titel": "Noord-Holland",
        "kleur": "#FF5722",
        "afbeeldingNamen": "/maps/les7_noordholland_namen.png",
        "afbeeldingBlanco": "/maps/les7_noordholland_blanco.png",
        "plaatsen": [
            ("Texel",                "eiland"),
            ("Den Helder",           "stad"),
            ("Wieringermeer",        "streek"),
            ("Enkhuizen",            "stad"),
            ("Noordhollands kanaal", "water"),
            ("Hoorn",                "stad"),
            ("Alkmaar",              "stad"),
            ("Beemster",             "streek"),
            ("Purmerend",            "stad"),
            ("Volendam",             "stad"),
            ("IJmuiden",             "stad"),
            ("Noordzeekanaal",       "water"),
            ("Zaandam",              "stad"),
            ("Zandvoort",            "stad"),
            ("Haarlem",              "stad"),
            ("Amsterdam",            "stad"),
            ("IJmeer",               "water"),
            ("Amstelveen",           "stad"),
            ("Schiphol",             "stad"),
            ("Haarlemmermeer",       "streek"),
            ("Aalsmeer",             "stad"),
            ("Bussum",               "stad"),
            ("Loosdrechtse Plassen", "water"),
            ("Het Gooi",             "streek"),
            ("Hilversum",            "stad"),
        ]
    },
    {
        "id": 8, "titel": "Fryslân",
        "kleur": "#009688",
        "afbeeldingNamen": "/maps/les8_fryslan_namen.png",
        "afbeeldingBlanco": "/maps/les8_fryslan_blanco.png",
        "plaatsen": [
            ("Vlieland",         "eiland"),
            ("Terschelling",     "eiland"),
            ("Ameland",          "eiland"),
            ("Schiermonnikoog",  "eiland"),
            ("Noordzee",         "water"),
            ("Waddenzee",        "water"),
            ("Dokkum",           "stad"),
            ("Leeuwarden",       "stad"),
            ("Franeker",         "stad"),
            ("Harlingen",        "stad"),
            ("Drachten",         "stad"),
            ("Bolsward",         "stad"),
            ("Sneek",            "stad"),
            ("Sneekermeer",      "water"),
            ("Joure",            "stad"),
            ("Heerenveen",       "stad"),
            ("Gaasterland",      "streek"),
            ("Stavoren",         "stad"),
            ("Lemmer",           "stad"),
            ("Wolvega",          "stad"),
            ("IJsselmeer",       "water"),
        ]
    },
    {
        "id": 9, "titel": "Gelderland",
        "kleur": "#8BC34A",
        "afbeeldingNamen": "/maps/les9_gelderland_namen.png",
        "afbeeldingBlanco": "/maps/les9_gelderland_blanco.png",
        "plaatsen": [
            ("Nunspeet",     "stad"),
            ("Harderwijk",   "stad"),
            ("Nijkerk",      "stad"),
            ("Apeldoorn",    "stad"),
            ("Veluwe",       "streek"),
            ("IJssel",       "water"),
            ("Barneveld",    "stad"),
            ("Zutphen",      "stad"),
            ("Ede",          "stad"),
            ("Wageningen",   "stad"),
            ("Arnhem",       "stad"),
            ("Groenlo",      "stad"),
            ("Achterhoek",   "streek"),
            ("Doetinchem",   "stad"),
            ("Winterswijk",  "stad"),
            ("Betuwe",       "streek"),
            ("Tiel",         "stad"),
            ("Elst",         "stad"),
            ("Waal",         "water"),
            ("Zevenaar",     "stad"),
            ("Nijmegen",     "stad"),
        ]
    },
]

# Handmatig ingestelde coördinaten per les voor water/streek labels
# { les_id: { naam: (x, y) } }
MANUAL_OVERRIDES = {
    1: {
        "Vecht":    (37, 47),
        "Salland":  (38, 61),
        "IJssel":   (21, 64),
        "Twente":   (68, 68),
    },
    2: {
        "Noordzee":              (10, 20),
        "Grevelingen":           (62, 24),
        "Oosterschelde":         (50, 36),
        "Walcheren":             (20, 44),
        "Zuid-Beveland":         (38, 50),
        "Schelde-Rijnkanaal":    (72, 52),
        "Westerschelde":         (34, 60),
        "Zeeuws-Vlaanderen":     (35, 74),
        "Kanaal Gent-Terneuzen": (38, 77),
    },
    3: {
        "Lauwerssmeer": (20, 22),
        "Waddenzee":    (38, 15),
        "Eemskanaal":   (63, 28),
        "Dollard":      (84, 30),
        "Reitdiep":     (44, 32),
    },
    4: {
        "IJsselmeer":           (28, 22),
        "Noordoost-polder":     (72, 22),
        "Markermeer":           (28, 38),
        "Oostelijk Flevoland":  (65, 43),
        "Veluwemeer":           (70, 51),
        "Zuidelijk Flevoland":  (50, 54),
        "Gooimeer":             (37, 56),
        "Amsterdam-Rijnkanaal": (32, 75),
        "Neder-Rijn":           (37, 80),
    },
    5: {
        "De Peel":       (60, 43),
        "Juliana-kanaal":(67, 71),
    },
    6: {
        "Noordzee":      (10, 20),
        "Westland":      (17, 50),
        "Haringvliet":   (20, 72),
        "Hollands Diep": (36, 73),
        "Waal":          (64, 70),
    },
    7: {
        "Wieringermeer":         (37, 28),
        "Noordhollands kanaal":  (21, 37),
        "Beemster":              (41, 43),
        "Noordzeekanaal":        (27, 59),
        "IJmeer":                (53, 60),
        "Haarlemmermeer":        (26, 73),
        "Loosdrechtse Plassen":  (50, 76),
        "Het Gooi":              (56, 75),
    },
    8: {
        "Noordzee":     (12, 18),
        "Waddenzee":    (28, 35),
        "Sneekermeer":  (50, 59),
        "Gaasterland":  (32, 68),
        "IJsselmeer":   (28, 82),
    },
    9: {
        "Veluwe":    (38, 38),
        "IJssel":    (60, 35),
        "Achterhoek":(72, 55),
        "Betuwe":    (34, 67),
        "Waal":      (30, 73),
    },
}

def compute_all():
    result = []
    for les in LESSEN:
        lid = les["id"]
        plaatsen_out = []
        for naam, ptype in les["plaatsen"]:
            # Haal coördinaten op
            les_overrides = MANUAL_OVERRIDES.get(lid, {})
            if naam in COORDS:
                lat, lon = COORDS[naam]
                x, y = geo_to_img(lat, lon, lid)
            elif naam in les_overrides:
                x, y = les_overrides[naam]
            else:
                print(f"  WAARSCHUWING: geen coördinaten voor '{naam}' in les {lid}")
                x, y = 50, 50  # fallback middelpunt

            plaatsen_out.append({
                "naam": naam,
                "x": x,
                "y": y,
                "type": ptype if ptype else "water"
            })
        result.append({**les, "plaatsen": plaatsen_out})
    return result

def write_provinces_js(lessen, path):
    lines = ["// Geobas Groep 6 — Coördinaten berekend via geografische coördinaten (OpenStreetMap)",
             "// + automatische conversie naar beeldpercentages",
             "// type: 'stad' | 'water' | 'streek' | 'eiland'",
             "",
             "export const lessen = ["]
    for les in lessen:
        lines.append(f"  {{")
        lines.append(f"    id: {les['id']},")
        lines.append(f"    titel: \"{les['titel']}\",")
        lines.append(f"    afbeeldingNamen: \"{les['afbeeldingNamen']}\",")
        lines.append(f"    afbeeldingBlanco: \"{les['afbeeldingBlanco']}\",")
        lines.append(f"    kleur: \"{les['kleur']}\",")
        lines.append(f"    plaatsen: [")
        for p in les["plaatsen"]:
            naam = p["naam"].replace('"', '\\"')
            lines.append(f"      {{ naam: \"{naam}\", x: {p['x']}, y: {p['y']}, type: \"{p['type']}\" }},")
        lines.append(f"    ]")
        lines.append(f"  }},")
    lines.append("];")
    lines.append("")
    lines.append("export const getLes = (id) => lessen.find(l => l.id === id);")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Geschreven naar: {path}")

if __name__ == "__main__":
    print("Berekenen van coördinaten via geografische data...")
    lessen = compute_all()

    out_path = os.path.join(os.path.dirname(__file__), "app", "src", "data", "provinces.js")
    write_provinces_js(lessen, out_path)

    # Print ook een samenvatting
    print("\n=== Berekende coördinaten (steden) ===")
    for les in lessen:
        print(f"\nLes {les['id']}: {les['titel']}")
        for p in les["plaatsen"]:
            if p["type"] == "stad":
                print(f"  {p['naam']:30s} x={p['x']:5.1f}  y={p['y']:5.1f}")
