"""
Genereert educatieve provincie-kaarten voor Geobas Groep 6.
Gebruikt echte provinciegrenzen van cartomap.github.io/nl (provincies.geojson).
Stipposities en kaartafbeeldingen gebruiken EXACT dezelfde projectie
zodat dots altijd op de juiste plek staan.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon as MplPoly
import numpy as np
import math, os, json

OUTPUT_DIR = r"C:\Software\Topografiekaart_6\app\public\maps"
GEOJSON    = r"C:\Software\Topografiekaart_6\provincies.geojson"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Laad echte provinciegrenzen ─────────────────────────────────────────────
with open(GEOJSON, encoding="utf-8") as f:
    _geo = json.load(f)

PROV_GEOM = {}
for feat in _geo["features"]:
    naam = feat["properties"]["statnaam"]
    if "Frys" in naam:
        naam = "Friesland"
    PROV_GEOM[naam] = feat["geometry"]

def teken_provincie(ax, naam, facecolor, edgecolor, linewidth, alpha, zorder=2):
    geom = PROV_GEOM.get(naam)
    if geom is None:
        return
    gtype = geom["type"]
    coords = geom["coordinates"]
    # Normaliseer naar lijst van polygons (elk = lijst van ringen)
    if gtype == "Polygon":
        polygons = [coords]           # één polygon
    else:  # MultiPolygon
        polygons = coords

    for polygon in polygons:
        outer = polygon[0]            # buitenste ring = lijst van [lon, lat] punten
        xs = [p[0] for p in outer]
        ys = [p[1] for p in outer]
        poly = MplPoly(list(zip(xs, ys)), closed=True,
                       facecolor=facecolor, edgecolor=edgecolor,
                       linewidth=linewidth, alpha=alpha, zorder=zorder)
        ax.add_patch(poly)

# ─── Kleuren ─────────────────────────────────────────────────────────────────
PROV_KLEUR = {
  "Groningen":"#FFE0B2","Drenthe":"#FFE0B2","Friesland":"#E0F2F1",
  "Overijssel":"#E8F5E9","Flevoland":"#EDE7F6","Gelderland":"#F1F8E9",
  "Utrecht":"#EDE7F6","Noord-Holland":"#FBE9E7","Zuid-Holland":"#E0F7FA",
  "Zeeland":"#E3F2FD","Noord-Brabant":"#FFEBEE","Limburg":"#FFEBEE",
}
BUUR_KLEUR = "#e8e8e8"
ZEE_KLEUR  = "#b8d4e8"
HOOFD_RAND = "#1a237e"
BUUR_RAND  = "#90A4AE"

# ─── Lessen definitie ─────────────────────────────────────────────────────────
LESSEN = [
  { "id":1, "titel":"Overijssel", "kleur":"#4CAF50",
    "hoofdprov":["Overijssel"],
    "buurprov":["Drenthe","Flevoland","Gelderland"],
    "extent":(5.55,7.15,51.95,52.92),
    "steden":[
      ("Steenwijk",52.788,6.119),("Giethoorn",52.733,6.083),
      ("Hardenberg",52.574,6.617),("Kampen",52.556,5.910),
      ("Zwolle",52.516,6.083),("Ommen",52.518,6.421),
      ("Deventer",52.254,6.163),("Nijverdal",52.363,6.463),
      ("Almelo",52.355,6.662),("Rijssen",52.305,6.514),
      ("Oldenzaal",52.314,6.928),("Hengelo",52.266,6.794),
      ("Enschede",52.222,6.893),("Haaksbergen",52.157,6.740),
    ],
    "water":[
      ("IJssel",52.38,6.07),("Vecht",52.47,6.28),
      ("Regge",52.26,6.56),("Dinkel",52.28,6.91),
      ("Zwarte Water",52.57,6.06),("Ketelmeer",52.61,5.78),
    ],
    "streek":[
      ("Salland",52.42,6.25),("Twente",52.27,6.72),
      ("Vechtdal",52.52,6.40),("Noordwest Overijssel",52.75,6.05),
    ],
  },
  { "id":2, "titel":"Zeeland", "kleur":"#2196F3",
    "hoofdprov":["Zeeland"],
    "buurprov":["Zuid-Holland","Noord-Brabant"],
    "extent":(3.32,4.32,51.12,51.88),
    "steden":[
      ("Zierikzee",51.651,3.917),("Domburg",51.563,3.499),
      ("Veere",51.558,3.667),("Middelburg",51.500,3.610),
      ("Goes",51.504,3.890),("Yerseke",51.496,4.054),
      ("Vlissingen",51.442,3.574),("Breskens",51.401,3.557),
      ("Terneuzen",51.335,3.828),("Hulst",51.278,4.044),
    ],
    "water":[
      ("Noordzee",51.72,3.42),("Westerschelde",51.40,3.75),
      ("Oosterschelde",51.60,4.00),("Grevelingen",51.75,3.93),
      ("Veerse Meer",51.56,3.76),("Volkerak",51.66,4.21),
      ("Schelde",51.36,4.05),
    ],
    "streek":[
      ("Walcheren",51.53,3.58),("Zuid-Beveland",51.48,3.85),
      ("Noord-Beveland",51.58,3.77),
      ("Schouwen-Duiveland",51.67,3.82),
      ("Zeeuws-Vlaanderen",51.30,3.82),
    ],
  },
  { "id":3, "titel":"Groningen en Drenthe", "kleur":"#FF9800",
    "hoofdprov":["Groningen","Drenthe"],
    "buurprov":["Friesland","Overijssel"],
    "extent":(5.90,7.25,52.45,53.68),
    "steden":[
      ("Roodeschool",53.389,6.780),("Appingedam",53.321,6.858),
      ("Delfzijl",53.327,6.920),("Groningen",53.219,6.567),
      ("Hoogezand-Sappemeer",53.165,6.769),("Winschoten",53.143,7.038),
      ("Haren",53.181,6.611),("Roden",53.144,6.431),
      ("Zuidlaren",53.097,6.689),("Veendam",53.107,6.877),
      ("Assen",52.993,6.563),("Stadskanaal",52.986,6.953),
      ("Borger",52.904,6.797),("Ter Apel",52.878,7.069),
      ("Beilen",52.861,6.511),("Westerbork",52.838,6.600),
      ("Hoogeveen",52.726,6.478),("Emmen",52.781,6.900),
      ("Klazienaveen",52.731,6.977),("Meppel",52.696,6.194),
      ("Coevorden",52.661,6.742),("Schoonebeek",52.665,6.885),
    ],
    "water":[
      ("Waddenzee",53.54,6.20),("Lauwerssmeer",53.37,6.22),
      ("Dollard",53.27,7.13),("Eemskanaal",53.28,6.87),
      ("Van Starkenborghkanaal",53.17,6.63),
      ("Hunze",52.85,6.75),("Drentsche Aa",53.06,6.53),
      ("Zuidlaardermeer",53.10,6.70),
    ],
    "streek":[
      ("Hondsrug",52.88,6.63),("Veenkoloniën",52.98,6.93),
      ("Drentse Aa-dal",53.06,6.50),("Borger-Odoorn",52.90,6.85),
    ],
  },
  { "id":4, "titel":"Flevoland en Utrecht", "kleur":"#9C27B0",
    "hoofdprov":["Flevoland","Utrecht"],
    "buurprov":["Noord-Holland","Gelderland","Zuid-Holland","Overijssel","Friesland"],
    "extent":(4.62,5.95,51.82,52.92),
    "steden":[
      ("Urk",52.664,5.601),("Emmeloord",52.712,5.749),
      ("Dronten",52.524,5.722),("Lelystad",52.518,5.471),
      ("Almere",52.350,5.265),("Zeewolde",52.335,5.540),
      ("Amersfoort",52.157,5.387),("Soest",52.177,5.301),
      ("De Bilt",52.106,5.175),("Woerden",52.087,4.882),
      ("Utrecht",52.091,5.122),("Zeist",52.088,5.234),
      ("Nieuwegein",52.025,5.082),("Veenendaal",52.027,5.556),
      ("Grebbeberg",51.965,5.604),
    ],
    "water":[
      ("IJsselmeer",52.65,5.05),("Markermeer",52.43,5.10),
      ("Veluwemeer",52.44,5.70),("Gooimeer",52.35,5.22),
      ("Eemmeer",52.37,5.37),("Neder-Rijn",51.97,5.62),
      ("Lek",51.90,4.95),("Randmeren",52.43,5.57),
    ],
    "streek":[
      ("Noordoostpolder",52.71,5.74),
      ("Oostelijk Flevoland",52.52,5.65),
      ("Zuidelijk Flevoland",52.35,5.42),
      ("Utrechtse Heuvelrug",52.10,5.34),
      ("Lopikerwaard",51.97,4.90),
      ("Gelderse Vallei",52.07,5.57),
    ],
  },
  { "id":5, "titel":"Noord-Brabant en Limburg", "kleur":"#F44336",
    "hoofdprov":["Noord-Brabant","Limburg"],
    "buurprov":["Zuid-Holland","Utrecht","Gelderland","Zeeland"],
    "extent":(3.78,6.28,50.72,51.95),
    "steden":[
      ("Bergen op Zoom",51.498,4.288),("Roosendaal",51.531,4.463),
      ("Waalwijk",51.682,5.070),("'s-Hertogenbosch",51.689,5.305),
      ("Oss",51.765,5.519),("Oisterhout",51.577,4.867),
      ("Kaatsheuvel",51.657,5.040),("Breda",51.589,4.779),
      ("Boxtel",51.594,5.331),("Uden",51.659,5.619),
      ("Boxmeer",51.645,5.948),("Venray",51.526,5.976),
      ("Tilburg",51.558,5.083),("Eindhoven",51.441,5.478),
      ("Helmond",51.481,5.661),("Valkenswaart",51.352,5.459),
      ("Weert",51.249,5.709),("Venlo",51.370,6.172),
      ("Roermond",51.195,5.987),("Sittard",51.004,5.866),
      ("Geleen",50.969,5.833),("Hoensbroek",50.930,5.919),
      ("Heerlen",50.888,5.979),("Kerkrade",50.864,6.061),
      ("Maastricht",50.851,5.688),("Valkenburg",50.866,5.829),
      ("Vaals",50.773,6.025),
    ],
    "water":[
      ("Maas",51.70,5.50),("Maas",51.20,5.88),
      ("Biesbosch",51.76,4.81),("Bergse Maas",51.73,4.97),
      ("Wilhelminakanaal",51.59,5.02),
      ("Zuid-Willemsvaart",51.46,5.65),
      ("Maas-Waalkanaal",51.86,5.77),
      ("Juliana-kanaal",51.05,5.87),
    ],
    "streek":[
      ("De Peel",51.45,5.88),("De Kempen",51.40,5.42),
      ("Land van Heusden en Altena",51.76,5.07),
      ("Maasdal",51.10,5.95),
    ],
  },
  { "id":6, "titel":"Zuid-Holland", "kleur":"#00BCD4",
    "hoofdprov":["Zuid-Holland"],
    "buurprov":["Noord-Holland","Utrecht","Zeeland","Noord-Brabant"],
    "extent":(3.80,5.12,51.58,52.38),
    "steden":[
      ("Noordwijk",52.235,4.449),("Leiden",52.160,4.497),
      ("Wassenaar",52.144,4.401),("Alphen aan den Rijn",52.127,4.659),
      ("Scheveningen",52.108,4.272),("Den Haag",52.075,4.299),
      ("Zoetermeer",52.057,4.494),("Gouda",52.018,4.707),
      ("Delft",52.011,4.359),("Hoek van Holland",51.979,4.132),
      ("Vlaardingen",51.913,4.340),("Schiedam",51.919,4.396),
      ("Rotterdam",51.925,4.479),("Spijkenisse",51.847,4.336),
      ("Dordrecht",51.814,4.668),("Gorinchem",51.831,4.976),
    ],
    "water":[
      ("Noordzee",52.18,3.91),("Nieuwe Waterweg",51.95,4.18),
      ("Haringvliet",51.79,4.17),("Hollands Diep",51.76,4.50),
      ("Brielse Meer",51.89,4.16),("Biesbosch",51.78,4.79),
      ("Lek",51.89,4.96),("Gouwe",52.02,4.73),
    ],
    "streek":[
      ("Westland",52.00,4.21),("Hoeksche Waard",51.77,4.46),
      ("Groen Hart",52.09,4.68),("Bollenstreek",52.19,4.52),
      ("Goeree-Overflakkee",51.77,4.07),
    ],
  },
  { "id":7, "titel":"Noord-Holland", "kleur":"#FF5722",
    "hoofdprov":["Noord-Holland"],
    "buurprov":["Friesland","Utrecht","Zuid-Holland"],
    "extent":(4.46,5.40,52.18,53.20),
    "steden":[
      ("Texel",53.067,4.817),("Den Helder",52.955,4.762),
      ("Enkhuizen",52.702,5.297),("Hoorn",52.641,5.062),
      ("Alkmaar",52.631,4.740),("Purmerend",52.502,4.955),
      ("Volendam",52.499,5.070),("IJmuiden",52.457,4.620),
      ("Zaandam",52.433,4.813),("Zandvoort",52.371,4.535),
      ("Haarlem",52.381,4.635),("Amsterdam",52.372,4.894),
      ("Amstelveen",52.305,4.862),("Schiphol",52.309,4.765),
      ("Aalsmeer",52.267,4.763),("Bussum",52.275,5.162),
      ("Hilversum",52.223,5.174),
    ],
    "eilanden":[("Texel",53.067,4.817)],
    "water":[
      ("Waddenzee",53.05,4.82),("Noordzeekanaal",52.44,4.74),
      ("IJmeer",52.40,5.05),("Afsluitdijk",53.02,5.17),
      ("Alkmaardermeer",52.68,4.78),("het IJ",52.38,4.92),
      ("IJsselmeer",52.90,5.18),
    ],
    "streek":[
      ("Wieringermeer",52.82,5.02),("Beemster",52.55,4.94),
      ("Haarlemmermeer",52.31,4.70),("Het Gooi",52.25,5.15),
      ("West-Friesland",52.70,4.98),("Kennemerland",52.44,4.63),
    ],
    "overrides": {
      "Texel":        (40.6, 19.7),
      "Den Helder":   (35.8, 28.6),
      "Enkhuizen":    (81.7, 49.0),
      "Alkmaar":      (34.0, 54.7),
      "Hoorn":        (61.6, 53.9),
      "Purmerend":    (52.1, 65.1),
      "Volendam":     (62.2, 65.3),
      "IJmuiden":     (23.3, 68.6),
      "Zaandam":      (40.0, 70.7),
      "Amsterdam":    (47.0, 75.6),
      "het IJ":       (49.5, 74.2),
      "IJmeer":       (63.6, 73.6),
      "Amstelveen":   (44.4, 80.9),
      "Schiphol":     (35.9, 80.6),
      "Haarlem":      (24.8, 74.8),
      "Zandvoort":    (16.1, 75.6),
      "Aalsmeer":     (35.9, 84.0),
      "Bussum":       (70.1, 83.3),
      "Hilversum":    (71.1, 87.5),
    },
  },
  { "id":8, "titel":"Fryslân", "kleur":"#009688",
    "hoofdprov":["Friesland"],
    "buurprov":["Groningen","Drenthe","Overijssel"],
    "extent":(4.80,6.55,52.58,53.60),
    "steden":[
      ("Dokkum",53.325,5.999),("Leeuwarden",53.201,5.800),
      ("Franeker",53.188,5.540),("Harlingen",53.174,5.416),
      ("Drachten",53.108,6.100),("Bolsward",53.065,5.531),
      ("Sneek",53.031,5.661),("Joure",52.967,5.792),
      ("Heerenveen",52.961,5.919),("Stavoren",52.879,5.365),
      ("Lemmer",52.845,5.714),("Wolvega",52.878,5.993),
    ],
    "eilanden":[
      ("Vlieland",53.253,5.063),("Terschelling",53.398,5.283),
      ("Ameland",53.443,5.657),("Schiermonnikoog",53.480,6.171),
    ],
    "water":[
      ("Waddenzee",53.28,5.20),("IJsselmeer",52.72,5.33),
      ("Noordzee",53.52,4.95),("Afsluitdijk",53.02,5.19),
      ("Sneekermeer",52.98,5.68),("Tjeukemeer",52.88,5.80),
      ("Lauwersmeer",53.37,6.22),("De Friese Meren",52.93,5.75),
    ],
    "streek":[
      ("Gaasterland",52.85,5.48),("De Friese Wouden",53.05,6.06),
      ("Waddeneilanden",53.44,5.60),
    ],
    "overrides": {
      "Gaasterland":      (43.6, 66.5),
      "Waddenzee":        (28.3, 36.9),
      "IJsselmeer":       (38.1, 77.3),
      "Terschelling":     (31.6, 25.4),
      "Vlieland":         (21.5, 36.9),
      "Schiermonnikoog":  (73.3, 18.4),
      "Stavoren":         (35.8, 67.1),
      "Lemmer":           (51.9, 69.7),
      "Dokkum":           (65.4, 31.1),
      "Harlingen":        (38.1, 43.5),
      "Drachten":         (70.1, 48.5),
      "Waddeneilanden":   (45.6, 26.7),
      "Ameland":          (49.3, 21.4),
      "Wolvega":          (64.9, 67.3),
      "Heerenveen":       (61.4, 60.5),
    },
  },
  { "id":9, "titel":"Gelderland", "kleur":"#8BC34A",
    "hoofdprov":["Gelderland"],
    "buurprov":["Overijssel","Utrecht","Zuid-Holland","Noord-Brabant","Limburg"],
    "extent":(5.33,6.85,51.68,52.52),
    "steden":[
      ("Nunspeet",52.358,5.783),("Harderwijk",52.341,5.623),
      ("Nijkerk",52.217,5.493),("Apeldoorn",52.212,5.970),
      ("Barneveld",52.143,5.590),("Zutphen",52.138,6.196),
      ("Ede",52.042,5.665),("Wageningen",51.969,5.664),
      ("Arnhem",51.985,5.898),("Groenlo",51.998,6.624),
      ("Doetinchem",51.965,6.300),("Winterswijk",51.975,6.716),
      ("Tiel",51.886,5.428),("Elst",51.921,5.840),
      ("Zevenaar",51.927,6.074),("Nijmegen",51.843,5.859),
    ],
    "water":[
      ("IJssel",52.22,6.07),("Waal",51.87,5.62),
      ("Neder-Rijn",51.96,5.75),("Rijn",51.97,5.90),
      ("Oude IJssel",51.96,6.32),("Maas",51.82,5.87),
    ],
    "streek":[
      ("Veluwe",52.22,5.85),("Achterhoek",52.01,6.42),
      ("Betuwe",51.88,5.55),("Liemers",51.93,6.09),
      ("Bommelerwaard",51.85,5.28),("Gelderse Vallei",52.10,5.58),
    ],
  },
]

NAAM_MAP = {
  1:"les1_overijssel",2:"les2_zeeland",3:"les3_groningen_drenthe",
  4:"les4_flevoland_utrecht",5:"les5_brabant_limburg",6:"les6_zuidholland",
  7:"les7_noordholland",8:"les8_fryslan",9:"les9_gelderland",
}

# ─── Projectie-instellingen ───────────────────────────────────────────────────
MARGIN = 0.10
IMG_W, IMG_H = 9.0, 11.0   # inch
DPI = 110

def extent_met_marge(ext):
    lon_min,lon_max,lat_min,lat_max = ext
    dlon = lon_max-lon_min; dlat = lat_max-lat_min
    return (lon_min-dlon*MARGIN, lon_max+dlon*MARGIN,
            lat_min-dlat*MARGIN, lat_max+dlat*MARGIN)

# ─── Kaart tekenen ────────────────────────────────────────────────────────────
def teken_les(les, met_namen):
    ext  = les["extent"]
    xmin,xmax,ymin,ymax = extent_met_marge(ext)
    lat_mid = (ymin + ymax) / 2

    fig, ax = plt.subplots(figsize=(IMG_W, IMG_H), dpi=DPI)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Correcte geografische aspect-ratio: 1° lon ≈ cos(lat)° lat
    ax.set_aspect(1 / math.cos(math.radians(lat_mid)))
    ax.set_facecolor(ZEE_KLEUR)
    ax.set_axis_off()

    # ── Teken alle buurprovincies eerst (achtergrond) ──
    alle_prov = list(PROV_GEOM.keys())
    for naam in alle_prov:
        if naam in les["hoofdprov"]:
            continue
        is_buur = naam in les.get("buurprov", [])
        kleur = PROV_KLEUR.get(naam, BUUR_KLEUR) if is_buur else BUUR_KLEUR
        alpha = 0.85 if is_buur else 0.60
        teken_provincie(ax, naam, facecolor=kleur, edgecolor=BUUR_RAND,
                        linewidth=0.6, alpha=alpha, zorder=2)

    # ── Teken hoofdprovincies bovenop ──
    for naam in les["hoofdprov"]:
        teken_provincie(ax, naam, facecolor=les["kleur"], edgecolor=HOOFD_RAND,
                        linewidth=2.0, alpha=0.55, zorder=3)

    # ── Steden ──
    for naam, lat, lon in les.get("steden", []):
        if not (xmin <= lon <= xmax and ymin <= lat <= ymax):
            continue
        ax.plot(lon, lat, marker='s', color='#111111',
                markersize=5, markeredgewidth=0.5,
                markeredgecolor='white', zorder=10)
        if met_namen:
            off = (xmax - xmin) * 0.007
            t = ax.text(lon + off, lat, naam, fontsize=7.0, fontfamily='Arial',
                        fontweight='bold', color='#0d0d5c',
                        va='center', ha='left', zorder=11)
            t.set_path_effects([pe.withStroke(linewidth=2.5, foreground='white')])

    # ── Eilanden ──
    for naam, lat, lon in les.get("eilanden", []):
        ax.plot(lon, lat, marker='D', color='#333333',
                markersize=4.5, markeredgewidth=0.5,
                markeredgecolor='white', zorder=10)
        if met_namen:
            off = (xmax - xmin) * 0.007
            t = ax.text(lon + off, lat, naam, fontsize=6.8, fontfamily='Arial',
                        color='#4a148c', va='center', ha='left', zorder=11)
            t.set_path_effects([pe.withStroke(linewidth=2.5, foreground='white')])

    # ── Water labels ──
    if met_namen:
        for naam, lat, lon in les.get("water", []):
            if xmin <= lon <= xmax and ymin <= lat <= ymax:
                ax.text(lon, lat, naam, fontsize=7, fontfamily='Arial',
                        fontstyle='italic', color='#0d47a1',
                        ha='center', va='center', zorder=8,
                        path_effects=[pe.withStroke(linewidth=2.5,
                                                    foreground=ZEE_KLEUR)])
        for naam, lat, lon in les.get("streek", []):
            if xmin <= lon <= xmax and ymin <= lat <= ymax:
                ax.text(lon, lat, naam, fontsize=7.5, fontfamily='Arial',
                        fontstyle='italic', color='#1b5e20',
                        ha='center', va='center', zorder=8, alpha=0.9,
                        path_effects=[pe.withStroke(linewidth=2.5,
                                                    foreground='white')])

    # ── Kompasroos ──
    cx = xmax - (xmax - xmin) * 0.07
    cy = ymin + (ymax - ymin) * 0.05
    ax.annotate('N', xy=(cx, cy + (ymax-ymin)*0.04), fontsize=9,
                ha='center', fontweight='bold', color='#222')
    ax.annotate('', xy=(cx, cy + (ymax-ymin)*0.04),
                xytext=(cx, cy),
                arrowprops=dict(arrowstyle='->', color='#222', lw=1.5))

    # ── Schaalbalke (10 km) ──
    deg_10km = 10.0 / (111.32 * math.cos(math.radians(lat_mid)))
    sx = xmin + (xmax - xmin) * 0.06
    sy = ymin + (ymax - ymin) * 0.035
    ax.plot([sx, sx + deg_10km], [sy, sy], 'k-', lw=2, zorder=12,
            solid_capstyle='butt')
    ax.plot([sx, sx], [sy-(ymax-ymin)*0.007, sy+(ymax-ymin)*0.007], 'k-', lw=1.5)
    ax.plot([sx+deg_10km, sx+deg_10km],
            [sy-(ymax-ymin)*0.007, sy+(ymax-ymin)*0.007], 'k-', lw=1.5)
    ax.text(sx + deg_10km/2, sy + (ymax-ymin)*0.015, '10 km',
            ha='center', va='bottom', fontsize=6.5, color='#333')

    fig.patch.set_facecolor(ZEE_KLEUR)
    plt.tight_layout(pad=0.2)

    soort = "namen" if met_namen else "blanco"
    fname = f"{NAAM_MAP[les['id']]}_{soort}.png"
    path  = os.path.join(OUTPUT_DIR, fname)
    plt.savefig(path, dpi=DPI, bbox_inches='tight',
                facecolor=ZEE_KLEUR, edgecolor='none')
    plt.close()
    print(f"  {fname}")
    return path

# ─── provinces.js schrijven (ZELFDE projectie als de kaart) ──────────────────
def schrijf_provinces_js():
    def ll_to_pct(lat, lon, ext):
        lon_min,lon_max,lat_min,lat_max = ext
        dlon = lon_max - lon_min; dlat = lat_max - lat_min
        xmin = lon_min - dlon*MARGIN; xmax = lon_max + dlon*MARGIN
        ymin = lat_min - dlat*MARGIN; ymax = lat_max + dlat*MARGIN
        x = (lon - xmin) / (xmax - xmin) * 100
        y = (ymax - lat) / (ymax - ymin) * 100
        return round(x, 1), round(y, 1)

    lines = [
        "// Geobas Groep 6 — coördinaten berekend vanuit DEZELFDE projectie als de kaartafbeeldingen",
        "export const lessen = ["
    ]

    for les in LESSEN:
        ext      = les["extent"]
        base     = NAAM_MAP[les["id"]]
        ov       = les.get("overrides", {})   # handmatige x%,y% overrides

        def pos(naam, lat, lon):
            """Gebruik override als die er is, anders berekende projectie."""
            if naam in ov:
                ox, oy = ov[naam]
                return round(ox, 1), round(oy, 1)
            return ll_to_pct(lat, lon, ext)

        lines.append("  {")
        lines.append(f"    id: {les['id']},")
        lines.append(f"    titel: \"{les['titel']}\",")
        lines.append(f"    afbeeldingNamen: \"maps/{base}_namen.png\",")
        lines.append(f"    afbeeldingBlanco: \"maps/{base}_blanco.png\",")
        lines.append(f"    kleur: \"{les['kleur']}\",")
        lines.append("    plaatsen: [")

        for naam, lat, lon in les.get("steden", []):
            x, y = pos(naam, lat, lon)
            n = naam.replace('"', '\\"')
            lines.append(f"      {{ naam: \"{n}\", x: {x}, y: {y}, type: \"stad\" }},")

        for naam, lat, lon in les.get("eilanden", []):
            x, y = pos(naam, lat, lon)
            n = naam.replace('"', '\\"')
            lines.append(f"      {{ naam: \"{n}\", x: {x}, y: {y}, type: \"eiland\" }},")

        for naam, lat, lon in les.get("water", []):
            x, y = pos(naam, lat, lon)
            n = naam.replace('"', '\\"')
            lines.append(f"      {{ naam: \"{n}\", x: {x}, y: {y}, type: \"water\" }},")

        for naam, lat, lon in les.get("streek", []):
            x, y = pos(naam, lat, lon)
            n = naam.replace('"', '\\"')
            lines.append(f"      {{ naam: \"{n}\", x: {x}, y: {y}, type: \"streek\" }},")

        lines.append("    ]")
        lines.append("  },")

    lines += ["];", "", "export const getLes = (id) => lessen.find(l => l.id === id);", ""]
    out = r"C:\Software\Topografiekaart_6\app\src\data\provinces.js"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("provinces.js geschreven")

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    for les in LESSEN:
        print(f"Les {les['id']}: {les['titel']}")
        teken_les(les, met_namen=True)
        teken_les(les, met_namen=False)
    schrijf_provinces_js()
    print("\nKlaar!")
