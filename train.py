from imageai.Prediction.Custom import ModelTraining
import shutil
 
def train_func(n):

	model_trainer = ModelTraining()
	model_trainer.setModelTypeAsResNet()
	model_trainer.setDataDirectory('Dataset')
	model_trainer.trainModel(num_objects=n, num_experiments=100, enhance_data=True, batch_size=32, show_network_summary=True)


