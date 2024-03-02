
from models.Predict import Predictor
from models.Velocity_assigner.assign_velocity import VelocityAssigner
if __name__ == '__main__':

    predictor = Predictor()
    res_path = predictor.generate_drum('static/midi/full_dataset_instance_cleaned-Contrabass_Bass.mid')

    va = VelocityAssigner('static/data/generated_drum_vel.midi')
    # va.assing_velocity2midi('static/midi/1_funk_80_beat_4-4.mid')
    va.assing_velocity2midi(res_path)
