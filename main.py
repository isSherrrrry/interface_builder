import openai


def read_api_key_from_file(file_path):
    with open(file_path, 'r') as f:
        api_key = f.read().strip()
    return api_key


def call_gpt3_5_turbo(api_key, prompt):
    openai.api_key = api_key
    model_engine = "gpt-4"
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant in designing web interfaces following "
                                          "the following rules in inclusivity if applicable to the web design project: "
                                          "1. Step-by-Step Assistance: The interface should offer a guided "
                                          "onboarding process for new users. "
                                          "2. Goal-Aligned Design: Ensure the interface's objectives "
                                          "match those of the identified user group. "
                                          "3. Open Feedback Channels: Include features that allow "
                                          "users to exchange feedback with one another. "
                                          "4. Equal Opportunity to Speak: If communication is a component, "
                                          "design functionalities that give each participant an equal chance to contribute. "
                                          "5. Skill-Sharing Features: Incorporate elements that facilitate "
                                          "the sharing of skills among users. "
                                          "6. Sensitive Language Filter: Implement filters and moderation tools to "
                                          "remove sensitive or problematic language from user-generated content."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def separate_results(text):
    index_html_start = text.find("```html") + len("```html")
    style_css_start = text.find("```css") + len("```css")
    script_js_start = text.find("```javascript") + len("```js")

    index_html_end = text.find("```", index_html_start)
    style_css_end = text.find("```", style_css_start)
    script_js_end = text.find("```", script_js_start)

    index_html_code = text[index_html_start: index_html_end].strip()
    style_css_code = text[style_css_start: style_css_end].strip()
    script_js_code = text[script_js_start: script_js_end].strip()

    with open('./interface_generated/index.html', 'w') as f:
        f.write(index_html_code)

    with open('./interface_generated/style.css', 'w') as f:
        f.write(style_css_code)

    with open('./interface_generated/script.js', 'w') as f:
        f.write(script_js_code)


if __name__ == '__main__':
    api_key = read_api_key_from_file("./api_key.txt")
    prompt = "Design a scheduling website like when2meet (https://www.when2meet.com/) " \
             "that take the inclusivity rules into consideration. " \
             "Please output a fully functioning HTML, Javascript, and CSS files. " \
             "Name the HTML file as index.html, CSS as style.css, and JS as script.js." \
             "Make sure that the files are functioning."
    result = call_gpt3_5_turbo(api_key, prompt)
    print(result)
    separate_results(result)

