from flask import Flask, request, redirect, render_template_string
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="dbsvc",
        user="root",
        password="Test123!",
        database="webtest",
        port=3306,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MySQL Test</title>

<style>
body{
    font-family:Arial;
    background:#f5f5f5;
}

.container{
    width:700px;
    margin:40px auto;
    background:white;
    padding:30px;
    border-radius:10px;
    box-shadow:0 0 10px rgba(0,0,0,.2);
}

input,textarea{
    width:100%;
    padding:10px;
    margin-bottom:15px;
}

button{
    width:100%;
    padding:12px;
    background:#222;
    color:white;
    border:none;
    cursor:pointer;
}

table{
    width:100%;
    margin-top:30px;
    border-collapse:collapse;
}

th,td{
    border:1px solid #ccc;
    padding:10px;
}

th{
    background:#333;
    color:white;
}
</style>

</head>

<body>

<div class="container">

<h2>Items 등록</h2>

<form method="POST">

<input
type="text"
name="title"
placeholder="Title"
required>

<textarea
name="description"
rows="5"
placeholder="Description"
required></textarea>

<button type="submit">저장</button>

</form>

<h2>저장된 데이터</h2>

<table>

<tr>
<th>Title</th>
<th>Description</th>
</tr>

{% for item in items %}

<tr>
<td>{{ item.title }}</td>
<td>{{ item.description }}</td>
</tr>

{% endfor %}

</table>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():

    conn = get_connection()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        try:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO items(title, description, created)
                    VALUES(%s, %s, NOW())
                    """,
                    (title, description)
                )

                conn.commit()

            print("저장 완료")

        except Exception as e:
            conn.rollback()
            print("오류 :", e)

        conn.close()
        return redirect("/")

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT title, description FROM items ORDER BY id DESC"
        )
        items = cursor.fetchall()

    conn.close()

    return render_template_string(HTML, items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
