
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id is not None:
        session[current_question_id] = answer
        return True, ""
    return False, "No question to answer."


def get_next_question(current_question_id):
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0
    
    current_question_index = current_question_id + 1
    if current_question_index < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[current_question_index], current_question_index
    else:
        return None, None

    return "dummy question", -1


def generate_final_response(session):
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question_id, correct_answer in enumerate(PYTHON_QUESTION_LIST):
        user_answer = session.get(question_id)
        if user_answer == correct_answer:
            score += 1

    score_percentage = (score / total_questions) * 100
    final_result = f"Your score: {score}/{total_questions} ({score_percentage:.2f}%)."
    return final_result
    return "dummy result"
