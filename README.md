# Manim Visualizations

Минимальная инфраструктура для генерации математических анимаций на Python + Manim.

## Что уже подготовлено

- Виртуальное окружение `.venv` (Python 3.13).
- Установлены зависимости для Manim.
- Базовая сцена по центральной предельной теореме:
  `scenes/central_limit_theorem.py`.

## Быстрый старт

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Рендер сцены

Быстрый превью-рендер (низкое качество):

```bash
manim -pql scenes/central_limit_theorem.py CentralLimitTheoremScene
```

Более качественный рендер:

```bash
manim -pqh scenes/central_limit_theorem.py CentralLimitTheoremScene
```

Результаты сохраняются в папке `media/`.

## Идеи для следующих сцен

- Закон больших чисел.
- Формула Байеса.
- Геометрическая интерпретация производной.
