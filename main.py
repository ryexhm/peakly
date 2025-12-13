import json
from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)

with open("data.json", "r") as f:
    DATA = json.load(f)

CHECKMARK_SVG = """
<svg width="20" height="20" viewBox="0 0 24 24" fill="#31B0D5" xmlns="http://www.w3.org/2000/svg" style="margin-left:5px;">
  <circle cx="12" cy="12" r="10" fill="#31B0D5"/>
  <path d="M17 9L10.5 15.5L7 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

FULL_STAR_SVG = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="#000000" xmlns="http://www.w3.org/2000/svg" style="margin-right:4px;">
  <path fill="#000000" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
</svg>
"""

EMPTY_STAR_SVG = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" xmlns="http://www.w3.org/2000/svg" style="margin-right:4px;">
  <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
</svg>
"""

FEMALE_AVATAR_SVG = """
<svg width="40" height="40" viewBox="0 0 24 24" fill="#c3d9e8" xmlns="http://www.w3.org/2000/svg" style="border-radius: 50%;">
  <circle cx="12" cy="12" r="12" fill="#B6CDE6"/>
  <circle cx="12" cy="8" r="4" fill="#7E96B7"/>
  <path fill="#547297" d="M7 19c0-3 10-3 10 0v1H7v-1z"/>
</svg>
"""

MALE_AVATAR_SVG = """
<svg width="40" height="40" viewBox="0 0 24 24" fill="#c3d9e8" xmlns="http://www.w3.org/2000/svg" style="border-radius: 50%;">
  <circle cx="12" cy="12" r="12" fill="#A1B8C4"/>
  <circle cx="12" cy="8" r="4" fill="#5A6B7B"/>
  <rect x="7" y="17" width="10" height="2" fill="#3F4E5F" rx="1"/>
</svg>
"""


@app.route("/")
def base():
    return render_template('main.html')


@app.route("/social")
def social():
    return render_template('social.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/trainer")
def trainer():
    return render_template('trainer.html')


@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = []

    for name, info in DATA.items():
        if query in info.get("sport", "").lower():
            rating = info.get("rating", 0)
            results.append({
                "name": name.upper(),
                "sport": f"{info.get('sport', '').upper()} TRAINER",
                "rating": rating,
                "avatar": "male" if name.lower() == "alex" else "female"
            })

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Search Results</title>

<link rel="stylesheet" href="{{ url_for('static', filename='css/search_style.css') }}">
</head>

<body>

<!-- Search Bar -->
<div class="search-container">
    <form action="/search" method="GET" class="search-box">
        <svg class="icon" viewBox="0 0 24 24">
            <image x="-3" y="1" height="20" width="20" href="{{ url_for('static', filename='images/v.png') }}"/>
        </svg>
        <input type="text" name="q" placeholder="Search for a sport..." />
        <button type="submit" style="background:none;border:none;padding:0;margin:0;">
            <svg class="icon" viewBox="0 0 24 24">
                <circle cx="11" cy="11" r="7" stroke="#2d7fa3" stroke-width="2" fill="none"/>
                <line x1="16" y1="16" x2="22" y2="22" stroke="#2d7fa3" stroke-width="2"/>
            </svg>
        </button>
    </form>
</div>

<h2>Search results for "{{ query }}"</h2>

{% if results %}
    {% for r in results %}
    <a href="/trainer?=yasha" class="result-item">
        <div class="avatar">
            {% if r.avatar == 'male' %}
                {{ male_avatar | safe }}
            {% else %}
                {{ female_avatar | safe }}
            {% endif %}
            <div class="checkmark">{{ checkmark_svg | safe }}</div>
        </div>

        <div class="info">
            <div class="name" style="margin-left:8px;">{{ r.name }}</div>
            <div class="sport"style="margin-left:8px; font-size:4;">{{ r.sport }}</div>
        </div>

        <div class="stars">
            {% for i in range(1,6) %}
                {% if r.rating >= i %}
                    {{ full_star | safe }}
                {% else %}
                    {{ empty_star | safe }}
                {% endif %}
            {% endfor %}
        </div>
    </a>
    {% endfor %}
{% else %}
    <p>No matches found.</p>
{% endif %}


<div class="bottom-bar">
    <a href="/social" class="circle-btn">
        <div class="notif">3</div>
        <img class="icon-img" src="{{ url_for('static', filename='images/megaphone.png') }}" alt="">
    </a>

    <a href="/" class="circle-btn">
       <img class="icon-img" src="{{ url_for('static', filename='images/lupus.png') }}" alt="">
    </a>

    <a href="/profile" class="circle-btn">
        <img class="icon-img" src="{{ url_for('static', filename='images/profile.png') }}" alt="">
    </a>
</div>

</div>

</body>
</html>

"""

    return render_template_string(
        html_template,
        query=query,
        results=results,
        checkmark_svg=CHECKMARK_SVG,
        full_star=FULL_STAR_SVG,
        empty_star=EMPTY_STAR_SVG,
        female_avatar=FEMALE_AVATAR_SVG,
        male_avatar=MALE_AVATAR_SVG,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
