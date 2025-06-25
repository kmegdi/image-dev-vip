
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

app = Flask(__name__)

API_KEY = "XZA"

@app.route("/api/outfit-image", methods=["GET"])
def get_outfit():
    uid = request.args.get("uid")
    region = request.args.get("region")
    key = request.args.get("key")

    if key != API_KEY:
        return jsonify({"error": "❌ API Key غير صالحة"}), 401

    if not uid or not uid.isdigit():
        return jsonify({"error": "❌ UID غير صحيح"}), 400

    if not region:
        return jsonify({"error": "❌ يجب تحديد region"}), 400

    source_url = f"https://aditya-outfit-v9op.onrender.com/outfit-image?uid={uid}&region={region}"
    try:
        response = requests.get(source_url)
        response.raise_for_status()
    except:
        return jsonify({"error": "❌ فشل في جلب الصورة"}), 502

    try:
        image = Image.open(BytesIO(response.content)).convert("RGBA")
        width, height = image.size
        background = Image.new("RGBA", (width, height), (0, 102, 204, 255))
        background.paste(image, (0, 0), image)

        draw = ImageDraw.Draw(background)
        font_size = int(width / 15)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        draw.text((10, 10), "XZA DEV", font=font, fill="white")
        draw.text((10, height - font_size - 10), "حمود", font=font, fill="white")

        output = BytesIO()
        background.save(output, format="PNG")
        output.seek(0)

        return send_file(output, mimetype="image/png", as_attachment=False,
                         download_name=f"{uid}_{region}_outfit.png")

    except Exception as e:
        return jsonify({"error": f"❌ خطأ في معالجة الصورة: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5111)
