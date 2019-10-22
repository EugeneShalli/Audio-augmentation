import librosa
import numpy as np
import os
import matplotlib.pyplot as plt


class AudioAugmentation:
    _settings = {
        'manipulate': "speed shift pitch noise".split(),
        # изменение скорости
        'speed': [0.7, 0.8, 0.9, 1, 1.3, 1.5, 1.7, 1.9, 2],
        # изменение высоты звука
        'pitch': [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 7, 9, 11, 15, 20],
        # сдвиг
        'shift': {
            'direction': "left right".split(),
            'max_shift': [1, 2, 3, 4, 5]
        },
        # добавление шума с коэффициентом, который влияет на "силу зашумленности"
        'noise': [0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    }

    @staticmethod
    def get_settings():
        return AudioAugmentation._settings

    def __init__(self, config, file_path, dest):
        data = self.read_audio_file(file_path)
        self.start(data, config, dest, file_path)

    def start(self, data, config, dest, file_path):
        if config['manipulate'] == 'speed':

            augmented_data = self.stretch(data, config['speed'])

            new_dest = os.path.join(dest, 'speed')

            try:
                os.mkdir(new_dest)
            except:
                pass

            name = os.path.basename(file_path)
            new_name = name[:-4] + '_' + str(config['speed']) + ".wav"
            self.write_audio_file(os.path.join(new_dest, new_name), augmented_data)

        elif config['manipulate'] == 'pitch':

            augmented_data = self.pitch(data, 16000, config['pitch'])

            new_dest = os.path.join(dest, 'pitch')

            try:
                os.mkdir(new_dest)
            except:
                pass

            name = os.path.basename(file_path)
            new_name = name[:-4] + '_' + str(config['pitch']) + ".wav"
            self.write_audio_file(os.path.join(new_dest, new_name), augmented_data)

        elif config['manipulate'] == 'noise':

            augmented_data = self.add_noise(data, config['noise'])

            new_dest = os.path.join(dest, 'noise')

            try:
                os.mkdir(new_dest)
            except:
                pass

            name = os.path.basename(file_path)
            new_name = name[:-4] + '_' + str(config['noise']) + ".wav"
            self.write_audio_file(os.path.join(new_dest, new_name), augmented_data)


        elif config['manipulate'] == 'shift':

            augmented_data = self.shift(data, 16000, config['max_shift'], config['direction'])

            new_dest = os.path.join(dest, 'shift')

            try:
                os.mkdir(new_dest)
            except:
                pass

            name = os.path.basename(file_path)
            new_name = name[:-4] + '_' + config['direction'] + '_' + str(config['max_shift']) + ".wav"
            self.write_audio_file(os.path.join(new_dest, new_name), augmented_data)

        # self.write_audio_file('output/generated.wav', augmented_data)

    def read_audio_file(self, file_path):
        data = librosa.core.load(file_path)[0]
        self.write_audio_file('read.wav', data)
        return data

    def write_audio_file(self, file, data, sample_rate=16000):
        librosa.output.write_wav(file, data, sample_rate)

    def plot_time_series(self, data):
        fig = plt.figure(figsize=(14, 8))
        plt.title('Raw wave ')
        plt.ylabel('Amplitude')
        plt.plot(np.linspace(0, 1, len(data)), data)
        plt.show()

    def add_noise(self, data, power):
        noise = np.random.randn(len(data))
        data_noise = data + power * noise
        data_noise = data_noise.astype(type(data[0]))
        return data_noise

    # def shift(self, data):
    #     return np.roll(data, 1600)

    def shift(self, data, sampling_rate, shift_max, shift_direction):
        shift = np.random.randint(sampling_rate * shift_max)
        if shift_direction == 'right':
            shift = -shift
        elif shift_direction == 'left':
            direction = np.random.randint(0, 2)
            if direction == 1:
                shift = -shift
        augmented_data = np.roll(data, shift)
        # Set to silence for heading/ tailing
        if shift > 0:
            augmented_data[:shift] = 0
        else:
            augmented_data[shift:] = 0
        return augmented_data

    def pitch(self, data, sampling_rate, pitch_factor):
        return librosa.effects.pitch_shift(data, 16000, pitch_factor)

    def stretch(self, data, rate):
        data = librosa.effects.time_stretch(data, rate)
        return data


# Create a new instance from AudioAugmentation class

config = {
    'manipulate': 'speed',
    'speed': 0.8
}

file_path = "data/example.wav"

destination = "output/"

aa = AudioAugmentation(config, file_path, destination)
