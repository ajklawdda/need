from g4f.client import Client
from flask import Flask, render_template
import os


app = Flask(__name__)
client = Client()


def get(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}],
        web_search=False,
    )
    return response.choices[0].message.content


def get_image(name):
    response = client.images.generate(
        model="flux",
        prompt=f"Картинка для поздравления на 8 марта по теме: {name}",
        response_format="url",
        temperature=1
    )

    return response.data[0].url


@app.route('/')
def hello_world():
    resp = get(
        "Напиши стихотворение-поздравление на 8 марта для Елены от 12 до 30 строчек, где первая строчка - это название стихотворения. Название не должно содержать имен и не должно сожержать сиивол '*'").split(
        "\n")
    print(resp)
    if "openai" in resp[0].lower():
        resp = resp[1:]
        while not resp[0]:
            resp = resp[1:]
    text = resp[1:]
    while not resp[0]:
        resp = resp[1:]
    title = resp[0]
    image = get_image(title)
    return render_template("index.html",
                           title=title,
                           text=text,
                           image=image)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)