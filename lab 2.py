


heart_rate_samples = {
    "J. Alvarez": [72, 75, 78],
    "M. Chen": [80,82],
    "R. Okafor": [65, 68, 70, 66],
    "S. Patel": [90, 95, 92, 88, 91],
    "T. Nguyen": [77, 79],
    "L. Kowalski": [68, 70, 69],
    "D. Osei": [98, 101, 95, 99],
    "A. Whitfield": [74, 76, 75, 73],
}

def get_patient_stats (patient, *args):
    if len(args) == 0:
        print(heart_rate_samples[patient])
    else:
        for sample in args:
            print(heart_rate_samples[patient][sample-1])


patient = input("Enter patient: ")
choice = input("Enter 'all' for all stats or 'specific' for specific stat:")
if choice == "all":
    get_patient_stats(patient)

elif choice == "specific":
    sample = int(input("Enter sample number: "))
    get_patient_stats(patient, sample)

else:
    print("invalid option")