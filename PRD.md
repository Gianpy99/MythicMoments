# Daily Fantasy Event Bot - PRD

## Vision
Fornire ogni giorno un evento o citazione rilevante dai mondi di Tolkien, Harry Potter e Matrix, con la possibilità di generare immagini ispirate allo stile Disney/Ghibli/Tolkien, per fruizione via Telegram o app futura.

## Obiettivi
- Fornire un fatto del giorno per ciascun universo.
- Supportare più eventi per giorno (fino a 3 per universo).
- Preparare il sistema per integrazione futura con immagini AI.
- Database flessibile per gestire espansione futura (nuovi universi o citazioni).

## Utenti Target
- Fan di Tolkien, Harry Potter e Matrix.
- Utenti Telegram o futuri utenti app mobile/social.

## Funzionalità Principali
1. **Database cronologico (SQLite)**  
   - Giorni predefiniti (01-01 → 12-31).  
   - Eventi multipli per universo.  
   - Campi: `year`, `fact`, `quote`.

2. **Bot giornaliero**  
   - Seleziona eventi del giorno.  
   - Genera testo pronto per Telegram o app.

3. **Generazione immagine AI (futura)**  
   - Stile Disney/Ghibli/Tolkien.  
   - Basata su fatto/citazione.

4. **Gestione multi-evento**  
   - Fino a 3 eventi per giorno/universo.

## Fasi del Progetto
1. Setup DB e prototipo Python (completato con script SQLite).  
2. Popolamento dati iniziali (Harry Potter e Tolkien primi eventi).  
3. Bot Telegram (pubblica evento del giorno).  
4. Integrazione immagine AI.  
5. Eventuale espansione social / app mobile.

## Metriche di Successo
- 100% giorni dell’anno coperti con almeno 1 evento.  
- Bot Telegram operativo, pubblica evento giornaliero senza errori.  
- Possibilità di aggiungere nuovi eventi senza modifiche al codice.
