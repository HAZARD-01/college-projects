import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")
            
            if message.lower() == 'hello':
                response = "Hello there! How can I assist you today?"
            elif message.lower() == 'how are you':
                response = "I'm doing well, thank you for asking!"
            elif message.lower() == 'what is your name':
                response = "I'm a chatbot, you can call me ChatBot."
            elif message.lower() == 'tell me a joke':
                response = "Sure, here's one: Why don't scientists trust atoms? Because they make up everything!"
            elif 'weather' in message.lower():
                response = "I don't have real-time weather information, but I can tell you a joke instead!"
            elif message.lower() == 'bye':
                response = "Goodbye! Have a great day."
            elif message.lower() == 'thanks' or message.lower() == 'thank you':
                response = "You're welcome! If you have more questions, feel free to ask."
            elif 'how do you do' in message.lower():
                response = "I'm just a computer program, so I don't experience feelings, but I'm here to help!"
            elif 'your favorite color' in message.lower():
                response = "I don't have a favorite color, but I can help you find information on colors if you'd like."
            elif 'programming language' in message.lower():
                response = "I'm built using Python, a programming language known for its simplicity and readability."
            elif 'meaning of life' in message.lower():
                response = "The meaning of life is a complex philosophical question. What do you think it is?"
            elif 'how are you doing' in message.lower():
                response = "I'm functioning well, thanks for asking!"
            elif 'where are you from' in message.lower():
                response = "I exist in the digital realm, so you could say I'm from the world of technology."
            elif 'can you dance' in message.lower():
                response = "I can't physically dance, but I can certainly help you find information about dancing!"
            elif 'your favorite food' in message.lower():
                response = "I don't eat, but I can provide information about various cuisines!"
            elif 'tell me a fun fact' in message.lower():
                response = "Sure, here's a fun fact: Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible."
            elif 'favorite book' in message.lower():
                response = "I don't have personal preferences, but I can recommend classic literature or the latest bestsellers!"
            elif 'do you dream' in message.lower():
                response = "No, I don't dream. I'm always ready to assist you with any questions or tasks!"
            elif 'are you human' in message.lower():
                response = "No, I'm not human. I'm a computer program designed to help with information and tasks."
            elif 'what is the capital of France' in message.lower():
                response = "The capital of France is Paris."
            elif 'do you play video games' in message.lower():
                response = "I don't play video games, but I can help you find information about them!"
            elif 'favorite movie' in message.lower():
                response = "I don't have personal preferences, but I can suggest popular movies in different genres."
            elif 'who is your creator' in message.lower():
                response = "I was created by elvis."
            elif 'tell me about yourself' in message.lower():
                response = "I'm a chatbot created to assist with information and answer your questions. How can I help you today?"
            elif 'what is the meaning of AI' in message.lower():
                response = "AI stands for Artificial Intelligence. It involves creating machines that can perform tasks that would typically require human intelligence."
            elif 'favorite music' in message.lower():
                response = "I don't have personal preferences, but I can suggest music based on your taste!"
            elif 'how tall are you' in message.lower():
                response = "I don't have a physical form, so I don't have height. I exist in the digital space."
            elif 'tell me about the universe' in message.lower():
                response = "The universe is vast and ever-expanding, containing galaxies, stars, planets, and other celestial objects. It's a fascinating subject with much to explore!"
            elif 'are you a robot' in message.lower():
                response = "Yes, I am a computer program designed to interact with users and provide information."
            elif 'favorite sport' in message.lower():
                response = "I don't have personal preferences, but I can provide information about various sports."
            elif 'how to learn programming' in message.lower():
                response = "Learning programming involves practice, online courses, and working on projects. There are many resources available, and I can help you find suitable learning materials."
            elif 'who is your best friend' in message.lower():
                response = "I don't have friends in the traditional sense, but I'm here to assist you!"
            elif 'tell me a science fact' in message.lower():
                response = "Sure, here's a science fact: The Earth's core is hotter than the surface of the Sun!"
            elif 'are you smart' in message.lower():
                response = "I'm designed to provide information and assist with tasks, but the concept of intelligence is complex and subjective."
            elif 'can you sing' in message.lower():
                response = "I don't have a voice, so I can't sing. However, I can help you find lyrics or information about songs!"
            elif 'favorite place' in message.lower():
                response = "I don't have personal preferences, but I can provide information about interesting places around the world."
            elif 'tell me a history fact' in message.lower():
                response = "Certainly! Here's a history fact: The Great Wall of China is the longest wall in the world, stretching over 13,000 miles."
            elif 'are you on social media' in message.lower():
                response = "No, I don't have a presence on social media. My purpose is to assist you with information and tasks here."
            elif 'how to stay motivated' in message.lower():
                response = "Staying motivated involves setting goals, breaking them into smaller tasks, and celebrating achievements along the way. Consistency is key!"
            elif 'can you code' in message.lower():
                response = "Yes, I can assist with coding-related questions and provide examples in various programming languages."
            elif 'tell me a technology fact' in message.lower():
                response = "Sure, here's a technology fact: The first computer mouse was made of wood and had two wheels. It was invented by Doug Engelbart in 1964."
            elif 'what is your favorite subject' in message.lower():
                response = "I don't have personal preferences, but I can help you with information on a wide range of subjects."
            elif 'are you learning' in message.lower():
                response = "I don't learn in the same way humans do. My responses are based on pre-existing information and patterns."
            elif 'tell me a space fact' in message.lower():
                response = "Certainly! Here's a space fact: Jupiter is the largest planet in our solar system and has the most massive planetary atmosphere."
            else:
                response = "I didn't understand that. Can you ask something else?"
            
            client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            print("Client disconnected.")
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345)) 
    server.listen(5)
    print("Server listening for connections...")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
