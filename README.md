# VRUTER_OPG
Om modulering av ruter appen

3/10/2026
jeg skal lage en nettside hvor kuben elever kan se når busser kommer, hvilket deadlines man har i dag (som man må putte inn alene som om det er qoutes), logge inn, og evt en liten yr widgfest som viser hva været er. 
planen er å gjennbruke litt av koden jeg allerede har, feks qoute of the day og logg in. den aller første ideen var å lage en ruter redesign men jeg var redd for at det ikke var nok bruk av databaser siden jeg bare "låner" informastjonen.



5/22/2026

Jeg la til en FAQ-modal på dashboardet med vanlige spørsmål og et skjema for å sende inn egne spørsmål, samt en GDPR-side for sletting av brukerdata. Underveis hadde jeg problemer med manglende Python-pakker som måtte installeres separat på Pi-en, databasebrukeren anohej fantes ikke i MariaDB og måtte opprettes manuelt, og jeg hadde satt host til IP-adressen i stedet for localhost siden jeg trodde databasen lå på en annen maskin — men alt kjører på samme Pi.
