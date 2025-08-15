# PRD — Daily Fantasy Citation & Image Generator

## Nome App
**Da decidere** (proposta: FantasyDaily, EpicDay, DailySaga)

## Scopo
Generare quotidianamente fatti e citazioni da universi fantastici: Tolkien, Harry Potter, Matrix.  
Inoltre generare immagini correlate in stile Disney/Ghibli/Tolkien.

## Funzionalità principali
1. Database SQLite con eventi giornalieri per:
   - Tolkien
   - Harry Potter
   - Matrix
2. Gestione fino a 3 eventi per giorno per universo (`event_index`)
3. Web UI Flask con:
   - Generazione prompt immagini
   - Dashboard AppPulse per monitorare DB e contenuti
4. Modulo generatore prompt immagini:
   - Include anno, citazione, universo
   - Stile predefinito Disney/Ghibli/Tolkien
5. Possibilità futura di integrazione con Telegram o social media

## Architettura
- Backend: Python + Flask
- Database: SQLite
- Moduli:
  - `daily_fantasy_db.py`: gestione database
  - `image_prompt_generator.py`: generatore prompt immagini
  - `app.py`: web UI + integrazione
- Dashboard interna: AppPulse

## Estensioni future
- Popolamento automatico DB via AI
- Pubblicazione su Telegram / social media
- Multi-event per giorno più esteso
- Generazione immagini con AI direttamente dalla UI
