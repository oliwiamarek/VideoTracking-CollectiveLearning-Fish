import csv

from config import get_csv_file, get_array_increments, is_not_string

read_rows = []
all_fish_coord = []
roi_fish_count = []


def get_data_from(fileName):
    current_frame_fish_coord_blah = []
    # reading csv file
    with open(fileName, 'r') as csv_file:
        # creating a csv reader object
        csv_reader = csv.reader(csv_file)

        # extracting each data row one by one
        for row in csv_reader:
            if row[0] == ' ':
                roi = get_no_fish_for_ROI(current_frame_fish_coord_blah)

                for r in range(len(roi)):
                    roi_fish_count.append({
                        'roi': r + 1,
                        'no_fish': roi[r]
                    })
                current_frame_fish_coord_blah = []
            else:
                current_frame_fish_coord_blah.append(row)
            read_rows.append(row)


def print_dictionary(output_file):
    for f in roi_fish_count:
        for key, value in f.items():
            # is recursive
            if hasattr(value, '__iter__'):
                print_dictionary(value)
            else:
                output_file.write('{0},'.format(value))
        output_file.write('\n')


def get_no_fish_for_ROI(current_frame_fish_coord):
    roi = [0, 0, 0, 0, 0, 0]
    for fish in current_frame_fish_coord:
        x = fish[0]
        y = fish[1]
        all_fish_coord.append(fish)
        if y < 380 and x < 428:
            roi[0] += 1
        elif y < 380 and x < 852:
            roi[1] += 1
        elif y < 380 and x > 852:
            roi[2] += 1
        elif y > 380 and x < 428:
            roi[3] += 1
        elif y > 380 and x < 852:
            roi[4] += 1
        elif y > 380 and x > 852:
            roi[5] += 1
    all_fish_coord.append("")
    return roi


get_data_from(get_csv_file())

output_filename = 'Outputs\\fish_no_output_{0}.csv'.format("whatever")

with open('Outputs\\fish_no_output_{0}.csv'.format("whatever"), 'w') as output_file:
    print_dictionary(output_file)
output_file.close()
print("Wrote no fish to file")

