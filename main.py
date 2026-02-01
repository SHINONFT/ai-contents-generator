import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))


def generate_content(prompt: str, content_type: str = "blog") -> str:
    """Generate content using Gemini API."""
    system_prompts = {
        "blog": "あなたはプロのブログライターです。SEOを意識した魅力的なブログ記事を日本語で作成してください。",
        "sns": "あなたはSNSマーケティングの専門家です。エンゲージメントの高いSNS投稿を日本語で作成してください。",
        "email": "あなたはメールマーケティングの専門家です。開封率の高いメール文面を日本語で作成してください。",
        "ad": "あなたはコピーライターです。効果的な広告コピーを日本語で作成してください。",
    }

    system_prompt = system_prompts.get(content_type, system_prompts["blog"])

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_prompt,
    )

    response = model.generate_content(prompt)
    return response.text


@app.route("/", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "ai-contents-generator"})


@app.route("/generate", methods=["POST"])
def generate():
    """Generate AI content based on the request."""
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify({"error": "prompt is required"}), 400

    prompt = data["prompt"]
    content_type = data.get("type", "blog")

    valid_types = ["blog", "sns", "email", "ad"]
    if content_type not in valid_types:
        return jsonify({"error": f"type must be one of: {', '.join(valid_types)}"}), 400

    try:
        result = generate_content(prompt, content_type)
        return jsonify({"content": result, "type": content_type})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
