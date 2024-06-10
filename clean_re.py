def clean_requirements(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cleaned_lines = [line for line in lines if not line.startswith('nvidia-')]

    with open(output_file, 'w') as f:
        f.writelines(cleaned_lines)

clean_requirements('whisper.txt', 'cleaned_requirements.txt')