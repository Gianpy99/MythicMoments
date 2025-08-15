from flask import Flask
from daily_fantasy_db import DailyFantasyDB
from image_prompt_generator import ImagePromptGenerator

app = Flask(__name__)
db = DailyFantasyDB()
generator = ImagePromptGenerator()

@app.route('/image_prompt/<int:month>/<int:day>')
def image_prompt(month, day):
    events = db.get_events_for_day(month, day)
    prompts = generator.generate_prompts_for_day(events)
    return "<br>".join(prompts)

@app.route('/apppulse')
def apppulse_dashboard():
    total_days = 366
    filled_days = sum(len(ev) for ev in db.get_events_for_day(month, day).values()
                      for month in range(1,13) for day in range(1,32))
    empty_days = total_days - filled_days
    return f"""
    <h1>AppPulse Dashboard</h1>
    <p>Total days: {total_days}</p>
    <p>Filled days with events: {filled_days}</p>
    <p>Empty days: {empty_days}</p>
    <a href="/">Back to main</a>
    """

if __name__ == '__main__':
    app.run(debug=True)
