import openai
import json
import os
import html5lib
import cssutils
from contextlib import suppress
import logging



cssutils.log.setLevel(logging.CRITICAL)
def read_api_key_from_file(file_path):
    with open(file_path, 'r') as f:
        api_key = f.read().strip()
    return api_key


def is_valid_html(html_content):
    with suppress(Exception):
        html5lib.parse(html_content)
        return True
    return False


def is_valid_css(css_content):
    with suppress(Exception):
        cssutils.parseString(css_content)
        return True
    return False


def call_gpt4(api_key, prompt):
    openai.api_key = api_key
    model_engine = "gpt-4"
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": "You are a helpful assistant in designing web interfaces following "
                                          "rules in inclusivity if applicable to the web design project:"
                                          "1.Step-by-Step Assistance: Guide new users through an onboarding process. "
                                          "2.Goal-Aligned Design: Make sure the interface's objectives match with "
                                          "the user group's goals. 3.Open Feedback Channels: Allow users to exchange "
                                          "feedback. 4.Equal Opportunity to Speak: If there's a communication "
                                          "feature, let each user have an equal chance to contribute. "
                                          "5.Skill-Sharing Features: "
                                          "Include elements that help users share skills. 6.Sensitive Language Filter: "
                                          "Use filters and moderation tools to remove problematic language. "
                                          "7.Agency Rule: Enable lower-status workers or people who are less inclusive "
                                          "to the group to handle collaboration overhead. "
                                          "8. Nudging Rule: Identify awkward social situations in collaborative tasks "
                                          "and offer nudges or notifications to help navigate them."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def separate_results_pages(text, page):
    os.makedirs(f'./interface_generated/{page}', exist_ok=True)

    index_html_start = text.find("```html") + len("```html")
    style_css_start = text.find("```css") + len("```css")
    script_js_start = text.find("```javascript") + len("```javascript")

    index_html_end = text.find("```", index_html_start)
    style_css_end = text.find("```", style_css_start)
    script_js_end = text.find("```", script_js_start)

    index_html_code = text[index_html_start: index_html_end].strip()
    style_css_code = text[style_css_start: style_css_end].strip()
    script_js_code = text[script_js_start: script_js_end].strip()

    with open(f'./interface_generated/{page}/index.html', 'w') as f:
        f.write(index_html_code)
    with open(f'./interface_generated/{page}/style.css', 'w') as f:
        f.write(style_css_code)
    with open(f'./interface_generated/{page}/script.js', 'w') as f:
        f.write(script_js_code)


def separate_results_page_html(text, page):
    index_html_start = text.find("```html") + len("```html")
    index_html_end = text.find("```", index_html_start)
    index_html_code = text[index_html_start: index_html_end].strip()

    with open(f'./interface_generated/{page}/index.html', 'w') as f:
        f.write(index_html_code)


def separate_results_page_css(text, page):
    style_css_start = text.find("```css") + len("```css")
    style_css_end = text.find("```", style_css_start)
    style_css_code = text[style_css_start: style_css_end].strip()

    with open(f'./interface_generated/{page}/style.css', 'w') as f:
        f.write(style_css_code)


def separate_results_page_js(text, page):
    script_js_start = text.find("```javascript") + len("```javascript")
    script_js_end = text.find("```", script_js_start)
    script_js_code = text[script_js_start: script_js_end].strip()

    with open(f'./interface_generated/{page}/script.js', 'w') as f:
        f.write(script_js_code)



def store_json(json):
    with open('./interface.json', 'w') as f:
        f.write(json)


def generate_page():
    with open('./interface.json', 'r') as f:
        interface = json.load(f)
    api_key_page = read_api_key_from_file("./api_key.txt")
    max_try = 5
    for page, page_info in interface.items():
        try_time = 0
        valid = False
        prompt_page = "In the scheduling website, design a page called " + str(
            page) + " using the inclusive rules you know. " \
                    "This is page is about " + str(page_info['description']) + " and have the following functions " + \
                      str(page_info['functions']) + ". Output the complete html, css, and javascript code separately."

        while try_time < max_try and not valid:
            result_page = call_gpt4(api_key_page, prompt_page)
            separate_results_pages(result_page, str(page))

            with open(f'./interface_generated/{page}/index.html', 'r') as f:
                html_content = f.read()
            with open(f'./interface_generated/{page}/style.css', 'r') as f:
                css_content = f.read()

            if is_valid_html(html_content) and is_valid_css(css_content):
                valid = True
            else:
                try_time += 1

        if try_time == max_try:
            print("Failed to generate valid html and css code for page " + str(page) + ".")

        second_layer_page_generation(page)


def second_layer_page_generation(page):
    api_key_page = read_api_key_from_file("./api_key.txt")

    with open(f'./interface_generated/{page}/index.html', 'r') as f:
        html_content = f.read()
    with open(f'./interface_generated/{page}/style.css', 'r') as f:
        css_content = f.read()
    with open(f'./interface_generated/{page}/script.js', 'r') as f:
        js_content = f.read()

    prompt_html = "In the scheduling website, this is a simple html page " + str(html_content) + ". " \
                    "Can you try to fill out the blanks and make the html page better using the inclusive rules you know?"

    result_html = call_gpt4(api_key_page, prompt_html)
    separate_results_page_html(result_html, str(page))
    with open(f'./interface_generated/{page}/index.html', 'r') as f:
        html_content = f.read()

    prompt_css = "In the scheduling website, this is a simple css page " + str(css_content) + ". " \
                    "with this html page " + str(html_content) + ". " \
                    "Can you try to make the css style better using the inclusive rules you know?"

    result_css = call_gpt4(api_key_page, prompt_css)
    separate_results_page_css(result_css, str(page))
    with open(f'./interface_generated/{page}/style.css', 'r') as f:
        css_content = f.read()

    prompt_js = "In the scheduling website, this is a simple javascript page " + str(js_content) + ". " \
                    "with this html page " + str(html_content) + ". " \
                    "Can you try to make the javascript code better and to realize as many functions on the html page as possible?"

    result_js = call_gpt4(api_key_page, prompt_js)
    separate_results_page_js(result_js, str(page))


if __name__ == '__main__':
    # api_key = read_api_key_from_file("./api_key.txt")
    # prompt = "Design an scheduling website's interface using the inclusive rules you know. " \
    #          "How many pages do we need? What are the functionalities in each page? " \
    #          "Output in a json format that under each page's name, we have 'description' and 'functions'." \
    #          "Following the format: {'page1': {'description': '...', 'functions': '...'}, 'page2': {'description': '...', 'functions': '...'}}}"
    # result = call_gpt4(api_key, prompt)
    # store_json(result)
    generate_page()
