def ask_questions(questions, category):
    responses = []
    print(f"Answer the following {category} questions on a scale of 1 (Strongly Disagree) to 5 (Strongly Agree):\n")
    for question in questions:
        while True:
            try:
                response = int(input(f"{question}\nYour response (1-5): "))
                if response < 1 or response > 5:
                    raise ValueError
                responses.append(response)
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
    avg_score = sum(responses) / len(responses)
    return (avg_score - 1) / 4  

risk_questions = [
    "I am uncomfortable holding cryptocurrencies that can lose 50% of their value in a short period.",
    "I prefer stable, long-term cryptocurrency investments rather than frequently trading to maximize short-term gains.",
    "If the market crashes and my portfolio loses 30% in a week, I would try and get out of my holdings.",
    "I avoid investing in lesser-known cryptocurrencies with high potential but uncertain futures."
]

ethical_questions = [
    "I prefer blockchains that offset their carbon footprint through renewable energy projects even if they yield lower profits.",
    "I prefer investing in cryptocurrencies that support social causes or fair distribution of wealth even if they yield lower profits.",
    "Governments should regulate cryptocurrency projects to ensure they meet ethical and environmental standards.",
    "In regions with energy shortages, cryptocurrency mining should be limited."
]

risk_score = ask_questions(risk_questions, "Risk")
ethical_score = ask_questions(ethical_questions, "Ethical")

print(f"\nYour Risk Adversity Score: {risk_score:.2f} (Higher = More Risk-Averse)")
print(f"Your Ethical Considerations Score: {ethical_score:.2f} (Higher = More Ethically Conscious)")

result = (risk_score, ethical_score)
print(f"\nFinal Result Tuple: {result}")