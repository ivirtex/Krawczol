from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import filters
from fbchat import *
import fbchat

chatbot = ChatBot("Adrian Krawczyk",
                  filters = [filters.get_recent_repeated_responses],
                  logic_adapters = [
                      'chatterbot.logic.BestMatch',
                      'chatterbot.logic.MathematicalEvaluation'
                  ]
                  )

trainer = ListTrainer(chatbot)

conversation = [
    "Hej",
    "Dzień dobry",
    "Co tam słodziaku?",
    "zajebiscie",
    "ooo",
    "dzieki",
    "spoko kotku"
]

trainer.train(conversation)

class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        if author_id != self.uid:
            self.setTypingStatus(fbchat.TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)
            self.send(fbchat.Message(text=chatbot.get_response(message_object.text)), thread_id=thread_id,
                      thread_type=thread_type)
            self.setTypingStatus(fbchat.TypingStatus.STOPPED, thread_id=thread_id, thread_type=thread_type)

client = EchoBot('vabeve2984@beiop.com', 'jp2gmd')
client.listen()