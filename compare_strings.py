import create_model

#good_sample = [[1.0, 1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]]
#bad_sample = [[0.0, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]
meh_sample = [[.5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5]]

data = 'files/data_frame_shortened.csv'

model = create_model.Model(data)

print(model.is_match('hi', 'hi'))

print(model.is_match('elephant', 'kenneth'))

print(model.is_match('california', 'cal'))

print(model.is_match('johnson matthey', 'johnson matthey public limited company'))

print(model.is_match('varian medical systems', 'ashland licensing and intellectual property llc'))

print(model.is_match('ge intelligent platforms', 'ge healthcare as'))

print(model.test(meh_sample))