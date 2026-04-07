import random
import json
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class ChatBot:
    def __init__(self):
        self.name = None
        self.mood = "neutral"
        self.history = []
        self.memory = {}
        self.stats = {"messages": 0}
        self.greetings = ["Hello!", "Hey there!", "Hi 👋", "What's up!"]
        self.how_are_you_responses = [
            "I'm doing great 😄",
            "Feeling awesome today!",
            "All good here 👍",
            "I'm okay 😊"
        ]
        self.positive_words = ["good", "great", "awesome", "happy", "nice"]
        self.negative_words = ["bad", "sad", "tired", "angry", "upset"]

    def save_data(self):
        data = {
            "name": self.name,
            "history": self.history,
            "memory": self.memory,
            "stats": self.stats
        }
        with open("chatbot_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists("chatbot_data.json"):
            with open("chatbot_data.json", "r") as f:
                data = json.load(f)
                self.name = data.get("name")
                self.history = data.get("history", [])
                self.memory = data.get("memory", {})
                self.stats = data.get("stats", {"messages": 0})

    def analyze_mood(self, text):
        for word in self.positive_words:
            if word in text:
                return "positive"
        for word in self.negative_words:
            if word in text:
                return "negative"
        return "neutral"

    def export_chat(self):
        with open("chat_export.txt", "w") as f:
            for entry in self.history:
                f.write(f"{entry['time']}\nYou: {entry['user']}\nBot: {entry['bot']}\n\n")

    def handle_command(self, cmd):
        if cmd == "/help":
            return (
                "/help - show commands\n"
                "/clear - clear chat history\n"
                "/stats - show number of messages\n"
                "/memory - show remembered facts\n"
                "/export - export chat to text file"
            )
        if cmd == "/clear":
            self.history = []
            return "Chat history cleared."
        if cmd == "/stats":
            return f"Messages: {self.stats['messages']}"
        if cmd == "/memory":
            if not self.memory:
                return "Memory is empty."
            return ", ".join(self.memory.values())
        if cmd == "/export":
            self.export_chat()
            return "Chat exported to chat_export.txt"
        return "Unknown command."

    def respond(self, user_input):
        text = user_input.lower()
        if text.startswith("/"):
            return self.handle_command(text)

        mood = self.analyze_mood(text)

        if "hello" in text or "hi" in text:
            return random.choice(self.greetings)

        if "how are you" in text:
            return random.choice(self.how_are_you_responses)

        if "my name is" in text:
            self.name = user_input.split("is")[-1].strip()
            return f"Nice to meet you, {self.name}!"

        if "remember" in text:
            parts = user_input.split("remember")
            if len(parts) > 1:
                info = parts[1].strip()
                key = f"fact_{len(self.memory)+1}"
                self.memory[key] = info
                return "Got it, I'll remember that."

        if "what do you know about me" in text:
            if not self.memory:
                return "I don't know much about you yet."
            return ", ".join(self.memory.values())

        if mood == "positive":
            return "That's great to hear 😄"

        if mood == "negative":
            return "Hope things get better soon 🙏"

        return "Interesting... tell me more."

    def chat(self):
        self.load_data()
        print(Fore.GREEN + "ChatBot is running. Type 'exit' to quit.\n")
        print(Fore.YELLOW + "Type /help for commands\n")

        while True:
            user_input = input(Fore.CYAN + "You: ")

            if user_input.lower() == "exit":
                self.save_data()
                print(Fore.YELLOW + "Goodbye!")
                break

            response = self.respond(user_input)
            self.stats["messages"] += 1
            self.history.append({
                "time": str(datetime.now()),
                "user": user_input,
                "bot": response
            })

            print(Fore.MAGENTA + "Bot:", response)


if __name__ == "__main__":
    bot = ChatBot()
    bot.chat()