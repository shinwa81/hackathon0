from flask import Flask, jsonify, request, send_from_directory
from database import init_db, get_all_memos, get_memo, create_memo, update_memo, delete_memo

app = Flask(__name__)

# アプリ起動時にDBを初期化する（テーブルが存在しない場合は作成する）
init_db()

@app.route("/")
def index():
    """HTMLページを配信する"""
    return send_from_directory("static", "index.html")

@app.route("/api/memos", methods=["GET"])
def api_get_memos():
    """全てのメモを取得する"""
    memos = get_all_memos()
    return jsonify(memos)

@app.route("/api/memos", methods=["POST"])
def api_create_memo():
    """新しいメモを作成する"""
    data = request.get_json()

    # バリデーション（入力チェック）
    if not data:
        return jsonify({"error": "リクエストボディが空です"}), 400

    title = data.get("title")
    body = data.get("body")

    if not title or not body:
        return jsonify({"error": "title と body は必須です"}), 400

    # メモを作成
    memo_id = create_memo(title, body)

    # 作成したメモを取得して返す
    memo = get_memo(memo_id)
    return jsonify(memo), 201

@app.route("/api/memos/<int:id>", methods=["GET"])
def api_get_memo(id):
    """指定されたIDのメモを取得する"""
    memo = get_memo(id)

    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404

    return jsonify(memo)

@app.route("/api/memos/<int:id>", methods=["PUT"])
def api_update_memo(id):
    """指定されたIDのメモを更新する"""
    # 更新対象が存在するか確認
    memo = get_memo(id)
    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "リクエストボディが空です"}), 400

    title = data.get("title")
    body = data.get("body")

    if not title or not body:
        return jsonify({"error": "title と body は必須です"}), 400

    # メモを更新
    update_memo(id, title, body)

    # 更新後のメモを返す
    updated_memo = get_memo(id)
    return jsonify(updated_memo)

@app.route("/api/memos/<int:id>", methods=["DELETE"])
def api_delete_memo(id):
    """指定されたIDのメモを削除する"""
    memo = get_memo(id)
    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404

    delete_memo(id)
    return jsonify({"message": f"メモ (ID:{id}) を削除しました"})

if __name__ == "__main__":
    app.run(debug=True)