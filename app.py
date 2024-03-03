import os
from openai import OpenAI
import base64

def decode_api_key(encoded_key):
    try:
        decoded_bytes = base64.b64decode(encoded_key.encode('utf-8'))
        decoded_key = decoded_bytes.decode('utf-8')
        return 'sk-' + decoded_key
    except Exception as e:
        print("Error decoding API key:", e)
        return None

def initialize_openai_api(encoded_key):
    api_key = decode_api_key(encoded_key)
    if api_key:
        client = OpenAI(api_key=api_key)
        return client
    else:
        return None

def get_chat_completion(client, user_input):
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="gpt-3.5-turbo",
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("Error fetching chat completion:", e)
        return None

def copy_code_to_file(code, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(code)
        print(f"Code successfully copied to {file_path}")
    except Exception as e:
        print("Error copying code to file:", e)

def main():
    encoded_key = 'bUd5b21TVksxanUySmM5OVpnVnpUM0JsYmtGSm5QNFJKNGMwaktZYU05RWIzYlZB'
    api_key = decode_api_key(encoded_key)
    if not api_key:
        print("Failed to decode API key. Exiting.")
        return

    client = initialize_openai_api(encoded_key)
    if not client:
        print("Failed to initialize OpenAI client. Exiting.")
        return

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'bye', 'goodbye']:
            print("Exiting...")
            break

        if user_input.lower() in ['hello', 'hi']:
            print("Assistant: Hello there!")

        elif "!c" in user_input:
            user_input = user_input.replace("!c", "") + ". GIVE CODE IN JAVA. AND GIVE ONLY FULL CODE. PLEASE. AND NO OTHER TEXT."
            try:
                assistant_response = get_chat_completion(client, user_input)
                print("Assistant (Code):", assistant_response)
            except Exception as e:
                print("Error:", e)

        elif "!save" in user_input:
            parts = user_input.split()
            if len(parts) >= 3:
                path = parts[1]
                prompt = ' '.join(parts[2:])
                java_files = [f for f in os.listdir(path) if f.endswith('.java')]
                if java_files:
                    print("Found the following .java files:")
                    for file_name in java_files:
                        print(file_name)
                    confirm = input("Do you want to proceed? (y/n): ")
                    if confirm.lower() == 'y':
                        selected_file = input("Enter the name of the file you want to copy code into: ")
                        if selected_file in java_files:
                            file_path = os.path.join(path, selected_file)
                            try:
                                prompt = prompt.replace("!save", '')
                                assistant_response = get_chat_completion(client, prompt + ". GIVE CODE IN JAVA. AND GIVE ONLY FULL CODE. PLEASE. AND NO OTHER TEXT.")
                                copy_code_to_file(assistant_response, file_path)
                            except Exception as e:
                                print("Error:", e)
                        else:
                            print("Invalid file name.")
                    else:
                        print("Operation cancelled.")
                else:
                    print("No .java files found in the specified directory.")
            else:
                print("Invalid input. Usage: !cs $package_name $promt_for_the_code")

        else:
            try:
                assistant_response = get_chat_completion(client, user_input)
                print("Assistant:", assistant_response)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()
