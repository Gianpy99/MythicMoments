class ImagePromptGenerator:
    def __init__(self, style="Disney/Ghibli/Tolkien style, magical, cinematic, detailed"):
        self.style = style

    def generate_prompt(self, universe, fact, year=None, quote=None):
        prompt = f"{fact} from {universe}"
        if year:
            prompt += f", year {year}"
        if quote:
            prompt += f", quote: '{quote}'"
        prompt += f", {self.style}"
        return prompt

    def generate_prompts_for_day(self, events_of_day):
        prompts = []
        for universe, ev_list in events_of_day.items():
            for ev in ev_list:
                prompt = self.generate_prompt(
                    universe,
                    ev.get('fact', ''),
                    year=ev.get('year'),
                    quote=ev.get('quote')
                )
                prompts.append(prompt)
        return prompts
