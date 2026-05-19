from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = 'tasks.json'

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()

# если старые задачи были строками
tasks = [
    task if isinstance(task, dict)
    else {'text': task, 'date': 'Без даты'}
    for task in tasks
]

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

from datetime import datetime

@app.route('/add', methods=['POST'])
def add_task():

    new_task = request.form['task']

    if new_task:

        task = {
            'text': new_task,
            'date': datetime.now().strftime('%d.%m.%Y %H:%M')
        }

        tasks.append(task)

        save_tasks(tasks)

    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):

    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)

    return redirect('/')

@app.route('/clear')
def clear_tasks():

    tasks.clear()

    save_tasks(tasks)

    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):

    # Проверка существования задачи
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404

    # GET-запрос
    task = tasks[task_id]

    if request.method == 'POST':

        # Новый текст
        new_text = request.form.get('task', '').strip()

        # Старый текст
        old_text = task['text']

        # Проверка на пустое поле
        if new_text == '':
            return render_template(
                'edit.html',
                task=task,
                message="Текст не может быть пустым!"
            )

        # Проверка:
        # ничего не изменилось
        if new_text == old_text:
            return render_template(
                'edit.html',
                task=task,
                message="Ничего не изменено"
            )

        # Обновление текста
        tasks[task_id]['text'] = new_text

        # Сохранение
        save_tasks(tasks)

        # Возврат на главную
        return redirect('/')

    # Открытие страницы
    return render_template(
        'edit.html',
        task=task
    )

if __name__ == '__main__':
    app.run(debug=True)


