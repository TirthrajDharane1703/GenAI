css = '''
<style>
.button {
  background-color: #0E1117;
  border: 2px solid red;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}

.button:hover {
  background-color: #2b313e;
}

.chat-message {
    padding: 0.7rem; border-radius: 0.5rem; margin-bottom: 0.2rem; display: flex;
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #0E1117
}
.chat-message .avatar {

}
.chat-message .avatar img {
  padding-right: 10px;
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 0.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img width="40" src="https://cdn3d.iconscout.com/3d/premium/thumb/chatbot-5841152-4884463.png" alt="Bot here">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img width="40" src="https://e7.pngegg.com/pngimages/134/822/png-clipart-computer-icons-business-man-people-logo.png" alt=>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

button = '''

'''
