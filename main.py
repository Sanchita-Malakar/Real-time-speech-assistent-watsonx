from stt import listen_and_convert
from agent import ask_agent
from tts import speak
import time

def main():
    print("🤖 Watsonx Voice Assistant Started")
    print("🎤 Speak something... (say 'exit' to stop)\n")

    consecutive_silence = 0  # Track consecutive silent attempts
    max_silence = 3  # After 3 silent attempts, prompt user

    while True:
        try:
            # Listen
            user_text = listen_and_convert()

            # Handle silence - KEY FIX!
            if user_text is None:
                consecutive_silence += 1
                if consecutive_silence >= max_silence:
                    print("💭 Still waiting for your input...")
                    consecutive_silence = 0
                time.sleep(0.5)
                continue
            
            # Reset silence counter
            consecutive_silence = 0

            print(f"🧑 You said: {user_text}")

            # Exit command
            if user_text.lower() in ["exit", "quit", "stop", "goodbye"]:
                print("👋 Exiting assistant.")
                speak("Goodbye. Have a great day.")
                break

            # Ask agent
            print("🤔 Thinking...")
            agent_reply = ask_agent(user_text)

            if not agent_reply or agent_reply.startswith("Agent error"):
                print("⚠️ Agent returned no valid response.")
                speak("Sorry, I couldn't process that request.")
                continue

            print(f"🤖 Agent reply: {agent_reply}")

            # Speak reply
            speak(agent_reply)

            # Small pause before listening again
            print("\n" + "="*50)
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n👋 Assistant stopped manually.")
            speak("Goodbye.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()