import cv2
import numpy as np
from pathlib import Path


class ImageProcessing:

    image_path = ''

    def __process_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return thresh

    def __save_axis_projections_to_txt(self, image, output_path='../output/output.txt'):
        projection_x = np.sum(image == 255, axis=0)
        projection_y = np.sum(image == 255, axis=1)

        output = Path(output_path).with_stem(
            str(Path(output_path).stem) + '_' + str(Path(self.image_path).stem)
        )

        with open(output, 'w') as file:
            file.write("Projection on X axis:\n")
            file.write(str(projection_x) + "\n")
            file.write("Projection on Y axis:\n")
            file.write(str(projection_y) + "\n")

    def get_spot_data(self, image_path: str):
        self.image_path = image_path
        image = self.__process_image()

        center_x = image.shape[1] // 2
        center_y = image.shape[0] // 2

        moments = cv2.moments(image)
        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
        else:
            cx, cy = 0, 0
        # Пары координат пятна y, x
        # spot = np.column_stack(np.where(np.array(image)))

        # Переводим в систему координат с точкой отсчёта в центре изображения
        # delta_y = spot[:, 0] - center_y - если нужны все пиксели пятна
        # delta_x = spot[:, 1] - center_x
        delta_y = cy - center_y # - если нужен только центр пятна => положение
        delta_x = cx - center_x

        # Дисперсия - среднее арифметическое квадратов отклонений от центра
        dispersion_x = np.mean(delta_x**2)
        dispersion_y = np.mean(delta_y**2)
        dispersion_total = dispersion_x + dispersion_y

        # Стандартное отклонение - квадратный корень из дисперсии
        deviation_total = np.sqrt(dispersion_total)

        self.__save_axis_projections_to_txt(image)

        return {"center_position": [delta_x, delta_y], "dispersion": dispersion_total, "deviation": deviation_total}
