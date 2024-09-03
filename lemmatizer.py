import os

import spacy

# from spacy.cli import download

# Install the en_core_web_sm model
# download("en_core_web_lg")
#
# Load the model after installation
nlp = spacy.load("en_core_web_lg")


def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])


def lemmatize_folder(input_folder):
    # Create a new folder with the name "input_folder_name lemmatized"
    output_folder = f"{input_folder} lemmatized"
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all txt files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)
            with open(input_file_path, "r") as file:
                text = file.read()

            # Lemmatize the content of the file
            lemmatized_text = lemmatize_text(text)

            # Write the lemmatized content to a new file in the output folder
            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, "w") as file:
                file.write(lemmatized_text)

    print(f"Lemmatized files are saved in '{output_folder}'.")


# Example usage:
print("start")
# lemmatize_folder("NABRE/NABRE Gospel")
# print("1")
# lemmatize_folder("NABRE/NABRE Old Testament")
# print("2")
# lemmatize_folder("NABRE/NABRE 2nd Readings")
# print("finished")
