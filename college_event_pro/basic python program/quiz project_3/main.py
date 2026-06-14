def run_quiz():
    questions=[
    {   "question": "What is the capital of France?",
        "options": ["A) Berlin", "B) Madrid", "C) Paris", "D) Rome"],
        "answer": "C"
    },
    {   "question": "What is the largest planet in our solar system?",
        "options": ["A) Earth", "B) Jupiter", "C) Mars", "D) Saturn"],
        "answer": "B"
    },
    {   "question": "Who wrote 'To Kill a Mockingbird'?",
        "options": ["A) Harper Lee", "B) Mark Twain", "C) J.K. Rowling", "D) Ernest Hemingway"],
        "answer": "A"
    }
]
    score = 0
    for index, q in enumerate(questions):
        # print(index,q)

        print(f"Q{index + 1}: {q['question']}")
        for option in q['options']:
            print(option)

        user_answer = input("Your answer:")
        if user_answer.strip().upper() == q['answer'][0]:

            # print("Correct!\n")
            score += 1
    print(f"Your final score is: {score}/{len(questions)}")


run_quiz()