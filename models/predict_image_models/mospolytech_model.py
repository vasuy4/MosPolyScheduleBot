from tensorflow.keras import models
from models.predict_image_models.base_model import BasePredictModel
import os


class ModelMospolytech(BasePredictModel):
    """Класс для модели предсказания изображений из датасета корпусов Мосполитеха."""

    def __init__(self):
        """Инициализирует модель Мосполитеха"""
        model_path: str = os.path.join(
            os.path.dirname(__file__), "keras_files", "mospolytech_model.keras"
        )
        self.model = models.load_model(model_path)
        self.class_names = ["Автозаводская_16", "Б_Семёновская_38", "Прянишникова_2а"]


if __name__ == "__main__":
    model = ModelMospolytech()
    print(model.predict_image("dog.png"))
