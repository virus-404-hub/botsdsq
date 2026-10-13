from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# إعدادات وهمية للوحة التحكم
bot_settings = {
    "status": "Online",
    "protection_level": "High (Anti-Spam & Anti-Link Enabled)",
    "ai_language": "Multi-language Auto-Detect",
    "active_shop": True
}

@app.route('/')
def dashboard():
    return render_template("dashboard.html", settings=bot_settings)

@app.route('/update', methods=['POST'])
def update_settings():
    data = request.json
    bot_settings.update(data)
    return jsonify({"status": "success", "message": "تم تحديث إعدادات الداشبورد بنجاح!"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)