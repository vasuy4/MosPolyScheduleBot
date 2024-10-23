from tensorflow.keras import models
import numpy as np
from PIL import Image
import os


class Model():
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "cifar10_model.keras")
        self.model = models.load_model(model_path)
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    def predict_image(self, image_path: str):
        # Загрузка и предобработка изображения
        image = Image.open(image_path).resize((32, 32))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)  # Добавляем размерность батча

        # Предсказание класса
        predictions = self.model.predict(image)
        predicted_class = np.argmax(predictions, axis=1)

        # Возвращаем название класса
        return self.class_names[predicted_class[0]]


if __name__ == "__main__":
    model = Model()
    print(model.predict_image("dog.jpg"))