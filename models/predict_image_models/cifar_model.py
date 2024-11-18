from tensorflow.keras import models
from models.predict_image_models.base_model import BasePredictModel
import os


class ModelCifar(BasePredictModel):
    """Класс для модели предсказания изображений из датасета CIFAR-10."""

    def __init__(self):
        """Инициализирует модель CIFAR-10."""
        model_path = os.path.join(
            os.path.dirname(__file__), "keras_files", "cifar10_model.keras"
        )
        self.model = models.load_model(model_path)
        self.class_names = [
            "airplane",
            "automobile",
            "bird",
            "cat",
            "deer",
            "dog",
            "frog",
            "horse",
            "ship",
            "truck",
        ]


if __name__ == "__main__":
    model = ModelCifar()
    print(model.predict_image("dog.png"))
