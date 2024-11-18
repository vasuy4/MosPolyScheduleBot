import numpy as np
from PIL import Image

from typing import List


class BasePredictModel:
    """Базовый класс для моделей предсказания изображений."""

    def predict_image(self, image_path: str) -> List[str]:
        """
        Предсказывает класс изображения.

        :param image_path: Путь к изображению.
        :return: Название класса.
        """
        # Загрузка и предобработка изображения
        image = self._load_and_preprocess_image(image_path)

        # Предсказание класса
        predictions = self.model.predict(image)
        predicted_class = np.argmax(predictions, axis=1)

        # Возвращаем название класса
        return self.class_names[predicted_class[0]]

    def _load_and_preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Загружает и предобрабатывает изображение.

        :param image_path: Путь к изображению.
        :return: Предобработанное изображение.
        """
        image = Image.open(image_path).resize((32, 32))
        image = np.array(image) / 255.0
        return np.expand_dims(image, axis=0)  # Добавляем размерность батча
