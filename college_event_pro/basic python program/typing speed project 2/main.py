import time
import random
sentences = ["the quick brown fox jumps over the lazy dog",
             "i am a aman singh rawat and i am a 25 year old boy",
             "i am a software engineer and i love coding",]
def typing_test():
    test_sentence = random.choice(sentences)
    print("type the sentences fast as you can: ")
    print(test_sentence)
    input("press enter when you are ready...")
    start_time = time.time()
    user_input = input("\n start typing:.../n")
    end_time = time.time()
    time_taken = end_time - start_time
    time_taken_in_minutes = time_taken / 60
    word_count = len(test_sentence.split())

    print("results:")
    print(f"time taken:{time_taken_in_minutes} minutes")
    print(f"word typed:{word_count} ")
    print(f"typing speed:{word_count/time_taken_in_minutes:.2f} words per minutes ")
    
typing_test()