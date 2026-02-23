#!/usr/bin/env python3
"""
tag_episodes.py — Indicizzazione tematica delle puntate di Tintoria.
Assegna tag basati sull'identità dell'ospite e sul contesto della puntata.

Categorie principali:
- professione: cosa fa l'ospite (comico, attore, musicista, scrittore, etc.)
- ambito: area tematica più ampia (comedy, cinema, musica, tv, giornalismo, etc.)
- tag: tag specifici per rendere cercabile la puntata
"""

import json

# --- Mappatura ospiti → tag ---
# Basata su identità pubblica reale di ciascun ospite.

GUEST_TAGS = {
    "Judah Friedlander feat Stefano Rapone": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "cinema"],
        "tag": ["stand-up", "comedy americana", "internazionale"]
    },
    "Giorgio Quarzo Guarascio aka Tutti Fenomeni": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["indie", "cantautore", "rap"]
    },
    "Valerio Lundini (2)": {
        "professione": ["comico", "conduttore", "musicista"],
        "ambito": ["comedy", "tv"],
        "tag": ["satira", "assurdo", "rai", "una pezza di Lundini"]
    },
    "Pippo Sowlo feat Christian the Seeker": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["indie", "cantautore"]
    },
    "Manuel Bongiorni aka Musica Per Bambini": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["elettronica", "indie"]
    },
    "Filippo Spreafico": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Pietro Sparacino (2)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "podcast"]
    },
    "Andrea Catenaro aka Laago!": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["rap", "hip-hop"]
    },
    "Daniela Delle Foglie": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Michela Giraud": {
        "professione": ["comica", "conduttrice"],
        "ambito": ["comedy", "tv"],
        "tag": ["stand-up", "netflix", "lol"]
    },
    "Daniele Manusia": {
        "professione": ["giornalista"],
        "ambito": ["giornalismo", "sport"],
        "tag": ["calcio", "il post"]
    },
    "Valerio Lundini e Matteo Tiberia": {
        "professione": ["comico", "conduttore", "musicista"],
        "ambito": ["comedy", "tv", "musica"],
        "tag": ["satira", "assurdo", "una pezza di Lundini", "vazzanikki"]
    },
    "Francesco Lancia (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Emanuela Fanelli (con Stefano Rapone)": {
        "professione": ["comica", "attrice"],
        "ambito": ["comedy", "cinema", "tv"],
        "tag": ["stand-up", "una pezza di Lundini"]
    },
    "Martina Catuzzi (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Edoardo Ferrario": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "satira", "imitazioni", "roma"]
    },
    "Velia Lalli (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Daniela Delle Foglie, Serena Tateo, Laura Grimaldi, Michela Giraud": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "donne nella comedy"]
    },
    "Stefano Rapone": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "co-host"]
    },
    "Liliana Fiorelli (con Stefano Rapone)": {
        "professione": ["attrice", "comica"],
        "ambito": ["comedy", "cinema"],
        "tag": ["stand-up", "attrice"]
    },
    "LIVE Elio Biffi (con Stefano Rapone)": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["live", "elio e le storie tese"]
    },
    "LIVE Giorgio Magri (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Adriano Venditti (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Ghemon (con Stefano Rapone)": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["live", "rap", "hip-hop", "cantautore"]
    },
    "LIVE Momoka (con Stefano Rapone)": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["live"]
    },
    "LIVE Francesco Mandelli con (Stefano Rapone)": {
        "professione": ["attore", "comico"],
        "ambito": ["comedy", "tv"],
        "tag": ["live", "i soliti idioti"]
    },
    "LIVE Emiliano Colasanti (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Daniele Tinti": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "host", "stand-up"]
    },
    "LIVE Serena Tateo e Luca Vecchi (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Stefano Gorno (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Alessandro Mannucci (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Francesco Pacifico": {
        "professione": ["scrittore"],
        "ambito": ["letteratura"],
        "tag": ["live", "romanzo", "narrativa"]
    },
    "Stefano Rapone e Daniele Tinti": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["host", "speciale"]
    },
    "LIVE Laura Formenti (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "Irene Graziosi (con Stefano Rapone)": {
        "professione": ["scrittrice", "giornalista"],
        "ambito": ["letteratura", "cultura"],
        "tag": ["narrativa", "social media", "critica culturale"]
    },
    "LIVE Nic Cester (con Stefano Rapone)": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["live", "rock", "jet", "internazionale"]
    },
    "LIVE Selton": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["live", "indie", "band"]
    },
    "LIVE Luca Ravenna (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up", "podcast"]
    },
    "LIVE Michela Giraud (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up", "netflix"]
    },
    "LIVE Sonia Ceriola (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Cicalone Simone": {
        "professione": ["content creator"],
        "ambito": ["web"],
        "tag": ["live", "youtube", "street interview", "roma"]
    },
    "LIVE Fabio Pinci aka Ceppaflex (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "con Stefano Rapone": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["co-host", "speciale"]
    },
    "LIVE Alessandro Cino Zolfanelli": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Luca Vecchi & Valerio Desirò": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Davide Marini + Sandro Canori + Andrea di Castro": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "vs Cachemire Podcast": {
        "professione": ["podcaster"],
        "ambito": ["comedy", "podcast"],
        "tag": ["crossover", "cachemire podcast"]
    },
    "LIVE Francesco De Carlo": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up", "internazionale", "londra"]
    },
    "Guia Scognamiglio & Tommaso Faoro": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Eleazaro Rossi": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "roma"]
    },
    "LIVE Raffaello Corti (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Pietro Sparacino & Mauro Fratini (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "stand-up"]
    },
    "LIVE Stefano Rapone": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["live", "co-host", "stand-up"]
    },
    "Daniele Fabbri (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Eleazaro Rossi (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "roma"]
    },
    "Riccardo Cotumaccio (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Danilo da Fiumicino (con Stefano Rapone)": {
        "professione": ["comico", "content creator"],
        "ambito": ["comedy", "web"],
        "tag": ["youtube", "personaggio"]
    },
    "Martina Catuzzi (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Covid-19": {
        "professione": [],
        "ambito": ["attualità"],
        "tag": ["covid", "pandemia", "speciale"]
    },
    "Velia Lalli (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Sergio Viglianese (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Giacomo Bevilacqua (con Stefano Rapone)": {
        "professione": ["fumettista"],
        "ambito": ["fumetto", "cultura"],
        "tag": ["a panda piace", "graphic novel"]
    },
    "Michela Giraud (con Stefano Rapone)": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "netflix"]
    },
    "Davide Marini": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Giada Messetti (con Stefano Rapone)": {
        "professione": ["giornalista", "scrittrice"],
        "ambito": ["giornalismo", "geopolitica"],
        "tag": ["cina", "asia", "politica internazionale"]
    },
    "Karma B (con Stefano Rapone)": {
        "professione": ["drag queen"],
        "ambito": ["spettacolo"],
        "tag": ["drag", "lgbtq+", "cabaret"]
    },
    "Carmelo Avanzato & Tahir Hussain (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Il Grande Caldo (con Stefano Rapone)": {
        "professione": ["podcaster"],
        "ambito": ["comedy", "podcast"],
        "tag": ["crossover"]
    },
    "Ditonellapiaga (con Stefano Rapone)": {
        "professione": ["musicista", "cantautrice"],
        "ambito": ["musica"],
        "tag": ["pop", "sanremo", "cantautrice"]
    },
    "Recanati (con Stefano Rapone)": {
        "professione": [],
        "ambito": ["comedy"],
        "tag": ["live", "speciale", "recanati"]
    },
    "Tutti Fenomeni (con Stefano Rapone)": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["indie", "rap"]
    },
    "Cecilia Sala (con Stefano Rapone)": {
        "professione": ["giornalista", "podcaster"],
        "ambito": ["giornalismo"],
        "tag": ["guerra", "geopolitica", "stories", "podcast"]
    },
    "Dado (con Stefano Rapone)": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["cabaret", "tv"]
    },
    "Prato (con Stefano Rapone)": {
        "professione": [],
        "ambito": ["comedy"],
        "tag": ["live", "speciale", "prato"]
    },
    "Martin e Luis Sal (con Stefano Rapone)": {
        "professione": ["content creator"],
        "ambito": ["web"],
        "tag": ["youtube", "podcast"]
    },
    "COMEDY VILLAGE": {
        "professione": [],
        "ambito": ["comedy"],
        "tag": ["live", "festival", "speciale"]
    },
    "Giovanni Benincasa": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Gero Arnone & Eliana Albertini": {
        "professione": ["attore", "comica"],
        "ambito": ["comedy", "cinema"],
        "tag": ["stand-up"]
    },
    "Massimo Ceccherini": {
        "professione": ["attore", "comico"],
        "ambito": ["comedy", "cinema"],
        "tag": ["toscana", "commedia italiana", "benigni"]
    },
    "Gipi": {
        "professione": ["fumettista", "regista"],
        "ambito": ["fumetto", "cinema", "cultura"],
        "tag": ["graphic novel", "arte", "narrativa"]
    },
    "Maccio Capatonda": {
        "professione": ["comico", "regista", "attore"],
        "ambito": ["comedy", "cinema", "web"],
        "tag": ["parodia", "youtube", "surreale"]
    },
    "Valerio Lundini": {
        "professione": ["comico", "conduttore", "musicista"],
        "ambito": ["comedy", "tv", "musica"],
        "tag": ["satira", "assurdo", "una pezza di Lundini", "rai"]
    },
    "Margherita Vicario": {
        "professione": ["musicista", "attrice", "regista"],
        "ambito": ["musica", "cinema"],
        "tag": ["cantautrice", "pop", "gloria!"]
    },
    "Paolo Calabresi": {
        "professione": ["attore"],
        "ambito": ["cinema", "tv"],
        "tag": ["commedia italiana", "caratterista"]
    },
    "Nuzzo e Di Biase": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["duo comico", "tv", "cabaret"]
    },
    "Aurora Leone": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "the jackal"]
    },
    "Zerocalcare": {
        "professione": ["fumettista"],
        "ambito": ["fumetto", "cultura"],
        "tag": ["graphic novel", "netflix", "strappare lungo i bordi", "roma", "rebibbia"]
    },
    "Riccardo Rossi": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy"],
        "tag": ["cabaret", "one man show", "roma"]
    },
    "Pietro Sermonti": {
        "professione": ["attore"],
        "ambito": ["cinema", "tv"],
        "tag": ["boris", "commedia italiana"]
    },
    "Barbascura X": {
        "professione": ["divulgatore", "content creator"],
        "ambito": ["scienza", "web"],
        "tag": ["divulgazione scientifica", "youtube"]
    },
    "Frank Matano": {
        "professione": ["comico", "youtuber"],
        "ambito": ["comedy", "tv", "web"],
        "tag": ["youtube", "lol", "pranks"]
    },
    "The Pills": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "web"],
        "tag": ["youtube", "web series", "roma"]
    },
    "Bugo": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["cantautore", "indie", "sanremo", "morgan"]
    },
    "Lillo": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "cinema", "tv"],
        "tag": ["lol", "lillo e greg", "commedia"]
    },
    "Andrea Delogu": {
        "professione": ["conduttrice", "scrittrice"],
        "ambito": ["tv", "letteratura"],
        "tag": ["rai", "radio", "narrativa"]
    },
    "Lo Stato Sociale": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["band", "indie", "sanremo", "bologna"]
    },
    "Alessandro Cattelan": {
        "professione": ["conduttore"],
        "ambito": ["tv"],
        "tag": ["x factor", "netflix", "rai"]
    },
    "Marco Marzocca": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "tv"],
        "tag": ["cabaret", "zelig", "ruggero de ceglie"]
    },
    "Rocco Tanica": {
        "professione": ["musicista", "comico", "scrittore"],
        "ambito": ["musica", "comedy", "letteratura"],
        "tag": ["elio e le storie tese", "satira"]
    },
    "Willie Peyote": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "cantautore", "torino", "sanremo"]
    },
    "Gianluca Fru": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "web"],
        "tag": ["the jackal", "lol"]
    },
    "Francesco Costa": {
        "professione": ["giornalista", "podcaster"],
        "ambito": ["giornalismo"],
        "tag": ["il post", "podcast", "usa", "politica"]
    },
    "Fulminacci": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["cantautore", "indie", "sanremo"]
    },
    "Giorgio Frassineti": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "imitazioni"]
    },
    "Massimo Bagnato": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["cabaret", "tv"]
    },
    "Piero Pelù": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["rock", "litfiba", "sanremo"]
    },
    "Pilar Fogliati": {
        "professione": ["attrice"],
        "ambito": ["cinema", "tv"],
        "tag": ["commedia", "rai"]
    },
    "Alessandro Masala (SHY)": {
        "professione": ["content creator", "giornalista"],
        "ambito": ["web", "giornalismo"],
        "tag": ["youtube", "divulgazione", "attualità"]
    },
    "Maurizio Battista": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["one man show", "roma", "cabaret", "tv"]
    },
    "Marco Cappato": {
        "professione": ["attivista", "politico"],
        "ambito": ["politica", "diritti civili"],
        "tag": ["eutanasia", "radicali", "diritti"]
    },
    "Alberto Grandi": {
        "professione": ["storico", "accademico"],
        "ambito": ["cultura", "storia"],
        "tag": ["storia dell'alimentazione", "cucina italiana", "food", "debunking"]
    },
    "Madame": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["rap", "pop", "sanremo", "gen z"]
    },
    "Carolina Crescentini": {
        "professione": ["attrice"],
        "ambito": ["cinema", "tv"],
        "tag": ["commedia", "dramma"]
    },
    "Giovanni Truppi": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["cantautore", "sanremo", "napoli"]
    },
    "Walter Fontana": {
        "professione": ["scrittore", "sceneggiatore"],
        "ambito": ["letteratura", "tv"],
        "tag": ["zelig", "comicità", "narrativa"]
    },
    "Piotta": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "roma", "supercafone"]
    },
    "Eterobasiche": {
        "professione": ["content creator"],
        "ambito": ["web", "comedy"],
        "tag": ["podcast", "social media"]
    },
    "Paolo Rossi": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "teatro"],
        "tag": ["teatro", "improvvisazione", "cabaret"]
    },
    "Giovanni Cacioppo": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "sicilia"]
    },
    "Arturo Brachetti": {
        "professione": ["trasformista", "artista"],
        "ambito": ["spettacolo", "teatro"],
        "tag": ["quick change", "teatro", "illusionismo"]
    },
    "Martufello": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "tv"],
        "tag": ["cabaret", "roma", "tv"]
    },
    "Gabriele Cirilli": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "tv"],
        "tag": ["zelig", "cabaret", "tale e quale"]
    },
    "Gigi Datome": {
        "professione": ["sportivo"],
        "ambito": ["sport"],
        "tag": ["basket", "nba", "olimpiadi"]
    },
    "Paola Minaccioni": {
        "professione": ["comica", "attrice"],
        "ambito": ["comedy", "cinema"],
        "tag": ["roma", "cabaret", "imitazioni"]
    },
    "Jacopo Fo": {
        "professione": ["scrittore", "attivista"],
        "ambito": ["cultura", "letteratura"],
        "tag": ["dario fo", "franca rame", "ecologia", "controcultura"]
    },
    "Linus": {
        "professione": ["conduttore", "dj"],
        "ambito": ["tv", "radio", "musica"],
        "tag": ["radio deejay", "radio"]
    },
    "Alex Britti": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["cantautore", "blues", "chitarrista"]
    },
    "Giobbe Covatta": {
        "professione": ["comico", "attivista"],
        "ambito": ["comedy", "diritti civili"],
        "tag": ["cabaret", "umorismo", "africa", "solidarietà"]
    },
    "Antonio Rezza e Flavia Mastrella": {
        "professione": ["artista", "performer"],
        "ambito": ["teatro", "arte"],
        "tag": ["performance", "avanguardia", "teatro contemporaneo"]
    },
    "Vinicio  Marchioni": {
        "professione": ["attore"],
        "ambito": ["cinema", "tv", "teatro"],
        "tag": ["romanzo criminale", "dramma"]
    },
    "Caterina Guzzanti": {
        "professione": ["comica", "attrice"],
        "ambito": ["comedy", "cinema", "tv"],
        "tag": ["satira", "boris", "guzzanti"]
    },
    "Trio Medusa": {
        "professione": ["comico", "conduttore"],
        "ambito": ["comedy", "radio"],
        "tag": ["radio deejay", "radio", "lol"]
    },
    "J-AX": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "hip-hop", "articolo 31", "pop"]
    },
    "Pietro Castellitto": {
        "professione": ["attore", "regista", "scrittore"],
        "ambito": ["cinema", "letteratura"],
        "tag": ["regia", "narrativa", "sergio castellitto"]
    },
    "Daniela Collu": {
        "professione": ["conduttrice", "podcaster"],
        "ambito": ["tv", "web"],
        "tag": ["podcast", "pop culture"]
    },
    "Greg": {
        "professione": ["comico", "musicista"],
        "ambito": ["comedy", "musica"],
        "tag": ["lillo e greg", "cabaret"]
    },
    "Cochi Ponzoni": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy"],
        "tag": ["cabaret milanese", "cochi e renato", "storico"]
    },
    "Gino Paoli": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["cantautore", "storico", "genova", "canzone italiana"]
    },
    "Brunori Sas": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["cantautore", "indie", "calabria"]
    },
    "Brenda Lodigiani": {
        "professione": ["comica", "attrice"],
        "ambito": ["comedy", "tv"],
        "tag": ["imitazioni", "lol", "gialappa"]
    },
    "Marco D'Amore": {
        "professione": ["attore", "regista"],
        "ambito": ["cinema", "tv"],
        "tag": ["gomorra", "napoli", "regia"]
    },
    "Ceccon & Balbontin": {
        "professione": ["sportivo", "comico"],
        "ambito": ["sport", "comedy"],
        "tag": ["nuoto", "olimpiadi"]
    },
    "Tinti & Rapone": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["host", "speciale"]
    },
    "Marcello Cesena": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "web"],
        "tag": ["web series", "the jackal"]
    },
    "Stefano Nazzi": {
        "professione": ["giornalista", "podcaster"],
        "ambito": ["giornalismo"],
        "tag": ["cronaca nera", "indagini", "podcast"]
    },
    "Giancarlo Magalli": {
        "professione": ["conduttore"],
        "ambito": ["tv"],
        "tag": ["rai", "tv storica"]
    },
    "Michela Giraud": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "netflix", "lol"]
    },
    "Lucia Ocone": {
        "professione": ["comica", "attrice"],
        "ambito": ["comedy", "cinema"],
        "tag": ["personaggi", "tv"]
    },
    "Elio Germano": {
        "professione": ["attore"],
        "ambito": ["cinema", "teatro"],
        "tag": ["cinema d'autore", "teatro"]
    },
    "Elio": {
        "professione": ["musicista", "comico"],
        "ambito": ["musica", "comedy"],
        "tag": ["elio e le storie tese", "satira", "sanremo"]
    },
    "Neri per Caso": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["a cappella", "vocal group", "sanremo"]
    },
    "Raul Cremona": {
        "professione": ["comico", "mago"],
        "ambito": ["comedy", "spettacolo"],
        "tag": ["zelig", "magia", "cabaret"]
    },
    "Francesco Fanucchi": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Dario Moccia": {
        "professione": ["content creator"],
        "ambito": ["web"],
        "tag": ["twitch", "anime", "manga", "pop culture"]
    },
    "Gioele Dix": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "teatro"],
        "tag": ["teatro", "cabaret", "milano"]
    },
    "Luca Bizzarri": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "tv"],
        "tag": ["luca e paolo", "genova"]
    },
    "Daria Bignardi": {
        "professione": ["giornalista", "conduttrice", "scrittrice"],
        "ambito": ["tv", "giornalismo", "letteratura"],
        "tag": ["le invasioni barbariche", "narrativa"]
    },
    "Alessandro Borghese": {
        "professione": ["chef", "conduttore"],
        "ambito": ["food", "tv"],
        "tag": ["cucina", "4 ristoranti"]
    },
    "Filippo Ceccarelli": {
        "professione": ["giornalista", "scrittore"],
        "ambito": ["giornalismo", "politica"],
        "tag": ["politica italiana", "repubblica", "costume"]
    },
    "Paolo Hendel": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy"],
        "tag": ["cabaret", "toscana"]
    },
    "Francesco Bianconi": {
        "professione": ["musicista", "scrittore"],
        "ambito": ["musica", "letteratura"],
        "tag": ["baustelle", "indie", "cantautore", "narrativa"]
    },
    "Gialappa's Band": {
        "professione": ["comico", "conduttore"],
        "ambito": ["comedy", "tv"],
        "tag": ["gialappa", "mai dire", "calcio", "satira tv"]
    },
    "Teo Teocoli": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "tv"],
        "tag": ["imitazioni", "cabaret", "milan", "adriano celentano"]
    },
    "Dargen D'Amico": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["rap", "elettronica", "sanremo", "x factor"]
    },
    "Sandro Cappai": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Max Giusti": {
        "professione": ["comico", "conduttore"],
        "ambito": ["comedy", "tv"],
        "tag": ["imitazioni", "rai", "one man show"]
    },
    "Rocco Papaleo": {
        "professione": ["attore", "regista", "musicista"],
        "ambito": ["cinema", "comedy", "musica"],
        "tag": ["basilicata coast to coast", "sanremo"]
    },
    "Diego Bianchi": {
        "professione": ["giornalista", "conduttore"],
        "ambito": ["giornalismo", "tv"],
        "tag": ["propaganda live", "gazebo", "politica"]
    },
    "Giorgio Montanini": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "dark comedy", "sociale"]
    },
    "Paolo Sorrentino": {
        "professione": ["regista", "scrittore"],
        "ambito": ["cinema", "letteratura"],
        "tag": ["oscar", "la grande bellezza", "napoli", "cinema d'autore"]
    },
    "Donato Carrisi": {
        "professione": ["scrittore", "regista"],
        "ambito": ["letteratura", "cinema"],
        "tag": ["thriller", "noir", "narrativa"]
    },
    "Matilda De Angelis": {
        "professione": ["attrice"],
        "ambito": ["cinema", "tv"],
        "tag": ["hbo", "internazionale"]
    },
    "Gianluca Gazzoli": {
        "professione": ["conduttore", "podcaster"],
        "ambito": ["radio", "web"],
        "tag": ["radio deejay", "podcast"]
    },
    "Claudio Bisio": {
        "professione": ["attore", "comico", "conduttore"],
        "ambito": ["cinema", "comedy", "tv"],
        "tag": ["zelig", "commedia italiana", "teatro"]
    },
    "Valerio Nicolosi": {
        "professione": ["giornalista", "fotoreporter"],
        "ambito": ["giornalismo"],
        "tag": ["reportage", "guerra", "migrazioni"]
    },
    "Irene Grandi": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["pop", "rock", "sanremo"]
    },
    "Ubaldo Pantani": {
        "professione": ["comico", "imitatore"],
        "ambito": ["comedy", "tv"],
        "tag": ["imitazioni", "gialappa"]
    },
    "Ferzan Özpetek": {
        "professione": ["regista"],
        "ambito": ["cinema"],
        "tag": ["cinema d'autore", "dramma", "turchia-italia"]
    },
    "Christian De Sica": {
        "professione": ["attore", "regista"],
        "ambito": ["cinema", "comedy"],
        "tag": ["cinepanettone", "commedia italiana", "de sica"]
    },
    "Cristina D'Avena": {
        "professione": ["cantante"],
        "ambito": ["musica", "tv"],
        "tag": ["sigle cartoni", "anime", "nostalgia", "pop"]
    },
    "Nino Frassica": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "tv", "cinema"],
        "tag": ["don matteo", "che tempo che fa", "surreale"]
    },
    "Leo Ortolani": {
        "professione": ["fumettista"],
        "ambito": ["fumetto"],
        "tag": ["rat-man", "graphic novel", "umorismo"]
    },
    "Fabio De Luigi": {
        "professione": ["attore", "comico", "regista"],
        "ambito": ["cinema", "comedy"],
        "tag": ["commedia italiana", "gialappa", "mai dire"]
    },
    "Maurizio Milani": {
        "professione": ["comico", "scrittore"],
        "ambito": ["comedy", "letteratura"],
        "tag": ["assurdo", "cabaret", "satira"]
    },
    "Coez": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "pop", "cantautore"]
    },
    "Sabina Guzzanti": {
        "professione": ["comica", "regista", "attrice"],
        "ambito": ["comedy", "cinema", "politica"],
        "tag": ["satira politica", "guzzanti", "documentario"]
    },
    "Serena Dandini": {
        "professione": ["conduttrice", "autrice"],
        "ambito": ["tv", "cultura"],
        "tag": ["satira", "la tv delle ragazze", "rai"]
    },
    "Salvatore Esposito": {
        "professione": ["attore"],
        "ambito": ["cinema", "tv"],
        "tag": ["gomorra", "napoli", "serie tv"]
    },
    "Matteo Berrettini": {
        "professione": ["sportivo"],
        "ambito": ["sport"],
        "tag": ["tennis", "atp"]
    },
    "Giorgio Tirabassi": {
        "professione": ["attore"],
        "ambito": ["cinema", "tv", "teatro"],
        "tag": ["distretto di polizia", "teatro"]
    },
    "Guè": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "hip-hop", "club dogo"]
    },
    "Valerio Mastandrea": {
        "professione": ["attore", "regista"],
        "ambito": ["cinema"],
        "tag": ["cinema d'autore", "roma"]
    },
    "Paola Iezzi": {
        "professione": ["musicista"],
        "ambito": ["musica", "tv"],
        "tag": ["paola e chiara", "pop", "x factor"]
    },
    "Giovanni Muciaccia": {
        "professione": ["conduttore"],
        "ambito": ["tv"],
        "tag": ["art attack", "rai", "nostalgia"]
    },
    "Coma_Cose": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["duo", "indie", "sanremo", "pop"]
    },
    "Costantino della Gherardesca": {
        "professione": ["conduttore"],
        "ambito": ["tv"],
        "tag": ["pechino express", "pop culture"]
    },
    "Nicola Savino": {
        "professione": ["conduttore", "dj"],
        "ambito": ["tv", "radio"],
        "tag": ["le iene", "radio deejay"]
    },
    "Fiorella Mannoia": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["cantautrice", "pop", "sanremo", "canzone italiana"]
    },
    "Francesca Michielin": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["pop", "sanremo", "x factor", "cantautrice"]
    },
    "Salvo Di Paola": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Roberto Saviano": {
        "professione": ["scrittore", "giornalista"],
        "ambito": ["letteratura", "giornalismo"],
        "tag": ["gomorra", "camorra", "mafia", "diritti civili"]
    },
    "Giorgio Panariello": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy", "tv"],
        "tag": ["one man show", "toscana", "imitazioni"]
    },
    "Neri Marcorè": {
        "professione": ["attore", "comico", "imitatore"],
        "ambito": ["cinema", "comedy", "tv"],
        "tag": ["imitazioni", "marche", "commedia"]
    },
    "Paolo Nori": {
        "professione": ["scrittore"],
        "ambito": ["letteratura"],
        "tag": ["narrativa", "russia", "dostoevskij", "umorismo letterario"]
    },
    "Gabriele Mainetti": {
        "professione": ["regista"],
        "ambito": ["cinema"],
        "tag": ["lo chiamavano jeeg robot", "freaks out", "cinema di genere"]
    },
    "Pif": {
        "professione": ["regista", "conduttore", "attore"],
        "ambito": ["cinema", "tv"],
        "tag": ["le iene", "mafia", "sicilia", "documentario"]
    },
    "Monir Ghassem": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Claudio Amendola": {
        "professione": ["attore", "regista"],
        "ambito": ["cinema", "tv"],
        "tag": ["roma", "commedia italiana", "serie tv"]
    },
    "Toni Bonji": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Stefano Bollani": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["jazz", "pianoforte", "tv"]
    },
    "Ema Stokholma": {
        "professione": ["conduttrice", "dj", "scrittrice"],
        "ambito": ["radio", "tv", "letteratura"],
        "tag": ["radio 2", "sanremo", "autobiografia"]
    },
    "Giorgia Fumo": {
        "professione": ["comica"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Max Angioni": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "zelig"]
    },
    "Fabri Fibra": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "hip-hop"]
    },
    "Francesca Albanese": {
        "professione": ["diplomatica"],
        "ambito": ["politica", "diritti civili"],
        "tag": ["onu", "palestina", "diritto internazionale"]
    },
    "Enzo Iacchetti": {
        "professione": ["comico", "conduttore"],
        "ambito": ["comedy", "tv"],
        "tag": ["striscia la notizia", "cabaret"]
    },
    "Jake La Furia": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "hip-hop", "club dogo"]
    },
    "Nathan Kiboba": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Claudia Gerini": {
        "professione": ["attrice"],
        "ambito": ["cinema", "tv"],
        "tag": ["commedia italiana"]
    },
    "Cecilia Sala": {
        "professione": ["giornalista", "podcaster"],
        "ambito": ["giornalismo"],
        "tag": ["guerra", "geopolitica", "stories", "podcast", "iran"]
    },
    "Carlo Amleto": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up", "tiktok"]
    },
    "Carlo Verdone": {
        "professione": ["attore", "regista"],
        "ambito": ["cinema", "comedy"],
        "tag": ["commedia italiana", "roma", "cult"]
    },
    "Caparezza": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "cantautore", "puglia"]
    },
    "Giovanni Floris": {
        "professione": ["giornalista", "conduttore"],
        "ambito": ["giornalismo", "tv"],
        "tag": ["dimartedì", "politica"]
    },
    "Carmine Del Grosso": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Daniele Fabbri": {
        "professione": ["comico"],
        "ambito": ["comedy"],
        "tag": ["stand-up"]
    },
    "Roberto Giacobbo": {
        "professione": ["conduttore", "giornalista"],
        "ambito": ["tv"],
        "tag": ["voyager", "misteri", "divulgazione"]
    },
    "Ambra Angiolini": {
        "professione": ["attrice", "conduttrice"],
        "ambito": ["cinema", "tv"],
        "tag": ["non è la rai", "teatro"]
    },
    "Toni Servillo": {
        "professione": ["attore"],
        "ambito": ["cinema", "teatro"],
        "tag": ["la grande bellezza", "sorrentino", "teatro", "napoli"]
    },
    "Maurizio Nichetti": {
        "professione": ["regista", "attore"],
        "ambito": ["cinema", "comedy"],
        "tag": ["commedia", "milano", "animazione"]
    },
    "Mika": {
        "professione": ["musicista"],
        "ambito": ["musica"],
        "tag": ["pop", "internazionale", "x factor"]
    },
    "Filippo Tortu": {
        "professione": ["sportivo"],
        "ambito": ["sport"],
        "tag": ["atletica", "velocista", "olimpiadi"]
    },
    "Giovanni Vernia": {
        "professione": ["comico", "attore"],
        "ambito": ["comedy"],
        "tag": ["one man show", "zelig"]
    },
    "Gemitaiz": {
        "professione": ["musicista", "rapper"],
        "ambito": ["musica"],
        "tag": ["rap", "hip-hop", "freestyle"]
    },
}

def main():
    import json, os

    with open("data/episodes.json") as f:
        data = json.load(f)

    tagged = []
    unmatched = []

    for ep in data["episodes"]:
        guest = ep["guest"]
        tags = GUEST_TAGS.get(guest)

        if tags:
            ep["professione"] = tags["professione"]
            ep["ambito"] = tags["ambito"]
            ep["tags"] = tags["tag"]
        else:
            ep["professione"] = []
            ep["ambito"] = []
            ep["tags"] = []
            unmatched.append(f"#{ep['episode_number']} {guest}")

        tagged.append(ep)

    # Statistiche tag
    all_ambiti = {}
    all_tags = {}
    for ep in tagged:
        for a in ep.get("ambito", []):
            all_ambiti[a] = all_ambiti.get(a, 0) + 1
        for t in ep.get("tags", []):
            all_tags[t] = all_tags.get(t, 0) + 1

    data["episodes"] = tagged
    data["meta"]["tags_generated"] = True
    data["meta"]["ambiti_counts"] = dict(sorted(all_ambiti.items(), key=lambda x: -x[1]))
    data["meta"]["top_tags"] = dict(sorted(all_tags.items(), key=lambda x: -x[1])[:30])

    os.makedirs("data", exist_ok=True)
    with open("data/episodes_tagged.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Episodi taggati: {len(tagged) - len(unmatched)}/{len(tagged)}")
    if unmatched:
        print(f"Non matchati ({len(unmatched)}):")
        for u in unmatched:
            print(f"  {u}")

    print(f"\nAmbiti:")
    for a, c in sorted(all_ambiti.items(), key=lambda x: -x[1]):
        print(f"  {a}: {c}")

    print(f"\nTop 20 tag:")
    for t, c in sorted(all_tags.items(), key=lambda x: -x[1])[:20]:
        print(f"  {t}: {c}")

if __name__ == "__main__":
    main()
