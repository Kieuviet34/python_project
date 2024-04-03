from flask import Flask, render_template,request
import requests
app = Flask(__name__)


@app.route('/',methods= ['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('index_new.html')
    else:
        user_msg = request.form['user_msg']
        livechatcontent = request.form['chat_content']
        
        r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": "test", "message":user_msg})
        livechatcontent += "\n[YOU]: " + user_msg
        livechatcontent += "\n[BOT]: " + r.json()[0]["text"]
        return render_template('index_new.html', livechatcontent=livechatcontent)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)